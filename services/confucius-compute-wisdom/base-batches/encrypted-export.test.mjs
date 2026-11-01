import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { generateKeyPairSync, createHash } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { Wallet } from 'ethers';
import { CONTRACT } from './verify-base-signatures.mjs';
import { __testing as ledgerTest } from './replay-ledger.mjs';
import { WITNESS_POLICY, WITNESS_FIELDS, __testing as witnessTest } from './acceptance-witness.mjs';
import { EXPORT_POLICY, EXPORT_FIELDS, createEncryptedProofExport, decryptExportEnvelope,
  __testing as exportTest } from './encrypted-export.mjs';

const BATCH=new Wallet('0x'+'77'.repeat(32));
const WITNESS=new Wallet('0x'+'99'.repeat(32));
const CREATOR=new Wallet('0x'+'55'.repeat(32));
const EXPORT=new Wallet('0x'+'66'.repeat(32));
const OTHER=new Wallet('0x'+'88'.repeat(32));
const NOW=1793560818, BLOCK=24600000;
const DOMAIN_FIELDS=[
 {name:'name',type:'string'},{name:'version',type:'string'},
 {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}];
const CONTROL=[
 {name:'origin',type:'string'},{name:'wallet',type:'address'},
 {name:'purpose',type:'string'},{name:'nonce',type:'bytes32'},
 {name:'issuedAt',type:'uint256'},{name:'expiresAt',type:'uint256'},
 {name:'policy',type:'string'}
];
const nonce=n=>'0x'+n.toString(16).padStart(64,'0');
const clone=x=>structuredClone(x);
function recipient(){
 const pair=generateKeyPairSync('x25519');
 const publicKeyPem=pair.publicKey.export({type:'spki',format:'pem'}).toString();
 const privateKeyPem=pair.privateKey.export({type:'pkcs8',format:'pem'}).toString();
 const fingerprint='0x'+createHash('sha256').update(pair.publicKey.export({type:'spki',format:'der'})).digest('hex');
 return {publicKeyPem,privateKeyPem,fingerprint};
}
async function batchProof(n){
 const domain={name:CONTRACT.name,version:CONTRACT.version,chainId:8453,salt:CONTRACT.salt};
 const message={origin:CONTRACT.origin,wallet:BATCH.address,purpose:CONTRACT.purpose,
   nonce:nonce(n),issuedAt:NOW-10,expiresAt:NOW+290,policy:CONTRACT.policy};
 return {expectedSigner:BATCH.address,typedData:{
   types:{EIP712Domain:DOMAIN_FIELDS,WalletControl:CONTROL},
   primaryType:'WalletControl',domain,message
 },signature:await BATCH.signTypedData(domain,{WalletControl:CONTROL},message)};
}
async function witnessProof(root,n){
 const domain={...WITNESS_POLICY.domain};
 const message={origin:WITNESS_POLICY.origin,root,
   createdAtBlock:BLOCK,observedAtBlock:BLOCK+2,observedAt:NOW+3,
   witnessNonce:nonce(n),purpose:WITNESS_POLICY.witnessedPurpose};
 return {expectedSigner:WITNESS.address,typedData:{
   types:{EIP712Domain:DOMAIN_FIELDS,AcceptanceWitness:WITNESS_FIELDS},
   primaryType:'AcceptanceWitness',domain,message
 },signature:await WITNESS.signTypedData(domain,{AcceptanceWitness:WITNESS_FIELDS},message)};
}
async function authorization(root,key,n,{scope='full',signer=EXPORT,actualSigner=signer,
  issuedAt=NOW+10,expiresAt=NOW+200,recipientId='did:example:reviewer'}={}){
 const domain={...EXPORT_POLICY.domain};
 const message={origin:EXPORT_POLICY.origin,action:'EXPORT_PROOF_BUNDLE',
   bundleRoot:root,recipient:recipientId,recipientKeyFingerprint:key.fingerprint,
   scope,issuedAt,expiresAt,exportNonce:nonce(n),
   exportAuthority:signer.address,purpose:EXPORT_POLICY.purpose};
 return {expectedSigner:signer.address,typedData:{
   types:{EIP712Domain:DOMAIN_FIELDS,ExportAuthorization:EXPORT_FIELDS},
   primaryType:'ExportAuthorization',domain,message
 },signature:await actualSigner.signTypedData(domain,{ExportAuthorization:EXPORT_FIELDS},message)};
}
function make(){
 const dir=mkdtempSync(join(tmpdir(),'coinbasekid-export-'));
 return {file:join(dir,'ledger.sqlite'),clean:()=>rmSync(dir,{recursive:true,force:true})};
}
async function accepted(file,n){
 const proof=await batchProof(n);
 const reserved=ledgerTest.reserveSyntheticSignedBatch([proof],{
   dbPath:file,nowSec:NOW,testSignerSet:[BATCH.address]});
 assert.equal(reserved.status,'LOCAL_CANDIDATE_RESERVED');
 const witness=await witnessProof(reserved.root,n+1000);
 const att=witnessTest.record({root:reserved.root,creator:CREATOR.address,
   createdAtBlock:BLOCK,witnesses:[witness],publication:false},{
    dbPath:file,nowSec:NOW+6,testWitnessSigners:[WITNESS.address]});
 assert.equal(att.status,'LOCAL_WITNESS_RECORDED');
 return {root:reserved.root,proof,witness};
}
const req=(base,auth)=>({root:base.root,creator:CREATOR.address,
  createdAtBlock:BLOCK,witnesses:[base.witness],proofs:[base.proof],authorization:auth});
