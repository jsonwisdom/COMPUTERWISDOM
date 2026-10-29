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
const json = (data,status=200,extra={}) => new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store',...extra}});
const denied = () => json({error:'DENIED'},403);
const noStore = {'cache-control':'no-store','x-content-type-options':'nosniff','referrer-policy':'no-referrer'};
const cookie = request => (request.headers.get('cookie')||'').match(/(?:^|;\s*)wd_session=([^;]+)/)?.[1];
async function storedCredentials(db) {
 const {results} = await db.prepare('SELECT id,public_key,counter,transports FROM credentials').all();
 return results.map(c=>({...c,transports:JSON.parse(c.transports)}));
}
async function challenge(db,purpose,value) {
 const id=b64url(bytes(24));
 await db.prepare('INSERT INTO challenges(id,challenge,purpose,expires_at) VALUES(?,?,?,?)').bind(id,value,purpose,now()+ttl).run();
 return id;
}
async function consume(db,id,purpose) {
 const c=await db.prepare('DELETE FROM challenges WHERE id=? AND purpose=? AND expires_at>? RETURNING challenge').bind(id,purpose,now()).first();
 return c?.challenge||null;
}
async function parse(request) {
 if((Number(request.headers.get('content-length')||0)>32768))throw Error('too big');
 const body=await request.text();if(body.length>32768)throw Error('too big');
 return JSON.parse(body);
}
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
    // Initial enrollment only. Bootstrap secret must be supplied out of band; never embedded in a web page.
    if(credentials.length||!env.BOOTSTRAP_TOKEN||request.headers.get('x-bootstrap-token')!==env.BOOTSTRAP_TOKEN)return denied();
    const options=await generateRegistrationOptions({
     rpName:'Computer Wisdom Workdesk',rpID:env.RP_ID,userName:'owner',
     userID:enc.encode('jason-workdesk-owner'),attestationType:'none',
     authenticatorSelection:{residentKey:'preferred',userVerification:'required'},
     supportedAlgorithmIDs:[-7]
    });
    const id=await challenge(db,'register',options.challenge);
    return json({challengeId:id,options},200,headers);
   }
   if(url.pathname==='/register/verify' && request.method==='POST') {
    if(credentials.length||!env.BOOTSTRAP_TOKEN||request.headers.get('x-bootstrap-token')!==env.BOOTSTRAP_TOKEN)return denied();
    const body=await parse(request);
    const expectedChallenge=await consume(db,body.challengeId,'register');
    if(!expectedChallenge)return denied();
    const check=await verifyRegistrationResponse({
     response:body.response,expectedChallenge,expectedOrigin:env.EXPECTED_ORIGIN,
     expectedRPID:env.RP_ID,requireUserVerification:true
    });
    if(!check.verified||!check.registrationInfo)return denied();
    const {credential}=check.registrationInfo;
    // Enrollment can succeed once, even under competing requests.
    const inserted=await db.prepare('INSERT INTO credentials(id,public_key,counter,transports,created_at) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM credentials)')
      .bind(credential.id,credential.publicKey,credential.counter,JSON.stringify(credential.transports||[]),now()).run();
    if(inserted.meta.changes!==1)return denied();
    return json({enrolled:true},200,headers);
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
    const expectedChallenge=await consume(db,body.challengeId,'login');
    if(!expectedChallenge)return denied();
    const c=credentials.find(x=>x.id===body.response?.id);
    if(!c)return denied();
    const check=await verifyAuthenticationResponse({
     response:body.response,expectedChallenge,expectedOrigin:env.EXPECTED_ORIGIN,
     expectedRPID:env.RP_ID,requireUserVerification:true,
     credential:{id:c.id,publicKey:new Uint8Array(c.public_key),counter:c.counter,transports:c.transports}
    });
    if(!check.verified)return denied();
    // Atomically advance the authenticator counter, refusing stale or concurrent assertions.
    const oldCounter=c.counter;
    const newCounter=check.authenticationInfo.newCounter;
    if(oldCounter!==0 && newCounter!==0 && newCounter<=oldCounter)return denied();
    const updated=await db.prepare('UPDATE credentials SET counter=? WHERE id=? AND counter=?')
      .bind(newCounter,c.id,oldCounter).run();
    if(updated.meta.changes!==1)return denied();
    const token=b64url(bytes(32)),expiry=now()+900;
    await db.prepare('INSERT INTO sessions(token_hash,expires_at) VALUES(?,?)').bind(await sha256(token),expiry).run();
    return json({authenticated:true,sessionExpiresIn:900},200,{
     ...headers,'set-cookie':`wd_session=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=900`
    });
   }
   if((url.pathname==='/private' || url.pathname==='/wallet/readiness') && request.method==='GET') {
    const token=cookie(request);
    if(!token)return denied();
    const session=await db.prepare('SELECT token_hash FROM sessions WHERE token_hash=? AND expires_at>?').bind(await sha256(token),now()).first();
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
