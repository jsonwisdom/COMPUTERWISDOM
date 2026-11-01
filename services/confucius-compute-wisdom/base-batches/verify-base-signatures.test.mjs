import test from 'node:test';
import assert from 'node:assert/strict';
import { Wallet, TypedDataEncoder } from 'ethers';
import { CONTRACT, verifyBaseProof as verifyProductionProof, verifyBaseProofBatch as verifyProductionBatch, merkleRoot, __testing } from './verify-base-signatures.mjs';
import { readFileSync } from 'node:fs';

const RIGHT=new Wallet('0x'+'77'.repeat(32)); // deterministic TEST ONLY, public and never funded
const WRONG=new Wallet('0x'+'88'.repeat(32)); // deterministic TEST ONLY
const NOW=1700000000;
const TEST_ALLOWLIST=[RIGHT.address,WRONG.address]; // Synthetic keys NEVER production authorized.
const verifyBaseProof=(record,{nowSec}={})=>
  __testing.verifyBaseProof(record,{nowSec,testSignerSet:TEST_ALLOWLIST});
const verifyBaseProofBatch=(records,{nowSec}={})=>
  __testing.verifyBaseProofBatch(records,{nowSec,testSignerSet:TEST_ALLOWLIST});
const policy=JSON.parse(readFileSync(new URL('../../../flywheel-connect/base-wallet-policy.v2.json',import.meta.url),'utf8'));
const CONTROL=[
  {name:'origin',type:'string'},
  {name:'wallet',type:'address'},
  {name:'purpose',type:'string'},
  {name:'nonce',type:'bytes32'},
  {name:'issuedAt',type:'uint256'},
  {name:'expiresAt',type:'uint256'},
  {name:'policy',type:'string'}
];
const DOMAIN_FIELDS=[
  {name:'name',type:'string'},{name:'version',type:'string'},
  {name:'chainId',type:'uint256'},{name:'salt',type:'bytes32'}
];
const copy=x=>structuredClone(x);

async function proof(n=1,options={}){
  const signer=options.signer??RIGHT;
  const issue=options.issuedAt??(NOW-10);
  const domain={name:CONTRACT.name,version:CONTRACT.version,chainId:options.chainId??8453,salt:options.salt??CONTRACT.salt};
  const m={
    origin:CONTRACT.origin,
    wallet:signer.address,
    purpose:CONTRACT.purpose,
    nonce:'0x'+n.toString(16).padStart(64,'0'),
    issuedAt:issue,
    expiresAt:issue+300,
    policy:CONTRACT.policy
  };
  const types={WalletControl:CONTROL};
  const signature=await (options.signerForSignature??signer).signTypedData(domain,types,m);
  return {
    expectedSigner:signer.address,
    typedData:{
      types:{EIP712Domain:DOMAIN_FIELDS,WalletControl:CONTROL},
      primaryType:'WalletControl',domain,message:m
    },
    signature
  };
}

