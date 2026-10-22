"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const script=fs.readFileSync(__dirname+"/wallet.js","utf8");
function makeDom(){
 const elements={};
 function element(id){
  if(elements[id])return elements[id];
  const node={
   id,value:id==="level"?"2":"",textContent:"",disabled:false,children:[],
   listeners:{},className:"",attributes:{},
   addEventListener(type,fn){this.listeners[type]=fn},
   appendChild(x){this.children.push(x);return x},
   replaceChildren(...items){this.children=items},
   setAttribute(name,value){this.attributes[name]=value}
  };
  elements[id]=node;
  return node;
 }
 ["coinbase-connect","coinbase-disconnect","wallet-status","wallet-account","wallet-chain","wallet-boundary","clawback-matrix","clawback-quote","level"].forEach(element);
 const events={};
 const win={
  ethereum:null,
  addEventListener(name,fn){(events[name]??=[]).push(fn)},
  dispatchEvent(evt){for(const fn of (events[evt.type]||[]))fn(evt)}
 };
 const document={getElementById:element,createElement:type=>({tagName:type,className:"",children:[],attributes:{},
   setAttribute(n,v){this.attributes[n]=v},appendChild(v){this.children.push(v)}})};
 const context={window:win,document,Event:class Event{constructor(type){this.type=type}}};
 return {elements,win,context};
}
function providerFactory(opts={}){
 const calls=[],events={};
 const p={
  isCoinbaseWallet:opts.coinbase??true,
  calls,events,
  async request({method}){
   calls.push(method);
   if(opts.fail && method==="eth_requestAccounts")throw Object.assign(Error("Rejected"),{code:4001});
   if(method==="eth_requestAccounts")return opts.accounts??["0x1234567890abcdef1234567890abcdef12345678"];
   if(method==="eth_chainId")return opts.chain??"0x2105";
   throw Error("FORBIDDEN RPC: "+method);
  },
  on(event,handler){(events[event]??=[]).push(handler)},
  removeListener(event,handler){events[event]=(events[event]||[]).filter(h=>h!==handler)},
  emit(event,val){for(const fn of events[event]||[])fn(val)}
 };
 return p;
}
function start(winProvider){
 const dom=makeDom();
 if(winProvider)dom.win.ethereum=winProvider;
 vm.runInNewContext(script,dom.context,{filename:"wallet.js"});
 return dom;
}
async function run(){
 const a=providerFactory();
 const d=start(a),e=d.elements;
 assert.deepEqual(a.calls,[],"No provider RPC on page load");
 assert.equal(e["wallet-account"].textContent,"Not connected");
 assert.equal(e["coinbase-disconnect"].disabled,true);
 assert.equal(e["clawback-matrix"].children.length,8);
 assert.equal(e["clawback-matrix"].children[0].children.filter(x=>x.className.includes("lit")).length,4);
 e.level.value="4";e.level.listeners.input();
 assert.match(e["clawback-quote"].textContent,/16 VIRTUAL QUARTERS/);
 assert.match(e["clawback-quote"].textContent,/REAL CHARGE \$0\.00/);
 assert.equal(e["clawback-matrix"].children.flatMap(x=>x.children).filter(x=>x.className.includes("lit")).length,16);
 await e["coinbase-connect"].listeners.click();
 assert.deepEqual(a.calls,["eth_requestAccounts","eth_chainId"]);
 assert.equal(e["wallet-account"].textContent,"0x1234…5678");
 assert.match(e["wallet-chain"].textContent,/Base Mainnet/);
 assert.equal(e["coinbase-connect"].disabled,true);
 a.emit("chainChanged","0x1");
 assert.match(e["wallet-status"].textContent,/non-Base/);
 a.emit("accountsChanged",["0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]);
 assert.equal(e["wallet-account"].textContent,"0xaaaa…aaaa");
 e["coinbase-disconnect"].listeners.click();
 assert.equal(e["wallet-account"].textContent,"Not connected");
 assert.match(e["wallet-status"].textContent,/revoke access in the wallet/);
 assert.deepEqual(a.calls,["eth_requestAccounts","eth_chainId"],"Disconnect makes no signing or revoke RPC");

 const without=start(providerFactory({coinbase:false}));
 await without.elements["coinbase-connect"].listeners.click();
 assert.match(without.elements["wallet-status"].textContent,/not detected/);
 assert.equal(without.win.ethereum.calls.length,0);

 const denied=start(providerFactory({fail:true}));
 await denied.elements["coinbase-connect"].listeners.click();
 assert.match(denied.elements["wallet-status"].textContent,/rejected/);
 assert.equal(denied.elements["coinbase-connect"].disabled,false);

 const wrong=start(providerFactory({accounts:["not-an-account"]}));
 await wrong.elements["coinbase-connect"].listeners.click();
 assert.equal(wrong.elements["wallet-account"].textContent,"Not connected");

 const announced=start();
 const p=providerFactory();
 announced.win.dispatchEvent({type:"eip6963:announceProvider",detail:{info:{rdns:"com.coinbase.wallet",name:"Coinbase Wallet"},provider:p}});
 await announced.elements["coinbase-connect"].listeners.click();
 assert.match(announced.elements["wallet-chain"].textContent,/Base Mainnet/);
 assert.deepEqual(p.calls,["eth_requestAccounts","eth_chainId"]);

 const source=script.toLowerCase();
 for(const disallowed of ["eth_sendtransaction","personal_sign","eth_sign","eth_signtransaction","wallet_switchethereumchain","wallet_addethereumchain","wallet_sendcalls","signmessage","fetch(","localstorage","sessionstorage","sendbeacon","navigator.geolocation"]){
   assert.equal(source.includes(disallowed),false,"Forbidden logic: "+disallowed);
 }
 console.log("WALLET_MATRIX_SENTINEL_SCOPED_MOCK_PASS: 6 cases; explicit consent, EIP-6963, no-spend, no provider fallback, rejection, invalid address, chain/account changes and 8x8 matrix.");
}
run().catch(e=>{console.error(e);process.exitCode=1});
