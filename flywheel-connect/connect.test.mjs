import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

const html=readFileSync(new URL('./index.html',import.meta.url),'utf8');
const match=html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(match,'wallet script missing');
const ADDRESS='0x0F7018fea1dc9ba32aE817D896211f72f1197AD8';
const OTHER='0x'+'aa'.repeat(20);

function harness({race=false}={}){
 const fields=Object.fromEntries(['connect','status','address'].map(id=>[id,{
  textContent:'',className:'',disabled:false,events:new Map(),
  addEventListener(name,fn){this.events.set(name,fn)}
 }]));
 const walletEvents={}; const calls=[];
 let address=ADDRESS,chain='0x1',chainReads=0;
 const provider={
  isCoinbaseWallet:true,
  on(name,fn){walletEvents[name]=fn},
  removeListener(name){delete walletEvents[name]},
  async request({method,params}){
   calls.push(method);
   switch(method){
    case 'eth_requestAccounts':return [address];
    case 'eth_accounts':return [address];
    case 'eth_chainId':
     chainReads++;
     // Trigger account change DURING the last asynchronous chain read.
     if(race&&chainReads===3){address=OTHER;walletEvents.accountsChanged?.([address]);}
     return chain;
    case 'wallet_switchEthereumChain':
     assert.equal(params?.[0]?.chainId,'0x2105');
     chain='0x2105';walletEvents.chainChanged?.(chain);return null;
    default:throw Error('Unexpected wallet method '+method);
   }
  }
 };
 const window={ethereum:provider,addEventListener(){},dispatchEvent(){}};
 const document={getElementById:id=>fields[id]};
 class Event{constructor(type){this.type=type}}
 runInNewContext(match[1],{window,document,Event},{timeout:2000});
 return {fields,calls,click:()=>fields.connect.events.get('click')(),
  setAddress(next){address=next;walletEvents.accountsChanged?.([next])}};
}

test('one click requests Coinbase connection then switches to Base 8453; never signs or pays',async()=>{
 const h=harness();await h.click();
 assert.ok(h.calls.includes('eth_requestAccounts'));
 assert.equal(h.calls.filter(x=>x==='wallet_switchEthereumChain').length,1);
 assert.match(h.fields.status.textContent,/connected on Base \(8453\)/);
 assert.match(h.fields.status.textContent,/Desktop address matches/);
 assert.equal(h.fields.address.textContent,ADDRESS);
 assert.equal(h.calls.filter(x=>/sign|send|transfer|approve|personal/i.test(x)).length,0);
});
test('clears all prior wallet observations and does not retain JSON receipts',async()=>{
 const h=harness();await h.click();
 h.setAddress(OTHER);
 assert.equal(h.fields.address.textContent,'');
 assert.doesNotMatch(h.fields.status.textContent,/Desktop address matches/);
 await h.click();
 assert.match(h.fields.status.textContent,/DIFFERENT wallet address/);
 assert.equal(h.fields.address.textContent,OTHER);
 assert.doesNotMatch(html,/receiptPanel|receiptText|localStorage|sessionStorage|createObjectURL|Download JSON/);
});
test('wallet change during final chain read cannot produce stale matching address',async()=>{
 const h=harness({race:true});await h.click();
 assert.doesNotMatch(h.fields.status.textContent,/Desktop address matches/);
 assert.match(h.fields.status.textContent,/Wallet account changed/);
 assert.equal(h.fields.address.textContent,'');
 assert.equal(h.calls.filter(x=>/sign|send|transfer|approve/i.test(x)).length,0);
});
