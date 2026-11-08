import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {createHash} from "node:crypto";
const path=(p)=>new URL("../../"+p,import.meta.url);
const c=JSON.parse(readFileSync(path("workers/jsonwisdom-io/backend-contract.json"),"utf8"));
test("exact original public Worker bytes preserved",()=>{
 for(const src of Object.values(c.sources)){
  const bytes=readFileSync(path(src.source_path));
  assert.equal(bytes.length,src.bytes);
  assert.equal(createHash("sha256").update(bytes).digest("hex"),src.sha256);
 }
});
test("io scripts never point to com service IDs",()=>{
 const com=new Set(Object.values(c.original_com));
 assert.equal(Object.keys(c.hostnames).length,3);
 for(const [hostname,service] of Object.entries(c.hostnames)){
  assert.ok(hostname.endsWith(".jsonwisdom.io"));
  assert.ok(!com.has(service),hostname+" shares a .com backend");
 }
 assert.notEqual(c.hostnames["proof.jsonwisdom.io"],c.original_com["proof.jsonwisdom.com"]);
 assert.equal(c.hostnames["proof.jsonwisdom.io"],c.hostnames["seymour.jsonwisdom.io"]);
 assert.notEqual(c.hostnames["proof.jsonwisdom.io"],c.hostnames["supreme.jsonwisdom.io"]);
});
for(const [role,hostname,service] of [
 ["proof","proof.jsonwisdom.io","jw-io-proof-seymour-v1"],
 ["proof","seymour.jsonwisdom.io","jw-io-proof-seymour-v1"],
 ["supreme","supreme.jsonwisdom.io","jw-io-supreme-v1"]
]){
 test(hostname+" identity GET/HEAD and method guard",async()=>{
  const m=await import(path("workers/jsonwisdom-io/"+role+"-backend.mjs"));
  const url="https://"+hostname+c.identity_path;
  const response=await m.default.fetch(new Request(url));
  assert.equal(response.status,200);
  assert.equal(response.headers.get("x-ci-first-backend"),service);
  const data=await response.json();
  assert.equal(data.worker_service,service);
  assert.equal(data.namespace,"jsonwisdom.io");
  assert.equal(data.source_sha256,c.sources[role].sha256);
  assert.equal(data.canon,false);
  assert.equal(data.authority_created,false);
  const head=await m.default.fetch(new Request(url,{method:"HEAD"}));
  assert.equal(head.status,200);
  assert.equal(await head.text(),"");
  const post=await m.default.fetch(new Request(url,{method:"POST"}));
  assert.equal(post.status,405);
 });
}
test("existing public homepages remain served",async()=>{
 for(const [role,hostname] of [["proof","proof.jsonwisdom.io"],["supreme","supreme.jsonwisdom.io"]]){
  const m=await import(path("workers/jsonwisdom-io/"+role+"-backend.mjs"));
  const response=await m.default.fetch(new Request("https://"+hostname+"/"));
  assert.equal(response.status,200);
  assert.match((await response.text()).slice(0,100),/<!DOCTYPE html>/i);
 }
});
test("no independent provider, payment, canon or authority claim",()=>{
 assert.equal(c.independent_provider,false);
 assert.equal(c.live_routing_promoted,false);
 assert.equal(c.canon,false);
 assert.equal(c.authority_created,false);
});
