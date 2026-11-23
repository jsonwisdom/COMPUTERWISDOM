import test from 'node:test';import assert from 'node:assert/strict';
import {sha256,verdict,reportCheck,businessDaysAfter,elapsedHours,birthdayModel,classifyHashes,assessPromotion,publicAudit,rdapAudit,privateAudit,humanAudit} from './JASONS_DNS_CI_RUNNER.mjs';
import {readFile} from 'node:fs/promises';
const contract=JSON.parse(await readFile(new URL('./JASONS_DNS_CI_CONTRACT.json',import.meta.url),'utf8'));
const p=(id,status)=>reportCheck(id,status);
test('SHA256 empty vector from Wolfram and FIPS',()=>assert.equal(sha256(''),'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'));
test('SHA256 abc vector from Wolfram and FIPS',()=>assert.equal(sha256('abc'),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'));
test('SHA-256 exact bytes not normalized',()=>assert.notEqual(sha256(Buffer.from('a\r\n')),sha256(Buffer.from('a\n'))));
test('birthday 64-bit Wolfram fixture',()=>assert.ok(Math.abs(birthdayModel(6000000000,64).probability-0.6231024786239225)<1e-14));
test('birthday 128-bit lower bound',()=>assert.ok(Math.abs(birthdayModel(6000000000,128).probability-5.289724577818673e-20)<1e-30));
test('birthday one ID has no collisions',()=>assert.equal(birthdayModel(1,32).probability,0));
test('birthday invalid precision rejected',()=>assert.throws(()=>birthdayModel(2,0)));
test('Nov 23 tenth business day excl Veterans Day',()=>assert.equal(businessDaysAfter('2026-11-06',10,['2026-11-11']),'2026-11-23'));
test('business-day starting day excluded',()=>assert.equal(businessDaysAfter('2026-11-06',1,['2026-11-11']),'2026-11-09'));
test('impossible date rejects',()=>assert.throws(()=>businessDaysAfter('2026-02-30',1)));
test('elapsed time requires explicit timezone',()=>assert.throws(()=>elapsedHours('2026-11-06T12:00:00','2026-11-06T13:00:00Z')));
test('elapsed time rejects chronology inversion',()=>assert.throws(()=>elapsedHours('2026-11-06T13:00:00Z','2026-11-06T12:00:00Z')));
test('elapsed UTC two hours',()=>assert.equal(elapsedHours('2026-11-06T12:00:00Z','2026-11-06T14:00:00Z'),2));
test('same file is duplicate not hash collision',()=>assert.equal(classifyHashes('a'.repeat(64),'a'.repeat(64),true),'DUPLICATE_CONTENT_NOT_COLLISION'));
test('same digest without original bytes is unknown evidence',()=>assert.equal(classifyHashes('a'.repeat(64),'a'.repeat(64),null),'MATCHING_DIGESTS_ORIGINAL_BYTES_UNVERIFIED'));
test('malformed hash is unknown',()=>assert.equal(classifyHashes('not_a_hash','a'.repeat(64),true),'UNKNOWN'));
test('invalid status rejected',()=>assert.throws(()=>reportCheck('fake','HOLD')));
test('status FAIL dominates UNKNOWN',()=>assert.equal(verdict([p('a','PASS'),p('b','UNKNOWN'),p('c','FAIL')]),'FAIL'));
test('status UNKNOWN blocks promotion',()=>assert.equal(assessPromotion([p('a','PASS'),p('b','UNKNOWN')],true).authorized,false));
test('human control blocks even all-PASS tests',()=>assert.equal(assessPromotion([p('a','PASS')],false).authorized,false));
test('public contract has four hosts and four pinned assets',()=>{assert.equal(contract.publicHosts.length,4);assert.equal(Object.keys(contract.assets).length,4)});
function resp(body,status=200,headers={}){return new Response(body,{status,headers})}
test('public synthetic fixture passes with expected bytes and secure headers',async()=>{
 const min={...contract,publicHosts:['fake.example'],assets:{'/':{sha256:sha256('app'),bytes:3}}};
 const request=async url=>url.endsWith('/__health')?resp(JSON.stringify({backend_persistence:false,payment_signing:false,x402_mainnet:false,authority_created:false,legal_verdicts:false}),200):resp('app',200,{'content-security-policy':"default-src 'none'; connect-src 'none'; form-action 'none'; script-src 'self'",'x-content-type-options':'nosniff'});
 const x=await publicAudit(min,{request});assert.equal(verdict(x.checks),'PASS');assert.equal(x.checks.length,4);
});
test('public modified bytes cause FAIL not PASS',async()=>{
 const min={...contract,publicHosts:['fake.example'],assets:{'/':{sha256:sha256('app'),bytes:3}}};
 const request=async url=>url.endsWith('/__health')?resp(JSON.stringify({backend_persistence:false,payment_signing:false,x402_mainnet:false,authority_created:false,legal_verdicts:false})):resp('tampered',200,{'content-security-policy':"connect-src 'none';form-action 'none';script-src 'self'",'x-content-type-options':'nosniff'});
 const x=await publicAudit(min,{request});assert.equal(verdict(x.checks),'FAIL');
});
test('unsafe health payment state causes FAIL',async()=>{
 const min={...contract,publicHosts:['fake.example'],assets:{'/':{sha256:sha256('app'),bytes:3}}};
 const request=async url=>url.endsWith('/__health')?resp(JSON.stringify({backend_persistence:false,payment_signing:true,x402_mainnet:false,authority_created:false,legal_verdicts:false})):resp('app',200,{'content-security-policy':"connect-src 'none';form-action 'none';script-src 'self'",'x-content-type-options':'nosniff'});
 const x=await publicAudit(min,{request});assert.equal(verdict(x.checks),'FAIL');
});
test('RDAP registry transfer lock and unsigned DNSSEC are distinct',async()=>{
 const min={rdap:{'fake.example':'https://rdap.test/domain/fake.example'}};
 const request=async()=>resp(JSON.stringify({status:['client transfer prohibited'],secureDNS:{delegationSigned:false}}));
 const x=await rdapAudit(min,{request});assert.equal(x.checks[0].status,'PASS');assert.equal(x.checks[1].status,'FAIL');
});
test('missing private Cloudflare credentials is UNKNOWN',async()=>{const x=await privateAudit(contract,{});assert.equal(x.checks[0].status,'UNKNOWN')});
test('sensitive human approvals remain UNKNOWN',()=>assert.equal(verdict(humanAudit().checks),'UNKNOWN'));
test('private Cloudflare synthetic insecure settings fail',async()=>{
 const calls=[];const request=async url=>{calls.push(url);let result;
 if(url.includes('/dnssec'))result={status:'disabled'};
 else if(url.includes('/settings'))result=[{id:'min_tls_version',value:'1.0'},{id:'always_use_https',value:'off'},{id:'ssl',value:'full'}];
 else throw Error('unexpected API request');
 return resp(JSON.stringify({success:true,result}),200,{'content-type':'application/json'});
 };
 const env={CF_API_TOKEN:'dummy',CF_ZONE_COM:'z1',CF_ZONE_IO:'z2'};
 const x=await privateAudit(contract,env,{request});assert.equal(x.checks.filter(y=>y.status==='FAIL').length,6);assert.ok(x.checks.some(y=>y.id==='strict-origin-readiness:jsonwisdom.com'&&y.status==='UNKNOWN'));assert.ok(calls.every(u=>u.startsWith('https://api.cloudflare.com/client/v4/')));
});
