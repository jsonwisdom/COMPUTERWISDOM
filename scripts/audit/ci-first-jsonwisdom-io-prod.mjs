// CI-FIRST read-only production .io acceptance: never runs a payment or modifies Cloudflare.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const contract=JSON.parse(readFileSync(new URL("../../workers/jsonwisdom-io/backend-contract.json",import.meta.url),"utf8"));
const cases=[
 {host:"proof.jsonwisdom.io",worker:"jw-io-proof-seymour-v1",source:"proof",comparison:"proof.jsonwisdom.com"},
 {host:"seymour.jsonwisdom.io",worker:"jw-io-proof-seymour-v1",source:"proof",comparison:"seymour.jsonwisdom.com"},
 {host:"supreme.jsonwisdom.io",worker:"jw-io-supreme-v1",source:"supreme",comparison:"supreme.jsonwisdom.com"}
];
async function read(url,method="GET"){
 const r=await fetch(url,{method,redirect:"manual",signal:AbortSignal.timeout(18000),headers:{"user-agent":"CI-FIRST-jsonwisdom-io-production-proof/1"}});
 const b=Buffer.from(await r.arrayBuffer());
 return {status:r.status,contentType:r.headers.get("content-type"),cfRay:r.headers.get("cf-ray"),sha256:createHash("sha256").update(b).digest("hex"),size:b.length,body:b};
}
const receipt={schema:"computerwisdom.ci-first.io-production-http-receipt.v1",observed_at:new Date().toISOString(),network:"Cloudflare public HTTP",status:"FAIL",canon:false,authority_created:false,independent_provider_failover:false,checks:[]};
try {
 for(const item of cases){
  const path="https://"+item.host;
  const identity=await read(path+contract.identity_path);
  assert.equal(identity.status,200,item.host+" identity HTTP status");
  assert.match(identity.contentType||"",/application\/json/i);
  const data=JSON.parse(identity.body.toString("utf8"));
  assert.equal(data.schema,"computerwisdom.ci-first.worker-identity.v1");
  assert.equal(data.namespace,"jsonwisdom.io");
  assert.equal(data.worker_service,item.worker);
  assert.equal(data.source_sha256,contract.sources[item.source].sha256);
  assert.equal(data.independent_provider,false);
  assert.equal(data.authority_created,false);
  assert.equal(data.canon,false);
  const head=await read(path+contract.identity_path,"HEAD");
  assert.equal(head.status,200);
  assert.equal(head.size,0);
  const app=await read(path+"/");
  const com=await read("https://"+item.comparison+"/");
  assert.equal(app.status,200,item.host+" root HTTP status");
  assert.equal(com.status,200,item.comparison+" control HTTP status");
  assert.equal(app.sha256,com.sha256,item.host+" homepage parity with "+item.comparison);
  assert.ok(app.size>1000,"homepage must not be placeholder");
  receipt.checks.push({host:item.host,worker:item.worker,source_sha256:data.source_sha256,http_status:app.status,identity_status:identity.status,homepage_sha256:app.sha256,homepage_bytes:app.size,identity_cf_ray:identity.cfRay,homepage_cf_ray:app.cfRay,baseline_com:item.comparison,baseline_sha256:com.sha256,status:"PASS"});
 }
 assert.equal(new Set(receipt.checks.map(c=>c.host)).size,3);
 assert.equal(new Set(receipt.checks.map(c=>c.worker)).size,2);
 receipt.status="PASS";
 console.log(JSON.stringify(receipt,null,2));
 console.log("CI_FIRST_PRODUCTION_IO_HTTP=PASS");
} catch(e) {
 receipt.error=String(e);
 console.error(JSON.stringify(receipt,null,2));
 throw e;
}
