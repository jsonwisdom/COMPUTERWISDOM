import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { webcrypto } from 'node:crypto';
import { Wallet, verifyTypedData } from 'ethers';

const html=readFileSync(new URL('./index.html',import.meta.url),'utf8');
const match=html.match(/<script>\s*'use strict';([\s\S]*?)<\/script>/);
assert.ok(match,'wallet script missing');
const ADDRESS='0x0F7018fea1dc9ba32aE817D896211f72f1197AD8';
const OTHER='0x'+'aa'.repeat(20);
const TEST_SIGNER=new Wallet('0x'+'77'.repeat(32)); // Public, unfunded synthetic key. NEVER use with actual funds.
const WRONG_SIGNER=new Wallet('0x'+'88'.repeat(32));

function harness({race=false, signer=null, rejected=false, wrongSignature=false, changeOnSignature=false, signWrongChain=false}={}){
 const fields=Object.fromEntries(['connect','status','address','verify','verification','challengePreview','previewHint']
  .map(id=>[id,{textContent:'',className:'',disabled:id==='verify',hidden:id==='challengePreview'||id==='previewHint',events:new Map(),
   addEventListener(name,fn){this.events.set(name,fn)}}]));
 const walletEvents={},calls=[];
 let address=signer?.address??ADDRESS,chain='0x1',chainReads=0;
 const provider={
  isCoinbaseWallet:true,
  on(name,fn){walletEvents[name]=fn},
  removeListener(name){delete walletEvents[name]},
  async request({method,params}){
   calls.push({method,params});
   switch(method){
    case 'eth_requestAccounts':return [address];
    case 'eth_accounts':return [address];
    case 'eth_chainId':
     chainReads++;
     if(race&&chainReads===3){address=OTHER;walletEvents.accountsChanged?.([address]);}
     return chain;
    case 'wallet_switchEthereumChain':
     assert.equal(params?.[0]?.chainId,'0x2105');
     chain='0x2105';walletEvents.chainChanged?.(chain);return null;
    case 'eth_signTypedData_v4': {
     if(rejected)throw Object.assign(Error('User declined'),{code:4001});
     assert.ok(signer,'Never sign with real desktop wallet in CI');
     assert.equal(params?.[0].toLowerCase(),signer.address.toLowerCase());
     assert.equal(typeof params?.[1],'string');
     const typed=JSON.parse(params[1]);
     assert.equal(typed.domain.chainId,8453,'Base domain chainId must be 8453');
     assert.equal(typed.domain.name,'Flywheel Base Wallet Control');
     assert.equal(typed.domain.version,'2');
     assert.equal(typed.domain.salt,'0xf09262a7cdc2a8dd05f80ed656604534efaba598f0d9a1b7016a60af6f1ec275');
     assert.ok(!Object.hasOwn(typed.domain,'verifyingContract'));
     assert.equal(typed.domain.version,'2');
     assert.equal(typed.primaryType,'WalletControl');
     assert.equal(typed.message.origin,'https://wallet.jsonwisdom.com');
     assert.equal(typed.message.wallet.toLowerCase(),signer.address.toLowerCase());
     assert.match(typed.message.purpose,/Base ONLY/);
     assert.match(typed.message.nonce,/^0x[0-9a-f]{64}$/);
     assert.match(typed.message.policy,/No transaction, token approval, payment/);
     assert.equal(typed.message.expiresAt-typed.message.issuedAt,300);
     if(changeOnSignature){address=OTHER;walletEvents.accountsChanged?.([address]);}
     const domain=signWrongChain?{...typed.domain,chainId:1}:typed.domain;
     return (wrongSignature?WRONG_SIGNER:signer).signTypedData(domain,{WalletControl:typed.types.WalletControl},typed.message);
    }
    default:throw Error('Unexpected wallet method: '+method);
   }
  }
 };
 const window={ethereum:provider,ethers:{verifyTypedData},addEventListener(){},dispatchEvent(){}};
 const document={getElementById:id=>fields[id]};
 class Event{constructor(type){this.type=type}}
 let script=match[0].replace(/^<script>/,'').replace(/<\/script>$/,'');
 if(signer)script=script.replace(ADDRESS.toLowerCase(),signer.address.toLowerCase());
 runInNewContext(script,{window,document,Event,crypto:webcrypto,TextEncoder,location:{origin:'https://wallet.jsonwisdom.com'},Date,BigInt,Uint8Array,Array},{timeout:2500});
 return {fields,calls,click:()=>fields.connect.events.get('click')(),sign:()=>fields.verify.events.get('click')(),
  setAddress(next){address=next;walletEvents.accountsChanged?.([next]);},
  setChain(next){chain=next;walletEvents.chainChanged?.(next);}};
}

