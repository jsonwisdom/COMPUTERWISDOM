// CI-FIRST rehearsal: rebuild a staging response from pinned GitHub backup bytes alone.
// Default SIMULATE only in OS temp dir. Remote staging upload requires separate explicit flags.
// NO production Cloudflare calls, custom domain changes, R2 deletion, wallet use, or fund transfers.
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {readFileSync, mkdirSync, writeFileSync, copyFileSync, mkdtempSync, rmSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";
import {pathToFileURL} from "node:url";

const contract=JSON.parse(readFileSync(new URL("../../workers/jsonwisdom-io/backend-contract.json",import.meta.url),"utf8"));
const baseline=JSON.parse(readFileSync(new URL("../../workers/jsonwisdom-io/CI_FIRST_IO_PRODUCTION_BASELINE_20261108.json",import.meta.url),"utf8"));
const sha256=(b)=>createHash("sha256").update(b).digest("hex");
const roles=["proof","supreme"];
export async function simulate(role){
 assert.ok(roles.includes(role),"only known staging roles");
 const src=contract.sources[role];
 const saved=readFileSync(new URL("../../"+src.source_path,import.meta.url));
 assert.equal(saved.byteLength,src.bytes,"backup source bytes must match contract");
 assert.equal(sha256(saved),src.sha256,"backup digest mismatch: STOP");
 const temp=mkdtempSync(join(tmpdir(),"ci-first-io-staging-drill-"));
 try{
   const backup=join(temp,"backup");
   const staging=join(temp,"staging");
   mkdirSync(backup);
   mkdirSync(staging);
   const copied=join(backup,role+"-origin.mjs");
   writeFileSync(copied,saved);
   const destroyed=join(staging,"prior-response.bin");
   writeFileSync(destroyed,Buffer.from("INTENTIONALLY_CORRUPTED_STAGING_FIXTURE"));
   rmSync(destroyed);
   // Restoration begins here; ONLY the temp backup is read. No production fetch.
   const mod=await import(pathToFileURL(copied).href);
   assert.equal(typeof mod.default?.fetch,"function","backup not executable");
   const response=await mod.default.fetch(new Request("https://ci-"+role+"-restore.invalid/"),{},{waitUntil:()=>{}});
   assert.equal(response.status,200);
   const restored=Buffer.from(await response.arrayBuffer());
   const target=baseline.resources.find(x=>x.source_key===role);
   assert.ok(target,"no immutable response baseline");
   assert.equal(restored.length,target.expected_bytes,"restored byte count differs");
   assert.equal(sha256(restored),target.expected_sha256,"restored SHA-256 differs");
   const path=join(staging,role+"-restored.bin");
   writeFileSync(path,restored);
   assert.equal(sha256(readFileSync(path)),target.expected_sha256);
   return {role,status:"PASS",source_sha256:src.sha256,
     restored_sha256:sha256(restored),restored_bytes:restored.length,
     destruction_scope:"TEMP_STAGING_FIXTURE_ONLY",
     remote_cloudflare_restore:false,independent_storage_proven:false};
 }finally{rmSync(temp,{recursive:true,force:true})}
}
function stagingEntry(role){
 const src=contract.sources[role];
 return `import original from "./${role}-origin.mjs";
const identity=Object.freeze({schema:"computerwisdom.ci-first.staging-recovery.v1",role:"${role}",
source_sha256:"${src.sha256}",authority_created:false,canon:false,staging_only:true});
export default {async fetch(request,env,ctx){
 const u=new URL(request.url);
 if(u.pathname==="/.well-known/ci-first-recovery.json"){
  return new Response(JSON.stringify(identity),{headers:{"content-type":"application/json","cache-control":"no-store"}});
 }
 return original.fetch(request,env,ctx);
}};`;
}
export async function uploadToIsolatedStaging(role){
 assert.ok(roles.includes(role));
 assert.equal(process.env.CI_FIRST_STAGING_ONLY,"1","staging safety switch missing");
 assert.equal(process.env.CI_FIRST_DRILL_APPROVED,"YES","explicit staging drill approval missing");
 const account=process.env.CF_ACCOUNT_ID,token=process.env.CF_API_TOKEN;
 assert.ok(account&&token,"missing staging-only Cloudflare API credentials");
 const name="jw-io-recovery-drill-20261108-"+role;
 // Fail closed if any public domain currently attaches to our target worker.
 const api="https://api.cloudflare.com/client/v4/accounts/"+encodeURIComponent(account);
 async function apiCall(endpoint,options={}){
   const res=await fetch(api+endpoint,{...options,headers:{"Authorization":"Bearer "+token,...(options.headers||{})},signal:AbortSignal.timeout(20000)});
   const json=await res.json();
   return {ok:res.ok,data:json,status:res.status};
 }
 const domains=await apiCall("/workers/domains");
 assert.ok(domains.ok&&domains.data?.success&&Array.isArray(domains.data.result),"cannot verify target isolation");
 assert.ok(!domains.data.result.some(x=>x.service===name),"staging target has a public custom domain; STOP");
 const existing=await apiCall("/workers/scripts/"+name);
 assert.equal(existing.status,404,"target Worker already exists; overwrite forbidden");
 const src=contract.sources[role];
 const content=readFileSync(new URL("../../"+src.source_path,import.meta.url));
 assert.equal(content.byteLength,src.bytes);
 assert.equal(sha256(content),src.sha256);
 const form=new FormData();
 form.append("metadata",new Blob([JSON.stringify({main_module:"restore-entry.mjs",
   compatibility_date:"2026-11-08",bindings:[]})],{type:"application/json"}));
 form.append("restore-entry.mjs",new Blob([stagingEntry(role)],{type:"application/javascript+module"}),"restore-entry.mjs");
 form.append(role+"-origin.mjs",new Blob([content],{type:"application/javascript+module"}),role+"-origin.mjs");
 const uploaded=await apiCall("/workers/scripts/"+name,{method:"PUT",body:form});
 assert.ok(uploaded.ok&&uploaded.data?.success,"staging upload rejected");
 return {role,status:"PASS",staging_worker:name,deployment:uploaded.data.result?.deployment_id??null,
   domain_attached:false,staging_http_health:"UNKNOWN",authority_created:false};
}
const mode=process.argv.includes("--stage-upload")?"stage-upload":"simulate";
const requested=roles.filter(x=>process.argv.includes("--role="+x));
const selected=requested.length?requested:roles;
const result={schema:"computerwisdom.ci-first.staging-restore-drill.v1",
 tested_at:new Date().toISOString(),mode,status:"UNKNOWN",checks:[],
 canon:false,authority_created:false,independent_provider_failover:false};
try{
 if(mode==="stage-upload"&&requested.length!==1)throw new Error("--stage-upload requires exactly one --role");
 for(const role of selected){
   const simulated=await simulate(role);result.checks.push(simulated);
   if(mode==="stage-upload")result.checks.push(await uploadToIsolatedStaging(role));
 }
 result.status="PASS";
}catch(e){result.status="FAIL";result.error=String(e);}
const out=resolve(".ci-first/receipts");
mkdirSync(out,{recursive:true});
const name="CI_FIRST_IO_STAGING_RESTORE_"+mode.replace(/[^a-z-]/g,"")+"_"+String(process.env.GITHUB_RUN_ID||"manual").replace(/[^a-zA-Z0-9_-]/g,"")+".json";
const receipt=Buffer.from(JSON.stringify(result,null,2)+"\n");
writeFileSync(join(out,name),receipt);
console.log(JSON.stringify({status:result.status,mode,checks:result.checks,
  receipt_file:join(out,name),receipt_sha256:sha256(receipt),error:result.error??null}));
if(result.status!=="PASS")process.exitCode=1;