const exportIt=(request,file,key,allowed=[EXPORT.address])=>exportTest.create(request,{
  dbPath:file,nowSec:NOW+12,recipientPublicKeyPem:key.publicKeyPem,
  testWitnessSigners:[WITNESS.address],testExportAuthorities:allowed,
  testBatchSigners:[BATCH.address]});
function eventRows(file){
 const db=new DatabaseSync(file);
 try{
  const exists=db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='export_events'").get();
  return exists?db.prepare('SELECT event_id,root,recipient,scope FROM export_events ORDER BY event_id').all():[];
 }finally{db.close();}
}

test('E1 authentic independent export authority signs scope and an X25519 recipient alone decrypts the full bundle',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2001),key=recipient();
  const auth=await authorization(base.root,key,3001);
  const out=exportIt(req(base,auth),s.file,key);
  assert.equal(out.status,'LOCAL_ENCRYPTED_EXPORT_CANDIDATE');
  assert.equal(out.publication,false);
  assert.equal(out.authority,false);
  assert.equal(out.fundsMoved,false);
  assert.ok(!JSON.stringify(out.envelope).includes(base.proof.signature));
  assert.ok(!JSON.stringify(out.envelope).includes(base.witness.signature));
  const plaintext=decryptExportEnvelope(out.envelope,key.privateKeyPem);
  assert.deepEqual(plaintext.proofs,[base.proof]);
  assert.deepEqual(plaintext.witnesses,[base.witness]);
  assert.equal(plaintext.root,base.root);
  assert.equal(eventRows(s.file).length,1);
  console.log('REPLAY007_EXPORT '+JSON.stringify({
    crypto:'X25519_HKDF_SHA256_AES256GCM',recipientOnlyDecrypt:true,
    unauthorizedKeyRejected:true,events:1,productionExportEnabled:false,payments:false
  }));
 }finally{s.clean()}
});
test('E2 wrong X25519 private key cannot decrypt, even with full encrypted envelope',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2002),key=recipient(),wrong=recipient();
  const out=exportIt(req(base,await authorization(base.root,key,3002)),s.file,key);
  assert.equal(out.status,'LOCAL_ENCRYPTED_EXPORT_CANDIDATE');
  assert.throws(()=>decryptExportEnvelope(out.envelope,wrong.privateKeyPem),/NOT_INTENDED_RECIPIENT_KEY/);
  const altered=clone(out.envelope);
  const bytes=Buffer.from(altered.ciphertext,'base64');bytes[0]^=1;altered.ciphertext=bytes.toString('base64');
  assert.throws(()=>decryptExportEnvelope(altered,key.privateKeyPem));
 }finally{s.clean()}
});
test('E3 root_only releases no signature fields even after authorized recipient decrypts',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2003),key=recipient();
  const auth=await authorization(base.root,key,3003,{scope:'root_only'});
  const out=exportIt(req(base,auth),s.file,key);
  assert.equal(out.status,'LOCAL_ENCRYPTED_EXPORT_CANDIDATE');
  const plaintext=decryptExportEnvelope(out.envelope,key.privateKeyPem);
  assert.deepEqual(plaintext,{root:base.root,createdAtBlock:BLOCK});
  assert.doesNotMatch(JSON.stringify(plaintext),/signature/i);
  assert.doesNotMatch(JSON.stringify(out.envelope),/signature/i);
 }finally{s.clean()}
});
test('E4 proofs_only scope decrypts exactly proofs, no witness/private creator fields',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2004),key=recipient();
  const auth=await authorization(base.root,key,3004,{scope:'proofs_only'});
  const out=exportIt(req(base,auth),s.file,key);
  const plaintext=decryptExportEnvelope(out.envelope,key.privateKeyPem);
  assert.deepEqual(plaintext,{root:base.root,proofs:[base.proof]});
  assert.ok(!Object.hasOwn(plaintext,'witnesses'));
  assert.ok(!Object.hasOwn(plaintext,'creator'));
 }finally{s.clean()}
});
test('E5 creator, batch signer and witness can never self-authorize export even if explicitly allowlisted in test',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2005),key=recipient();
  for(const signer of [CREATOR,BATCH,WITNESS]){
    const a=await authorization(base.root,key,3005,{signer});
    const out=exportIt(req(base,a),s.file,key,[signer.address]);
    assert.equal(out.status,'HOLD');
    assert.equal(out.reason,'EXPORT_SIGNER_NOT_INDEPENDENT');
  }
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
test('E6 expired export signature is rejected with no event row',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2006),key=recipient();
  const auth=await authorization(base.root,key,3006,{issuedAt:NOW-400,expiresAt:NOW-100});
  const result=exportIt(req(base,auth),s.file,key);
  assert.equal(result.status,'HOLD');assert.equal(result.reason,'EXPORT_EXPIRED');
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
test('E7 wrong recipient encryption public key fails signed fingerprint binding',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2007),correct=recipient(),wrong=recipient();
  const auth=await authorization(base.root,correct,3007);
  const result=exportIt(req(base,auth),s.file,wrong);
  assert.equal(result.reason,'RECIPIENT_KEY_BINDING_MISMATCH');
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
test('E8 same root can generate two distinct signed authorized export events; logs append, not toggle',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2008),key=recipient();
  const a1=await authorization(base.root,key,3008);
  const a2=await authorization(base.root,key,3009);
  const one=exportIt(req(base,a1),s.file,key);
  const two=exportIt(req(base,a2),s.file,key);
  assert.equal(one.status,'LOCAL_ENCRYPTED_EXPORT_CANDIDATE');
  assert.equal(two.status,'LOCAL_ENCRYPTED_EXPORT_CANDIDATE');
  assert.ok(two.eventId>one.eventId);
  assert.deepEqual(eventRows(s.file).map(x=>x.event_id),[one.eventId,two.eventId]);
  assert.equal(one.root,two.root);
 }finally{s.clean()}
});
test('E9 one signed export nonce cannot be reused to create a second log event',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2009),key=recipient();
  const auth=await authorization(base.root,key,3010);
  assert.equal(exportIt(req(base,auth),s.file,key).status,'LOCAL_ENCRYPTED_EXPORT_CANDIDATE');
  const replay=exportIt(req(base,auth),s.file,key);
  assert.equal(replay.status,'HOLD');
  assert.equal(replay.reason,'EXPORT_NONCE_REPLAY');
  assert.equal(eventRows(s.file).length,1);
 }finally{s.clean()}
});
test('E10 wrong cryptographic export signer is rejected',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2010),key=recipient();
  const auth=await authorization(base.root,key,3011,{actualSigner:OTHER});
  const out=exportIt(req(base,auth),s.file,key);
  assert.equal(out.reason,'EXPORT_SIGNATURE_NOT_AUTHORITY');
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
test('E11 orphan bundle lacking independently recorded witness cannot be exported',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2011),key=recipient();
  const db=new DatabaseSync(s.file);
  try{db.exec('PRAGMA foreign_keys=ON;');
    db.prepare('DELETE FROM witness_nonces WHERE root=?').run(base.root);
    db.prepare('DELETE FROM witness_attestations WHERE root=?').run(base.root);
  }finally{db.close()}
  const out=exportIt(req(base,await authorization(base.root,key,3012)),s.file,key);
  assert.equal(out.reason,'NO_WITNESS');
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
test('E12 production export is impossible without an out-of-band independent authority',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2012),key=recipient();
  const auth=await authorization(base.root,key,3013);
  const out=createEncryptedProofExport(req(base,auth),{
    dbPath:s.file,nowSec:NOW+12,recipientPublicKeyPem:key.publicKeyPem});
  assert.equal(out.status,'HOLD');
  assert.equal(out.reason,'EXPORT_AUTHORITY_NOT_CONFIGURED');
  assert.equal(EXPORT_POLICY.productionEnabled,false);
  assert.equal(EXPORT_POLICY.authorizedExportAuthorities.length,0);
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
test('E13 recipient cannot alter signed scope or bundle root to extract more data',async()=>{
 const s=make();try{
  const base=await accepted(s.file,2013),key=recipient();
  const auth=await authorization(base.root,key,3014,{scope:'root_only'});
  const changed=clone(auth);changed.typedData.message.scope='full';
  assert.equal(exportIt(req(base,changed),s.file,key).reason,'EXPORT_SIGNATURE_NOT_AUTHORITY');
  const diffRoot=clone(auth);diffRoot.typedData.message.bundleRoot='0x'+'ab'.repeat(32);
  assert.equal(exportIt(req(base,diffRoot),s.file,key).reason,'EXPORT_ROOT_MISMATCH');
  assert.equal(eventRows(s.file).length,0);
 }finally{s.clean()}
});
