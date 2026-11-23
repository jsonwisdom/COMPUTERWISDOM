/**
 * Jason's DNS CI-FIRST v1.0.0 — zero-dependency, GET-only verification.
 * Public checks assert exact delivered bytes. Private checks require a
 * separately-scoped read-only Cloudflare API token. Never writes upstream.
 * UNKNOWN is not PASS. This code makes no authority or fraud findings.
 */
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';

export const sha256 = (value) => createHash('sha256').update(value).digest('hex');
export const VALID = new Set(['PASS','FAIL','UNKNOWN']);
export const verdict = (checks) => checks.some(x=>x.status==='FAIL')?'FAIL':checks.some(x=>x.status==='UNKNOWN')?'UNKNOWN':'PASS';
export function reportCheck(id, status, observed=null, expected=null, notes='') {
 if(!VALID.has(status))throw new Error('Unsupported CI state: '+status);
 return {id,status,observed,expected,notes};
}
export function businessDaysAfter(isoDate,count,holidays=[]) {
 if(!/^\d{4}-\d{2}-\d{2}$/.test(isoDate)||!Number.isInteger(count)||count<0)throw Error('Invalid date or count');
 const d=new Date(isoDate+'T00:00:00.000Z');
 if(Number.isNaN(d.valueOf())||d.toISOString().slice(0,10)!==isoDate)throw Error('Invalid ISO date');
 const excluded=new Set(holidays); let remaining=count;
 while(remaining>0){ d.setUTCDate(d.getUTCDate()+1);const day=d.getUTCDay();const date=d.toISOString().slice(0,10);if(day!==0&&day!==6&&!excluded.has(date))remaining--; }
 return d.toISOString().slice(0,10);
}
export function elapsedHours(first,last){
 if(typeof first!=='string'||typeof last!=='string'|| !/([zZ]|[+-]\d\d:\d\d)$/.test(first)||!/([zZ]|[+-]\d\d:\d\d)$/.test(last))throw Error('Explicit timezone required');
 const x=Date.parse(first),y=Date.parse(last);if(!Number.isFinite(x)||!Number.isFinite(y)||y<x)throw Error('Invalid or inverted times');return (y-x)/3_600_000;
}
export function birthdayModel(n,bits) {
 if(!Number.isSafeInteger(n)||n<0||!Number.isInteger(bits)||bits<=0||bits>256)throw Error('Bad model inputs');
 const lambda=n*(n-1)/Math.pow(2,bits+1);
 return {n,bits,lambda,probability:-Math.expm1(-lambda),assumptions:'independent, uniform b-bit identifiers; hypothetical'};
}
export const classifyHashes = (a,b,areOriginalBytesEqual) => {
 if(!/^[a-f0-9]{64}$/.test(a)||!/^[a-f0-9]{64}$/.test(b))return 'UNKNOWN';
 if(a!==b)return 'DIFFERENT_DIGESTS';
 if(areOriginalBytesEqual===true)return 'DUPLICATE_CONTENT_NOT_COLLISION';
 if(areOriginalBytesEqual===false)return 'SUSPECTED_HASH_COLLISION_REQUIRES_INDEPENDENT_VALIDATION';
 return 'MATCHING_DIGESTS_ORIGINAL_BYTES_UNVERIFIED';
};
export function assessPromotion(checks,humanAuthorization) {
 const v=verdict(checks);
 return {tests:checks.length,passed:checks.filter(x=>x.status==='PASS').length,failed:checks.filter(x=>x.status==='FAIL').length,unknown:checks.filter(x=>x.status==='UNKNOWN').length,verdict:v,authorized:humanAuthorization===true&&v==='PASS',reason:humanAuthorization!==true?'Human promotion authorization not established':(v!=='PASS'?'Unresolved CI findings':'Eligible for separate human action')};
}
const timeoutMs=Number(process.env.CI_FETCH_TIMEOUT_MS||12000);
export async function retrieve(url,headers={}){
 const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),timeoutMs);
 try {return await fetch(url,{method:'GET',redirect:'follow',headers,signal:controller.signal,cache:'no-store'});}finally{clearTimeout(timer)}
}
export async function publicAudit(contract,{request=retrieve}={}){
 const checks=[];const snap={};
 await Promise.all(contract.publicHosts.map(async (host)=>{
   snap[host]={};
   await Promise.all(Object.entries(contract.assets).map(async ([path,expect])=>{
     const url='https://'+host+path;
     try{
       const r=await request(url);if(r.status!==200){checks.push(reportCheck('http:'+host+path,'FAIL',r.status,200));return}
       const bytes=Buffer.from(await r.arrayBuffer());const actual={http:r.status,bytes:bytes.length,sha256:sha256(bytes),contentType:r.headers.get('content-type')};snap[host][path]=actual;
       checks.push(reportCheck('integrity:'+host+path,(actual.bytes===expect.bytes&&actual.sha256===expect.sha256)?'PASS':'FAIL',actual,expect));
       if(path==='/'){
         const csp=r.headers.get('content-security-policy')||'';
         checks.push(reportCheck('csp:'+host,csp.includes("connect-src 'none'")&&csp.includes("form-action 'none'")&&csp.includes("script-src 'self'")?'PASS':'FAIL',csp,'connect-src none; form-action none; script-src self'));
         const noSniff=r.headers.get('x-content-type-options');
         checks.push(reportCheck('nosniff:'+host,noSniff==='nosniff'?'PASS':'FAIL',noSniff,'nosniff'));
       }
     }catch(e){checks.push(reportCheck('fetch:'+host+path,'UNKNOWN',String(e.message||e),'HTTP 200 and matching bytes'))}
   }));
   const url='https://'+host+'/__health';
   try {
     const r=await request(url);if(r.status!==200){checks.push(reportCheck('health:'+host,'FAIL',r.status,200));return}
     const j=await r.json();const safe=j.backend_persistence===false&&j.payment_signing===false&&j.x402_mainnet===false&&j.authority_created===false&&j.legal_verdicts===false;
     checks.push(reportCheck('health-scope:'+host,safe?'PASS':'FAIL',{service:j.service,version:j.version,backend_persistence:j.backend_persistence,payment_signing:j.payment_signing,x402_mainnet:j.x402_mainnet,authority_created:j.authority_created,legal_verdicts:j.legal_verdicts},'All five false; public static only','Self-reported capabilities must also be confirmed in private binding check'));
   }catch(e){checks.push(reportCheck('health:'+host,'UNKNOWN',String(e.message||e)))}
 }));
 return {checks,observations:snap};
}
export async function rdapAudit(contract,{request=retrieve}={}) {
 const checks=[],snapshot={};
 for(const [domain,url] of Object.entries(contract.rdap)){
   try{
     const r=await request(url,{accept:'application/rdap+json'});
     if(r.status!==200){checks.push(reportCheck('rdap:'+domain,'UNKNOWN',r.status,200));continue}
     const bytes=Buffer.from(await r.arrayBuffer());const j=JSON.parse(bytes.toString('utf8'));
     const status=(j.status||[]).map(s=>String(s).toLowerCase().replaceAll(/[_-]/g,' '));const transfer=status.some(s=>/client transfer prohibited|server transfer prohibited/.test(s));
     const signed=j.secureDNS?.delegationSigned??null;
     snapshot[domain]={sha256:sha256(bytes),bytes:bytes.length,status,delegationSigned:signed};
     checks.push(reportCheck('registrar-transfer-lock:'+domain,transfer?'PASS':'FAIL',status,'client/server transfer prohibited','Public RDAP does not establish account MFA or recovery'));
     checks.push(reportCheck('rdap-delegation:'+domain,signed===true?'PASS':signed===false?'FAIL':'UNKNOWN',signed,true));
   }catch(e){checks.push(reportCheck('rdap:'+domain,'UNKNOWN',String(e.message||e)))}
 }
 return {checks,observations:snapshot};
}
async function cfGet(path,token,{request=retrieve}={}){
 const r=await request('https://api.cloudflare.com/client/v4'+path,{Authorization:'Bearer '+token,Accept:'application/json'});
 if(r.status!==200)throw new Error('Cloudflare read HTTP '+r.status+' at '+path);
 const j=await r.json();if(!j.success)throw new Error('Cloudflare read unsuccessful '+path);return j.result;
}
const setting=(all,id)=>all.find(x=>x.id===id)?.value;
export async function privateAudit(contract,env=process.env,{request=retrieve}={}){
 const checks=[], observations={};const token=env.CF_API_TOKEN||'';
 const ids={'jsonwisdom.com':env.CF_ZONE_COM,'jsonwisdom.io':env.CF_ZONE_IO};
 if(!token){checks.push(reportCheck('cloudflare-token','UNKNOWN','not configured','read-only token required'));return {checks,observations}}
 for(const [domain,id] of Object.entries(ids)){
   if(!id){checks.push(reportCheck('cf-zone-id:'+domain,'UNKNOWN','missing','configured zone ID'));continue}
   try{
     const [dnssec,settings]=await Promise.all([cfGet(`/zones/${id}/dnssec`,token,{request}),cfGet(`/zones/${id}/settings`,token,{request})]);
     const obs={dnssec:dnssec.status,always_use_https:setting(settings,'always_use_https'),min_tls_version:setting(settings,'min_tls_version'),ssl:setting(settings,'ssl')};observations[domain]=obs;
     checks.push(reportCheck('dnssec:'+domain,obs.dnssec==='active'?'PASS':'FAIL',obs.dnssec,'active'));
     checks.push(reportCheck('https-policy:'+domain,obs.always_use_https==='on'?'PASS':'FAIL',obs.always_use_https,'on'));
     checks.push(reportCheck('tls-min:'+domain,Number.parseFloat(obs.min_tls_version)>=1.2?'PASS':'FAIL',obs.min_tls_version,'>=1.2'));
     // Full strict is a separate origin compatibility gate and may not be changed blindly.
     checks.push(reportCheck('strict-origin-readiness:'+domain,obs.ssl==='strict'?'PASS':'UNKNOWN',obs.ssl,'strict / externally verified cert chain','Not a promotion blocker for Worker-only origins; unresolved for external origins'));
   }catch(e){checks.push(reportCheck('cf-security:'+domain,'UNKNOWN',String(e.message||e)))}
 }
 if(env.CF_ACCOUNT_ID){
   try{
     const acc=env.CF_ACCOUNT_ID;
     const [workers,domains,settings]=await Promise.all([
       cfGet(`/accounts/${acc}/workers/scripts`,token,{request}),
       cfGet(`/accounts/${acc}/workers/domains`,token,{request}),
       cfGet(`/accounts/${acc}/workers/scripts/jasons-dns-burden-of-proof/settings`,token,{request})
     ]);
     const workerNames=new Set(workers.map(x=>x.id));
     checks.push(reportCheck('worker-count',workers.length>=contract.inventoryMinimum?'PASS':'FAIL',workers.length,`>=${contract.inventoryMinimum}`));
     checks.push(reportCheck('worker-core-presence',contract.requiredWorkers.every(x=>workerNames.has(x))?'PASS':'FAIL',contract.requiredWorkers.filter(x=>workerNames.has(x)),contract.requiredWorkers));
     const current=Object.fromEntries(domains.filter(x=>contract.publicHosts.includes(x.hostname)).map(x=>[x.hostname,{service:x.service,enabled:x.enabled}]));
     checks.push(reportCheck('domain-worker-map',contract.publicHosts.every(x=>current[x]?.service==='jasons-dns-burden-of-proof'&&current[x]?.enabled===true)?'PASS':'FAIL',current,'All four hosts mapped to Burden of Proof'));
     const bindings=(settings.bindings||[]).map(x=>({type:x.type,name:x.name}));
     checks.push(reportCheck('public-worker-bindings',bindings.length===0?'PASS':'FAIL',bindings,'zero','No payment/database binding on public Worker'));
     observations.inventory={count:workers.length,core:contract.requiredWorkers.map(x=>({name:x,exists:workerNames.has(x)})),mapping:current,publicWorkerBindings:bindings};
   }catch(e){checks.push(reportCheck('cf-inventory','UNKNOWN',String(e.message||e)))}
 }else checks.push(reportCheck('cf-account-id','UNKNOWN','missing','account ID to verify Worker inventories'));
 return {checks,observations};
}
export function humanAudit(){return {checks:[
 reportCheck('registrar-mfa','UNKNOWN','not observed','direct registrar account verification'),
 reportCheck('registrar-recovery','UNKNOWN','not observed','recovery access verified without reset'),
 reportCheck('origin-certificate-compatibility','UNKNOWN','not tested','per-origin validated certificate chain before Full (strict)'),
 reportCheck('evidence-independent-replay','UNKNOWN','not established','original bytes and separate independent locker receipt'),
 reportCheck('human-release-authorization','UNKNOWN','none recorded','explicit approval after all security gates')],observations:{}}}
