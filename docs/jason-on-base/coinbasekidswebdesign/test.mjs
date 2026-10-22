import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {dirname,join} from "node:path";
import {drawIndex,createReceipt,replayReceipt,svgCard,VERSION,CATALOG_VERSION} from "./engine.mjs";
const dir=dirname(fileURLToPath(import.meta.url));
const catalog=JSON.parse(readFileSync(join(dir,"catalog.v0.1.json"),"utf8"));
const items=catalog.items;

test("catalog exactly six public concept references, no prices, no identities",()=>{
 assert.equal(catalog.schema,CATALOG_VERSION);
 assert.equal(items.length,6);
 assert.equal(new Set(items.map(x=>x.id)).size,6);
 for(const p of items){
  assert.match(p.url,/^https:\/\/zora\.co\/coin\/base:0x[0-9a-f]{40}$/);
  assert.equal(typeof p.gag,"string");
  assert.equal(typeof p.frame,"string");
  assert.ok(!Object.keys(p).some(k=>/wallet|private|price|balance|nameOfChild/i.test(k)));
 }
});
test("six equal outcomes for full accepted 32-bit range: Wolfram math replay",()=>{
 const n=6,SPACE=2**32,limit=Math.floor(SPACE/n)*n,counts=Array(n).fill(0);
 assert.equal(limit,4294967292);
 assert.equal(SPACE-limit,4);
 const acceptedPerOutcome=limit/n;
 assert.equal(acceptedPerOutcome,715827882);
 assert.equal(acceptedPerOutcome*n,limit);
 for(let k=0;k<1200;k++){
  const x=k%limit;
  const draw=drawIndex(n,()=>x);
  assert.equal(draw.index,x%n);
  counts[draw.index]++;
 }
 assert.deepEqual(counts,[200,200,200,200,200,200]);
});
test("reject end-of-domain samples without modulo bias",()=>{
 let attempts=0;
 const inputs=[4294967295,4294967292,5];
 const draw=drawIndex(6,()=>{attempts++;return inputs.shift()});
 assert.equal(draw.index,5);
 assert.equal(draw.randomWord,5);
 assert.equal(draw.attempts,3);
 assert.equal(attempts,3);
});
test("reject malformed random words and catalog lengths",()=>{
 assert.throws(()=>drawIndex(0,()=>1),/Invalid catalog/);
 assert.throws(()=>drawIndex(6,()=>-1),/Invalid random word/);
 assert.throws(()=>drawIndex(6,()=>2**32),/Invalid random word/);
});
test("every concept produces same non-cash receipt/art after replay",()=>{
 for(let i=0;i<6;i++){
  const draw=drawIndex(6,()=>i);
  const receipt=createReceipt(draw,items[i]);
  assert.equal(receipt.schema,VERSION);
  assert.equal(receipt.no_money,true);
  assert.equal(receipt.prize_value_usd,0);
  assert.equal(receipt.crypto_transfer,false);
  assert.equal(receipt.wallet_identity,null);
  assert.equal(receipt.entropy_proof,false);
  assert.equal(receipt.authority,false);
  const result=replayReceipt(JSON.parse(JSON.stringify(receipt)),items);
  assert.equal(result.valid,true);
  assert.equal(result.concept.id,items[i].id);
  assert.equal(svgCard(result.concept),svgCard(items[i]));
  assert.match(svgCard(items[i]),/<svg /);
  assert.match(svgCard(items[i]),/width="360" height="480"/);
 }
});
test("tampered imported replay is rejected and not promoted to proof",()=>{
 const base=createReceipt(drawIndex(6,()=>3),items[3]);
 const mutate=(k,v)=>({...base,[k]:v});
 for(const [key,value] of [
  ["catalog_count",5],["selected_index",4],["accepted_random_word",4294967295],
  ["concept_id","fake"],["public_reference","https://scam.example"],["wallet_identity","0x01"],
  ["prize_value_usd",1],["no_money",false],["crypto_transfer",true],
  ["authority",true],["server_attestation",true],["entropy_proof",true],["liked","true"]
 ]){
  const result=replayReceipt(mutate(key,value),items);
  assert.equal(result.valid,false,key);
 }
});
test("XML art safely escapes untrusted concept text",()=>{
 const crafted={title:'<script>alert(1)</script>',gag:'A & <bad>',frame:'"<x>'};
 const svg=svgCard(crafted);
 assert.ok(!svg.includes("<script>"));
 assert.ok(svg.includes("&lt;script&gt;"));
 assert.ok(svg.includes("&amp;"));
 assert.ok(svg.includes("&quot;"));
});
test("browser source requests only consented account/network and no telemetry or storage",()=>{
 const js=readFileSync(join(dir,"app.mjs"),"utf8");
 const html=readFileSync(join(dir,"index.html"),"utf8");
 const rpc=[...js.matchAll(/method:"([a-zA-Z0-9_]+)"/g)].map(x=>x[1]);
 assert.deepEqual(rpc,["eth_requestAccounts","eth_chainId"]);
 for(const word of ["eth_sendTransaction","personal_sign","wallet_sendCalls","localStorage","sessionStorage","sendBeacon","geolocation","signTypedData","navigator.gpu"]){
  assert.ok(!js.includes(word),"Forbidden: "+word);
 }
 assert.equal((js.match(/fetch\(/g)||[]).length,1);
 assert.match(js,/fetch\("\.\/catalog\.v0\.1\.json"/);
 assert.ok(!html.includes("nightjr-walkback"));
 const requested=[...js.matchAll(/\$\("([a-z0-9-]+)"\)/g)].map(x=>x[1]);
 for(const id of new Set(requested))assert.ok(html.includes('id="'+id+'"'),"Missing element: "+id);
 assert.ok(!html.includes("https://cdn."));
 assert.ok(!html.includes("analytics"));
});
console.log("NO_SPEND_GAME_REPLAY: TEST FILE LOADED; REAL_DEVICE_QA=HOLD; LIVE_WALLET_QA=HOLD");