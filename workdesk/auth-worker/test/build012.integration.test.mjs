// Build 012 dual-key enrollment tests. Local Miniflare D1 only (persist:false, no remote bindings).
// Blue and Purple are synthetic software authenticators, never real YubiKeys.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {randomBytes} from 'node:crypto';
import {getPlatformProxy} from 'wrangler';
import worker from '../src/index.js';
import {SoftAuthenticator} from './softauthn.mjs';

const ORIGIN='https://jsonwisdom.com';
const proxy=await getPlatformProxy({configPath:new URL('./wrangler.test.toml',import.meta.url).pathname,persist:false});
const db=proxy.env.AUTH_DB;
const BOOT='synthetic-bootstrap-'+randomBytes(16).toString('hex');
const env={AUTH_DB:db,RP_ID:'jsonwisdom.com',EXPECTED_ORIGIN:ORIGIN,BOOTSTRAP_TOKEN:BOOT};
test.after(()=>proxy.dispose());

const stmts=sql=>sql.split(';').map(s=>s.replace(/--.*$/gm,'').trim()).filter(Boolean);
async function applySql(file){for(const s of stmts(readFileSync(new URL(file,import.meta.url),'utf8')))await db.prepare(s).run();}
async function fresh(schema='../schema.sql'){
 for(const t of ['credentials','challenges','sessions','credential_events'])await db.prepare('DROP TABLE IF EXISTS '+t).run();
 await applySql(schema);
}
async function call(path,{method='POST',body,headers={},session,origin=ORIGIN}={}){
 const h={...headers};if(origin)h.origin=origin;if(session)h.cookie='wd_session='+session;
 if(body!==undefined)h['content-type']='application/json';
 const r=await worker.fetch(new Request('https://auth.jsonwisdom.com'+path,{method,headers:h,body:body===undefined?undefined:JSON.stringify(body)}),env);
 const text=await r.text();let data;try{data=JSON.parse(text)}catch{data=text}
 return {status:r.status,data,cookie:(r.headers.get('set-cookie')||'').match(/wd_session=([^;]*)/)?.[1]};
}
async function bootstrap(key){
 const o=await call('/register/options',{headers:{'x-bootstrap-token':BOOT}});
 assert.equal(o.status,200);
 return call('/register/verify',{headers:{'x-bootstrap-token':BOOT},body:{challengeId:o.data.challengeId,response:key.create(o.data.options,{origin:ORIGIN})}});
}
async function login(key,opts={}){
 const o=await call('/login/options');
 assert.equal(o.status,200);
 const r=await call('/login/verify',{body:{challengeId:o.data.challengeId,response:key.get(o.data.options,{origin:ORIGIN,...opts})}});
 return {...r,options:o.data.options};
}
async function grant(signer,session,opts={}){
 const o=await call('/enroll/authorize/options',{session});
 if(o.status!==200)return o;
 return call('/enroll/authorize/verify',{session,body:{challengeId:o.data.challengeId,response:signer.get(o.data.options,{origin:ORIGIN,...opts})}});
}
// Removal: step-up assertion (any enrolled key) bound to session + target, then remove.
async function removeKey(signer,session,credentialId,opts={}){
 const o=await call('/credentials/remove/options',{session,body:{credentialId}});
 if(o.status!==200)return o;
 return call('/credentials/remove',{session,body:{credentialId,challengeId:o.data.challengeId,response:signer.get(o.data.options,{origin:ORIGIN,...opts})}});
}
const enroll=(key,g,session,opts={})=>call('/register/verify',{session,body:{challengeId:g.data.challengeId,response:key.create(g.data.options,{origin:ORIGIN,...opts})}});
const rows=async()=>(await db.prepare('SELECT id,label,counter,aaguid,transports,enrolled_by FROM credentials ORDER BY label,created_at,id').all()).results;
async function bluePlusPurple(){
 await fresh();const blue=new SoftAuthenticator('Blue'),purple=new SoftAuthenticator('Purple');
 assert.equal((await bootstrap(blue)).status,200);
 const s=(await login(blue)).cookie;const g=await grant(blue,s);assert.equal(g.status,200);
 assert.equal((await enroll(purple,g,s)).status,200);
 return {blue,purple};
}

