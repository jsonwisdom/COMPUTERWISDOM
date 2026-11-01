/**
 * REPLAY 007: Local atomic SQLite nonce consumption for real EIP-712 proofs.
 * Never signs, publishes, spends, or grants payments/ENS/API authority.
 * Nonce consumption monotonically accumulates permanently for
 * (chain_id, lowercase_signer, random_bytes32_nonce), regardless of
 * EIP-712 domain version or salt. Nonce VALUES are random, not ordered.
 * Different databases/hosts do not coordinate. No global replay claim.
 */
import { DatabaseSync } from 'node:sqlite';
import { existsSync, chmodSync } from 'node:fs';
import { resolve } from 'node:path';
import { CONTRACT, verifyBaseProofBatch, merkleRoot, __testing as cryptoTest } from './verify-base-signatures.mjs';

const HEX32=/^0x[0-9a-f]{64}$/;
const ADDR=/^0x[0-9a-f]{40}$/;
const deny=(reason,extra={})=>({status:'HOLD',reason,root:null,authorization:false,onchain:false,fundsMoved:false,productionApproved:false,...extra});
function databasePath(dbPath){
  if(typeof dbPath!=='string'||!dbPath.trim()||dbPath.length>2048||
    dbPath===':memory:'||dbPath.startsWith('file:')||dbPath.includes('\0'))throw Error('DURABLE_DB_PATH_REQUIRED');
  return resolve(dbPath);
}
function openDb(dbPath){
  const path=databasePath(dbPath),existed=existsSync(path);
  const db=new DatabaseSync(path);
  try{
    if(!existed&&process.platform!=='win32')chmodSync(path,0o600);
    db.exec('PRAGMA journal_mode=WAL;PRAGMA synchronous=FULL;PRAGMA busy_timeout=5000;PRAGMA foreign_keys=ON;');
    db.exec('CREATE TABLE IF NOT EXISTS replay_batches (root TEXT PRIMARY KEY NOT NULL,policy_version TEXT NOT NULL,signer_set_version TEXT NOT NULL,chain_id INTEGER NOT NULL CHECK(chain_id=8453),item_count INTEGER NOT NULL CHECK(item_count>0),reserved_at INTEGER NOT NULL); CREATE TABLE IF NOT EXISTS consumed_nonces (chain_id INTEGER NOT NULL CHECK(chain_id=8453),signer TEXT NOT NULL,nonce TEXT NOT NULL,typed_data_digest TEXT NOT NULL UNIQUE,batch_root TEXT NOT NULL REFERENCES replay_batches(root),PRIMARY KEY(chain_id,signer,nonce));');
    return db;
  }catch(e){db.close();throw e;}
}
function consistent(proofs,c,allowed){
  if(!Array.isArray(proofs)||!c||c.status!=='CANDIDATE_ROOT_READY'||
    c.policyVersion!==CONTRACT.policyVersion||c.signerSetVersion!==CONTRACT.signerSetVersion||
    !HEX32.test(c.root??'')||c.count!==proofs.length||
    !Array.isArray(c.items)||c.items.length!==proofs.length)return false;
  const seenNonces=new Set(),seenDigests=new Set();
  for(let i=0;i<proofs.length;i++){
    const x=c.items[i],p=proofs[i];
    if(x?.index!==i||x.status!=='EXACT_CRYPTOGRAPHIC_MATCH'||
      !HEX32.test(x.leafSha256??'')||!HEX32.test(x.digest??'')||
      !ADDR.test(x.signer??'')||!allowed.includes(x.signer)||
      !HEX32.test(p?.typedData?.message?.nonce?.toLowerCase()??'')||
      p.typedData.domain.chainId!==CONTRACT.chainId)return false;
    const key=x.signer+':'+p.typedData.message.nonce.toLowerCase();
    if(seenNonces.has(key)||seenDigests.has(x.digest))return false;
    seenNonces.add(key);seenDigests.add(x.digest);
  }
  return merkleRoot(c.items.map(x=>x.leafSha256))===c.root;
}
function reserveCore(proofs,options,verifier,allowed){
  const {dbPath,nowSec=Math.floor(Date.now()/1000)}=options??{};
  try{databasePath(dbPath);}catch{return deny('DURABLE_DB_PATH_REQUIRED');}
  if(!Number.isSafeInteger(nowSec)||nowSec<0)return deny('INVALID_CURRENT_TIME');
  // CRITICAL: every cryptographic signature and entire batch are verified BEFORE
  // opening SQLite, acquiring a lock, or writing ANY permanent nonce.
  let c;
  try{c=verifier(proofs,{nowSec});}catch{return deny('PROOF_INVALID',{verificationReason:'VERIFIER_ERROR'});}
  if(c?.status!=='CANDIDATE_ROOT_READY')
    return deny('PROOF_INVALID',{verificationReason:c?.reason??'MEMBER_FAILURE'});
  if(!consistent(proofs,c,allowed))return deny('CRYPTOGRAPHIC_BATCH_NOT_READY');
  let db,started=false;
  try{
    db=openDb(dbPath);db.exec('BEGIN IMMEDIATE');started=true;
    const seenNonce=db.prepare('SELECT 1 FROM consumed_nonces WHERE chain_id=? AND signer=? AND nonce=?');
    const seenDigest=db.prepare('SELECT 1 FROM consumed_nonces WHERE typed_data_digest=?');
    const seenRoot=db.prepare('SELECT 1 FROM replay_batches WHERE root=?');
    for(let i=0;i<proofs.length;i++){
      const item=c.items[i],nonce=proofs[i].typedData.message.nonce.toLowerCase();
      if(seenNonce.get(CONTRACT.chainId,item.signer,nonce)||seenDigest.get(item.digest)){
        db.exec('ROLLBACK');started=false;return deny('NONCE_REPLAY');
      }
    }
    if(seenRoot.get(c.root)){
      db.exec('ROLLBACK');started=false;return deny('BATCH_ROOT_REPLAY');
    }
    db.prepare('INSERT INTO replay_batches(root,policy_version,signer_set_version,chain_id,item_count,reserved_at) VALUES(?,?,?,?,?,?)')
      .run(c.root,CONTRACT.policyVersion,CONTRACT.signerSetVersion,CONTRACT.chainId,proofs.length,nowSec);
    const insert=db.prepare('INSERT INTO consumed_nonces(chain_id,signer,nonce,typed_data_digest,batch_root) VALUES(?,?,?,?,?)');
    for(let i=0;i<proofs.length;i++){
      const item=c.items[i],nonce=proofs[i].typedData.message.nonce.toLowerCase();
      insert.run(CONTRACT.chainId,item.signer,nonce,item.digest,c.root);
    }
    db.exec('COMMIT');started=false;
    return {status:'LOCAL_CANDIDATE_RESERVED',root:c.root,count:proofs.length,
      policyVersion:CONTRACT.policyVersion,signerSetVersion:CONTRACT.signerSetVersion,
      noncePersistence:'PERMANENT_PER_CHAIN_SIGNER_NONCE_LOCAL_DB',
      verification:'EIP712_EOA_RECOVERY',issuerNonceVerified:false,
      crossHostReplayProtection:false,authorization:false,onchain:false,
      fundsMoved:false,productionApproved:false};
  }catch(e){
    if(db&&started){try{db.exec('ROLLBACK');}catch{}}
    const msg=String(e?.message||'');
    if(/UNIQUE constraint failed|constraint failed|PRIMARY KEY/i.test(msg))
      return deny('NONCE_REPLAY',{databaseConstraint:true});
    return deny('NONCE_LEDGER_ERROR',{detail:msg.slice(0,140)});
  }finally{if(db){try{db.close();}catch{}}}
}
/** Production-policy entrypoint: canonical authorized signer set only. */
export function reserveBaseBatch(proofs,options={}){
  return reserveCore(proofs,options,verifyBaseProofBatch,CONTRACT.authorizedSigners);
}
/** TEST ONLY: uses real cryptography against deliberately isolated synthetic keys. */
export const __testing=Object.freeze({
  reserveSyntheticSignedBatch:(proofs,options={})=>{
    const allowed=options.testSignerSet??[];
    if(!Array.isArray(allowed)||allowed.length<1||!allowed.every(x=>typeof x==='string'&&ADDR.test(x.toLowerCase())))
      return deny('SYNTHETIC_TEST_SIGNER_SET_REQUIRED');
    const signerSet=allowed.map(x=>x.toLowerCase());
    return reserveCore(proofs,options,
      (items,{nowSec})=>cryptoTest.verifyBaseProofBatch(items,{nowSec,testSignerSet:signerSet}),signerSet);
  }
});
