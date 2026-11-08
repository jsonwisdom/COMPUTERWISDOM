/** Read-only proof viewer candidate. Does not register proofs or attest identities. */
import manifest from './manifest.json' with {type:'json'};
import domain from './records/CF_PROOF_DOMAIN_ROUTE_20261108.json' with {type:'json'};
import build from './records/GH_TPM_CLIENT_BUILD_20261108.json' with {type:'json'};
import attest from './records/PC_TPM_INDEPENDENT_ATTEST_20261108.json' with {type:'json'};
const byId=new Map([domain,build,attest].map(x=>[x.id,x]));
const common={
 'cache-control':'no-store',
 'x-content-type-options':'nosniff',
 'referrer-policy':'no-referrer',
 'access-control-allow-origin':'*',
 'content-security-policy':"default-src 'none'; form-action 'none'; frame-ancestors 'none'"
};
function json(data,status=200){return new Response(JSON.stringify(data,null,2)+'\n',{status,headers:{...common,'content-type':'application/json; charset=utf-8'}})}
export default {async fetch(request){
 const u=new URL(request.url);
 if(request.method!=='GET'&&request.method!=='HEAD')return json({error:'METHOD_NOT_ALLOWED',authority_created:false},405);
 let payload;
 if(u.pathname==='/'||u.pathname==='/v1/proofs')payload={schema:'CW_PROOF_SURFACE_V1',source:'GitHub PR draft; unpromoted',manifest,proofs:manifest.records.map(x=>({id:x.id,ci_verdict:x.ci_verdict,scope:x.scope})),warning:'Hash inclusion does not prove source truth, hardware identity or external certification.'};
 else if(u.pathname==='/v1/manifest')payload=manifest;
 else if(u.pathname==='/v1/health')payload={status:'SELF_REPORTED',registry:'READ_ONLY',service:'CW_PROOF_SURFACE_V1',public_http_cryptographic_attestation:'UNKNOWN'};
 else if(/^\/v1\/proofs\/[A-Z0-9_-]+$/.test(u.pathname)){
  const id=u.pathname.split('/').at(-1);payload=byId.has(id)?{record:byId.get(id),manifest_entry:manifest.records.find(x=>x.id===id),root_sha256:manifest.root_sha256}:null;
 } else payload=null;
 if(!payload)return json({error:'NOT_FOUND'},404);
 if(request.method==='HEAD')return new Response(null,{headers:{...common,'content-type':'application/json; charset=utf-8'}});
 return json(payload);
 }};
