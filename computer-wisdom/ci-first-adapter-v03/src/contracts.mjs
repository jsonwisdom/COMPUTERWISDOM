import { insist, ID, HEX64, hash, decimalMicroUSD } from './canonical.mjs';
export const CONTRACT_VERSION = 'computerwisdom.ci-first.adapter.v0.3';
export const ADAPTER_VERSION = '0.3.0-mock';
export const STATES = Object.freeze(['RESERVED','DISPATCHED','RECONCILED','REJECTED','EXPIRED_UNDISPATCHED','UNKNOWN_COST','FAILED_DISPATCH','RECONCILIATION_FAILED']);
const requireKeys=(object,names,reason)=>{
  insist(object && Object.getPrototypeOf(object)===Object.prototype,reason);
  insist(Object.keys(object).length===names.length && names.every(k=>Object.hasOwn(object,k)),reason);
};
export function validateBudgetRecord(b) {
  insist(b?.schema === 'computerwisdom.ci-first.budget.v0.3', 'BUDGET_SCHEMA');
  requireKeys(b,['schema','budget_context_id','owner','authorized_callers','global_cap_micro_usd','agent_caps_micro_usd','created_at','expires_at','authorization','authority_created'],'BUDGET_FIELDS');
  insist(ID.test(b.budget_context_id) && ID.test(b.owner) && Array.isArray(b.authorized_callers), 'BUDGET_IDENTITY');
  insist(b.authorized_callers.every(x => ID.test(x)), 'BUDGET_AUTHORIZATION');
  insist(Number.isSafeInteger(b.global_cap_micro_usd) && b.global_cap_micro_usd >= 0, 'BUDGET_CAP');
  insist(b.agent_caps_micro_usd && typeof b.agent_caps_micro_usd === 'object', 'BUDGET_AGENT_CAPS');
  for (const cap of Object.values(b.agent_caps_micro_usd)) insist(Number.isSafeInteger(cap) && cap >= 0, 'BUDGET_AGENT_CAP');
  insist(Date.parse(b.expires_at) > Date.parse(b.created_at), 'BUDGET_EXPIRY');
  insist(b.authorization === 'MOCK_FIXTURE_ONLY' && b.authority_created === false, 'BUDGET_AUTHORITY');
  return b;
}
export function validatePrice(p) {
  insist(p?.schema === 'computerwisdom.ci-first.price.v0.3', 'PRICE_SCHEMA');
  requireKeys(p,['schema','currency','unit','input_usd_per_1k','output_usd_per_1k','cached_input_usd_per_1k','effective_from','effective_to','source_url','fetched_at','fetched_by','fetch_method'],'PRICE_FIELDS');
  insist(p.currency === 'USD' && p.unit === 'per_1000_tokens', 'PRICE_UNIT');
  for (const x of ['input_usd_per_1k','output_usd_per_1k','cached_input_usd_per_1k']) decimalMicroUSD(p[x]);
  insist(typeof p.source_url === 'string' && p.source_url.startsWith('https://'), 'PRICE_SOURCE');
  insist(Date.parse(p.effective_to) > Date.parse(p.effective_from), 'PRICE_WINDOW');
  insist(Date.parse(p.fetched_at) >= Date.parse(p.effective_from), 'PRICE_FETCHED_AT');
  insist(typeof p.fetched_by === 'string' && typeof p.fetch_method === 'string', 'PRICE_FETCH_PROVENANCE');
  return p;
}
export function validateEnvelope(e, { budget, price, authenticatedCaller, nowISO }) {
  insist(e?.contract_version === CONTRACT_VERSION && e.adapter_version === ADAPTER_VERSION, 'ENVELOPE_VERSION');
  requireKeys(e,['contract_version','adapter_version','case_id','agent_id','invocation_id','idempotency_key','caller_identity','budget_context_id','provider','model_id','model_revision_requested','endpoint_id','prompt_sha256','parameters_sha256','tool_allowlist_sha256','price_schedule_sha256','max_input_tokens','max_output_tokens','global_cap_micro_usd','agent_cap_micro_usd','invocation_created_at','connect_timeout_ms','first_byte_timeout_ms','total_timeout_ms','reservation_ttl_seconds','canon','authority_created','payment','wallet_signing'],'ENVELOPE_EXTRA_OR_MISSING_FIELDS');
  insist(e.provider === 'mock', 'PAID_PROVIDER_FORBIDDEN');
  for(const name of ['invocation_id','idempotency_key','case_id','agent_id','budget_context_id','provider','model_id','model_revision_requested','endpoint_id']) insist(ID.test(e[name]||''), 'ENVELOPE_FIELD_'+name);
  for(const name of ['prompt_sha256','parameters_sha256','tool_allowlist_sha256','price_schedule_sha256']) insist(HEX64.test(e[name]||''), 'ENVELOPE_HASH_'+name);
  insist(e.canon === false && e.authority_created === false && e.payment === false && e.wallet_signing === false, 'ENVELOPE_AUTHORITY');
  insist(e.caller_identity === authenticatedCaller && budget.owner === authenticatedCaller && budget.authorized_callers.includes(authenticatedCaller), 'AUTHENTICATED_CALLER_MISMATCH');
  insist(e.budget_context_id === budget.budget_context_id, 'BUDGET_CONTEXT_MISMATCH');
  insist(e.global_cap_micro_usd === budget.global_cap_micro_usd && e.agent_cap_micro_usd === budget.agent_caps_micro_usd[e.agent_id], 'BUDGET_CAP_MISMATCH');
  insist(Date.parse(nowISO) < Date.parse(budget.expires_at), 'BUDGET_EXPIRED');
  insist(Number.isSafeInteger(e.max_input_tokens) && e.max_input_tokens > 0 && Number.isSafeInteger(e.max_output_tokens) && e.max_output_tokens > 0, 'TOKEN_LIMIT');
  insist(e.max_input_tokens <= 200000 && e.max_output_tokens <= 64000, 'TOKEN_CEILING');
  for(const n of ['connect_timeout_ms','first_byte_timeout_ms','total_timeout_ms','reservation_ttl_seconds']) insist(Number.isSafeInteger(e[n]) && e[n] > 0, 'TIMEOUT_'+n);
  insist(e.connect_timeout_ms <= e.first_byte_timeout_ms && e.first_byte_timeout_ms <= e.total_timeout_ms && e.total_timeout_ms <= 120000, 'TIMEOUT_ORDER');
  insist(e.reservation_ttl_seconds >= Math.ceil(e.total_timeout_ms/1000), 'RESERVATION_TTL_TOO_SHORT');
  insist(e.price_schedule_sha256 === hash(price), 'PRICE_HASH_MISMATCH');
  insist(Date.parse(nowISO) >= Date.parse(price.effective_from) && Date.parse(nowISO) < Date.parse(price.effective_to), 'PRICE_EXPIRED');
  insist(Date.parse(price.fetched_at) <= Date.parse(nowISO) && Date.parse(nowISO)-Date.parse(price.fetched_at) <= 24*3600*1000, 'PRICE_FETCH_STALE');
  insist(Date.parse(e.invocation_created_at) <= Date.parse(nowISO), 'INVOCATION_FROM_FUTURE');
  insist(e.caller_identity && e.tool_allowlist_sha256 && e.canon === false, 'ENVELOPE_GUARD');
  return e;
}
export function invocationHashes({system_prompt,user_prompt,tool_schemas,tool_allowlist,parameters}) {
  insist(Array.isArray(tool_schemas) && Array.isArray(tool_allowlist) && !tool_allowlist.some(x=>/wallet|payment|sign|shell|exec/i.test(x)), 'TOOLS_FORBIDDEN');
  insist(typeof system_prompt==='string' && typeof user_prompt==='string','PROMPT_FORMAT');
  return {prompt_sha256:hash({system_prompt,user_prompt}),parameters_sha256:hash(parameters),tool_allowlist_sha256:hash({tool_schemas,tool_allowlist:[...tool_allowlist].sort()})};
}