test('T01 empty table: Blue bootstrap enrollment succeeds as primary with key metadata',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue');
 const r=await bootstrap(blue);
 assert.equal(r.status,200);assert.deepEqual(r.data,{enrolled:true,label:'primary'});
 const [row]=await rows();
 assert.equal(row.id,blue.id);assert.equal(row.label,'primary');assert.equal(row.enrolled_by,'bootstrap');
 assert.equal(row.aaguid.replace(/-/g,''),blue.aaguid.toString('hex'));assert.deepEqual(JSON.parse(row.transports),['usb','nfc']);
});
test('T02 bootstrap protection preserved: missing or wrong bootstrap secret denied on empty table',async()=>{
 await fresh();
 assert.equal((await call('/register/options')).status,403);
 assert.equal((await call('/register/options',{headers:{'x-bootstrap-token':'wrong'}})).status,403);
 const o=await call('/register/options',{headers:{'x-bootstrap-token':BOOT}});
 const r=await call('/register/verify',{body:{challengeId:o.data.challengeId,response:new SoftAuthenticator('x').create(o.data.options,{origin:ORIGIN})}});
 assert.equal(r.status,403);assert.equal((await rows()).length,0);
});
test('T03 nonempty table: bootstrap path closed even with the valid bootstrap secret (root-cause behaviour kept for bootstrap only)',async()=>{
 await fresh();await bootstrap(new SoftAuthenticator('Blue'));
 const o=await call('/register/options',{headers:{'x-bootstrap-token':BOOT}});
 assert.equal(o.status,403);assert.equal(o.data.error,'ENROLLED_USE_AUTHORIZED_ENROLLMENT');
});
test('T04 nonempty table: Purple rejected without secondary authorization',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue'),purple=new SoftAuthenticator('Purple');await bootstrap(blue);
 assert.equal((await call('/enroll/authorize/options')).status,403,'no session');
 const s=(await login(blue)).cookie;
 // A session alone is not enough: an assertion challenge or login challenge is not an enrollment grant.
 const a=await call('/enroll/authorize/options',{session:s});
 const fake={data:{challengeId:a.data.challengeId,options:{challenge:a.data.options.challenge,rp:{id:'jsonwisdom.com'}}}};
 assert.equal((await enroll(purple,fake,s)).status,403,'assertion challenge reused as grant');
 const l=await call('/login/options');
 assert.equal((await enroll(purple,{data:{challengeId:l.data.challengeId,options:{challenge:l.data.options.challenge,rp:{id:'jsonwisdom.com'}}}},s)).status,403,'login challenge as grant');
 assert.equal((await enroll(purple,{data:{challengeId:'nope',options:{challenge:'AAAA',rp:{id:'jsonwisdom.com'}}}},undefined,{})).status,403,'no session, bootstrap-less');
 assert.equal((await rows()).length,1);
});
test('T05 Purple accepted with fresh UV assertion from Blue; labelled recovery; excludeCredentials lists Blue',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue'),purple=new SoftAuthenticator('Purple');await bootstrap(blue);
 const s=(await login(blue)).cookie;const g=await grant(blue,s);
 assert.equal(g.status,200);assert.equal(g.data.authorizedBy,'primary');assert.equal(g.data.expiresIn,120);
 assert.deepEqual(g.data.options.excludeCredentials.map(x=>x.id),[blue.id]);
 assert.equal(g.data.options.authenticatorSelection.userVerification,'required');
 const r=await enroll(purple,g,s);
 assert.equal(r.status,200);assert.deepEqual(r.data,{enrolled:true,label:'recovery'});
 const rs=await rows();assert.deepEqual(rs.map(x=>[x.id,x.label,x.enrolled_by]),[[blue.id,'primary','bootstrap'],[purple.id,'recovery',blue.id]]);
 const ev=(await db.prepare('SELECT event,credential_id,actor FROM credential_events ORDER BY seq').all()).results;
 assert.deepEqual(ev.map(e=>[e.event,e.credential_id,e.actor]),[['enrolled',blue.id,'bootstrap'],['enrolled',purple.id,blue.id]]);
});
test('T06 forged authorization assertions rejected (wrong key, UV absent, wrong origin, wrong RP)',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue'),mallory=new SoftAuthenticator('Mallory');await bootstrap(blue);
 const s=(await login(blue)).cookie;
 assert.equal((await grant(blue,s,{signWith:mallory})).status,403,'signature from unenrolled key under Blue id');
 assert.equal((await grant(mallory,s)).status,403,'unknown credential');
 assert.equal((await grant(blue,s,{uv:false})).status,403,'user verification flag missing');
 assert.equal((await grant(blue,s,{origin:'https://evil.example'})).status,403,'wrong origin in clientData');
 assert.equal((await grant(blue,s,{rpId:'evil.example'})).status,403,'wrong RP ID hash');
 assert.equal((await db.prepare("SELECT COUNT(*) n FROM challenges WHERE purpose='register_secondary'").first()).n,0);
});
test('T07 expired enrollment grant rejected',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue');await bootstrap(blue);
 const s=(await login(blue)).cookie;const g=await grant(blue,s);assert.equal(g.status,200);
 await db.prepare('UPDATE challenges SET expires_at=expires_at-121 WHERE id=?').bind(g.data.challengeId).run();
 assert.equal((await enroll(new SoftAuthenticator('Purple'),g,s)).status,403);
});
test('T08 expired authorization challenge rejected',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue');await bootstrap(blue);
 const s=(await login(blue)).cookie;const o=await call('/enroll/authorize/options',{session:s});
 await db.prepare('UPDATE challenges SET expires_at=expires_at-181 WHERE id=?').bind(o.data.challengeId).run();
 assert.equal((await call('/enroll/authorize/verify',{session:s,body:{challengeId:o.data.challengeId,response:blue.get(o.data.options,{origin:ORIGIN})}})).status,403);
});
test('T09 replay rejected: authorization assertion and enrollment grant are single use',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue'),purple=new SoftAuthenticator('Purple');await bootstrap(blue);
 const s=(await login(blue)).cookie;const o=await call('/enroll/authorize/options',{session:s});
 const body={challengeId:o.data.challengeId,response:blue.get(o.data.options,{origin:ORIGIN})};
 const g=await call('/enroll/authorize/verify',{session:s,body});assert.equal(g.status,200);
 assert.equal((await call('/enroll/authorize/verify',{session:s,body})).status,403,'assertion replay');
 const attestation=purple.create(g.data.options,{origin:ORIGIN});
 assert.equal((await call('/register/verify',{session:s,body:{challengeId:g.data.challengeId,response:attestation}})).status,200);
 assert.equal((await removeKey(blue,s,purple.id)).status,200);
 assert.equal((await call('/register/verify',{session:s,body:{challengeId:g.data.challengeId,response:attestation}})).status,403,'grant replay after removal');
 assert.equal((await rows()).length,1);
});
test('T10 grant is bound to the session that produced the assertion',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue');await bootstrap(blue);
 const s1=(await login(blue)).cookie,s2=(await login(blue)).cookie;
 const g=await grant(blue,s1);assert.equal(g.status,200);
 assert.equal((await enroll(new SoftAuthenticator('Purple'),g,s2)).status,403,'other session');
 const o=await call('/enroll/authorize/options',{session:s1});
 assert.equal((await call('/enroll/authorize/verify',{session:s2,body:{challengeId:o.data.challengeId,response:blue.get(o.data.options,{origin:ORIGIN})}})).status,403,'assertion under other session');
 await call('/logout',{session:s1});
 const g2=await grant(blue,s2);await call('/logout',{session:s2});
 assert.equal((await enroll(new SoftAuthenticator('Purple'),g2,s2)).status,403,'logged-out session');
});
test('T11 duplicate rejected: re-enrolling Blue credential id under a valid grant',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue');await bootstrap(blue);
 const s=(await login(blue)).cookie;const g=await grant(blue,s);
 const r=await enroll(blue,g,s);
 assert.equal(r.status,409);assert.equal(r.data.error,'DUPLICATE_CREDENTIAL');assert.equal((await rows()).length,1);
});
test('T12 same-model authenticators (shared AAGUID) are both accepted; credential limit 2 enforced',async()=>{
 await fresh();const aaguid=randomBytes(16);
 const blue=new SoftAuthenticator('Blue',{aaguid}),purple=new SoftAuthenticator('Purple',{aaguid});
 await bootstrap(blue);const s=(await login(blue)).cookie;
 assert.equal((await enroll(purple,await grant(blue,s),s)).status,200);
 const third=await grant(blue,s);assert.equal(third.status,409);assert.equal(third.data.error,'CREDENTIAL_LIMIT');
});
test('T13 concurrent grants cannot exceed the limit',async()=>{
 await fresh();const blue=new SoftAuthenticator('Blue');await bootstrap(blue);
 const s=(await login(blue)).cookie;const g1=await grant(blue,s),g2=await grant(blue,s);
 const res=await Promise.all([enroll(new SoftAuthenticator('P1'),g1,s),enroll(new SoftAuthenticator('P2'),g2,s)]);
 assert.deepEqual(res.map(r=>r.status).sort(),[200,403]);assert.equal((await rows()).length,2);
});
test('T14 Blue and Purple authenticate independently; each verified only against its own key',async()=>{
 const {blue,purple}=await bluePlusPurple();
 const b=await login(blue);assert.equal(b.status,200);assert.equal(b.data.credential,'primary');
 assert.deepEqual(b.options.allowCredentials.map(x=>x.id).sort(),[blue.id,purple.id].sort());
 const p=await login(purple);assert.equal(p.status,200);assert.equal(p.data.credential,'recovery');
 assert.equal((await call('/private',{method:'GET',session:p.cookie,origin:null})).status,200);
 assert.equal((await login(purple,{asId:blue.id})).status,403,'Purple signature presented as Blue');
 assert.equal((await login(blue,{asId:purple.id})).status,403,'Blue signature presented as Purple');
 const list=await call('/credentials',{method:'GET',session:p.cookie,origin:null});
 assert.deepEqual(list.data.credentials.map(c=>[c.label,c.current]),[['primary',false],['recovery',true]]);
 assert.ok(!JSON.stringify(list.data).includes('public_key'));
});
test('T15 counter regression rejected per credential, without affecting the other key',async()=>{
 const {blue,purple}=await bluePlusPurple();
 for(let i=0;i<3;i++)assert.equal((await login(blue)).status,200);
 const c=(await rows()).find(r=>r.id===blue.id).counter;assert.ok(c>0);
 assert.equal((await login(blue,{counter:c})).status,403,'equal counter');
 assert.equal((await login(blue,{counter:c-1})).status,403,'lower counter');
 assert.equal((await login(blue,{counter:0})).status,403,'counter reset to zero');
 assert.equal((await login(purple)).status,200,'Purple unaffected');
 assert.equal((await login(blue)).status,200,'Blue continues with higher counter');
});
test('T16 removal: requires session; one key removable; last key refused; removed key sessions revoked',async()=>{
 const {blue,purple}=await bluePlusPurple();
 assert.equal((await call('/credentials/remove/options',{body:{credentialId:purple.id}})).status,403,'no session');
 const pS=(await login(purple)).cookie,bS=(await login(blue)).cookie;
 const r=await removeKey(blue,bS,purple.id);
 assert.equal(r.status,200);
 assert.equal((await call('/private',{method:'GET',session:pS,origin:null})).status,403,'Purple session revoked');
 assert.equal((await login(purple)).status,403,'Purple no longer authenticates');
 const last=await call('/credentials/remove/options',{session:bS,body:{credentialId:blue.id}});
 assert.equal(last.status,409);assert.equal(last.data.error,'LAST_CREDENTIAL_PROTECTED');
 assert.equal((await login(blue)).status,200);
});
test('T17 concurrent removal of both keys leaves exactly one',async()=>{
 const {blue,purple}=await bluePlusPurple();const s=(await login(blue)).cookie;
 const res=await Promise.all([removeKey(blue,s,purple.id),removeKey(purple,s,blue.id)]);
 assert.deepEqual(res.map(r=>r.status).sort(),[200,409]);assert.equal((await rows()).length,1);
});
test('T18 recovery: lost Blue removed using Purple; Purple then authorizes a replacement primary',async()=>{
 const {blue,purple}=await bluePlusPurple();const s=(await login(purple)).cookie;
 assert.equal((await removeKey(purple,s,blue.id)).status,200);
 assert.equal((await login(blue)).status,403);
 const s2=(await login(purple)).cookie;const replacement=new SoftAuthenticator('Blue-2');
 const r=await enroll(replacement,await grant(purple,s2),s2);
 assert.equal(r.status,200);assert.equal(r.data.label,'primary');
 assert.equal((await login(replacement)).status,200);
});
test('T19 existing recovery method preserved: bootstrap re-enrollment still works if the table is empty',async()=>{
 await fresh();const k=new SoftAuthenticator('Blue');
 assert.equal((await bootstrap(k)).status,200);assert.equal((await login(k)).status,200);
});
test('T20 login stays separate from wallet authority',async()=>{
 const {purple}=await bluePlusPurple();const s=(await login(purple)).cookie;
 const w=await call('/wallet/readiness',{method:'GET',session:s,origin:null});
 assert.equal(w.status,200);assert.equal(w.data.signingEnabled,false);assert.equal(w.data.paymentsEnabled,false);
 for(const p of ['/wallet/sign','/wallet/send','/x402/pay'])assert.equal((await call(p,{session:s})).status,404);
});
test('T21 migration 0002 on a Build 011 database preserves the enrolled key, then enables Purple',async()=>{
 await fresh('./schema.build011.sql');
 const blue=new SoftAuthenticator('Blue');
 // Simulate a Build 011 enrollment row (Build 011 code is not loaded here).
 const reg=blue.create({challenge:'AAAA',rp:{id:'jsonwisdom.com'}},{origin:ORIGIN});
 const {verifyRegistrationResponse}=await import('@simplewebauthn/server');
 const v=await verifyRegistrationResponse({response:reg,expectedChallenge:'AAAA',expectedOrigin:ORIGIN,expectedRPID:'jsonwisdom.com',requireUserVerification:true});
 await db.prepare('INSERT INTO credentials(id,public_key,counter,transports,created_at) VALUES(?,?,?,?,?)').bind(v.registrationInfo.credential.id,v.registrationInfo.credential.publicKey,0,'["usb"]',1).run();
 await db.prepare('INSERT INTO sessions(token_hash,expires_at) VALUES(?,?)').bind('legacy',9999999999).run();
 await applySql('../migrations/0002_build012_dual_key.sql');
 const [row]=await rows();assert.equal(row.id,blue.id);assert.equal(row.label,'primary');
 assert.equal((await db.prepare('SELECT COUNT(*) n FROM sessions').first()).n,1,'sessions preserved');
 const s=(await login(blue)).cookie;assert.ok(s);
 assert.equal((await enroll(new SoftAuthenticator('Purple'),await grant(blue,s),s)).status,200);
});

