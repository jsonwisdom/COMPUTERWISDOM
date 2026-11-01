import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { webcrypto } from 'node:crypto';
import { TextEncoder } from 'node:util';
import { Wallet, verifyMessage } from 'ethers';

const html=readFileSync(new URL('./index.html',import.meta.url),'utf8');
const match=html.match(/<script>\s*'use strict';([\s\S]*?)<\/script>/);
assert.ok(match,'wallet script missing');
const ADDRESS='0x0F7018fea1dc9ba32aE817D896211f72f1197AD8';
const OTHER='0x'+'aa'.repeat(20);
const TEST_SIGNER=new Wallet('0x'+'77'.repeat(32)); // Public, unfunded synthetic key. NEVER use with actual funds.
const WRONG_SIGNER=new Wallet('0x'+'88'.repeat(32));

function harness({race=false, signer=null, rejected=false, wrongSignature=false, changeOnSignature=false}={}){
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
    case 'personal_sign':
     if(rejected)throw Object.assign(Error('User declined'),{code:4001});
     assert.ok(signer,'Never sign with real desktop wallet in CI');
     assert.equal(params?.[1].toLowerCase(),signer.address.toLowerCase());
     assert.match(params[0],/^0x[0-9a-f]+$/);
     const message=Buffer.from(params[0].slice(2),'hex').toString('utf8');
     assert.match(message,/Flywheel Wallet Control Check/);
     assert.match(message,/Network: Base mainnet \(8453\)/);
     assert.match(message,/Origin: https:\/\/wallet\.jsonwisdom\.com/);
     assert.match(message,/Nonce: 0x[0-9a-f]{32}/);
     assert.match(message,/not a transaction|Not a transaction/i);
     if(changeOnSignature){address=OTHER;walletEvents.accountsChanged?.([address]);}
     return (wrongSignature?WRONG_SIGNER:signer).signMessage(message);
    default:throw Error('Unexpected wallet method: '+method);
   }
  }
 };
 const window={ethereum:provider,ethers:{verifyMessage},addEventListener(){},dispatchEvent(){}};
 const document={getElementById:id=>fields[id]};
 class Event{constructor(type){this.type=type}}
 let script=match[0].replace(/^<script>/,'').replace(/<\/script>$/,'');
 if(signer)script=script.replace(ADDRESS,signer.address);
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
 assert.match(h.fields.challengePreview.textContent,/Not a transaction, token approval, payment, login, DNS\/ENS ownership proof or Coinbase API authorization/);
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
test('G4 synthetic wallet signs exact EIP-191 challenge; ethers independently recovers signer, no funds',async()=>{
 const h=harness({signer:TEST_SIGNER});
 await h.click();
 assert.equal(h.calls.filter(c=>c.method==='personal_sign').length,0);
 assert.equal(h.fields.verify.disabled,false);
 await h.sign();
 assert.match(h.fields.verification.textContent,/VERIFIED: EIP-191/);
 assert.match(h.fields.verification.textContent,/No ENS\/DNS ownership, API-key access/);
 assert.equal(h.calls.filter(c=>c.method==='personal_sign').length,1);
 assert.equal(h.fields.verify.disabled,true);
 assert.equal(h.calls.filter(c=>/eth_sendTransaction|eth_signTransaction|wallet_sendCalls|approve|transfer/i.test(c.method)).length,0);
 await h.sign();
 assert.equal(h.calls.filter(c=>c.method==='personal_sign').length,1,'challenge must be one-use');
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
 assert.equal(h.calls.filter(c=>c.method==='personal_sign').length,0);
});