test('G1 one click connects Coinbase and switches to Base; never signs or pays',async()=>{
 const h=harness();await h.click();
 assert.ok(h.calls.some(c=>c.method==='eth_requestAccounts'));
 assert.equal(h.calls.filter(c=>c.method==='wallet_switchEthereumChain').length,1);
 assert.match(h.fields.status.textContent,/connected on Base \(8453\)/);
 assert.match(h.fields.status.textContent,/Desktop address matches/);
 assert.equal(h.fields.address.textContent,ADDRESS);
 assert.equal(h.fields.verify.disabled,false);
 assert.match(h.fields.challengePreview.textContent,/No transaction, token approval, payment, login, ENS\/DNS ownership proof or Coinbase API authorization/);
 assert.match(h.fields.challengePreview.textContent,/"chainId": 8453/);
 assert.doesNotMatch(html,/personal_sign|verifyMessage|eip155:1/);
 assert.equal(h.calls.filter(c=>/sign|send|transfer|approve|personal/i.test(c.method)).length,0);
});
test('G2 clears old wallet result, challenge and signature state; no receipts or stored sessions',async()=>{
 const h=harness();await h.click();
 h.setAddress(OTHER);
 assert.equal(h.fields.address.textContent,'');
 assert.equal(h.fields.verify.disabled,true);
 assert.equal(h.fields.challengePreview.textContent,'');
 assert.match(h.fields.verification.textContent,/not performed/);
 await h.click();
 assert.match(h.fields.status.textContent,/DIFFERENT wallet address/);
 assert.equal(h.fields.verify.disabled,true);
 assert.doesNotMatch(html,/receiptPanel|receiptText|localStorage|sessionStorage|createObjectURL|Download JSON/);
});
test('G3 stale account from final network read cannot be falsely matched',async()=>{
 const h=harness({race:true});await h.click();
 assert.doesNotMatch(h.fields.status.textContent,/Desktop address matches/);
 assert.match(h.fields.status.textContent,/Wallet account changed/);
 assert.equal(h.fields.address.textContent,'');
 assert.equal(h.fields.verify.disabled,true);
});
test('G4 synthetic wallet signs Base-8453 EIP-712 typed data, independently recovers signer, no funds',async()=>{
 const h=harness({signer:TEST_SIGNER});
 await h.click();
 assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,0);
 assert.equal(h.fields.verify.disabled,false);
 await h.sign();
 assert.match(h.fields.verification.textContent,/VERIFIED: Base-only EIP-712 domain v2 \(chainId 8453, Flywheel salt\)/);
 assert.match(h.fields.verification.textContent,/No Ethereum-mainnet request, ENS\/DNS ownership, API-key access/);
 assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,1);
 assert.equal(h.fields.verify.disabled,true);
 assert.equal(h.calls.filter(c=>/eth_sendTransaction|eth_signTransaction|wallet_sendCalls|approve|transfer/i.test(c.method)).length,0);
 await h.sign();
 assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,1,'challenge must be one-use');
});
test('G5 wrong cryptographic signer fails closed',async()=>{
 const h=harness({signer:TEST_SIGNER,wrongSignature:true});
 await h.click();await h.sign();
 assert.match(h.fields.verification.textContent,/Signature recovered a different address/);
 assert.doesNotMatch(h.fields.verification.textContent,/VERIFIED:/);
});
test('G6 rejected signature is not wallet proof',async()=>{
 const h=harness({signer:TEST_SIGNER,rejected:true});
 await h.click();await h.sign();
 assert.match(h.fields.verification.textContent,/Signature declined/);
 assert.doesNotMatch(h.fields.verification.textContent,/VERIFIED:/);
});
test('G7 changing the account while signing prevents verification',async()=>{
 const h=harness({signer:TEST_SIGNER,changeOnSignature:true});
 await h.click();await h.sign();
 assert.match(h.fields.verification.textContent,/Wallet changed during signature verification/);
 assert.doesNotMatch(h.fields.verification.textContent,/VERIFIED:/);
});
test('G8 unrecognized address cannot request signing',async()=>{
 const h=harness();
 h.setAddress(OTHER);
 await h.click();
 assert.equal(h.fields.verify.disabled,true);
 assert.match(h.fields.status.textContent,/DIFFERENT wallet address/);
 assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,0);
});

test('G9 signature with Ethereum mainnet EIP-712 domain chain 1 cannot verify as Base 8453',async()=>{
 const h=harness({signer:TEST_SIGNER,signWrongChain:true});
 await h.click();await h.sign();
 assert.doesNotMatch(h.fields.verification.textContent,/VERIFIED:/);
 assert.match(h.fields.verification.textContent,/Signature recovered a different address/);
});
test('G10 switching from Base to Ethereum mainnet clears optional signature permission',async()=>{
 const h=harness({signer:TEST_SIGNER});
 await h.click();
 assert.equal(h.fields.verify.disabled,false);
 h.setChain('0x1');
 assert.equal(h.fields.verify.disabled,true);
 assert.equal(h.fields.challengePreview.textContent,'');
 await h.sign();
 assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,0);
});

test('G11 browser and offline signer policies pin the exact same v2 account, salt, version and origin',()=>{
 const policy=JSON.parse(readFileSync(new URL('./base-wallet-policy.v2.json',import.meta.url),'utf8'));
 assert.equal(policy.policyVersion,'2.0.0');
 assert.equal(policy.signerSetVersion,'desktop-v1');
 assert.deepEqual(policy.authorizedSigners,[ADDRESS.toLowerCase()]);
 assert.ok(html.includes(policy.domain.salt));
 assert.match(html,/const ALLOWED_SIGNERS=Object.freeze\(\['0x0f7018fea1dc9ba32ae817d896211f72f1197ad8'\]\)/);
 assert.equal(policy.domain.chainId,8453);
 assert.equal(policy.domain.version,'2');
 assert.equal(policy.scope,'offchain_wallet_control_only');
});
test('G12 EIP712 browser challenge is contract-free with app salt; not a cross-chain sign-in or payment',async()=>{
 const h=harness({signer:TEST_SIGNER});
 await h.click();
 const t=JSON.parse(h.fields.challengePreview.textContent);
 assert.equal(t.domain.chainId,8453);
 assert.equal(t.domain.version,'2');
 assert.equal(t.domain.salt,'0xf09262a7cdc2a8dd05f80ed656604534efaba598f0d9a1b7016a60af6f1ec275');
 assert.equal(t.message.origin,'https://wallet.jsonwisdom.com');
 assert.equal(t.message.wallet.toLowerCase(),TEST_SIGNER.address.toLowerCase());
 assert.ok(!Object.hasOwn(t.domain,'verifyingContract'));
 assert.equal(t.message.purpose,'Prove control of this account on Base ONLY');
});
