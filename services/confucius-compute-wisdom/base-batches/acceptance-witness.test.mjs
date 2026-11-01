import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { Wallet } from 'ethers';
import { CONTRACT } from './verify-base-signatures.mjs';
import { __testing as ledgerTest } from './replay-ledger.mjs';
import { WITNESS_POLICY,WITNESS_FIELDS,recordAcceptanceWitness,
  checkWitnessForPublication,__testing as witnessTest } from './acceptance-witness.mjs';

const BATCH=new Wallet('0x'+'77'.repeat(32));
const WITNESS=new Wallet('0x'+'99'.repeat(32));
const CREATOR=new Wallet('0x'+'55'.repeat(32));
const OTHER=new Wallet('0x'+'88'.repeat(32));
const NOW=1793560818, CREATED_BLOCK=24600000;
const WALLET_FIELDS=[
  {name:'origin',type:'string'},{name:'wallet',type:'address'},
  {name:'purpose',type:'string'},{name:'nonce',type:'bytes32'},
  {name:'issuedAt',type:'uint256'},{name:'expiresAt',type:'uint256'},
  {name:'policy',type:'string'}
];
const W_DOMAIN_FIELDS=[
  {name:'name',type:'string'},{name:'version',type:'string'},
  {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}
];
const nonce=n=>'0x'+n.toString(16).padStart(64,'0');
const clone=x=>structuredClone(x);
async function batchProof(n){
 const domain={name:CONTRACT.name,version:CONTRACT.version,chainId:8453,salt:CONTRACT.salt};
 const message={origin:CONTRACT.origin,wallet:BATCH.address,purpose:CONTRACT.purpose,
   nonce:nonce(n),issuedAt:NOW-10,expiresAt:NOW+290,policy:CONTRACT.policy};
 const signature=await BATCH.signTypedData(domain,{WalletControl:WALLET_FIELDS},message);
 return {expectedSigner:BATCH.address,signature,typedData:{
   types:{EIP712Domain:W_DOMAIN_FIELDS,WalletControl:WALLET_FIELDS},
   primaryType:'WalletControl',domain,message}};
}
async function witnessProof(root,n,{signer=WITNESS,observedAtBlock=CREATED_BLOCK+2,
  createdAtBlock=CREATED_BLOCK,observedAt=NOW+3,wrongSigningKey=null}={}){
 const domain={...WITNESS_POLICY.domain};
 const message={origin:WITNESS_POLICY.origin,root,createdAtBlock,observedAtBlock,
   observedAt,witnessNonce:nonce(n),purpose:WITNESS_POLICY.witnessedPurpose};
 return {expectedSigner:signer.address,
   typedData:{types:{EIP712Domain:W_DOMAIN_FIELDS,
     AcceptanceWitness:WITNESS_FIELDS.map(x=>({...x}))},
     primaryType:'AcceptanceWitness',domain,message},
   signature:await (wrongSigningKey??signer).signTypedData(domain,
     {AcceptanceWitness:WITNESS_FIELDS},message)};
}
function context(){
 const dir=mkdtempSync(join(tmpdir(),'coinbasekid-witness-'));
 return {dir,file:join(dir,'nonce.sqlite'),cleanup:()=>rmSync(dir,{recursive:true,force:true})};
}
async function reserve(file,n){
 const proof=await batchProof(n);
 const result=ledgerTest.reserveSyntheticSignedBatch([proof],
   {dbPath:file,nowSec:NOW,testSignerSet:[BATCH.address]});
 assert.equal(result.status,'LOCAL_CANDIDATE_RESERVED');
 return result.root;
}
const bundle=(root,proof,{creator=CREATOR.address,publication=false,
   createdAtBlock=CREATED_BLOCK}={})=>({
 root,creator,createdAtBlock,witnesses:proof?[proof]:[],publication
});
const enroll=(record,file)=>witnessTest.record(record,{
 dbPath:file,nowSec:NOW+6,testWitnessSigners:[WITNESS.address]
});
const review=(record,file)=>witnessTest.checkPublication(record,{
 dbPath:file,nowSec:NOW+8,testWitnessSigners:[WITNESS.address]
});
function witnessCounts(file){
 const db=new DatabaseSync(file);
 try{
  return {
   attestations:Number(db.prepare("SELECT count(*) n FROM sqlite_master WHERE type='table' AND name='witness_attestations'").get().n)
      ?Number(db.prepare('SELECT count(*) n FROM witness_attestations').get().n):0,
   nonces:Number(db.prepare("SELECT count(*) n FROM sqlite_master WHERE type='table' AND name='witness_nonces'").get().n)
      ?Number(db.prepare('SELECT count(*) n FROM witness_nonces').get().n):0
  };
 }finally{db.close()}
}
test('W1 strict independent witness signs exact accepted batch root/block; one durable attestation',async()=>{
 const c=context();try{
  const root=await reserve(c.file,101);
  const w=await witnessProof(root,201);
  const result=enroll(bundle(root,w),c.file);
  assert.equal(result.status,'LOCAL_WITNESS_RECORDED');
  assert.equal(result.root,root);
  assert.equal(result.witness,WITNESS.address.toLowerCase());
  assert.equal(result.observedAtBlock,CREATED_BLOCK+2);
  assert.equal(result.publication,false);
  assert.deepEqual(witnessCounts(c.file),{attestations:1,nonces:1});
  const reviewed=review(bundle(root,w,{publication:true}),c.file);
  assert.equal(reviewed.status,'WITNESS_PRESENT_REVIEW_ONLY');
  assert.equal(reviewed.publication,false);
  console.log('REPLAY007_WITNESS '+JSON.stringify({status:result.status,
   independentlyRecovered:true,createdBlock:CREATED_BLOCK,observedBlock:CREATED_BLOCK+2,
   publication:false,productionWitnessEnrolled:false,payments:false}));
 }finally{c.cleanup()}
});
test('W2 zero witnesses for publication:true return NO_WITNESS; no historical evidence',async()=>{
 const c=context();try{
  const root=await reserve(c.file,102);
  const check=review(bundle(root,null,{publication:true}),c.file);
  assert.equal(check.status,'HOLD');
  assert.equal(check.reason,'NO_WITNESS');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W3 witness signer must differ from batch signer even if signature is cryptographically valid',async()=>{
 const c=context();try{
  const root=await reserve(c.file,103);
  const w=await witnessProof(root,203,{signer:BATCH});
  const result=witnessTest.record(bundle(root,w),{dbPath:c.file,nowSec:NOW+6,
    testWitnessSigners:[BATCH.address]});
  assert.equal(result.status,'HOLD');
  assert.equal(result.reason,'WITNESS_IS_BATCH_SIGNER');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W4 witness must differ from creator; self-witness fails',async()=>{
 const c=context();try{
  const root=await reserve(c.file,104);
  const w=await witnessProof(root,204);
  const result=enroll(bundle(root,w,{creator:WITNESS.address}),c.file);
  assert.equal(result.reason,'WITNESS_IS_CREATOR');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W5 unattested foreign root and changed signed root fail; witness signing does not approve altered bundle',async()=>{
 const c=context();try{
  const rootA=await reserve(c.file,105);
  const rootB=await reserve(c.file,106);
  const w=await witnessProof(rootA,205);
  assert.equal(enroll(bundle(rootB,w),c.file).reason,'WITNESS_ROOT_MISMATCH');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W6 block-height observation must be inside [createdAtBlock, createdAtBlock+WINDOW]',async()=>{
 const c=context();try{
  const root=await reserve(c.file,107);
  const high=await witnessProof(root,207,{observedAtBlock:CREATED_BLOCK+WITNESS_POLICY.maximumBlockWindow+1});
  assert.equal(enroll(bundle(root,high),c.file).reason,'WITNESS_BLOCK_WINDOW');
  const low=await witnessProof(root,208,{observedAtBlock:CREATED_BLOCK-1});
  assert.equal(enroll(bundle(root,low),c.file).reason,'WITNESS_BLOCK_WINDOW');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W7 two separately reserved bundle roots cannot reuse a witness nonce, even with different valid signatures',async()=>{
 const c=context();try{
  const rootA=await reserve(c.file,108);
  const rootB=await reserve(c.file,109);
  const first=await witnessProof(rootA,209),second=await witnessProof(rootB,209);
  assert.equal(enroll(bundle(rootA,first),c.file).status,'LOCAL_WITNESS_RECORDED');
  const duplicate=enroll(bundle(rootB,second),c.file);
  assert.equal(duplicate.status,'HOLD');
  assert.equal(duplicate.reason,'WITNESS_NONCE_REPLAY');
  assert.deepEqual(witnessCounts(c.file),{attestations:1,nonces:1});
 }finally{c.cleanup()}
});
test('W8 exactly one persisted attestation per root; duplicate and two-witness inputs HOLD',async()=>{
 const c=context();try{
  const root=await reserve(c.file,110);
  const w=await witnessProof(root,210),another=await witnessProof(root,211);
  const multiple=bundle(root,w);multiple.witnesses.push(another);
  assert.equal(enroll(multiple,c.file).reason,'NO_WITNESS');
  assert.equal(enroll(bundle(root,w),c.file).status,'LOCAL_WITNESS_RECORDED');
  assert.equal(enroll(bundle(root,another),c.file).reason,'WITNESS_ALREADY_RECORDED');
  assert.deepEqual(witnessCounts(c.file),{attestations:1,nonces:1});
 }finally{c.cleanup()}
});
test('W9 mis-signed witness, wrong domain, wrong chain or unrelated signer fail before witness DB writes',async()=>{
 const c=context();try{
  const root=await reserve(c.file,111);
  const wrong=await witnessProof(root,212,{wrongSigningKey:OTHER});
  assert.equal(enroll(bundle(root,wrong),c.file).reason,'WITNESS_SIGNER_MISMATCH');
  const changed=await witnessProof(root,213);
  changed.typedData.domain.chainId=1;
  assert.equal(enroll(bundle(root,changed),c.file).reason,'WITNESS_DOMAIN_MISMATCH');
  const notAllowed=await witnessProof(root,214,{signer:OTHER});
  assert.equal(enroll(bundle(root,notAllowed),c.file).reason,'WITNESS_NOT_AUTHORIZED');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W10 witness event time must be acceptance-bound and fresh, not future or late',async()=>{
 const c=context();try{
  const root=await reserve(c.file,112);
  const old=await witnessProof(root,215,{observedAt:NOW-400});
  assert.equal(enroll(bundle(root,old),c.file).reason,'WITNESS_TIME_WINDOW');
  const future=await witnessProof(root,216,{observedAt:NOW+800});
  assert.equal(enroll(bundle(root,future),c.file).reason,'WITNESS_TIME_WINDOW');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W11 production has no registered independent witness: returns HOLD, no event or publication',async()=>{
 const c=context();try{
  const root=await reserve(c.file,113),w=await witnessProof(root,217);
  assert.deepEqual(WITNESS_POLICY.authorizedWitnesses,[]);
  assert.equal(WITNESS_POLICY.productionEnabled,false);
  assert.equal(recordAcceptanceWitness(bundle(root,w),{dbPath:c.file,nowSec:NOW+6}).reason,'WITNESS_NOT_CONFIGURED');
  assert.equal(checkWitnessForPublication(bundle(root,w,{publication:true}),{dbPath:c.file,nowSec:NOW+6}).reason,'WITNESS_NOT_CONFIGURED');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
test('W12 stored attestation cannot be replaced or read as valid if payload changes',async()=>{
 const c=context();try{
  const root=await reserve(c.file,114),w=await witnessProof(root,218);
  assert.equal(enroll(bundle(root,w),c.file).status,'LOCAL_WITNESS_RECORDED');
  const altered=structuredClone(w);
  altered.typedData.message.observedAtBlock++;
  const result=review(bundle(root,altered,{publication:true}),c.file);
  assert.equal(result.status,'HOLD');
  assert.equal(result.reason,'WITNESS_NOT_RECORDED_EXACTLY');
  assert.deepEqual(witnessCounts(c.file),{attestations:1,nonces:1});
 }finally{c.cleanup()}
});

test('W13 publication with plausible signed witness but no persisted witness table returns NO_WITNESS',async()=>{
 const c=context();try{
  const root=await reserve(c.file,115),w=await witnessProof(root,219);
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
  const r=review(bundle(root,w,{publication:true}),c.file);
  assert.equal(r.status,'HOLD');
  assert.equal(r.reason,'NO_WITNESS');
  assert.deepEqual(witnessCounts(c.file),{attestations:0,nonces:0});
 }finally{c.cleanup()}
});
