import {
  generateRegistrationOptions, verifyRegistrationResponse,
  generateAuthenticationOptions, verifyAuthenticationResponse
} from '@simplewebauthn/server';

const enc = new TextEncoder();
const b64url = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const bytes = n => crypto.getRandomValues(new Uint8Array(n));
const sha256 = async s => b64url(new Uint8Array(await crypto.subtle.digest('SHA-256',enc.encode(s))));
const now = () => Math.floor(Date.now()/1000);
const ttl = 180; // one-time challenge
// Build 012: a secondary-enrollment grant is short-lived, single-use, and bound to one session.
const enrollGrantTtl = 120;
// Build 012: Blue (primary) + Purple (independent recovery). Raising this is a separate decision.
const MAX_CREDENTIALS = 2;
const USER_ID = 'jason-workdesk-owner';
const json = (data,status=200,extra={}) => new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store',...extra}});
const denied = () => json({error:'DENIED'},403);
const noStore = {'cache-control':'no-store','x-content-type-options':'nosniff','referrer-policy':'no-referrer'};
const cookie = request => (request.headers.get('cookie')||'').match(/(?:^|;\s*)wd_session=([^;]+)/)?.[1];
async function storedCredentials(db) {
 const {results} = await db.prepare('SELECT id,public_key,counter,transports,label FROM credentials ORDER BY created_at,id').all();
 return results.map(c=>({...c,transports:JSON.parse(c.transports)}));
}
async function challenge(db,purpose,value,{sessionHash=null,authorizedBy=null,lifetime=ttl}={}) {
 const id=b64url(bytes(24));
 await db.prepare('INSERT INTO challenges(id,challenge,purpose,expires_at,session_hash,authorized_by) VALUES(?,?,?,?,?,?)')
  .bind(id,value,purpose,now()+lifetime,sessionHash,authorizedBy).run();
 return id;
}
// Single use: the row is deleted whether or not the ceremony later verifies.
async function consume(db,id,purpose) {
 if(typeof id!=='string')return null;
 return await db.prepare('DELETE FROM challenges WHERE id=? AND purpose=? AND expires_at>? RETURNING challenge,session_hash,authorized_by').bind(id,purpose,now()).first();
}
async function parse(request) {
 if((Number(request.headers.get('content-length')||0)>32768))throw Error('too big');
 const body=await request.text();if(body.length>32768)throw Error('too big');
 return JSON.parse(body);
}
// Returns the active session (hash + credential that created it) or null.
async function activeSession(db,request) {
 const token=cookie(request);
 if(!token)return null;
 const hash=await sha256(token);
 return await db.prepare('SELECT token_hash,credential_id FROM sessions WHERE token_hash=? AND expires_at>?').bind(hash,now()).first();
}
// Verifies a WebAuthn assertion against the one stored credential it names, then advances that
// credential's own counter atomically. Each credential is checked independently.
async function verifyAssertion(env,db,credentials,body,expectedChallenge) {
 const c=credentials.find(x=>x.id===body.response?.id);
 if(!c)return null;
 const check=await verifyAuthenticationResponse({
  response:body.response,expectedChallenge,expectedOrigin:env.EXPECTED_ORIGIN,
  expectedRPID:env.RP_ID,requireUserVerification:true,
  credential:{id:c.id,publicKey:new Uint8Array(c.public_key),counter:c.counter,transports:c.transports}
 });
 if(!check.verified)return null;
 // Atomically advance the authenticator counter, refusing stale or concurrent assertions.
 const oldCounter=c.counter;
 const newCounter=check.authenticationInfo.newCounter;
 if(oldCounter!==0 && newCounter!==0 && newCounter<=oldCounter)return null;
 const updated=await db.prepare('UPDATE credentials SET counter=?,last_used_at=? WHERE id=? AND counter=?')
   .bind(newCounter,now(),c.id,oldCounter).run();
 if(updated.meta.changes!==1)return null;
 return c;
}
const registrationOptions = (env,credentials) => generateRegistrationOptions({
 rpName:'Computer Wisdom Workdesk',rpID:env.RP_ID,userName:'owner',
 userID:enc.encode(USER_ID),attestationType:'none',
 authenticatorSelection:{residentKey:'preferred',userVerification:'required'},
 // Duplicate rejection, client side: the browser refuses an authenticator already holding one of these.
 excludeCredentials:credentials.map(c=>({id:c.id,transports:c.transports})),
 supportedAlgorithmIDs:[-7]
});
const event = (db,kind,credentialId,actor) => db.prepare('INSERT INTO credential_events(at,event,credential_id,actor) VALUES(?,?,?,?)').bind(now(),kind,credentialId,actor).run();
export default {
 async fetch(request,env) {
  const url=new URL(request.url);
  const origin=request.headers.get('origin');
  const headers={...noStore,'access-control-allow-origin':env.EXPECTED_ORIGIN,'access-control-allow-credentials':'true','vary':'Origin'};
  // Never grant browser-facing APIs access from an unconfigured or mismatched host.
  if(url.hostname!=='auth.jsonwisdom.com' && !url.hostname.endsWith('.workers.dev') && url.hostname!=='localhost' && url.hostname!=='127.0.0.1')return denied();
  if(origin && origin!==env.EXPECTED_ORIGIN)return denied();
  // Browser writes must declare the configured first-party origin; reject opaque POSTs.
  if(request.method==='POST' && origin!==env.EXPECTED_ORIGIN)return denied();
  if(request.method==='OPTIONS')return origin===env.EXPECTED_ORIGIN
   ? new Response(null,{status:204,headers:{...headers,'access-control-allow-methods':'POST, GET','access-control-allow-headers':'Content-Type, X-Bootstrap-Token'}})
   : denied();
  if(!env.AUTH_DB||!env.RP_ID||!env.EXPECTED_ORIGIN)return json({error:'NOT_CONFIGURED'},503,headers);
  if(url.pathname==='/health' && request.method==='GET')return json({configured:true,authenticated:false},200,headers);
  try {
   const db=env.AUTH_DB, credentials=await storedCredentials(db);
   if(url.pathname==='/register/options' && request.method==='POST') {
    // Initial (Blue/primary) enrollment only. Bootstrap secret must be supplied out of band; never embedded in a web page.
    // Once any key is enrolled, further keys use /enroll/authorize/* (fresh assertion from an enrolled key).
    if(credentials.length)return json({error:'ENROLLED_USE_AUTHORIZED_ENROLLMENT'},403,headers);
    if(!env.BOOTSTRAP_TOKEN||request.headers.get('x-bootstrap-token')!==env.BOOTSTRAP_TOKEN)return denied();
    const options=await registrationOptions(env,credentials);
    const id=await challenge(db,'register',options.challenge);
    return json({challengeId:id,options},200,headers);
   }
   if(url.pathname==='/enroll/authorize/options' && request.method==='POST') {
    // Step 1 of secondary enrollment: requires a live session AND a fresh UV assertion (step 2).
    const session=await activeSession(db,request);
    if(!session||!credentials.length)return denied();
    if(credentials.length>=MAX_CREDENTIALS)return json({error:'CREDENTIAL_LIMIT'},409,headers);
    const options=await generateAuthenticationOptions({
     rpID:env.RP_ID,userVerification:'required',
     allowCredentials:credentials.map(c=>({id:c.id,transports:c.transports}))
    });
    const id=await challenge(db,'enroll_auth',options.challenge,{sessionHash:session.token_hash});
    return json({challengeId:id,options},200,headers);
   }
   if(url.pathname==='/enroll/authorize/verify' && request.method==='POST') {
    const session=await activeSession(db,request);
    if(!session)return denied();
    const body=await parse(request);
    const grant=await consume(db,body.challengeId,'enroll_auth');
    if(!grant||grant.session_hash!==session.token_hash)return denied();
    const authorizer=await verifyAssertion(env,db,credentials,body,grant.challenge);
    if(!authorizer)return denied();
    if(credentials.length>=MAX_CREDENTIALS)return json({error:'CREDENTIAL_LIMIT'},409,headers);
    const options=await registrationOptions(env,credentials);
    const id=await challenge(db,'register_secondary',options.challenge,{sessionHash:session.token_hash,authorizedBy:authorizer.id,lifetime:enrollGrantTtl});
    return json({challengeId:id,options,authorizedBy:authorizer.label,expiresIn:enrollGrantTtl},200,headers);
   }
   if(url.pathname==='/register/verify' && request.method==='POST') {
    const body=await parse(request);
    let grant=null, session=null;
    if(!credentials.length) {
     // Bootstrap path, unchanged from Build 011: empty table + out-of-band bootstrap secret.
     if(!env.BOOTSTRAP_TOKEN||request.headers.get('x-bootstrap-token')!==env.BOOTSTRAP_TOKEN)return denied();
     grant=await consume(db,body.challengeId,'register');
    } else {
     // Secondary path: only a grant minted by a fresh assertion, for this same session.
     session=await activeSession(db,request);
     if(!session)return denied();
     grant=await consume(db,body.challengeId,'register_secondary');
     if(grant&&(grant.session_hash!==session.token_hash||!grant.authorized_by))grant=null;
    }
    if(!grant)return denied();
    const check=await verifyRegistrationResponse({
     response:body.response,expectedChallenge:grant.challenge,expectedOrigin:env.EXPECTED_ORIGIN,
     expectedRPID:env.RP_ID,requireUserVerification:true
    });
    if(!check.verified||!check.registrationInfo)return denied();
    const {credential,aaguid}=check.registrationInfo;
    // Duplicate rejection, server side (also enforced by the primary key).
    if(credentials.some(c=>c.id===credential.id))return json({error:'DUPLICATE_CREDENTIAL'},409,headers);
    const row=[credential.id,credential.publicKey,credential.counter,JSON.stringify(credential.transports||[]),now(),aaguid||null];
    let inserted, label='primary';
    if(!session) {
     // Enrollment can succeed once, even under competing requests.
     inserted=await db.prepare("INSERT INTO credentials(id,public_key,counter,transports,created_at,aaguid,label,enrolled_by) SELECT ?,?,?,?,?,?,'primary','bootstrap' WHERE NOT EXISTS (SELECT 1 FROM credentials)")
      .bind(...row).run();
    } else {
     label=credentials.some(c=>c.label==='primary')?'recovery':'primary';
     // Atomic: the authorizing key must still exist, the new id must be new, and the cap must hold.
     inserted=await db.prepare('INSERT INTO credentials(id,public_key,counter,transports,created_at,aaguid,label,enrolled_by) SELECT ?,?,?,?,?,?,?,? WHERE EXISTS (SELECT 1 FROM credentials WHERE id=?) AND NOT EXISTS (SELECT 1 FROM credentials WHERE id=?) AND (SELECT COUNT(*) FROM credentials)<?')
      .bind(...row,label,grant.authorized_by,grant.authorized_by,credential.id,MAX_CREDENTIALS).run();
    }
    if(inserted.meta.changes!==1)return denied();
    await event(db,'enrolled',credential.id,session?grant.authorized_by:'bootstrap');
    return json({enrolled:true,label},200,headers);
   }
   if(url.pathname==='/login/options' && request.method==='POST') {
    if(!credentials.length)return json({error:'NO_ENROLLED_KEY'},503,headers);
    const options=await generateAuthenticationOptions({
     rpID:env.RP_ID,userVerification:'required',
     allowCredentials:credentials.map(c=>({id:c.id,transports:c.transports}))
    });
    const id=await challenge(db,'login',options.challenge);
    return json({challengeId:id,options},200,headers);
   }
   if(url.pathname==='/login/verify' && request.method==='POST') {
    const body=await parse(request);
    const grant=await consume(db,body.challengeId,'login');
    if(!grant)return denied();
    const c=await verifyAssertion(env,db,credentials,body,grant.challenge);
    if(!c)return denied();
    const token=b64url(bytes(32)),expiry=now()+900;
    await db.prepare('INSERT INTO sessions(token_hash,expires_at,credential_id) VALUES(?,?,?)').bind(await sha256(token),expiry,c.id).run();
    return json({authenticated:true,sessionExpiresIn:900,credential:c.label},200,{
     ...headers,'set-cookie':`wd_session=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=900`
    });
   }
   if(url.pathname==='/credentials' && request.method==='GET') {
    const session=await activeSession(db,request);
    if(!session)return denied();
    const {results}=await db.prepare('SELECT id,label,transports,aaguid,created_at,last_used_at FROM credentials ORDER BY label,created_at,id').all();
    return json({credentials:results.map(r=>({...r,transports:JSON.parse(r.transports),current:r.id===session.credential_id}))},200,headers);
   }
   if(url.pathname==='/credentials/remove/options' && request.method==='POST') {
    // Removal step 1: live session required; issues a single-use, session-bound, target-bound assertion challenge.
    const session=await activeSession(db,request);
    if(!session)return denied();
    const body=await parse(request);
    if(typeof body.credentialId!=='string'||!credentials.some(c=>c.id===body.credentialId))return denied();
    if(credentials.length<2)return json({error:'LAST_CREDENTIAL_PROTECTED'},409,headers);
    const options=await generateAuthenticationOptions({
     rpID:env.RP_ID,userVerification:'required',
     allowCredentials:credentials.map(c=>({id:c.id,transports:c.transports}))
    });
    const id=await challenge(db,'remove_auth',options.challenge,{sessionHash:session.token_hash,authorizedBy:body.credentialId,lifetime:enrollGrantTtl});
    return json({challengeId:id,options,expiresIn:enrollGrantTtl},200,headers);
   }
   if(url.pathname==='/credentials/remove' && request.method==='POST') {
    // Removal step 2: session AND a fresh user-verified assertion from ANY enrolled key (including the key
    // being removed), for the exact target named at step 1. The last key can never be removed.
    const session=await activeSession(db,request);
    if(!session)return denied();
    const body=await parse(request);
    if(typeof body.credentialId!=='string')return denied();
    const grant=await consume(db,body.challengeId,'remove_auth');
    if(!grant||grant.session_hash!==session.token_hash||grant.authorized_by!==body.credentialId)return denied();
    const asserter=await verifyAssertion(env,db,credentials,body,grant.challenge);
    if(!asserter)return denied();
    // Last-credential protection is enforced inside the same statement, so concurrent removals cannot reach zero.
    const removed=await db.prepare('DELETE FROM credentials WHERE id=? AND (SELECT COUNT(*) FROM credentials)>1').bind(body.credentialId).run();
    if(removed.meta.changes!==1) {
     const exists=credentials.some(c=>c.id===body.credentialId);
     return exists?json({error:'LAST_CREDENTIAL_PROTECTED'},409,headers):denied();
    }
    // Sessions created by the removed key end with it.
    await db.prepare('DELETE FROM sessions WHERE credential_id=?').bind(body.credentialId).run();
    await event(db,'removed',body.credentialId,asserter.id);
    return json({removed:true,verifiedBy:asserter.label},200,headers);
   }
   if((url.pathname==='/private' || url.pathname==='/wallet/readiness') && request.method==='GET') {
    const session=await activeSession(db,request);
    if(!session)return denied();
    if(url.pathname==='/wallet/readiness')return json({ownerAuthenticated:true,chain:'eip155:8453',mode:'READ_ONLY',walletConnected:false,signingEnabled:false,paymentsEnabled:false,authority:'separate in-wallet human confirmation required',next:'Connect wallet client-side only after an approved signed transaction-review build.'},200,headers);
    return new Response('<!doctype html><meta charset="utf-8"><title>Private Workdesk</title><h1>Jason Workdesk</h1><p>Authenticated session. Wallet signing and x402 payments remain disabled.</p><p>Read-only wallet readiness is exposed at /wallet/readiness only to authenticated sessions.</p>',{
     headers:{...headers,'content-type':'text/html; charset=utf-8','content-security-policy':"default-src 'none'; style-src 'unsafe-inline'",'vary':'Origin, Cookie'}
    });
   }
   if(url.pathname==='/logout' && request.method==='POST') {
    const token=cookie(request);
    if(token)await db.prepare('DELETE FROM sessions WHERE token_hash=?').bind(await sha256(token)).run();
    return json({loggedOut:true},200,{...headers,'set-cookie':'wd_session=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0'});
   }
   return json({error:'NOT_FOUND'},404,headers);
  } catch(e) {
   // No internals or cryptographic detail in publicly visible errors.
   return json({error:'DENIED_OR_UNAVAILABLE'},403,headers);
  }
 }
};
