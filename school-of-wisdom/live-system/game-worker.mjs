import {bundle} from './bundle.mjs';
import {registry} from './registry.mjs';
const canon=x=>JSON.stringify(x&&typeof x==='object'?Array.isArray(x)?x.map(v=>JSON.parse(canon(v))):Object.fromEntries(Object.keys(x).sort().map(k=>[k,JSON.parse(canon(x[k]))])):x);
const hash=async s=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('');
const json=(v,status=200)=>Response.json(v,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
const err=(s,m)=>{throw {status:s,message:m};};
function fraction(s){if(typeof s!=='string'||s!==s.trim()||s.length>257||! /^[0-9]{1,128}\/[0-9]{1,128}$/.test(s))err(400,'invalid_fraction');let [n,d]=s.split('/').map(BigInt);if(!d)err(400,'zero_denominator');let a=n,b=d;while(b){[a,b]=[b,a%b];}return [String(n/a),String(d/a)];}
function score(c,a){if(c.id==='CH-001'){if(!Number.isSafeInteger(a))err(400,'integer_required');return {earned:Number(a===c.fixture.values.reduce((s,v)=>s+v,0)),possible:1};}
if(c.id==='CH-002'){const key=c.private.answers;if(!a||Array.isArray(a)||typeof a!=='object'||canon(Object.keys(a).sort())!==canon(Object.keys(key).sort())||Object.values(a).some(v=>!bundle.labels.includes(v)))err(400,'invalid_classification');return {earned:Object.keys(key).filter(k=>a[k]===key[k]).length,possible:4};}
return {earned:Number(canon(fraction(a))===canon(fraction(c.private.answer))),possible:1};}
const publicChallenge=c=>{const p=Object.fromEntries(['id','version','sku','prompt'].map(k=>[k,c[k]]));p.fixture=c.id==='CH-001'?{synthetic:true,values:c.fixture.values}:c.id==='CH-002'?{definitions:c.fixture.definitions,items:c.fixture.items}:{format:'unsigned n/d'};return p;};
function validateBundle(b){
 const allowed=['id','version','sku','prompt','fixture','private'];
 if(!b||!Array.isArray(b.challenges)||b.challenges.length!==3)err(503,'bundle_schema_invalid');
 for(const c of b.challenges){
 if(canon(Object.keys(c).sort())!==canon(allowed.sort())||typeof c.prompt!=='string'||!Number.isSafeInteger(c.version))err(503,'bundle_schema_invalid');
 if(c.id==='CH-001'&&(!Array.isArray(c.fixture.values)||c.fixture.values.some(v=>!Number.isSafeInteger(v))||c.fixture.synthetic!==true||canon(Object.keys(c.fixture).sort())!==canon(['synthetic','values'])))err(503,'bundle_schema_invalid');
 if(c.id==='CH-002'&&(canon(Object.keys(c.fixture).sort())!==canon(['definitions','items'])||canon(Object.keys(c.fixture.items).sort())!==canon(['a','b','c','d'])||Object.values(c.fixture.items).some(v=>typeof v!=='string')||canon(Object.keys(c.fixture.definitions).sort())!==canon(['ASSUMPTION','DOCUMENTED','SATIRE','UNVERIFIED'])||Object.values(c.fixture.definitions).some(v=>typeof v!=='string')))err(503,'bundle_schema_invalid');
 if(c.id==='CH-003'&&(canon(Object.keys(c.fixture))!==canon(['format'])||typeof c.fixture.format!=='string'))err(503,'bundle_schema_invalid');
 }
}
export default {async fetch(req,env){try{
 validateBundle(bundle);
 if(await hash(canon(bundle))!==env.BUNDLE_DIGEST)err(503,'artifact_integrity_failed');
 const u=new URL(req.url);
 if(u.pathname==='/health'&&req.method==='GET')return json({service:'jasons-game-fixture-e2e',scope:'TEST_FIXTURES_ONLY',content_status:'DRAFT',approved_content_validation:'PENDING',commerce:'HOLD',build_sha:env.BUILD_SHA,bundle_digest:env.BUNDLE_DIGEST});
 if(typeof env.TEST_TOKEN!=='string'||env.TEST_TOKEN.length<32)err(503,'authentication_unconfigured');
 if(req.headers.get('Authorization')!==`Bearer ${env.TEST_TOKEN}`)err(401,'unauthorized');
 if(u.pathname==='/catalog'&&req.method==='GET')return json({scope:'TEST_FIXTURES_ONLY',catalog:bundle.catalog,challenges:bundle.challenges.map(publicChallenge),bundle_digest:env.BUNDLE_DIGEST});
 if(req.method!=='POST')err(404,'not_found');
 const raw=await req.text();if(new TextEncoder().encode(raw).length>16384)err(413,'body_too_large');let body;try{body=JSON.parse(raw)}catch{err(400,'invalid_json')}
 if(u.pathname==='/replay'){
 if(!body||typeof body.receipt_id!=='string'||Object.keys(body).length!==1)err(400,'invalid_replay');
 const row=await env.DB.prepare('SELECT receipt FROM attempts WHERE principal=? AND receipt_id=?').bind('fixture-test-operator',body.receipt_id).first();if(!row)err(404,'receipt_not_found');
 const receipt=JSON.parse(row.receipt),a=receipt.attempt,historical=registry.find(b=>b.digest===a.bundle_digest),c=historical?.bundle.challenges.find(c=>c.id===a.challenge_id&&c.version===a.version);
 return json({receipt_id:receipt.receipt_id,reproduced:!!c&&historical.scorer==='fixture-score-v1'&&await hash(canon(historical.bundle))===a.bundle_digest&&canon(score(c,a.input))===canon(a.result),result:c?score(c,a.input):null});}
 if(u.pathname!=='/attempt')err(404,'not_found');
 if(!body||canon(Object.keys(body).sort())!==canon(['answer','bundle_digest','challenge_id','version'].sort()))err(400,'invalid_attempt_fields');
 const key=req.headers.get('Idempotency-Key');if(!key||! /^[A-Za-z0-9:_-]{1,128}$/.test(key))err(400,'invalid_key');
 if(body.bundle_digest!==env.BUNDLE_DIGEST)err(409,'bundle_mismatch');
 const c=bundle.challenges.find(c=>c.id===body.challenge_id&&c.version===body.version);if(!c)err(400,'unknown_challenge_version');
 const attempt={challenge_id:c.id,version:c.version,bundle_digest:env.BUNDLE_DIGEST,input:body.answer,result:score(c,body.answer)};
 const request=canon(attempt),id=crypto.randomUUID(),receipt={receipt_id:id,attempt};
 // One atomic statement: uniqueness arbitrates concurrent writers. Conflicts never replace original fields.
 const row=await env.DB.prepare(`INSERT INTO attempts(principal,idem_key,request,receipt_id,receipt) VALUES(?,?,?,?,?) ON CONFLICT(principal,idem_key) DO UPDATE SET idem_key=attempts.idem_key RETURNING request,receipt_id,receipt`).bind('fixture-test-operator',key,request,id,canon(receipt)).first();
 if(!row)err(503,'persistence_failed');if(row.request!==request)err(409,'idempotency_conflict');
 return json(JSON.parse(row.receipt),row.receipt_id===id?201:200);
 }catch(e){return json({error:e.status?e.message:'internal_error'},e.status||500)}}};
export {canon,fraction,score,hash,validateBundle};
