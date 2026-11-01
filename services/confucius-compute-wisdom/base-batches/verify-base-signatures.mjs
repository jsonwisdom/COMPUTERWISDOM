/**
 * CoinBaseKidSignatureProofExactMatch v1
 * Offline-only EIP-712 Base 8453 cryptographic proof gate.
 * No wallet interactions, RPC, transactions, key material, ENS resolutions, or publishing.
 */
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { getAddress, verifyTypedData, TypedDataEncoder } from 'ethers';

export const CONTRACT = Object.freeze({
  label:'COINBASEKID_BASE_SIGNATURE_EXACT_MATCH_V1',
  chainId:8453,
  name:'Flywheel Base Wallet Control',
  version:'1',
  origin:'https://wallet.jsonwisdom.com',
  purpose:'Prove control of this account on Base ONLY',
  policy:'No transaction, token approval, payment, login, ENS/DNS ownership proof or Coinbase API authorization',
  expirySeconds:300,
  maxFutureSkewSeconds:30,
  maxBatchSize:1000,
});

const DOMAIN_FIELDS=[
  {name:'name',type:'string'},{name:'version',type:'string'},{name:'chainId',type:'uint256'}
];
const CONTROL_FIELDS=[
  {name:'origin',type:'string'},
  {name:'wallet',type:'address'},
  {name:'purpose',type:'string'},
  {name:'nonce',type:'bytes32'},
  {name:'issuedAt',type:'uint256'},
  {name:'expiresAt',type:'uint256'},
  {name:'policy',type:'string'}
];
const HEX65=/^0x[0-9a-fA-F]{130}$/;
const HEX32=/^0x[0-9a-fA-F]{64}$/;
const HEX20=/^0x[0-9a-fA-F]{40}$/;

function insist(p,code){if(!p)throw Error(code);}
function object(p){return p!==null && typeof p==='object' && !Array.isArray(p);}
function exactKeys(o,keys,code){
  insist(object(o),code);
  const actual=Object.keys(o).sort().join('|');
  insist(actual===keys.slice().sort().join('|'),code);
}
function matchFields(fields,expected,code){
  insist(Array.isArray(fields)&&JSON.stringify(fields)===JSON.stringify(expected),code);
}
function addressOf(x){
  insist(typeof x==='string'&&HEX20.test(x),'INVALID_ADDRESS');
  return getAddress(x).toLowerCase();
}
function normalizeNow(nowSec){
  insist(Number.isSafeInteger(nowSec)&&nowSec>=0,'INVALID_CURRENT_TIME');
  return nowSec;
}
function sha256(data){
  return '0x'+createHash('sha256').update(data).digest('hex');
}
function exactLeaf(p){
  // length/order are fixed and include the exact EIP-712 digest and signature hash.
  const tuple=JSON.stringify([
    CONTRACT.label,p.signer,p.typedDataDigest,p.signatureHash
  ]);
  return sha256(Buffer.concat([Buffer.from([0]),Buffer.from(tuple,'utf8')]));
}
export function merkleRoot(leaves){
  insist(Array.isArray(leaves)&&leaves.length>0&&leaves.every(x=>HEX32.test(x)),'INVALID_LEAVES');
  let nodes=leaves.map(x=>Buffer.from(x.slice(2),'hex'));
  while(nodes.length>1){
    const next=[];
    for(let i=0;i<nodes.length;i+=2){
      const l=nodes[i],r=nodes[i+1]??nodes[i];
      next.push(createHash('sha256').update(Buffer.concat([Buffer.from([1]),l,r])).digest());
    }
    nodes=next;
  }
  return '0x'+nodes[0].toString('hex');
}

/**
 * Does NOT establish historical origin, ENS ownership, authorization, or onchain status.
 * Inputs can be replayed offline until expiry; the caller must establish provenance
 * and fresh challenge issuance separately.
 */
