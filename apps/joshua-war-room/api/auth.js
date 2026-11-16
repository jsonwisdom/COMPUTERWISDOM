import {canAuthorize} from "../lib/authority.js";
import {validateReplaySelection} from "../lib/evidence.js";

import { createHmac, randomBytes, timingSafeEqual, createHash } from "node:crypto";
import { verifyMessage, createPublicClient, http } from "viem";
import { base } from "viem/chains";

const OWNER = "0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0";
const SECRET = process.env.JOSHUA_SESSION_SECRET || "";
const baseClient = createPublicClient({chain:base,transport:http("https://mainnet.base.org",{timeout:9000})});
const ttl = 5*60*1000;
const sessionTtl = 30*60*1000;
const digest = (v) => createHash("sha256").update(v).digest("hex");
function hmac(s){return createHmac("sha256", SECRET).update(s).digest("hex");}
function seal(obj){const raw=Buffer.from(JSON.stringify(obj)).toString("base64url");return raw+"."+hmac(raw);}
function unseal(value){
 try {
  if(!value||!SECRET)return null;
  const [raw,mac,...extra] = value.split(".");
  if(extra.length||!raw||!mac||!/^[0-9a-f]{64}$/.test(mac))return null;
  const a=Buffer.from(mac,"hex"), b=Buffer.from(hmac(raw),"hex");
  if(a.length!==b.length||!timingSafeEqual(a,b))return null;
  return JSON.parse(Buffer.from(raw,"base64url").toString("utf8"));
 }catch{return null;}
}
function cookies(req){
 const out={};for(const part of (req.headers.cookie||"").split(";")){const i=part.indexOf("=");if(i>0)out[part.slice(0,i).trim()]=part.slice(i+1).trim();}
 return out;
}
const cookie = (name,value,age)=>name+"="+value+"; Path=/; Max-Age="+age+"; HttpOnly; Secure; SameSite=Strict";
const json=(res,status,data)=>res.status(status).json(data);
function messageFor(p){
 return [
 p.host+" wants you to sign in with your Ethereum account:",
 OWNER,
 "",
 "JOSHUA WAR ROOM: Prove control of Computer Wisdom PC. No payment, deployment, transfer, or contract execution.",
 "",
 "URI: https://"+p.host,
 "Version: 1",
 "Chain ID: 8453",
 "Nonce: "+p.nonce,
 "Issued At: "+p.issuedAt,
 "Expiration Time: "+p.expirationTime
 ].join("\n");
}
function originValid(req,host){
 const origin=req.headers.origin;
 return typeof origin==="string"&&origin==="https://"+host;
}
const validAddress=(v)=>typeof v==="string"&&/^0x[a-fA-F0-9]{40}$/.test(v)&&v.toLowerCase()===OWNER.toLowerCase();
export default async function handler(req,res){
 res.setHeader("Cache-Control","no-store, private");
 res.setHeader("X-Content-Type-Options","nosniff");
 res.setHeader("Vary","Cookie, Origin");
 const mode=(req.query&&req.query.mode)||new URL(req.url,"https://example.invalid").searchParams.get("mode");
 const host=(req.headers.host||"").toLowerCase();
 if(!SECRET || SECRET.length<32)return json(res,503,{error:"Wallet authentication not configured."});
 if(!/^[a-z0-9.-]+(?::[0-9]+)?$/.test(host))return json(res,400,{error:"Invalid host"});
 if(mode==="session"&&req.method==="GET"){
   const session=unseal(cookies(req).joshua_session);
   if(!canAuthorize(session,host))return json(res,200,{authenticated:false});
   return json(res,200,{authenticated:true,address:session.address,verifiedAt:session.verifiedAt,expiresAt:session.expiresAt,proofDigest:session.proofDigest,verification:session.verification,chainId:8453});
 }
 if(!["challenge","verify","logout","attest"].includes(mode)||req.method!=="POST")return json(res,405,{error:"Method not allowed"});
 if(!originValid(req,host))return json(res,403,{error:"Origin verification failed."});
 if(mode==="logout"){
  res.setHeader("Set-Cookie",[cookie("joshua_session","",0),cookie("joshua_challenge","",0)]);
  return json(res,200,{authenticated:false});
 }

 if(mode==="attest"){
  const session=unseal(cookies(req).joshua_session);
  if(!canAuthorize(session,host))return json(res,403,{error:"OWNER_DENIED: valid Computer Wisdom PC session required."});
  const input=req.body&&typeof req.body==="object"?req.body:{};
  if(input.action!=="attest-replay"||!input.replay||typeof input.replay!=="object")
   return json(res,400,{error:"Only attest-replay is authorized."});
  const raw=JSON.stringify(input.replay);
  if(raw.length>20000)return json(res,413,{error:"Replay too large."});
  const selected=validateReplaySelection(input.replay,input.source,input.sourceDigest);
  if(!selected.ok)return json(res,422,{error:"Replay selection rejected: "+selected.reason});
  const verified=selected.rules;
  const replayDigest=digest(JSON.stringify(input.replay.state.history)+"|"+JSON.stringify(verified.final));
  const issuedAt=new Date().toISOString();
  const witness={case:"CW-JOSHUA-STACK-001",action:"attest-replay",address:session.address,sessionProofDigest:session.proofDigest,
   source:selected.source,sourceDigest:selected.sourceDigest,replayDigest,turns:verified.turns,final:verified.final,issuedAt,
   scope:"Server-validated explicitly selected replay under a wallet-authenticated session. Archive source digest pins exact uploaded file bytes. NOT a wallet signature over game turns, original-action proof, durable record, or public digital signature."};
  return json(res,200,{authorized:true,attested:true,receipt:witness,serverMac:seal({kind:"rules-attestation-v1",...witness})});
 }
 const body=req.body&&typeof req.body==="object"?req.body:{};
 if(!validAddress(body.address))return json(res,403,{error:"Select Computer Wisdom PC; a different wallet cannot sign in."});
 if(mode==="challenge"){
  const issued=Date.now(), exp=issued+ttl;
  const p={address:OWNER,host,nonce:randomBytes(16).toString("hex"),issuedAt:new Date(issued).toISOString(),expirationTime:new Date(exp).toISOString(),expiresAt:exp};
  res.setHeader("Set-Cookie",cookie("joshua_challenge",seal(p),300));
  return json(res,200,{message:messageFor(p),expiresAt:exp,chainId:8453});
 }
 if(typeof body.signature!=="string"||!/^0x[0-9a-fA-F]+$/.test(body.signature)||body.signature.length>8192)return json(res,400,{error:"Invalid signature format."});
 if(typeof body.message!=="string"||body.message.length>2048)return json(res,400,{error:"Invalid message."});
 const p=unseal(cookies(req).joshua_challenge);
 if(!p||p.expiresAt<Date.now()||p.host!==host||!validAddress(p.address)||body.message!==messageFor(p)){
  return json(res,403,{error:"Challenge missing, expired, or mismatched. Connect and sign again."});
 }
 let verified=false,verification="unknown";
 try { verified=await verifyMessage({address:OWNER,message:body.message,signature:body.signature}); if(verified)verification="EIP-191 EOA";}
 catch{}
 if(!verified){
  try{verified=await baseClient.verifyMessage({address:OWNER,message:body.message,signature:body.signature}); if(verified)verification="Base wallet (EIP-1271/6492 compatible)";}catch{}
 }
 if(!verified)return json(res,401,{error:"Signature did not verify for Computer Wisdom PC."});
 const now=Date.now(), proofDigest=digest(body.message+"\n"+body.signature);
 const session={address:OWNER,host,verifiedAt:new Date(now).toISOString(),expiresAt:now+sessionTtl,proofDigest,verification};
 res.setHeader("Set-Cookie",[cookie("joshua_challenge","",0),cookie("joshua_session",seal(session),1800)]);
 return json(res,200,{authenticated:true,address:OWNER,verifiedAt:session.verifiedAt,expiresAt:session.expiresAt,proofDigest,verification,chainId:8453});
}
