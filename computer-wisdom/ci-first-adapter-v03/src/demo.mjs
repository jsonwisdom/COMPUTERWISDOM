import {mkdtempSync, readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {MockAdapter, MockProvider} from './adapter.mjs';
import {hash} from './canonical.mjs';
import {invocationHashes,CONTRACT_VERSION,ADAPTER_VERSION} from './contracts.mjs';
const budget=JSON.parse(readFileSync(new URL('../fixtures/budget.mock.json',import.meta.url)));
const price=JSON.parse(readFileSync(new URL('../fixtures/price.mock.json',import.meta.url)));
const payload={system_prompt:'CI-FIRST',user_prompt:'Classify missing live proof.',tool_schemas:[],tool_allowlist:[],parameters:{temperature_decimal:'0'}};
const now='2026-11-08T22:00:00.000Z';
const e={contract_version:CONTRACT_VERSION,adapter_version:ADAPTER_VERSION,case_id:'case-ci-demo',agent_id:'provenance',invocation_id:'inv-demo-001',idempotency_key:'idem-demo-001',caller_identity:'ci-owner-001',budget_context_id:budget.budget_context_id,provider:'mock',model_id:'mock-kimi',model_revision_requested:'revision-pinned-001',endpoint_id:'mock-endpoint-01',...invocationHashes(payload),price_schedule_sha256:hash(price),max_input_tokens:1000,max_output_tokens:1000,global_cap_micro_usd:budget.global_cap_micro_usd,agent_cap_micro_usd:budget.agent_caps_micro_usd.provenance,invocation_created_at:now,connect_timeout_ms:1000,first_byte_timeout_ms:2000,total_timeout_ms:3000,reservation_ttl_seconds:15,canon:false,authority_created:false,payment:false,wallet_signing:false};
const root=mkdtempSync(join(tmpdir(),'cw-v03-demo-'));
const a=new MockAdapter({dir:root,budget,price,authenticatedCaller:'ci-owner-001',provider:new MockProvider(),clock:()=>now});
try{
 const receipt=await a.call(e,payload);
 const checkpoint=a.journal.checkpoint();
 const output=process.env.CW_CI_OUTPUT_DIR??'ci-first-artifacts';mkdirSync(output,{recursive:true});
 writeFileSync(join(output,'mock-adapter-receipt.json'),JSON.stringify(receipt,null,2)+'\n');
 writeFileSync(join(output,'mock-ledger-checkpoint.json'),JSON.stringify(checkpoint,null,2)+'\n');
 console.log(JSON.stringify({receipt_sha256:receipt.receipt_sha256,checkpoint_sha256:checkpoint.checkpoint_sha256,verdict:receipt.verdict,cost_outcome:receipt.cost_outcome,model_api_calls:0,scope:'MOCK_ONLY'}));
}finally{a.close();}
