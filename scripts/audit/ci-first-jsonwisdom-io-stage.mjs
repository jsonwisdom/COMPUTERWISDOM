// CI-FIRST independent HTTP evidence from GitHub-hosted runner; no secrets or writes.
// Public routes only. Do not infer separate vendor fault domains from distinct Worker IDs.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const expected = JSON.parse(readFileSync(new URL("../../workers/jsonwisdom-io/backend-contract.json",import.meta.url),"utf8"));
const staging = [
 {host:"jw-io-proof-seymour-v1.jaywisdom44.workers.dev",service:"jw-io-proof-seymour-v1",origin:"proof",parity:"https://proof.jsonwisdom.com/"},
 {host:"jw-io-supreme-v1.jaywisdom44.workers.dev",service:"jw-io-supreme-v1",origin:"supreme",parity:"https://supreme.jsonwisdom.com/"}
];
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
async function get(url,method="GET") {
 const result=await fetch(url,{method,redirect:"manual",signal:AbortSignal.timeout(18000),headers:{"user-agent":"CI-FIRST-jsonwisdom-io-replay/1"}});
 const buf=Buffer.from(await result.arrayBuffer());
 return {status:result.status,headers:result.headers,bytes:buf,sha256:digest(buf)};
}
for(const {host,service,origin,parity} of staging){
 const target="https://"+host;
 const identity=await get(target+expected.identity_path);
 const rootDiagnostic=await get(target+"/");
 console.log(JSON.stringify({gate:"STAGING_PROBE_DIAGNOSTIC",host,identity_status:identity.status,root_status:rootDiagnostic.status,identity_body_sample:identity.bytes.toString("utf8").slice(0,350),root_body_sample:rootDiagnostic.bytes.toString("utf8").slice(0,180),identity_cf_ray:identity.headers.get("cf-ray"),identity_server:identity.headers.get("server"),identity_type:identity.headers.get("content-type")}));
 if(identity.status!==200){
  for(const control of [
    "https://jasons-dns-burden-of-proof.jaywisdom44.workers.dev/",
    "https://seymour-supreme-public.jaywisdom44.workers.dev/",
    "https://proof.jsonwisdom.com/",
    "https://proof.jsonwisdom.io/",
    "https://www.cloudflare.com/"
  ]) {
    try {
      const r=await get(control);
      const str=r.bytes.toString("utf8");
      const start=str.toLowerCase().indexOf("<title"); const open=start>=0?str.indexOf(">",start):-1; const end=start>=0?str.toLowerCase().indexOf("</title>",start):-1; const title=open>=0&&end>open?str.slice(open+1,end):"";
      const errorCode=null;
      console.log(JSON.stringify({gate:"CONTROL_HTTP",url:control,status:r.status,server:r.headers.get("server"),title:title.slice(0,120),errorCode}));
    } catch(err) {console.error(JSON.stringify({gate:"CONTROL_HTTP",url:control,error:String(err).slice(0,180)}));}
  }
  const page=identity.bytes.toString("utf8");
  console.error(JSON.stringify({gate:"STAGING_ERROR_DETAILS",body_tail:page.slice(-600)}));
}
assert.equal(identity.status,200,host+" identity endpoint must be HTTP 200");
 assert.match(identity.headers.get("content-type")||"",/application\/json/);
 const record=JSON.parse(identity.bytes.toString("utf8"));
 assert.equal(record.worker_service,service);
 assert.equal(record.namespace,"jsonwisdom.io");
 assert.equal(record.source_sha256,expected.sources[origin].sha256);
 assert.equal(record.authority_created,false);
 assert.equal(record.canon,false);
 const head=await get(target+expected.identity_path,"HEAD");
 assert.equal(head.status,200);
 assert.equal(head.bytes.length,0);
 const app=await get(target+"/");
 assert.equal(app.status,200,host+" homepage must be HTTP 200");
 assert.match(app.bytes.toString("utf8",0,80),/<!DOCTYPE html>/i);
 const known=await get(parity);
 assert.equal(known.status,200,parity+" existing production homepage must be HTTP 200");
 assert.equal(app.sha256,known.sha256,host+" homepage must have equal bytes to .com");
 console.log(JSON.stringify({gate:"STAGING_HTTP_AND_PARITY",status:"PASS",host,service,origin_sha256:record.source_sha256,homepage_sha256:app.sha256,homepage_bytes:app.bytes.length}));
}
console.log("CI_FIRST_STAGING_HTTP=PASS");
