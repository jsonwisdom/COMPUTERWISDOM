import {VERSION,drawIndex,browserRand32,createReceipt,replayReceipt,svgCard} from "./engine.mjs";
const $=id=>document.getElementById(id);
const state={catalog:null,item:null,draw:null,receipt:null,draws:[],reveals:0,provider:null,account:null,chain:null,serial:0,providers:[]};
const status=s=>{$("status").textContent=s};
const label=c=>c==="0x2105"?"Base Mainnet · 8453":c==="0x1"?"Ethereum Mainnet · 1":c?"Other EVM network · "+c:"Unknown network";
const masked=a=>typeof a==="string"?a.slice(0,6)+"…"+a.slice(-4):"Anonymous";
function node(tag,txt){const e=document.createElement(tag);if(txt!==undefined)e.textContent=txt;return e}
function save(name,body,type){
 const url=URL.createObjectURL(new Blob([body],{type:type}));
 const a=node("a");a.href=url;a.download=name;a.hidden=true;document.body.appendChild(a);a.click();a.remove();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
}
window.addEventListener("eip6963:announceProvider",e=>{
 const d=e&&e.detail;
 const name=String(d&&d.info&&d.info.name||"").toLowerCase(),rdns=String(d&&d.info&&d.info.rdns||"").toLowerCase();
 if(d&&d.provider&&typeof d.provider.request==="function"&&(d.provider.isCoinbaseWallet===true||(rdns==="com.coinbase.wallet"&&name.includes("coinbase")))){
  if(!state.providers.includes(d.provider))state.providers.push(d.provider);
 }
});
function requestDiscover(){try{window.dispatchEvent(new Event("eip6963:requestProvider"))}catch(e){}}
requestDiscover();
function candidate(){
 if(state.providers.length)return state.providers[0];
 const e=window.ethereum;
 if(e&&Array.isArray(e.providers))return e.providers.find(p=>p&&p.isCoinbaseWallet&&typeof p.request==="function")||null;
 return e&&e.isCoinbaseWallet&&typeof e.request==="function"?e:null;
}
function walletDisplay(){
 $("wallet-account").textContent=state.account?masked(state.account):"Anonymous / not connected";
 $("wallet-chain").textContent=state.account?label(state.chain):"No network requested";
 $("wallet-connect").disabled=Boolean(state.account);
 $("wallet-clear").disabled=!state.account;
}
$("wallet-connect").addEventListener("click",async()=>{
 requestDiscover();
 const provider=candidate();
 if(!provider){$("wallet-status").textContent="Coinbase Wallet provider not detected. Use a compatible wallet in-app browser; ordinary Safari pairing is not provided.";return}
 const ticket=++state.serial;
 $("wallet-connect").disabled=true;
 $("wallet-status").textContent="Requesting optional account visibility from your wallet. You can decline.";
 try{
  const accounts=await provider.request({method:"eth_requestAccounts"});
  if(ticket!==state.serial)return;
  const account=Array.isArray(accounts)?accounts[0]:null;
  if(typeof account!=="string"||!/^0x[a-fA-F0-9]{40}$/.test(account))throw Error("No EVM account");
  let chain=null;
  try{chain=await provider.request({method:"eth_chainId"})}catch(e){}
  if(ticket!==state.serial)return;
  state.provider=provider;state.account=account;state.chain=typeof chain==="string"?chain.toLowerCase():null;
  walletDisplay();$("wallet-status").textContent="Account displayed locally. No signing, payments, preference upload or family permission.";
 }catch(e){
  if(ticket!==state.serial)return;
  state.provider=null;state.account=null;state.chain=null;
  walletDisplay();$("wallet-status").textContent=e&&e.code===4001?"Permission declined. Anonymous play works.":"No wallet linked. Anonymous play works.";
 }finally{if(ticket===state.serial)$("wallet-connect").disabled=!!state.account}
});
$("wallet-clear").addEventListener("click",()=>{
 state.serial++;state.provider=null;state.account=null;state.chain=null;walletDisplay();
 $("wallet-status").textContent="Local account display cleared. Revoke site permissions in wallet settings separately if needed.";
});
walletDisplay();
function showCatalog(items){
 const host=$("creator-items");host.replaceChildren();
 for(const item of items){
  const a=node("article");a.className="concept";
  const h=node("h3",item.title),p=node("p",item.category+" · curated "+item.date),link=node("a","View public Zora concept ↗");
  link.href=item.url;link.target="_blank";link.rel="noopener noreferrer";
  a.append(h,p,link);host.appendChild(a);
 }
}
function logRender(){
 const list=$("session-log");list.replaceChildren();
 state.draws.forEach((rec,i)=>list.append(node("li",String(i+1)+". "+rec.concept_id+" — "+(rec.liked?"Liked":"Revealed")+" · local only")));
 $("play-count").textContent=String(state.reveals);
 $("like-count").textContent=String(state.draws.filter(r=>r.liked).length);
 if(state.reveals>=3){
  $("toolbox").hidden=false;
  $("toolbox-status").textContent="Public Seymour toolbox found after three reveals. This Easter egg does not grant identity or private access.";
 }
}
function show(){
 if(!state.receipt)return;
 const parsed=new DOMParser().parseFromString(svgCard(state.item),"image/svg+xml");
 $("art").replaceChildren(document.importNode(parsed.documentElement,true));
 $("scratch-cover").hidden=true;
 $("reveal").disabled=true;$("like").disabled=false;$("download-art").disabled=false;$("export").disabled=false;
 state.reveals++;state.draws.push(state.receipt);logRender();
 status("Satirical art revealed. All plays receive art. No payouts, rarity prize, token mint or price.");
}
const cover=$("scratch-cover"),ctx=cover.getContext("2d");
let down=false,strokes=0;
function resetCover(){
 ctx.globalCompositeOperation="source-over";ctx.clearRect(0,0,cover.width,cover.height);
 ctx.fillStyle="#a8c1cf";ctx.fillRect(0,0,cover.width,cover.height);
 ctx.fillStyle="#102339";ctx.textAlign="center";ctx.font="bold 24px monospace";
 ctx.fillText("SCRATCH / SWIPE",180,210);ctx.font="17px monospace";ctx.fillText("OR PRESS REVEAL",180,240);
 strokes=0;cover.hidden=false;
}
function scratch(evt){
 if(!down||!state.receipt)return;
 const rect=cover.getBoundingClientRect(),x=(evt.clientX-rect.left)*cover.width/rect.width,y=(evt.clientY-rect.top)*cover.height/rect.height;
 ctx.globalCompositeOperation="destination-out";ctx.beginPath();ctx.arc(x,y,32,0,Math.PI*2);ctx.fill();
 if(++strokes>=15){down=false;show()}
}
cover.addEventListener("pointerdown",evt=>{if(!state.receipt)return;down=true;cover.setPointerCapture&&cover.setPointerCapture(evt.pointerId);scratch(evt)});
cover.addEventListener("pointermove",scratch);
["pointerup","pointercancel","lostpointercapture"].forEach(ev=>cover.addEventListener(ev,()=>{down=false}));
$("draw").addEventListener("click",()=>{
 if(!state.catalog){status("Public catalog unavailable.");return}
 try{
  state.draw=drawIndex(state.catalog.items.length,browserRand32);
  state.item=state.catalog.items[state.draw.index];
  state.receipt=createReceipt(state.draw,state.item);
  $("art").replaceChildren();
  $("current-concept").textContent="A public concept has been selected. Scratch to reveal the art.";
  $("reveal").disabled=false;$("like").disabled=true;$("download-art").disabled=true;$("export").disabled=true;
  resetCover();status("Scratch or use the accessible Reveal button. Nothing costs money.");
 }catch(e){status("Secure random draw unavailable. No outcome recorded.")}
});
$("reveal").addEventListener("click",show);
$("like").addEventListener("click",()=>{
 if(!state.receipt)return;
 state.receipt=createReceipt(state.draw,state.item,{liked:true});
 if(state.draws.length)state.draws[state.draws.length-1]=state.receipt;
 $("like").disabled=true;logRender();
 status("Liked locally in this page session. Nothing sent to a server.");
});
$("download-art").addEventListener("click",()=>{
 if(state.item)save("jay-satire-"+state.item.id+".svg",svgCard(state.item),"image/svg+xml");
});
$("export").addEventListener("click",()=>{
 if(!state.draws.length)return;
 const packet={schema:"JAYS_SESSION_EXPORT_V0_1",version:VERSION,entries:state.draws,contains_wallet_address:false,network_submitted:false,claim_of_entropy_attestation:false};
 save("jaywisdom-local-replay.json",JSON.stringify(packet,null,2)+"\n","application/json");
});
$("import").addEventListener("change",async e=>{
 const file=e.target.files&&e.target.files[0];
 if(!file||file.size>100000){$("replay-status").textContent="Replay file missing or too large.";return}
 try{
  const packet=JSON.parse(await file.text());
  if(!state.catalog||packet.schema!=="JAYS_SESSION_EXPORT_V0_1"||!Array.isArray(packet.entries)||packet.entries.length>100)throw Error("Unsupported packet");
  const results=packet.entries.map(rec=>replayReceipt(rec,state.catalog.items));
  $("replay-status").textContent="Replay check: "+results.filter(x=>x.valid).length+" consistent, "+results.filter(x=>!x.valid).length+" rejected. Validity covers deterministic arithmetic, not entropy authenticity.";
 }catch(e){$("replay-status").textContent="Unsupported or invalid receipt file. No session records imported."}
 e.target.value="";
});
$("feedback-copy").addEventListener("click",async()=>{
 const note=$("feedback").value.trim().slice(0,1200);
 const plain="Jay CoinBaseKidsWebDesign feedback\nVersion: "+VERSION+"\nManual note: "+(note||"(empty)")+"\nNo wallet address included by app.\nReport sensitive vulnerabilities privately, never via a public issue.";
 try{await navigator.clipboard.writeText(plain);$("feedback-status").textContent="Copied. Nothing submitted to Coinbase or GitHub."}
 catch(e){$("feedback-status").textContent="Clipboard unavailable. Select and copy your note manually."}
});
$("puppy").addEventListener("click",()=>{
 $("puppy-note").hidden=false;
 $("puppy-note").textContent="This prototype does not scan for zero-days or notify anyone automatically. Stop the test and report serious findings privately to the maintainer. A machine cannot approve its own actions.";
});
fetch("./catalog.v0.1.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP status");return r.json()}).then(catalog=>{
 if(catalog.schema!=="JAYWISDOM_PUBLIC_ZORA_CONCEPT_SNAPSHOT_V0_1"||!Array.isArray(catalog.items)||catalog.items.length!==6)throw Error("Catalog mismatch");
 for(const x of catalog.items){if(!/^https:\/\/zora\.co\/coin\/base:0x[a-f0-9]{40}$/i.test(x.url))throw Error("Unexpected concept link")}
 state.catalog=catalog;showCatalog(catalog.items);
 $("catalog-status").textContent="6 public concepts · archived snapshot 2026-09-01 · not live Zora sync";
 $("draw").disabled=false;
}).catch(()=>status("Public catalog failed. No random draw is permitted without the correct catalog."));