test('C1 synthetic Base EIP-712 matches EXACT expected signer, digest, SHA256 leaf and no authority',async()=>{
  const p=await proof(1);
  const v=verifyBaseProof(p,{nowSec:NOW});
  assert.equal(v.status,'EXACT_CRYPTOGRAPHIC_MATCH');
  assert.equal(v.signer,RIGHT.address.toLowerCase());
  assert.equal(v.typedDataDigest,TypedDataEncoder.hash(p.typedData.domain,{WalletControl:CONTROL},p.typedData.message).toLowerCase());
  assert.match(v.signatureHash,/^0x[0-9a-f]{64}$/);
  assert.match(v.leafSha256,/^0x[0-9a-f]{64}$/);
  const b=verifyBaseProofBatch([p],{nowSec:NOW});
  assert.equal(b.status,'CANDIDATE_ROOT_READY');
  assert.equal(b.root,v.leafSha256);
  assert.equal(b.authorization,false);assert.equal(b.onchain,false);assert.equal(b.fundsMoved,false);
  assert.ok(!JSON.stringify(b).includes(p.signature));
});
test('C2 Ethereum mainnet chain 1 is rejected even with a mathematically valid Ethereum EIP-712 signature',async()=>{
  const p=await proof(2,{chainId:1});
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'NOT_BASE_8453');
});
test('C3 signature produced on chain 1 while falsely labelling the EIP-712 data chain 8453 does not recover authorized account',async()=>{
  const p=await proof(3,{chainId:1});
  p.typedData.domain.chainId=8453;
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_RECOVERED_SIGNER');
});
test('C4 EIP-191 personal_sign cannot substitute for Base EIP-712',async()=>{
  const p=await proof(4);
  p.signature=await RIGHT.signMessage(JSON.stringify(p.typedData));
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_RECOVERED_SIGNER');
});
test('C5 different private key signature fails exactly, even when address and data are unchanged',async()=>{
  const p=await proof(5,{signerForSignature:WRONG});
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_RECOVERED_SIGNER');
});
test('C6 extra or missing authorization fields are rejected, not silently ignored',async()=>{
  const p=await proof(6);
  p.typedData.message.amount='1000000';
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_MESSAGE_FIELDS');
  delete p.typedData.message.amount;
  p.permission='payment';
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_PROOF_FIELDS');
});
test('C7 wrong origin / domain version / message purpose / chain as string all rejected',async()=>{
  const original=await proof(7);
  const cases=[
    {fn:p=>p.typedData.message.origin='https://example.com',reason:'ORIGIN_MISMATCH'},
    {fn:p=>p.typedData.domain.version='3',reason:'DOMAIN_MISMATCH'},
    {fn:p=>p.typedData.message.purpose='Authorize batch transfer',reason:'SCOPE_MISMATCH'},
    {fn:p=>p.typedData.domain.chainId='8453',reason:'NOT_BASE_8453'},
    {fn:p=>p.typedData.message.wallet=WRONG.address,reason:'SIGNER_ADDRESS_MISMATCH'},
    {fn:p=>p.expectedSigner=WRONG.address,reason:'SIGNER_ADDRESS_MISMATCH'},
    {fn:p=>p.typedData.types.WalletControl.reverse(),reason:'CONTROL_TYPE_MISMATCH'}
  ];
  for(const c of cases){const p=copy(original);c.fn(p);assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,c.reason);}
});
test('C8 expires after exactly 300s, refuses stale, future and malformed timestamps',async()=>{
  const p=await proof(8);
  assert.equal(verifyBaseProof(p,{nowSec:NOW+291}).reason,'CHALLENGE_EXPIRED');
  assert.equal(verifyBaseProof(p,{nowSec:NOW-100}).reason,'CHALLENGE_FROM_FUTURE');
  const q=copy(p);
  q.typedData.message.expiresAt+=1;
  assert.equal(verifyBaseProof(q,{nowSec:NOW}).reason,'INVALID_CHALLENGE_WINDOW');
});
test('C9 two valid independently signed records produce deterministic order-bound candidate Merkle root',async()=>{
  const a=await proof(9),b=await proof(10,{signer:WRONG});
  const x=verifyBaseProofBatch([a,b],{nowSec:NOW});
  const repeat=verifyBaseProofBatch([a,b],{nowSec:NOW});
  const swapped=verifyBaseProofBatch([b,a],{nowSec:NOW});
  assert.equal(x.status,'CANDIDATE_ROOT_READY');
  assert.equal(x.root,repeat.root);
  assert.notEqual(x.root,swapped.root);
  assert.equal(x.root,merkleRoot(x.items.map(i=>i.leafSha256)));
  assert.equal(x.count,2);assert.equal(x.valid,2);
  assert.equal(x.authorization,false);assert.equal(x.onchain,false);
});
test('C10 duplicate nonce, even with different timestamps/signatures, holds whole batch and suppresses root',async()=>{
  const a=await proof(11);
  const b=await proof(11,{issuedAt:NOW-5});
  const result=verifyBaseProofBatch([a,b],{nowSec:NOW});
  assert.equal(result.status,'HOLD');
  assert.equal(result.root,null);
  assert.equal(result.items[1].reason,'DUPLICATE_NONCE_OR_PROOF');
});
test('C11 duplicate exact proof digest holds entire batch',async()=>{
  const a=await proof(12);
  const result=verifyBaseProofBatch([a,copy(a)],{nowSec:NOW});
  assert.equal(result.status,'HOLD');
  assert.equal(result.root,null);
  assert.equal(result.items[1].reason,'DUPLICATE_NONCE_OR_PROOF');
});
test('C12 one invalid batch member cannot be promoted by other valid members',async()=>{
  const a=await proof(13),b=await proof(14,{chainId:1});
  const result=verifyBaseProofBatch([a,b],{nowSec:NOW});
  assert.equal(result.status,'HOLD');assert.equal(result.valid,1);
  assert.equal(result.root,null);assert.equal(result.authorization,false);
  assert.equal(result.items[1].reason,'NOT_BASE_8453');
});
test('C13 empty or oversized bulk batch fails closed',async()=>{
  for(const rows of [[],null,new Array(CONTRACT.maxBatchSize+1).fill(null)]){
    const x=verifyBaseProofBatch(rows,{nowSec:NOW});
    assert.equal(x.status,'HOLD');
    assert.equal(x.root,null);
    assert.equal(x.authorization,false);
  }
});
test('C14 malformed EOA signature cannot be accepted as an ownership or contract-wallet proof',async()=>{
  const p=await proof(15);
  p.signature='0x00';
  assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_EOA_SIGNATURE_FORMAT');
  assert.doesNotMatch(JSON.stringify(verifyBaseProof(p,{nowSec:NOW})),/VERIFIED|SUCCESS/);
});
test('C15 odd number of independently signed leaves yields reproducible deterministic candidate root',async()=>{
  const proofs=[await proof(16),await proof(17),await proof(18)];
  const x=verifyBaseProofBatch(proofs,{nowSec:NOW});
  assert.equal(x.status,'CANDIDATE_ROOT_READY');
  assert.equal(x.root,merkleRoot(x.items.map(y=>y.leafSha256)));
  assert.match(x.root,/^0x[0-9a-f]{64}$/);
});

