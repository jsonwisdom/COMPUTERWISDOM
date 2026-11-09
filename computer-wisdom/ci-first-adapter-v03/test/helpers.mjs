import {mkdtempSync,rmSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {hash} from '../src/canonical.mjs';
import {invocationHashes,CONTRACT_VERSION,ADAPTER_VERSION} from '../src/contracts.mjs';
import {MockAdapter,MockProvider} from '../src/adapter.mjs';
export const budget=JSON.parse(readFileSync(new URL('../fixtures/budget.mock.json',import.meta.url)));
export const price=JSON.parse(readFileSync(new URL('../fixtures/price.mock.json',import.meta.url)));
export const payload={system_prompt:'You verify claims; you do not assert production authority.',user_prompt:'Classify a historical `.io` route as FAIL.',tool_schemas:[],tool_allowlist:[],parameters:{temperature_decimal:'0',max_output_tokens:1000}};
export const START='2026-11-08T22:00:00.000Z';
export function makeEnvelope(n=1,overrides={}) {return {
  contract_version:CONTRACT_VERSION,adapter_version:ADAPTER_VERSION,case_id:'case-ci-001',agent_id:'provenance',invocation_id:'inv-mock-'+n,idempotency_key:'idem-mock-'+n,
  caller_identity:'ci-owner-001',budget_context_id:'budget-mock-001',provider:'mock',model_id:'mock-kimi',model_revision_requested:'revision-pinned-001',endpoint_id:'mock-endpoint-01',
  ...invocationHashes(payload),price_schedule_sha256:hash(price),max_input_tokens:1000,max_output_tokens:1000,global_cap_micro_usd:30000,agent_cap_micro_usd:30000,
  invocation_created_at:START,connect_timeout_ms:1000,first_byte_timeout_ms:2000,total_timeout_ms:3000,reservation_ttl_seconds:15,
  canon:false,authority_created:false,payment:false,wallet_signing:false,...overrides
};}
export function rig({provider=new MockProvider(),now=START,customBudget=budget,customPrice=price,breaker}={}){
 const dir=mkdtempSync(join(tmpdir(),'cw-adapter-test-'));
 let currentTime=now;
 const adapter=new MockAdapter({dir,budget:customBudget,price:customPrice,authenticatedCaller:'ci-owner-001',provider,clock:()=>currentTime,breaker});
 return {adapter,provider,dir,setTime:(x)=>{currentTime=x},cleanup:()=>{adapter.close();rmSync(dir,{recursive:true,force:true})}};
}
