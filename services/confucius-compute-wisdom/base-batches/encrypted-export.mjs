/**
 * REPLAY 007 §5b — signed, scope-bound, recipient-key-encrypted PRIVATE
 * export candidate. No HTTP endpoint, publication, payment or onchain calls.
 * Production FAIL CLOSED: no independent witness / export signer enrolled.
 */
import { readFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { resolve } from 'node:path';
import {
  createHash, createPublicKey, createPrivateKey, generateKeyPairSync,
  diffieHellman, randomBytes, hkdfSync, createCipheriv, createDecipheriv
} from 'node:crypto';
import { getAddress, verifyTypedData, TypedDataEncoder } from 'ethers';
import { CONTRACT, verifyBaseProofBatch, __testing as batchTest } from './verify-base-signatures.mjs';
import { checkWitnessForPublication, __testing as witnessTest } from './acceptance-witness.mjs';

const POLICY=JSON.parse(readFileSync(new URL('./export-policy.v1.json',import.meta.url),'utf8'));
if(POLICY.schema!=='COINBASEKID_PRIVATE_EXPORT_POLICY_V1'||
  POLICY.productionEnabled!==false||POLICY.authorizedExportAuthorities.length!==0||
  POLICY.externalAuthorityVerification!=='NOT_ESTABLISHED'||
  POLICY.domain.chainId!==8453)throw Error('EXPORT_PRODUCTION_POLICY_UNEXPECTED');
export const EXPORT_POLICY=Object.freeze({...POLICY});
export const EXPORT_FIELDS=Object.freeze([
  {name:'origin',type:'string'},
  {name:'action',type:'string'},
  {name:'bundleRoot',type:'bytes32'},
  {name:'recipient',type:'string'},
  {name:'recipientKeyFingerprint',type:'bytes32'},
  {name:'scope',type:'string'},
  {name:'issuedAt',type:'uint256'},
  {name:'expiresAt',type:'uint256'},
  {name:'exportNonce',type:'bytes32'},
  {name:'exportAuthority',type:'address'},
  {name:'purpose',type:'string'}
]);
const DOMAIN_FIELDS=[
  {name:'name',type:'string'},{name:'version',type:'string'},
  {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}
];
const HEX32=/^0x[0-9a-fA-F]{64}$/;
const SIG65=/^0x[0-9a-fA-F]{130}$/;
const ADDRESS=/^0x[0-9a-fA-F]{40}$/;
const deny=(reason,detail)=>({status:'HOLD',reason,detail,
  authority:false,publication:false,onchain:false,fundsMoved:false});
function insist(ok,code){if(!ok)throw Error(code);}
function exact(obj,fields,code){
  insist(obj!==null&&typeof obj==='object'&&!Array.isArray(obj)&&
    Object.keys(obj).sort().join('|')===[...fields].sort().join('|'),code);
}
function addr(s){insist(typeof s==='string'&&ADDRESS.test(s),'INVALID_ADDRESS');return getAddress(s).toLowerCase();}
function dbFile(s){insist(typeof s==='string'&&s.trim()&&s!==':memory:'&&!s.startsWith('file:')&&!s.includes('\0'),'DURABLE_DB_REQUIRED');return resolve(s);}
function digestBytes(bytes){return '0x'+createHash('sha256').update(bytes).digest('hex');}
const hhex=s=>digestBytes(Buffer.from(s.slice(2),'hex'));
const validNumber=n=>Number.isSafeInteger(n)&&n>=0;
function recipientKey(key){
  insist(typeof key==='string'&&key.length<=10000,'INVALID_RECIPIENT_KEY');
  const obj=createPublicKey(key);
  insist(obj.asymmetricKeyType==='x25519','RECIPIENT_KEY_NOT_X25519');
  const der=obj.export({type:'spki',format:'der'});
  return {key:obj,fingerprint:digestBytes(der)};
}
function prepareAuth(auth,root,creator,batchSigners,witness,recipientFingerprint,nowSec,allowed){
  exact(auth,['expectedSigner','typedData','signature'],'INVALID_EXPORT_AUTH');
  insist(typeof auth.signature==='string'&&SIG65.test(auth.signature),'INVALID_EXPORT_SIGNATURE');
  const signer=addr(auth.expectedSigner);
  insist(allowed.includes(signer),'EXPORT_AUTHORITY_NOT_ALLOWED');
  insist(signer!==creator&&!batchSigners.includes(signer)&&signer!==witness,
    'EXPORT_SIGNER_NOT_INDEPENDENT');
  const td=auth.typedData;
  exact(td,['types','primaryType','domain','message'],'INVALID_EXPORT_TYPED_DATA');
  exact(td.types,['EIP712Domain','ExportAuthorization'],'INVALID_EXPORT_TYPES');
  insist(JSON.stringify(td.types.EIP712Domain)===JSON.stringify(DOMAIN_FIELDS)&&
    JSON.stringify(td.types.ExportAuthorization)===JSON.stringify(EXPORT_FIELDS),'EXPORT_TYPES_MISMATCH');
  insist(td.primaryType==='ExportAuthorization','EXPORT_PRIMARY_TYPE');
  exact(td.domain,['name','version','chainId','salt'],'EXPORT_DOMAIN_FIELDS');
  for(const key of ['name','version','chainId','salt'])
    insist(td.domain[key]===POLICY.domain[key],'EXPORT_DOMAIN_MISMATCH');
  exact(td.message,EXPORT_FIELDS.map(x=>x.name),'EXPORT_MESSAGE_FIELDS');
  const m=td.message;
  insist(m.action==='EXPORT_PROOF_BUNDLE','INVALID_EXPORT_ACTION');
  insist(m.origin===POLICY.origin,'EXPORT_ORIGIN_MISMATCH');
  insist(m.purpose===POLICY.purpose,'EXPORT_PURPOSE_MISMATCH');
  insist(m.bundleRoot===root,'EXPORT_ROOT_MISMATCH');
  insist(typeof m.recipient==='string'&&m.recipient.length<=180&&
    (m.recipient.startsWith('did:')||ADDRESS.test(m.recipient)),'INVALID_EXPORT_RECIPIENT');
  insist(m.recipientKeyFingerprint===recipientFingerprint,'RECIPIENT_KEY_BINDING_MISMATCH');
  insist(POLICY.allowedScopes.includes(m.scope),'EXPORT_SCOPE_INVALID');
  insist(typeof m.exportNonce==='string'&&HEX32.test(m.exportNonce),'EXPORT_NONCE_INVALID');
  insist(addr(m.exportAuthority)===signer,'EXPORT_AUTHORITY_ADDRESS_MISMATCH');
  insist(validNumber(m.issuedAt)&&validNumber(m.expiresAt)&&
    m.expiresAt>m.issuedAt&&m.expiresAt<=m.issuedAt+POLICY.maxLifetimeSeconds,'EXPORT_EXPIRY_INVALID');
  insist(nowSec>=m.issuedAt-POLICY.maxLifetimeSeconds/10,'EXPORT_FUTURE');
  insist(nowSec<=m.expiresAt,'EXPORT_EXPIRED');
  const recovered=addr(verifyTypedData(td.domain,
    {ExportAuthorization:td.types.ExportAuthorization},m,auth.signature));
  insist(recovered===signer,'EXPORT_SIGNATURE_NOT_AUTHORITY');
  return {signer,record:m,authDigest:TypedDataEncoder.hash(td.domain,
    {ExportAuthorization:td.types.ExportAuthorization},m).toLowerCase()};
}
function confidentialPayload(bundle,scope){
  if(scope==='root_only')return {root:bundle.root,createdAtBlock:bundle.createdAtBlock};
  if(scope==='proofs_only')return {root:bundle.root,proofs:bundle.proofs};
  return {root:bundle.root,creator:bundle.creator,createdAtBlock:bundle.createdAtBlock,
    witnesses:bundle.witnesses,proofs:bundle.proofs};
}
function encryptPayload(plaintext,recipient,metadata){
  const ephemeral=generateKeyPairSync('x25519');
  const shared=diffieHellman({privateKey:ephemeral.privateKey,publicKey:recipient.key});
  const salt=randomBytes(32),iv=randomBytes(12);
  const aad=Buffer.from(JSON.stringify(metadata),'utf8');
  const k=Buffer.from(hkdfSync('sha256',shared,salt,
    Buffer.from('COINBASEKID_EXPORT_ENVELOPE_V1','utf8'),32));
  const cipher=createCipheriv('aes-256-gcm',k,iv);
  cipher.setAAD(aad);
  const ciphertext=Buffer.concat([cipher.update(Buffer.from(JSON.stringify(plaintext),'utf8')),cipher.final()]);
  const tag=cipher.getAuthTag();
  k.fill(0);shared.fill(0);
  return {...metadata,scheme:'X25519-HKDF-SHA256-AES-256-GCM',
    ephemeralPublicKey:ephemeral.publicKey.export({type:'spki',format:'der'}).toString('base64'),
    hkdfSalt:salt.toString('base64'),iv:iv.toString('base64'),
    ciphertext:ciphertext.toString('base64'),tag:tag.toString('base64')};
}
/** Recipient-side local decrypt, never an HTTP server operation. */
export function decryptExportEnvelope(envelope,privateKeyPem){
  exact(envelope,['schema','root','recipient','recipientKeyFingerprint','scope',
    'expiresAt','eventNonce','authorizationDigest','scheme','ephemeralPublicKey',
    'hkdfSalt','iv','ciphertext','tag'],'INVALID_EXPORT_ENVELOPE');
  insist(envelope.schema==='COINBASEKID_ENCRYPTED_EXPORT_V1'&&
    envelope.scheme==='X25519-HKDF-SHA256-AES-256-GCM','INVALID_ENCRYPTION_SCHEME');
  const key=createPrivateKey(privateKeyPem);
  insist(key.asymmetricKeyType==='x25519','NOT_X25519_PRIVATE_KEY');
  const publicKey=createPublicKey(key);
  insist(digestBytes(publicKey.export({type:'spki',format:'der'}))===
    envelope.recipientKeyFingerprint,'NOT_INTENDED_RECIPIENT_KEY');
  const theirKey=createPublicKey({key:Buffer.from(envelope.ephemeralPublicKey,'base64'),
    type:'spki',format:'der'});
  insist(theirKey.asymmetricKeyType==='x25519','INVALID_EPHEMERAL_KEY');
  const shared=diffieHellman({privateKey:key,publicKey:theirKey});
  const hk=Buffer.from(hkdfSync('sha256',shared,Buffer.from(envelope.hkdfSalt,'base64'),
    Buffer.from('COINBASEKID_EXPORT_ENVELOPE_V1','utf8'),32));
  const {scheme,ephemeralPublicKey,hkdfSalt,iv,ciphertext,tag,...aadFields}=envelope;
  const decipher=createDecipheriv('aes-256-gcm',hk,Buffer.from(iv,'base64'));
  decipher.setAAD(Buffer.from(JSON.stringify(aadFields),'utf8'));
  decipher.setAuthTag(Buffer.from(tag,'base64'));
  try{
    const plaintext=Buffer.concat([decipher.update(Buffer.from(ciphertext,'base64')),decipher.final()]);
    const obj=JSON.parse(plaintext.toString('utf8'));
    insist(obj.root===envelope.root,'DECRYPTED_ROOT_MISMATCH');
    return obj;
  }finally{hk.fill(0);shared.fill(0);}
}
function openDb(path){
  const db=new DatabaseSync(dbFile(path));
  try{db.exec('PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; PRAGMA synchronous=FULL;');
    return db;}catch(e){db.close();throw e;}
}
function runExport(request,opts,configuration){
  if(!configuration.allowedAuthorities.length)return deny('EXPORT_AUTHORITY_NOT_CONFIGURED');
  const {dbPath,nowSec=Math.floor(Date.now()/1000),recipientPublicKeyPem}=opts??{};
  if(!validNumber(nowSec))return deny('INVALID_CLOCK');
  let db,tx=false;
  try{
    exact(request,['root','creator','createdAtBlock','witnesses','proofs','authorization'],'INVALID_EXPORT_REQUEST');
    insist(typeof request.root==='string'&&HEX32.test(request.root),'INVALID_ROOT');
    const creator=addr(request.creator);
    const recipient=recipientKey(recipientPublicKeyPem);
    const candidateBundle={root:request.root,creator:request.creator,
      createdAtBlock:request.createdAtBlock,witnesses:request.witnesses,publication:true};
    const reviewed=configuration.witnessReview(candidateBundle,{dbPath,nowSec});
    insist(reviewed.status==='WITNESS_PRESENT_REVIEW_ONLY',
      reviewed.reason==='NO_WITNESS'?'NO_WITNESS':'WITNESS_REQUIRED');
    // Re-verify historical signatures at the separately witnessed acceptance
    // timestamp; using wall-clock "now" would falsely expire archival proofs.
    const observedAt=request.witnesses[0].typedData.message.observedAt;
    const proof=configuration.proofVerifier(request.proofs,{nowSec:observedAt});
    insist(proof?.status==='CANDIDATE_ROOT_READY'&&proof.root===request.root,'BUNDLE_PROOFS_INVALID');
    db=openDb(dbPath);
    const recorded=db.prepare('SELECT DISTINCT signer FROM consumed_nonces WHERE batch_root=?').all(request.root).map(x=>x.signer.toLowerCase());
    insist(recorded.length>0,'BATCH_NOT_RESERVED');
    const signers=[...new Set(proof.items.map(x=>x.signer))].sort();
    insist(JSON.stringify(signers)===JSON.stringify(recorded.sort()),'BUNDLE_SIGNER_SET_MISMATCH');
    const parsed=prepareAuth(request.authorization,request.root,creator,recorded,
      reviewed.witness,recipient.fingerprint,nowSec,configuration.allowedAuthorities);
    const payload=confidentialPayload(request,parsed.record.scope);
    const metadata={
      schema:'COINBASEKID_ENCRYPTED_EXPORT_V1',
      root:request.root,
      recipient:parsed.record.recipient,
      recipientKeyFingerprint:recipient.fingerprint,
      scope:parsed.record.scope,
      expiresAt:parsed.record.expiresAt,
      eventNonce:parsed.record.exportNonce.toLowerCase(),
      authorizationDigest:parsed.authDigest
    };
    const envelope=encryptPayload(payload,recipient,metadata);
    const ciphertextHash=digestBytes(Buffer.from(envelope.ciphertext,'base64'));
    db.exec('BEGIN IMMEDIATE');tx=true;
    db.exec('CREATE TABLE IF NOT EXISTS export_events (event_id INTEGER PRIMARY KEY AUTOINCREMENT,root TEXT NOT NULL REFERENCES replay_batches(root),authority TEXT NOT NULL,recipient TEXT NOT NULL,recipient_key_hash TEXT NOT NULL,scope TEXT NOT NULL,authorization_digest TEXT NOT NULL UNIQUE,authorization_typed_data TEXT NOT NULL,authorization_signature TEXT NOT NULL,envelope_sha256 TEXT NOT NULL,created_at INTEGER NOT NULL);CREATE TABLE IF NOT EXISTS export_nonces (chain_id INTEGER NOT NULL CHECK(chain_id=8453),authority TEXT NOT NULL,nonce TEXT NOT NULL,event_id INTEGER NOT NULL REFERENCES export_events(event_id),PRIMARY KEY(chain_id,authority,nonce));');
    if(db.prepare('SELECT 1 FROM export_nonces WHERE chain_id=8453 AND authority=? AND nonce=?').get(parsed.signer,metadata.eventNonce))
      throw Error('EXPORT_NONCE_REPLAY');
    const result=db.prepare('INSERT INTO export_events(root,authority,recipient,recipient_key_hash,scope,authorization_digest,authorization_typed_data,authorization_signature,envelope_sha256,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)')
      .run(request.root,parsed.signer,metadata.recipient,recipient.fingerprint,metadata.scope,
        metadata.authorizationDigest,JSON.stringify(request.authorization.typedData),
        request.authorization.signature,ciphertextHash,nowSec);
    db.prepare('INSERT INTO export_nonces(chain_id,authority,nonce,event_id) VALUES(8453,?,?,?)')
      .run(parsed.signer,metadata.eventNonce,Number(result.lastInsertRowid));
    db.exec('COMMIT');tx=false;
    return {status:'LOCAL_ENCRYPTED_EXPORT_CANDIDATE',envelope,
      eventId:Number(result.lastInsertRowid),root:request.root,scope:metadata.scope,
      publication:false,authority:false,onchain:false,fundsMoved:false,
      witnessIndependence:'SYNTHETIC_TEST_ONLY_UNLESS_INDEPENDENTLY_ENROLLED',
      recipientIdentityVerified:false};
  }catch(e){
    if(tx){try{db.exec('ROLLBACK')}catch{}}
    const message=String(e?.message||'EXPORT_ERROR');
    return deny(/UNIQUE constraint/i.test(message)?'EXPORT_NONCE_REPLAY':message.slice(0,150));
  }finally{if(db){try{db.close()}catch{}}}
}
export function createEncryptedProofExport(request,opts={}){
  return runExport(request,opts,{
    allowedAuthorities:POLICY.authorizedExportAuthorities,
    witnessReview:checkWitnessForPublication,
    proofVerifier:verifyBaseProofBatch
  });
}
/** Offline, synthetic-key TEST ONLY; never export into an HTTP route. */
export const __testing=Object.freeze({
  create:(request,opts={})=>{
    const witnesses=(opts.testWitnessSigners??[]).map(addr);
    const authorities=(opts.testExportAuthorities??[]).map(addr);
    const builders=(opts.testBatchSigners??[]).map(addr);
    return runExport(request,opts,{
      allowedAuthorities:authorities,
      witnessReview:(bundle,o)=>witnessTest.checkPublication(bundle,{...o,testWitnessSigners:witnesses}),
      proofVerifier:(records,o)=>batchTest.verifyBaseProofBatch(records,{...o,testSignerSet:builders})
    });
  }
});