// ---- Step 1 hardening: fresh hardware-key verification for removal ----
test('T22 removal without a fresh assertion is refused (session alone not enough)',async()=>{
 const {blue,purple}=await bluePlusPurple();const s=(await login(blue)).cookie;
 assert.equal((await call('/credentials/remove',{session:s,body:{credentialId:purple.id}})).status,403,'no challenge, no assertion');
 const o=await call('/credentials/remove/options',{session:s,body:{credentialId:purple.id}});
 assert.equal((await call('/credentials/remove',{session:s,body:{credentialId:purple.id,challengeId:o.data.challengeId}})).status,403,'challenge but no assertion');
 assert.equal((await rows()).length,2);
});
test('T23 stale (expired) removal challenge refused',async()=>{
 const {blue,purple}=await bluePlusPurple();const s=(await login(blue)).cookie;
 const o=await call('/credentials/remove/options',{session:s,body:{credentialId:purple.id}});
 assert.equal(o.data.expiresIn,120);
 await db.prepare('UPDATE challenges SET expires_at=expires_at-121 WHERE id=?').bind(o.data.challengeId).run();
 assert.equal((await call('/credentials/remove',{session:s,body:{credentialId:purple.id,challengeId:o.data.challengeId,response:blue.get(o.data.options,{origin:ORIGIN})}})).status,403);
 assert.equal((await rows()).length,2);
});
test('T24 replayed removal assertion refused',async()=>{
 const aaguid=randomBytes(16);await fresh();
 const blue=new SoftAuthenticator('Blue',{aaguid}),purple=new SoftAuthenticator('Purple',{aaguid});
 await bootstrap(blue);let s=(await login(blue)).cookie;await enroll(purple,await grant(blue,s),s);
 s=(await login(blue)).cookie;
 const o=await call('/credentials/remove/options',{session:s,body:{credentialId:purple.id}});
 const body={credentialId:purple.id,challengeId:o.data.challengeId,response:blue.get(o.data.options,{origin:ORIGIN})};
 assert.equal((await call('/credentials/remove',{session:s,body})).status,200);
 // Re-enroll Purple, then replay the captured removal request.
 assert.equal((await enroll(purple,await grant(blue,s),s)).status,200);
 assert.equal((await call('/credentials/remove',{session:s,body})).status,403,'replay');
 assert.equal((await rows()).length,2);
});
test('T25 foreign-session and retargeted removal challenges refused',async()=>{
 const {blue,purple}=await bluePlusPurple();
 const s1=(await login(blue)).cookie,s2=(await login(blue)).cookie;
 const o=await call('/credentials/remove/options',{session:s1,body:{credentialId:purple.id}});
 assert.equal((await call('/credentials/remove',{session:s2,body:{credentialId:purple.id,challengeId:o.data.challengeId,response:blue.get(o.data.options,{origin:ORIGIN})}})).status,403,'other session');
 const o2=await call('/credentials/remove/options',{session:s1,body:{credentialId:purple.id}});
 assert.equal((await call('/credentials/remove',{session:s1,body:{credentialId:blue.id,challengeId:o2.data.challengeId,response:purple.get(o2.data.options,{origin:ORIGIN})}})).status,403,'target swapped after challenge');
 assert.equal((await call('/credentials/remove/options',{session:s1,body:{credentialId:'not-enrolled'}})).status,403,'unknown target');
 assert.equal((await rows()).length,2);
});
test('T26 removal assertion with UV missing, forged signature, or wrong origin refused',async()=>{
 const {blue,purple}=await bluePlusPurple();const s=(await login(blue)).cookie;const mallory=new SoftAuthenticator('Mallory');
 assert.equal((await removeKey(blue,s,purple.id,{uv:false})).status,403,'UV missing');
 assert.equal((await removeKey(blue,s,purple.id,{signWith:mallory})).status,403,'forged signature');
 assert.equal((await removeKey(mallory,s,purple.id)).status,403,'unenrolled key');
 assert.equal((await removeKey(blue,s,purple.id,{origin:'https://evil.example'})).status,403,'wrong origin');
 assert.equal((await rows()).length,2);
});
test('T27 valid removal: any enrolled key may verify, including the key being removed; never the last',async()=>{
 let {blue,purple}=await bluePlusPurple();let s=(await login(blue)).cookie;
 const self=await removeKey(purple,s,purple.id);
 assert.equal(self.status,200);assert.equal(self.data.verifiedBy,'recovery');
 const ev=(await db.prepare("SELECT credential_id,actor FROM credential_events WHERE event='removed'").all()).results;
 assert.deepEqual(ev.map(e=>[e.credential_id,e.actor]),[[purple.id,purple.id]]);
 const last=await call('/credentials/remove/options',{session:s,body:{credentialId:blue.id}});
 assert.equal(last.status,409);assert.equal(last.data.error,'LAST_CREDENTIAL_PROTECTED');
 assert.equal((await login(blue)).status,200);
});