test('C16 signer set is durable, versioned and identical to the Flywheel browser policy',()=>{
 assert.equal(CONTRACT.policyVersion,policy.policyVersion);
 assert.equal(CONTRACT.signerSetVersion,policy.signerSetVersion);
 assert.deepEqual([...CONTRACT.authorizedSigners],policy.authorizedSigners);
 const html=readFileSync(new URL('../../../flywheel-connect/index.html',import.meta.url),'utf8');
 assert.match(html,/const SIGNER_POLICY_VERSION='2.0.0', SIGNER_SET_VERSION='desktop-v1'/);
 assert.match(html,/const ALLOWED_SIGNERS=Object.freeze\(\['0x0f7018fea1dc9ba32ae817d896211f72f1197ad8'\]\)/);
 assert.match(html,/version:'2',chainId:8453/);
 assert.ok(html.includes(policy.domain.salt));
 assert.ok(html.includes("method:'eth_signTypedData_v4'"));
});
test('C17 production policy rejects any valid synthetic signer, even if claimed account and recovery match',async()=>{
 const p=await proof(21);
 const v=verifyProductionProof(p,{nowSec:NOW});
 assert.equal(v.status,'HOLD');
 assert.equal(v.reason,'SIGNER_NOT_AUTHORIZED');
 const batch=verifyProductionBatch([p],{nowSec:NOW});
 assert.equal(batch.status,'HOLD');
 assert.equal(batch.root,null);
});
test('C18 EIP712 verifyingContract is not configured for this offchain protocol; injected contract is rejected',async()=>{
 const p=await proof(22);
 p.typedData.domain.verifyingContract='0x000000000000000000000000000000000000dEaD';
 assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'INVALID_DOMAIN_FIELDS');
 const q=await proof(23);
 q.typedData.types.EIP712Domain.push({name:'verifyingContract',type:'address'});
 assert.equal(verifyBaseProof(q,{nowSec:NOW}).reason,'DOMAIN_TYPE_MISMATCH');
});
test('C19 valid signature for another Base EIP712 salt is rejected',async()=>{
 const p=await proof(24,{salt:'0x'+'aa'.repeat(32)});
 assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'DOMAIN_SALT_MISMATCH');
});
test('C20 old v1 EIP712 signatures are cleanly rejected; format version is mandatory',async()=>{
 const p=await proof(25);
 p.typedData.domain.version='1';
 delete p.typedData.domain.salt;
 p.typedData.types.EIP712Domain.pop();
 p.signature=await RIGHT.signTypedData(p.typedData.domain,{WalletControl:CONTROL},p.typedData.message);
 assert.equal(verifyBaseProof(p,{nowSec:NOW}).reason,'DOMAIN_TYPE_MISMATCH');
});
test('C21 signed origin is part of the EIP712 hash: cross-origin and altered-after-signing proofs fail',async()=>{
 const p=await proof(26);
 const q=structuredClone(p);
 q.typedData.message.origin='https://evil.example';
 assert.equal(verifyBaseProof(q,{nowSec:NOW}).reason,'ORIGIN_MISMATCH');
 const r=await proof(27);
 r.typedData.message.origin='https://evil.example';
 r.signature=await RIGHT.signTypedData(r.typedData.domain,{WalletControl:CONTROL},r.typedData.message);
 assert.equal(verifyBaseProof(r,{nowSec:NOW}).reason,'ORIGIN_MISMATCH');
});
test('C22 empty batch distinct from size violation, not vacuous proof',()=>{
 const result=verifyProductionBatch([],{nowSec:NOW});
 assert.equal(result.status,'HOLD');
 assert.equal(result.reason,'EMPTY_BATCH');
 assert.equal(result.root,null);
});
test('C23 canonical policy has only explicitly scoped desktop signer, never public synthetic test keys',()=>{
 assert.equal(policy.authority,false);
 assert.equal(policy.scope,'offchain_wallet_control_only');
 assert.equal(policy.authorizedSigners.length,1);
 assert.ok(!policy.authorizedSigners.includes(RIGHT.address.toLowerCase()));
 assert.ok(!policy.authorizedSigners.includes(WRONG.address.toLowerCase()));
});
