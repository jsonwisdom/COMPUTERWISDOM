/**
 * REPLAY 007 §5a: Local candidate acceptance-time witness attestation.
 * Witness must be an independent role, not the batch signer or alleged creator.
 * Production witness allowlist intentionally EMPTY until out-of-band enrollment.
 * No RPC, signing keys, export, publication, blockchain settlement or payment.
 */
import { readFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { getAddress, verifyTypedData, TypedDataEncoder } from 'ethers';
import { CONTRACT } from './verify-base-signatures.mjs';

const POLICY=JSON.parse(readFileSync(new URL('./witness-policy.v1.json',import.meta.url),'utf8'));
if(POLICY.schema!=='COINBASEKID_ACCEPTANCE_WITNESS_POLICY_V1'||
   POLICY.version!=='1.0.0'||POLICY.domain.chainId!==8453||
   POLICY.productionEnabled!==false||POLICY.authorizedWitnesses.length!==0||
   POLICY.externalKeyRegistration!=='NOT_ESTABLISHED')
  throw Error('PRODUCTION_WITNESS_POLICY_UNEXPECTED');
export const WITNESS_POLICY=Object.freeze({...POLICY,domain:Object.freeze({...POLICY.domain}),
  authorizedWitnesses:Object.freeze([...POLICY.authorizedWitnesses])});
const EIP712_DOMAIN=[
  {name:'name',type:'string'},{name:'version',type:'string'},
  {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}
];
export const WITNESS_FIELDS=Object.freeze([
  {name:'origin',type:'string'},
  {name:'root',type:'bytes32'},
  {name:'createdAtBlock',type:'uint256'},
  {name:'observedAtBlock',type:'uint256'},
  {name:'observedAt',type:'uint256'},
  {name:'witnessNonce',type:'bytes32'},
  {name:'purpose',type:'string'}
]);
const HASH32=/^0x[0-9a-fA-F]{64}$/;
const ADDRESS=/^0x[0-9a-fA-F]{40}$/;
const SIG65=/^0x[0-9a-fA-F]{130}$/;
const deny=(reason,extra={})=>({
  status:'HOLD',reason,authority:false,publication:false,
  exportAuthorized:false,onchain:false,fundsMoved:false,...extra
});
const isObj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
function exact(x,expected,code){
  if(!isObj(x)||Object.keys(x).sort().join('|')!==[...expected].sort().join('|'))throw Error(code);
}
function eq(a,b,code){if(a!==b)throw Error(code);}
function address(value){if(typeof value!=='string'||!ADDRESS.test(value))throw Error('INVALID_WITNESS_OR_CREATOR_ADDRESS');return getAddress(value).toLowerCase();}
function hash(value){return '0x'+createHash('sha256').update(Buffer.from(value.slice(2),'hex')).digest('hex');}
function dbPath(file){if(typeof file!=='string'||!file.trim()||file===':memory:'||file.startsWith('file:')||file.includes('\0'))throw Error('DURABLE_DB_REQUIRED');return resolve(file);}
function validInt(x){return Number.isSafeInteger(x)&&x>=0;}
function openedDb(file){
  const db=new DatabaseSync(dbPath(file),{readOnly:false});
  try{db.exec('PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; PRAGMA synchronous=FULL;');return db;}
  catch(e){db.close();throw e;}
}
function readLedgerBatch(db,root){
  const batch=db.prepare('SELECT root, reserved_at, chain_id FROM replay_batches WHERE root=?').get(root);
  if(!batch)throw Error('BATCH_NOT_RESERVED');
  if(batch.chain_id!==8453)throw Error('NOT_BASE_8453');
  const signers=db.prepare('SELECT DISTINCT signer FROM consumed_nonces WHERE batch_root=? ORDER BY signer').all(root).map(x=>x.signer.toLowerCase());
  if(!signers.length)throw Error('BATCH_SIGNERS_MISSING');
  return {batch,signers};
}
function checkWitness(att, context, allowed, nowSec){
  exact(att,['expectedSigner','typedData','signature'],'INVALID_WITNESS_RECORD');
  if(typeof att.signature!=='string'||!SIG65.test(att.signature))throw Error('INVALID_WITNESS_SIGNATURE');
  const signer=address(att.expectedSigner);
  if(!allowed.includes(signer))throw Error('WITNESS_NOT_AUTHORIZED');
  if(signer===context.creator)throw Error('WITNESS_IS_CREATOR');
  if(context.batchSigners.includes(signer))throw Error('WITNESS_IS_BATCH_SIGNER');
  const td=att.typedData;
  exact(td,['types','primaryType','domain','message'],'INVALID_WITNESS_TYPED_DATA');
  exact(td.types,['EIP712Domain','AcceptanceWitness'],'INVALID_WITNESS_TYPES');
  if(JSON.stringify(td.types.EIP712Domain)!==JSON.stringify(EIP712_DOMAIN)||
     JSON.stringify(td.types.AcceptanceWitness)!==JSON.stringify(WITNESS_FIELDS))throw Error('WITNESS_TYPE_MISMATCH');
  eq(td.primaryType,'AcceptanceWitness','INVALID_WITNESS_PRIMARY_TYPE');
  exact(td.domain,['name','version','chainId','salt'],'INVALID_WITNESS_DOMAIN_FIELDS');
  for(const field of ['name','version','chainId','salt']){
    eq(td.domain[field],POLICY.domain[field],'WITNESS_DOMAIN_MISMATCH');
  }
  exact(td.message,WITNESS_FIELDS.map(x=>x.name),'INVALID_WITNESS_FIELDS');
  const m=td.message;
  eq(m.origin,POLICY.origin,'WITNESS_ORIGIN_MISMATCH');
  eq(m.purpose,POLICY.witnessedPurpose,'WITNESS_PURPOSE_MISMATCH');
  eq(m.root,context.root,'WITNESS_ROOT_MISMATCH');
  eq(m.createdAtBlock,context.createdAtBlock,'WITNESS_CREATED_BLOCK_MISMATCH');
  if(!HASH32.test(m.witnessNonce)||!validInt(m.createdAtBlock)||!validInt(m.observedAtBlock)||!validInt(m.observedAt))
    throw Error('WITNESS_TIME_NONCE_INVALID');
  if(m.observedAtBlock<m.createdAtBlock||
     m.observedAtBlock>m.createdAtBlock+POLICY.maximumBlockWindow)throw Error('WITNESS_BLOCK_WINDOW');
  if(m.observedAt<context.reservedAt-POLICY.maximumClockSkewSeconds||
     m.observedAt>context.reservedAt+POLICY.maximumAcceptanceLagSeconds||
     m.observedAt>nowSec+POLICY.maximumClockSkewSeconds||
     nowSec>m.observedAt+POLICY.maximumAcceptanceLagSeconds)
    throw Error('WITNESS_TIME_WINDOW');
  const recovered=address(verifyTypedData(td.domain,
    {AcceptanceWitness:td.types.AcceptanceWitness},td.message,att.signature));
  eq(recovered,signer,'WITNESS_SIGNER_MISMATCH');
  return {
    signer,nonce:m.witnessNonce.toLowerCase(),signatureHash:hash(att.signature),
    typedDataDigest:TypedDataEncoder.hash(td.domain,
      {AcceptanceWitness:td.types.AcceptanceWitness},td.message).toLowerCase(),
    observedAtBlock:m.observedAtBlock,observedAt:m.observedAt
  };
}
function validateInputs(bundle, nowSec, db){
  if(!validInt(nowSec))throw Error('INVALID_CLOCK');
  exact(bundle,['root','creator','createdAtBlock','witnesses','publication'],'INVALID_BUNDLE_METADATA');
  if(typeof bundle.root!=='string'||!HASH32.test(bundle.root))throw Error('INVALID_ROOT');
  if(!validInt(bundle.createdAtBlock))throw Error('INVALID_CREATED_BLOCK');
  if(!Array.isArray(bundle.witnesses)||bundle.witnesses.length!==1)throw Error('NO_WITNESS');
  const creator=address(bundle.creator);
  const {batch,signers}=readLedgerBatch(db,bundle.root);
  return {root:bundle.root,creator,createdAtBlock:bundle.createdAtBlock,
    batchSigners:signers,reservedAt:batch.reserved_at};
}
function validateAndRecord(bundle,{dbPath:sqliteFile,nowSec=Math.floor(Date.now()/1000)}={},allowed){
  if(!allowed.length)return deny('WITNESS_NOT_CONFIGURED');
  let db,transaction=false;
  try{
    // Read-only checks first, so malformed evidence is rejected before writes.
    db=openedDb(sqliteFile);
    const context=validateInputs(bundle,nowSec,db);
    if(bundle.publication!==false)throw Error('PUBLICATION_MUST_REMAIN_FALSE');
    const v=checkWitness(bundle.witnesses[0],context,allowed,nowSec);
    db.exec('BEGIN IMMEDIATE');transaction=true;
    // Re-check the reservation inside the write transaction.
    const current=readLedgerBatch(db,bundle.root);
    if(current.batch.reserved_at!==context.reservedAt||
       current.signers.join('|')!==context.batchSigners.join('|'))
      throw Error('BATCH_CHANGED');
    db.exec('CREATE TABLE IF NOT EXISTS witness_attestations (root TEXT PRIMARY KEY REFERENCES replay_batches(root),witness_signer TEXT NOT NULL,nonce TEXT NOT NULL,signature TEXT NOT NULL,typed_data TEXT NOT NULL,signature_hash TEXT NOT NULL UNIQUE,typed_data_digest TEXT NOT NULL UNIQUE,creator_claim TEXT NOT NULL,created_at_block INTEGER NOT NULL,observed_at_block INTEGER NOT NULL,observed_at INTEGER NOT NULL);CREATE TABLE IF NOT EXISTS witness_nonces (chain_id INTEGER NOT NULL CHECK(chain_id=8453),witness_signer TEXT NOT NULL,nonce TEXT NOT NULL,root TEXT NOT NULL REFERENCES witness_attestations(root),PRIMARY KEY(chain_id,witness_signer,nonce));');
    if(db.prepare('SELECT 1 FROM witness_attestations WHERE root=?').get(bundle.root))
      throw Error('WITNESS_ALREADY_RECORDED');
    if(db.prepare('SELECT 1 FROM witness_nonces WHERE chain_id=8453 AND witness_signer=? AND nonce=?')
      .get(v.signer,v.nonce))throw Error('WITNESS_NONCE_REPLAY');
    db.prepare('INSERT INTO witness_attestations(root,witness_signer,nonce,signature,typed_data,signature_hash,typed_data_digest,creator_claim,created_at_block,observed_at_block,observed_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)')
      .run(bundle.root,v.signer,v.nonce,bundle.witnesses[0].signature,JSON.stringify(bundle.witnesses[0].typedData),
        v.signatureHash,v.typedDataDigest,context.creator,context.createdAtBlock,v.observedAtBlock,v.observedAt);
    db.prepare('INSERT INTO witness_nonces(chain_id,witness_signer,nonce,root) VALUES(8453,?,?,?)')
      .run(v.signer,v.nonce,bundle.root);
    db.exec('COMMIT');transaction=false;
    return {status:'LOCAL_WITNESS_RECORDED',root:bundle.root,witness:v.signer,
      observedAtBlock:v.observedAtBlock,publication:false,authority:false,
      exportAuthorized:false,onchain:false,fundsMoved:false,
      realBlockVerified:false,creatorIdentityVerified:false,
      independentWitnessEnrolled:false};
  }catch(e){
    if(transaction){try{db.exec('ROLLBACK')}catch{}}
    let reason=String(e?.message||'WITNESS_UNKNOWN_ERROR');
    if(/UNIQUE constraint/i.test(reason))reason='WITNESS_REUSE';
    return deny(reason.slice(0,160));
  }finally{if(db){try{db.close()}catch{}}}
}
export function recordAcceptanceWitness(bundle,opts={}){
  return validateAndRecord(bundle,opts,POLICY.authorizedWitnesses);
}
/**
 * Read-only publication safety check: validates exactly one persisted witness
 * for root and signer independence. Does not actually publish or grant access.
 */
function inspectPublication(bundle,{dbPath:sqliteFile,nowSec=Math.floor(Date.now()/1000)}={},allowed){
  if(!allowed.length)return deny('WITNESS_NOT_CONFIGURED');
  let db;
  try{
    db=openedDb(sqliteFile);
    if(bundle?.publication!==true)throw Error('PUBLICATION_NOT_REQUESTED');
    const base={...bundle,publication:false};
    const context=validateInputs(base,nowSec,db);
    const row=db.prepare("SELECT * FROM witness_attestations WHERE root=?").get(bundle.root);
    if(!row)throw Error('NO_WITNESS');
    if(row.witness_signer!==address(base.witnesses[0].expectedSigner)||
       row.signature!==base.witnesses[0].signature||
       row.typed_data!==JSON.stringify(base.witnesses[0].typedData))
      throw Error('WITNESS_NOT_RECORDED_EXACTLY');
    const v=checkWitness(base.witnesses[0],context,allowed,row.observed_at);
    if(v.signatureHash!==row.signature_hash||v.typedDataDigest!==row.typed_data_digest)
      throw Error('WITNESS_RECORD_CORRUPT');
    const count=db.prepare('SELECT COUNT(*) n FROM witness_attestations WHERE root=?').get(bundle.root).n;
    if(count!==1)throw Error('WITNESS_COUNT_INVALID');
    return {status:'WITNESS_PRESENT_REVIEW_ONLY',root:bundle.root,witness:v.signer,
      publication:false,authority:false,exportAuthorized:false,realBlockVerified:false,
      creatorIdentityVerified:false,onchain:false,fundsMoved:false};
  }catch(e){return deny(String(e?.message||'NO_WITNESS').slice(0,160));}
  finally{if(db){try{db.close()}catch{}}}
}
export function checkWitnessForPublication(bundle,opts={}){
  return inspectPublication(bundle,opts,POLICY.authorizedWitnesses);
}
/** TEST ONLY: separate synthetic witness from an equally synthetic batch signer. */
export const __testing=Object.freeze({
  record:(bundle,opts={})=>validateAndRecord(bundle,opts,
    (opts.testWitnessSigners??[]).map(address)),
  checkPublication:(bundle,opts={})=>inspectPublication(bundle,opts,
    (opts.testWitnessSigners??[]).map(address))
});
