import {createHash} from 'node:crypto';
export const ROLES = Object.freeze(['intake','provenance','mathematics','contradiction','safety','replay','synthesis','supervisor']);
export const sha256 = (x) => createHash('sha256').update(typeof x === 'string' ? Buffer.from(x,'utf8') : x).digest('hex');
export function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(k=>`${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
}
export const digest = (value) => sha256(canonical(value));
export const assert = (ok,reason) => {if(!ok)throw new Error(reason)};
export function inputContract(c) {
  assert(c && typeof c==='object' && c.schema==='computerwisdom.ci-first.case.v1','SCHEMA_UNKNOWN');
  assert(/^[a-z0-9][a-z0-9._-]{2,79}$/.test(c.case_id||''),'BAD_CASE_ID');
  assert(c.mode==='offline_fixture','OFFLINE_ONLY_NO_EXTERNAL_RUNTIME');
  assert(c.canon===false && c.authority_created===false,'AUTHORITY_BOUNDARY');
  assert(Array.isArray(c.evidence)&&Array.isArray(c.claims),'BAD_DATA');
  assert(c.evidence.length<=100&&c.claims.length<=100,'MAX_RECORDS');
  assert(new Set(c.evidence.map(x=>x.id)).size===c.evidence.length,'DUPLICATE_EVIDENCE');
  assert(new Set(c.claims.map(x=>x.id)).size===c.claims.length,'DUPLICATE_CLAIM');
  return c;
}
export function verifiedSource(e) {
  const fields=typeof e.id==='string' && typeof e.uri==='string' && typeof e.content==='string' &&
    /^[a-f0-9]{64}$/.test(e.sha256||'') && e.kind==='historical_fixture';
  if(!fields)return {id:e.id||'invalid',verdict:'FAIL',reason:'SOURCE_CONTRACT'};
  return {id:e.id,verdict:sha256(e.content)===e.sha256?'PASS':'FAIL',reason:sha256(e.content)===e.sha256?'BYTES_MATCH':'SHA256_MISMATCH',authenticity:'UNKNOWN',scope:'HISTORICAL_FIXTURE_ONLY'};
}
export function handoff(role, status, verdict, sources, findings, memory_updates={facts:[],decisions:[],open_questions:[]}) {
  assert(ROLES.includes(role),'UNKNOWN_AGENT_ROLE');
  assert(['done','failed','partial'].includes(status),'BAD_HANDOFF_STATUS');
  assert(['PASS','FAIL','UNKNOWN'].includes(verdict),'BAD_VERDICT');
  assert(Array.isArray(sources)&&Array.isArray(findings),'BAD_HANDOFF_LIST');
  for(const k of ['facts','decisions','open_questions'])assert(Array.isArray(memory_updates[k]),'MEMORY_SCHEMA_'+k);
  for(const record of memory_updates.facts)assert(typeof record.source_id==='string','UNSOURCED_FACT');
  for(const record of memory_updates.decisions)assert(typeof record.rationale==='string','UNREASONED_DECISION');
  const out={schema:'computerwisdom.ci-first.handoff.v1',agent:role,status,verdict,confidence:verdict==='UNKNOWN'?0:1,sources:[...new Set(sources)].sort(),findings,memory_updates,canon:false,authority_created:false};
  return {...out,sha256:digest(out)};
}
export function verifyHandoff(h,role) {
  assert(h.agent===role && h.schema==='computerwisdom.ci-first.handoff.v1','INVALID_AGENT_HANDOFF');
  const {sha256:hash,...body}=h;
  assert(digest(body)===hash,'HANDOFF_DIGEST_MISMATCH_'+role);
  assert(h.canon===false && h.authority_created===false,'HANDOFF_AUTHORITY');
  assert(['PASS','FAIL','UNKNOWN'].includes(h.verdict),'HANDOFF_VERDICT');
  return true;
}
export function combine(verdicts) {
  return verdicts.includes('FAIL')?'FAIL':verdicts.includes('UNKNOWN')?'UNKNOWN':'PASS';
}
