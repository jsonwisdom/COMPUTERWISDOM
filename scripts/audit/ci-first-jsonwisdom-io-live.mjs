// Read-only authenticated production gate. Never modifies DNS, Workers, wallets or funds.
import {readFileSync} from "node:fs";
const c=JSON.parse(readFileSync(new URL("../../workers/jsonwisdom-io/backend-contract.json",import.meta.url),"utf8"));
const token=process.env.CF_API_TOKEN,account=process.env.CF_ACCOUNT_ID;
if(!token||!account){console.error("UNKNOWN: Cloudflare read-only API token/account missing");process.exit(2)}
const result=await fetch("https://api.cloudflare.com/client/v4/accounts/"+encodeURIComponent(account)+"/workers/domains",{
 headers:{"Authorization":"Bearer "+token}});
if(!result.ok){console.error("UNKNOWN: Cloudflare HTTP "+result.status);process.exit(2)}
const body=await result.json();
if(!body.success||!Array.isArray(body.result)){console.error("UNKNOWN: malformed Cloudflare response");process.exit(2)}
const domains=new Map(body.result.map(d=>[d.hostname,d.service]));
let failed=[];
for(const [host,worker] of Object.entries({...c.original_com,...c.hostnames})){
 if(domains.get(host)!==worker)failed.push({host,expected:worker,actual:domains.get(host)||"NOT_FOUND"});
}
if(failed.length){console.error(JSON.stringify({gate:"IO_ROUTING",status:"FAIL",failed}));process.exit(1)}
for(const [host,worker] of Object.entries(c.hostnames)){
 let response;try{response=await fetch("https://"+host+c.identity_path,{cache:"no-store"})}catch(e){console.error("UNKNOWN: HTTP probe",host,String(e));process.exit(2)}
 if(response.status!==200){console.error("FAIL: identity endpoint",host,response.status);process.exit(1)}
 const body=await response.json();
 if(body.worker_service!==worker||body.authority_created!==false||body.canon!==false){console.error("FAIL: identity not valid",host);process.exit(1)}
}
console.log(JSON.stringify({gate:"IO_ROUTING",status:"PASS",scope:"distinct Worker IDs in one Cloudflare account only"}));
