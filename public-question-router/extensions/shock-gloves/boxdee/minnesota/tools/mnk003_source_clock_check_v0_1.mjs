// CI-FIRST Minnesota MNK-003: source-grounded clock candidate checks.
// Offline/read-only. Hash equality is byte consistency, not origin authentication.
import {createHash} from 'node:crypto';

export const CLOCKS=Object.freeze([
 'event_time','document_time','publication_time',
 'effective_time','update_time','retrieval_time'
]);
const FORMAT=/^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])T([01]\d|2[0-3]):[0-5]\d:[0-5]\dZ$/;
function parsed(value){
 if(typeof value!=='string'||!FORMAT.test(value))return null;
 const t=Date.parse(value);
 return Number.isFinite(t)&&new Date(t).toISOString().replace('.000Z','Z')===value?t:null;
}
export function checkMnk003Candidate(packet,sourceText){
 const out={
  gate:'MNK-003',classification:'READ_ONLY_CLOCK_CANDIDATE',
  status:'HOLD',gate_exercised:false,coverage_increment:0,
  authority_created:false,legal_finding_created:false,
  wrongdoing_finding_created:false,proof_admission:false,
  primary_source_authenticated:false,issues:[],
  source_bytes_sha256:null,original_clocks:{},comparisons:[]
 };
 if(!packet||typeof packet!=='object'||packet.gate!=='MNK-003'){
  out.issues.push('MISSING_OR_WRONG_GATE');return out;
 }
 if(packet.jurisdiction!=='Minnesota')out.issues.push('JURISDICTION_UNBOUND');
 if(typeof packet.source_url!=='string'||!/^https:\/\//.test(packet.source_url))
  out.issues.push('SOURCE_URL_UNBOUND');
 if(typeof sourceText!=='string'||!sourceText.length){
  out.issues.push('SOURCE_BYTES_UNAVAILABLE');return out;
 }
 out.source_bytes_sha256=createHash('sha256').update(sourceText,'utf8').digest('hex');
 if(packet.expected_source_sha256!==out.source_bytes_sha256)
  out.issues.push('SOURCE_BYTES_HASH_MISMATCH');
 const clocks=packet.clocks||{};
 for(const key of CLOCKS){
  const item=clocks[key];
  if(!item||typeof item!=='object'){
   out.original_clocks[key]='UNKNOWN';
   out.issues.push('CLOCK_UNBOUND:'+key);
   continue;
  }
  out.original_clocks[key]=item.value??'UNKNOWN';
  if(parsed(item.value)===null)out.issues.push('CLOCK_INVALID_OR_UNBOUND:'+key);
  if(typeof item.quote!=='string'||!item.quote.trim()||!sourceText.includes(item.quote))
   out.issues.push('CLOCK_QUOTE_UNANCHORED:'+key);
  if(typeof item.locator!=='string'||!item.locator.trim())
   out.issues.push('CLOCK_LOCATOR_UNBOUND:'+key);
 }
 if(!Array.isArray(packet.comparisons)||!packet.comparisons.length)
  out.issues.push('NO_SEMANTIC_COMPARISON_RULE');
 for(const rule of (Array.isArray(packet.comparisons)?packet.comparisons:[])){
  if(!CLOCKS.includes(rule?.before)||!CLOCKS.includes(rule?.after)||
     rule.before===rule.after||typeof rule.reason!=='string'||!rule.reason.trim()){
   out.issues.push('INVALID_COMPARISON_RULE');continue;
  }
  const left=parsed(clocks[rule.before]?.value),right=parsed(clocks[rule.after]?.value);
  const check=left===null||right===null?'UNKNOWN':
   left>right?'INVERSION_CANDIDATE':'ORDER_COMPATIBLE';
  out.comparisons.push({before:rule.before,after:rule.after,reason:rule.reason,check});
 }
 if(out.comparisons.some(c=>c.check==='INVERSION_CANDIDATE'))
  out.issues.push('CLOCK_CONFLICT_CANDIDATE_NEEDS_CONTEXT');
 out.issues.push('INDEPENDENT_SOURCE_PROVENANCE_AND_REVIEW_UNBOUND');
 return out;
}
