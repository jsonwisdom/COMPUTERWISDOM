// CI-FIRST: read-only public HTTP regression against an immutable-in-commit SHA-256 baseline.
// No Cloudflare credentials, wallet keys, DNS writes, or baseline self-updates.
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {readFileSync, mkdirSync, writeFileSync} from "node:fs";
import {resolve} from "node:path";
import {fileURLToPath} from "node:url";

export const baseline = JSON.parse(readFileSync(
  new URL("../../workers/jsonwisdom-io/CI_FIRST_IO_PRODUCTION_BASELINE_20261108.json",import.meta.url),"utf8"
));
const sha256=bytes=>createHash("sha256").update(bytes).digest("hex");
function boundedHost(host, io){
  assert.match(host, io ? /^(proof|seymour|supreme)\.jsonwisdom\.io$/ : /^(proof|seymour|supreme)\.jsonwisdom\.com$/);
  return host;
}
export async function replay({fetcher=fetch, expected=baseline}={}){
  const receipt={schema:"computerwisdom.ci-first.io-regression-replay.v1",
    checked_at:new Date().toISOString(),baseline_commit:expected.source_commit,
    baseline_run:expected.source_workflow,head:process.env.GITHUB_SHA??null,
    status:"UNKNOWN",canon:false,authority_created:false,
    independent_provider_failover:false,checks:[]};
  assert.equal(expected.resources.length,3,"exactly three production hosts");
  const limit=expected.rules.max_response_bytes;
  async function get(url, method="GET"){
    const resp=await fetcher(url,{method,redirect:"manual",cache:"no-store",signal:AbortSignal.timeout(18000)});
    const length=Number(resp.headers.get("content-length")??0);
    assert.ok(!length||length<=limit,"oversize content-length");
    const bytes=Buffer.from(await resp.arrayBuffer());
    assert.ok(bytes.length<=limit,"oversize body");
    return {status:resp.status,contentType:resp.headers.get("content-type"),bytes,sha256:sha256(bytes),cfRay:resp.headers.get("cf-ray")};
  }
  try {
    const names=new Set();
    for(const spec of expected.resources){
      const hostname=boundedHost(spec.hostname,true);
      const control=boundedHost(spec.com_control,false);
      assert.ok(!names.has(hostname),"duplicate route");
      names.add(hostname);
      const identity=await get("https://"+hostname+"/.well-known/ci-first-backend.json");
      assert.equal(identity.status,200,hostname+" identity status");
      assert.match(identity.contentType??"",/application\/json/);
      const id=JSON.parse(identity.bytes.toString("utf8"));
      assert.equal(id.worker_service,spec.worker,hostname+" worker");
      assert.equal(id.namespace,"jsonwisdom.io");
      assert.equal(id.canon,false);
      assert.equal(id.authority_created,false);
      assert.equal(id.independent_provider,false);
      const head=await get("https://"+hostname+"/.well-known/ci-first-backend.json","HEAD");
      assert.equal(head.status,200);
      assert.equal(head.bytes.length,0);
      const publicResponse=await get("https://"+hostname+spec.path);
      const controlResponse=await get("https://"+control+spec.path);
      assert.equal(publicResponse.status,spec.expected_status??expected.rules.http_status);
      assert.equal(controlResponse.status,200);
      assert.equal(publicResponse.bytes.length,spec.expected_bytes,hostname+" byte count");
      assert.equal(publicResponse.sha256,spec.expected_sha256,hostname+" pinned SHA-256");
      assert.equal(controlResponse.sha256,spec.expected_sha256,control+" pinned SHA-256");
      receipt.checks.push({hostname,control,worker:id.worker_service,http_status:publicResponse.status,
        identity_status:identity.status,sha256:publicResponse.sha256,bytes:publicResponse.bytes.length,
        control_sha256:controlResponse.sha256,cf_ray:publicResponse.cfRay,status:"PASS"});
    }
    receipt.status="PASS";
  }catch(e){
    receipt.status="FAIL";
    receipt.error=String(e);
  }
  return receipt;
}
export function writeReceipt(receipt){
  const run=String(process.env.GITHUB_RUN_ID||"manual").replace(/[^a-zA-Z0-9_-]/g,"");
  const head=String(process.env.GITHUB_SHA||"unversioned").slice(0,12).replace(/[^a-zA-Z0-9_-]/g,"");
  const folder=resolve(".ci-first/receipts");
  mkdirSync(folder,{recursive:true});
  const path=resolve(folder,"CI_FIRST_IO_REGRESSION_"+head+"_"+run+".json");
  const bytes=Buffer.from(JSON.stringify(receipt,null,2)+"\n","utf8");
  writeFileSync(path,bytes,{flag:"w"});
  return {path,sha256:sha256(bytes),bytes:bytes.length};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const receipt=await replay();
 const artifact=writeReceipt(receipt);
 console.log(JSON.stringify({status:receipt.status,...artifact,checks:receipt.checks.length,error:receipt.error??null}));
 if(receipt.status!=="PASS") process.exitCode=1;
}
