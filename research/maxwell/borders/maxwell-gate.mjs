// Computer Wisdom: Maxwell's Demon MN Border v1
// Only manually provided public educational records; never fetch or publish.
export const BORDER = Object.freeze({
 id:"MAXWELL_DEMON_MN_BORDER_V1",scope:"US-MN-EDUCATION",
 mode:"MANUAL_READ_ONLY_SANDBOX",maxBatch:50,maxBytes:32768,maxHops:0,
 network:false,crawler:false,cron:false,write:false,publish:false,
 wallet:false,payment:false,authority:false,humanReview:true
});
const encode=new TextEncoder();
const status=(state,reason)=>({state,reason,authority_created:false,escalation:false});
const hex=bytes=>Array.from(bytes,x=>x.toString(16).padStart(2,"0")).join("");
export async function inspectOne(x) {
 if(!x||typeof x!=="object"||Array.isArray(x))return status("REJECT","BAD_INPUT");
 if(x.scope!==BORDER.scope)return status("REJECT","OUT_OF_SCOPE");
 if(x.private||x.classified||x.contains_pii||x.credential||x.action||x.execute)return status("REJECT","RESTRICTED_DATA_OR_ACTION");
 if(!["public_record","classroom_fixture","lesson"].includes(x.kind))return status("REJECT","RECORD_CLASS");
 if(typeof x.claim!=="string"||!x.claim.trim())return status("HOLD","MISSING_QUESTION");
 if(x.claim.length>2000)return status("REJECT","CLAIM_SIZE");
 if(typeof x.source_uri!=="string"||typeof x.source_text!=="string"||typeof x.observed_at!=="string"||typeof x.sha256!=="string")return status("HOLD","SOURCE_BYTES_TIMESTAMP_DIGEST_REQUIRED");
 let u;try{u=new URL(x.source_uri)}catch{return status("REJECT","SOURCE_URL")}
 if(u.protocol!=="https:"||u.username||u.password)return status("REJECT","HTTPS_ONLY_NO_CREDENTIALS");
 if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(x.observed_at)||!Number.isFinite(Date.parse(x.observed_at)))return status("REJECT","TIMESTAMP");
 if(!/^[0-9a-f]{64}$/.test(x.sha256))return status("REJECT","SHA256_FORMAT");
 const bytes=encode.encode(x.source_text);
 if(bytes.length>BORDER.maxBytes)return status("REJECT","BYTE_BUDGET");
 const digest=hex(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)));
 if(digest!==x.sha256)return {...status("CONFLICT","DIGEST_MISMATCH"),claimed_sha256:x.sha256,actual_sha256:digest};
 return {...status("BOUND_READ_ONLY","INPUT_BYTE_MATCH_ONLY"),source_uri:x.source_uri,observed_at:x.observed_at,sha256:digest,bytes:bytes.length,source_authenticated:false,meaning_authenticated:false,next:"INDEPENDENT_REPLAY_AND_HUMAN_REVIEW"};
}
export async function inspectBatch(records){
 if(!Array.isArray(records)||records.length>BORDER.maxBatch)return {state:"REJECT",reason:"BATCH_LIMIT",results:[],authority_created:false};
 const results=[];
 for(const record of records)results.push(await inspectOne(record));
 return {schema:BORDER.id,state:BORDER.mode,count:results.length,results,external_calls:0,writes:0,authority_created:false};
}
export function shannonBits(p){
 if(!Array.isArray(p)||!p.length||p.some(x=>!Number.isFinite(x)||x<0||x>1)||Math.abs(p.reduce((a,b)=>a+b,0)-1)>1e-10)throw Error("INVALID_DISTRIBUTION");
 return -p.reduce((a,x)=>a+(x?x*Math.log2(x):0),0);
}