export async function run(mode='all', options={}){
 const contract=options.contract||JSON.parse(await readFile(new URL('./JASONS_DNS_CI_CONTRACT.json',import.meta.url),'utf8'));
 const parts=[];
 if(['public','all'].includes(mode))parts.push(await publicAudit(contract,options));
 if(['rdap','all'].includes(mode))parts.push(await rdapAudit(contract,options));
 if(['private','all'].includes(mode))parts.push(await privateAudit(contract,options.env,options));
 if(['human','all'].includes(mode))parts.push(humanAudit());
 if(!['public','rdap','private','human','all'].includes(mode))throw Error('Unknown CI mode');
 const checks=parts.flatMap(x=>x.checks).sort((a,b)=>a.id.localeCompare(b.id)),observations=Object.assign({},...parts.map(x=>x.observations));
 const result={schema:'JASONS_DNS_CI_FIRST_V1',at_utc:new Date().toISOString(),mode,source:'connector independent, runtime specific',checks,summary:assessPromotion(checks,false),observations,no_mutations:true};
 return result;
}
if(import.meta.url===new URL('file://'+process.argv[1]).href){
 const mode=process.argv[2]||'all',out=process.argv[3];let result;
 try{result=await run(mode)}catch(e){result={schema:'JASONS_DNS_CI_FIRST_V1',at_utc:new Date().toISOString(),mode,checks:[reportCheck('fatal','UNKNOWN',String(e.message||e))],summary:{verdict:'UNKNOWN',authorized:false},no_mutations:true}}
 const bytes=Buffer.from(JSON.stringify(result,null,2)+'\n');const digest=sha256(bytes);
 if(out){await mkdir(dirname(resolve(out)),{recursive:true});await writeFile(out,bytes);await writeFile(out+'.sha256',`${digest}  ${out.split('/').at(-1)}\n`);}
 else process.stdout.write(bytes);
 console.error(`CI-FIRST ${result.summary.verdict} / ${result.checks.length} checks / sha256 ${digest}`);
 process.exit(result.summary.verdict==='PASS'?0:result.summary.verdict==='FAIL'?1:2);
}