export function verifyBaseProof(record,{nowSec=Math.floor(Date.now()/1000)}={}){
  try{
    const now=normalizeNow(nowSec);
    exactKeys(record,['expectedSigner','typedData','signature'],'INVALID_PROOF_FIELDS');
    const expected=addressOf(record.expectedSigner);
    insist(typeof record.signature==='string'&&HEX65.test(record.signature),'INVALID_EOA_SIGNATURE_FORMAT');
    const td=record.typedData;
    exactKeys(td,['types','primaryType','domain','message'],'INVALID_TYPED_DATA_FIELDS');
    exactKeys(td.types,['EIP712Domain','WalletControl'],'INVALID_TYPE_SET');
    matchFields(td.types.EIP712Domain,DOMAIN_FIELDS,'DOMAIN_TYPE_MISMATCH');
    matchFields(td.types.WalletControl,CONTROL_FIELDS,'CONTROL_TYPE_MISMATCH');
    insist(td.primaryType==='WalletControl','PRIMARY_TYPE_MISMATCH');
    exactKeys(td.domain,['name','version','chainId'],'INVALID_DOMAIN_FIELDS');
    insist(td.domain.name===CONTRACT.name&&td.domain.version===CONTRACT.version,'DOMAIN_MISMATCH');
    insist(typeof td.domain.chainId==='number'&&td.domain.chainId===CONTRACT.chainId,'NOT_BASE_8453');
    exactKeys(td.message,CONTROL_FIELDS.map(x=>x.name),'INVALID_MESSAGE_FIELDS');
    const m=td.message;
    insist(m.origin===CONTRACT.origin,'ORIGIN_MISMATCH');
    insist(m.purpose===CONTRACT.purpose&&m.policy===CONTRACT.policy,'SCOPE_MISMATCH');
    const actual=addressOf(m.wallet);
    insist(expected===actual,'SIGNER_ADDRESS_MISMATCH');
    insist(typeof m.nonce==='string'&&HEX32.test(m.nonce),'INVALID_NONCE');
    insist(Number.isSafeInteger(m.issuedAt)&&Number.isSafeInteger(m.expiresAt)&&
      m.issuedAt>=0&&m.expiresAt===m.issuedAt+CONTRACT.expirySeconds,'INVALID_CHALLENGE_WINDOW');
    insist(m.issuedAt<=now+CONTRACT.maxFutureSkewSeconds,'CHALLENGE_FROM_FUTURE');
    insist(now<=m.expiresAt,'CHALLENGE_EXPIRED');
    const domain=td.domain;
    const types={WalletControl:td.types.WalletControl};
    const recovered=addressOf(verifyTypedData(domain,types,m,record.signature));
    insist(recovered===expected,'INVALID_RECOVERED_SIGNER');
    const digest=TypedDataEncoder.hash(domain,types,m).toLowerCase();
    const signatureHash=sha256(Buffer.from(record.signature.slice(2),'hex'));
    const result={
      status:'EXACT_CRYPTOGRAPHIC_MATCH',
      signer:expected,
      typedDataDigest:digest,
      signatureHash,
      nonce:m.nonce.toLowerCase()
    };
    return {...result,leafSha256:exactLeaf(result)};
  }catch(e){
    return {status:'HOLD',reason:String(e?.message||'UNKNOWN_VERIFICATION_ERROR').slice(0,120)};
  }
}

/**
 * Every item must validate, every nonce must be unique.
 * No partial green batch, no authorization by mere batch membership.
 */
export function verifyBaseProofBatch(records,{nowSec=Math.floor(Date.now()/1000)}={}){
  if(!Array.isArray(records)||records.length===0||records.length>CONTRACT.maxBatchSize)
    return {status:'HOLD',reason:'BATCH_SIZE_OUT_OF_RANGE',count:Array.isArray(records)?records.length:0,items:[],root:null,authorization:false,onchain:false};
  const now=normalizeNow(nowSec);
  const items=[];
  const nonces=new Set();
  const digests=new Set();
  for(let i=0;i<records.length;i++){
    const result=verifyBaseProof(records[i],{nowSec:now});
    if(result.status!=='EXACT_CRYPTOGRAPHIC_MATCH'){
      items.push({index:i,status:'HOLD',reason:result.reason});continue;
    }
    if(nonces.has(result.nonce)||digests.has(result.typedDataDigest)){
      items.push({index:i,status:'HOLD',reason:'DUPLICATE_NONCE_OR_PROOF'});continue;
    }
    nonces.add(result.nonce);
    digests.add(result.typedDataDigest);
    // Only digests and hashes are reported. Never echo the signature bytes.
    items.push({index:i,status:'EXACT_CRYPTOGRAPHIC_MATCH',signer:result.signer,digest:result.typedDataDigest,leafSha256:result.leafSha256});
  }
  const all=items.length===records.length&&items.every(x=>x.status==='EXACT_CRYPTOGRAPHIC_MATCH');
  return {
    status:all?'CANDIDATE_ROOT_READY':'HOLD',
    count:records.length,
    valid:items.filter(x=>x.status==='EXACT_CRYPTOGRAPHIC_MATCH').length,
    items,
    root:all?merkleRoot(items.map(x=>x.leafSha256)):null,
    authorization:false,
    onchain:false,
    fundsMoved:false,
    productionApproved:false
  };
}

if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  try{
    const text=readFileSync(0,{encoding:'utf8'});
    insist(text.length<=4000000,'INPUT_TOO_LARGE');
    const payload=JSON.parse(text);
    exactKeys(payload,['proofs'],'INVALID_BATCH_FIELDS');
    const outcome=verifyBaseProofBatch(payload.proofs);
    process.stdout.write(JSON.stringify(outcome,null,2)+'\n');
    if(outcome.status!=='CANDIDATE_ROOT_READY')process.exitCode=1;
  }catch(e){
    process.stdout.write(JSON.stringify({status:'HOLD',reason:String(e?.message||'INVALID_INPUT').slice(0,120),authorization:false,onchain:false})+'\n');
    process.exitCode=1;
  }
}
