import test from 'node:test';
import assert from 'node:assert/strict';
import { Wallet, TypedDataEncoder } from 'ethers';
import { CONTRACT, verifyBaseProof, verifyBaseProofBatch, merkleRoot } from './verify-base-signatures.mjs';

const RIGHT=new Wallet('0x'+'77'.repeat(32)); // deterministic TEST ONLY, public and never funded
const WRONG=new Wallet('0x'+'88'.repeat(32)); // deterministic TEST ONLY
const NOW=1700000000;
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
  {name:'name',type:'string'},{name:'version',type:'string'},{name:'chainId',type:'uint256'}
];
const copy=x=>structuredClone(x);

async function proof(n=1,options={}){
  const signer=options.signer??RIGHT;
  const issue=options.issuedAt??(NOW-10);
  const domain={name:CONTRACT.name,version:CONTRACT.version,chainId:options.chainId??8453};
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
    {fn:p=>p.typedData.domain.version='2',reason:'DOMAIN_MISMATCH'},
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
