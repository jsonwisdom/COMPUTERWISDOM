import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {replay,baseline} from "./ci-first-io-production-regression.mjs";

const contract=JSON.parse(readFileSync(new URL("../../workers/jsonwisdom-io/backend-contract.json",import.meta.url),"utf8"));
const modules={
 proof:(await import(new URL("../../workers/jsonwisdom-io/proof-origin.mjs",import.meta.url))).default,
 supreme:(await import(new URL("../../workers/jsonwisdom-io/supreme-origin.mjs",import.meta.url))).default
};
function mockFetcher({tamper=false}={}){
 return async (url,options={})=>{
  const u=new URL(url);
  const identity=u.pathname==="/.well-known/ci-first-backend.json";
  const spec=baseline.resources.find(x=>x.hostname===u.hostname||x.com_control===u.hostname);
  assert.ok(spec,"unrecognized domain in mock");
  if(options.method==="HEAD") return new Response(null,{status:200,headers:{"content-type":"application/json"}});
  if(identity){
   return new Response(JSON.stringify({schema:"computerwisdom.ci-first.worker-identity.v1",
    namespace:"jsonwisdom.io",worker_service:spec.worker,
    source_sha256:contract.sources[spec.source_key].sha256,
    canon:false,authority_created:false,independent_provider:false}),{
    status:200,headers:{"content-type":"application/json"}});
  }
  const r=await modules[spec.source_key].fetch(new Request(url));
  const b=Buffer.from(await r.arrayBuffer());
  if(tamper&&u.hostname==="proof.jsonwisdom.io")return new Response(Buffer.concat([b,Buffer.from("TAMPER")]),{status:200});
  return new Response(b,{status:200,headers:{"content-type":"text/html"}});
 };
}
test("immutable production baseline host set",()=>{
 assert.deepEqual(baseline.resources.map(x=>x.hostname).sort(),
  ["proof.jsonwisdom.io","seymour.jsonwisdom.io","supreme.jsonwisdom.io"]);
 assert.ok(baseline.resources.every(x=>/^[a-f0-9]{64}$/.test(x.expected_sha256)));
});
test("mock live regression validates independent immutable bytes",async()=>{
 const report=await replay({fetcher:mockFetcher()});
 assert.equal(report.status,"PASS",report.error);
 assert.equal(report.checks.length,3);
});
test("tampering with one response fails closed",async()=>{
 const report=await replay({fetcher:mockFetcher({tamper:true})});
 assert.equal(report.status,"FAIL");
 assert.match(report.error,/byte count|SHA-256/i);
});
test("drill restores both roles after loss of isolated staging fixture",()=>{
 const p=fileURLToPath(new URL("./ci-first-io-staging-restore.mjs",import.meta.url));
 const output=execFileSync(process.execPath,[p,"--simulate"],{cwd:process.cwd(),encoding:"utf8"});
 const json=JSON.parse(output.trim());
 assert.equal(json.status,"PASS");
 assert.equal(json.checks.length,2);
 assert.ok(json.checks.every(x=>x.status==="PASS"&&x.remote_cloudflare_restore===false));
});
test("staging upload with no explicit approval fails closed",()=>{
 const p=fileURLToPath(new URL("./ci-first-io-staging-restore.mjs",import.meta.url));
 let msg="";
 try{execFileSync(process.execPath,[p,"--stage-upload","--role=proof"],{
  cwd:process.cwd(),encoding:"utf8",env:{...process.env,CI_FIRST_DRILL_APPROVED:"",CI_FIRST_STAGING_ONLY:""}})}
 catch(e){msg=String(e.stdout||"");}
 assert.match(msg,/explicit staging drill approval missing|staging safety switch missing/);
});
