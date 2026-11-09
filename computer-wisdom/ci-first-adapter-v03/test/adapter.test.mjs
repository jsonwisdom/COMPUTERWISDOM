import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,openSync,closeSync} from 'node:fs';
import {join} from 'node:path';
import {canonical,hash} from '../src/canonical.mjs';
import {MockProvider,MockAdapter,Breaker} from '../src/adapter.mjs';
import {Journal} from '../src/ledger.mjs';
import {invocationHashes} from '../src/contracts.mjs';
import {rig,makeEnvelope,payload,budget,price,START} from './helpers.mjs';

async function harness(fn,options={}){const h=rig(options);try{await fn(h)}finally{h.cleanup()}}

test('Gate A: model revision remains unverified despite successful mock reconciliation',()=>harness(async({adapter,provider})=>{
 const e=makeEnvelope(1),r=await adapter.call(e,payload);
 assert.equal(r.verdict,'UNKNOWN');assert.equal(r.cost_outcome,'RECONCILED');assert.equal(r.model_revision_verification,'unverified');
 assert.equal(r.model_api_calls,0);assert.equal(provider.calls,1);
 assert.equal(r.response_bytes_sha256.length,64);assert.equal(r.canon,false);assert.equal(r.authority_created,false);
 assert.equal(adapter.journal.events.map(x=>x.type).join(','),'RESERVED,DISPATCHED,RECONCILED');
 assert.equal(adapter.journal.balance().global_remaining_micro_usd,29400);
}));

test('atomic single-writer budget rejects one of two concurrent 18k reservations',()=>harness(async({adapter,provider})=>{
 const results=await Promise.allSettled([adapter.call(makeEnvelope(1),payload),adapter.call(makeEnvelope(2),payload)]);
 assert.equal(results.filter(r=>r.status==='fulfilled').length,1);
 assert.equal(results.filter(r=>r.status==='rejected'&&r.reason.message==='BUDGET_EXHAUSTED').length,1);
 assert.equal(provider.calls,1);
 assert.equal(adapter.journal.events.filter(e=>e.type==='REJECTED').length,1);
}));

test('duplicate idempotency key returns same receipt without a second call',()=>harness(async({adapter,provider})=>{
 const e=makeEnvelope(1),a=await adapter.call(e,payload),b=await adapter.call(e,payload);
 assert.deepEqual(a,b);assert.equal(provider.calls,1);
 await assert.rejects(adapter.call(makeEnvelope(2,{idempotency_key:e.idempotency_key}),payload),/IDEMPOTENCY_CONFLICT/);
}));

test('rejects envelope self-asserted caps, caller, unauthorized power, model tool allowlist',()=>harness(async({adapter,provider})=>{
 await assert.rejects(adapter.call(makeEnvelope(1,{global_cap_micro_usd:999999999}),payload),/BUDGET_CAP_MISMATCH/);
 await assert.rejects(adapter.call(makeEnvelope(1,{caller_identity:'external-owner'}),payload),/AUTHENTICATED_CALLER_MISMATCH/);
 await assert.rejects(adapter.call(makeEnvelope(1,{wallet_signing:true}),payload),/ENVELOPE_AUTHORITY/);
 await assert.rejects(adapter.call(makeEnvelope(1),{...payload,tool_allowlist:['wallet_sign']}),/TOOLS_FORBIDDEN/);
 assert.equal(provider.calls,0);assert.equal(adapter.journal.events.length,0);
}));

test('source prompt, parameters and tool schema digest mismatches block provider',()=>harness(async({adapter,provider})=>{
 await assert.rejects(adapter.call(makeEnvelope(1),{...payload,user_prompt:'changed content'}),/PAYLOAD_HASH_MISMATCH_prompt_sha256/);
 await assert.rejects(adapter.call(makeEnvelope(1),{...payload,parameters:{temperature_decimal:'0.7'}}),/PAYLOAD_HASH_MISMATCH_parameters_sha256/);
 await assert.rejects(adapter.call(makeEnvelope(1),{...payload,tool_schemas:[{name:'read'}]}),/PAYLOAD_HASH_MISMATCH_tool_allowlist_sha256/);
 assert.equal(provider.calls,0);
}));

test('price schedule fails before dispatch when hash differs or effective window expires',()=>harness(async({adapter,provider})=>{
 await assert.rejects(adapter.call(makeEnvelope(1,{price_schedule_sha256:'1'.repeat(64)}),payload),/PRICE_HASH_MISMATCH/);
 assert.equal(provider.calls,0);
}));

test('append failure after RESERVED blocks dispatch and conservatively holds funds',()=>harness(async({adapter,provider})=>{
 const old=adapter.journal.add.bind(adapter.journal);
 adapter.journal.add=function(x){if(x.type==='DISPATCHED')this.failNextAppend=true;return old(x)};
 await assert.rejects(adapter.call(makeEnvelope(1),payload),/INJECTED_LEDGER_APPEND_FAILURE/);
 assert.equal(provider.calls,0);
 assert.equal(adapter.journal.getByKey('idem-mock-1').state,'RESERVED');
 assert.equal(adapter.journal.balance().global_remaining_micro_usd,12000);
}));

test('ambiguous transport result keeps reservation as UNKNOWN_COST even after TTL',()=>harness(async({adapter,provider,setTime})=>{
 provider.mode='error_after_dispatch';const r=await adapter.call(makeEnvelope(1),payload);
 assert.equal(r.verdict,'UNKNOWN');assert.equal(r.cost_outcome,'UNKNOWN_COST');
 setTime('2026-11-08T22:01:00.000Z');
 await assert.rejects(adapter.releaseExpiredUndispatched('idem-mock-1'),/MAY_HAVE_DISPATCHED/);
 assert.equal(adapter.journal.balance().global_remaining_micro_usd,12000);
}));

test('mock authoritative no-match plus expired TTL can release proven non-dispatch only',()=>harness(async({adapter,provider,setTime})=>{
 provider.mode='preflight_denied';const r=await adapter.call(makeEnvelope(1),payload);
 assert.equal(r.cost_outcome,'FAILED_DISPATCH');assert.equal(provider.calls,0);
 await assert.rejects(adapter.releaseExpiredUndispatched('idem-mock-1'),/TTL_NOT_EXPIRED/);
 setTime('2026-11-08T22:01:00.000Z');
 const release=await adapter.releaseExpiredUndispatched('idem-mock-1');
 assert.equal(release.released_micro_usd,18000);
 assert.equal(adapter.journal.balance().global_remaining_micro_usd,30000);
}));

test('revision mismatch and reported endpoint mismatch FAIL without releasing holds',()=>harness(async({adapter,provider})=>{
 provider.reported_revision='wrong-revision';const r=await adapter.call(makeEnvelope(1),payload);
 assert.equal(r.verdict,'FAIL');assert.equal(r.model_revision_verification,'mismatch');
 assert.equal(r.cost_outcome,'RECONCILIATION_FAILED');
 assert.equal(adapter.journal.balance().global_remaining_micro_usd,12000);
}));

test('partial stream, missing usage, price drift all keep cost unresolved',async()=>{
 for (const options of [{stream_completed:false},{response_truncated:true},{mode:'missing_usage'},{mode:'price_changed'},{endpoint:'unexpected-endpoint'}]) {
  await harness(async({adapter,provider})=>{
   const r=await adapter.call(makeEnvelope(1),payload);
   assert.equal(r.cost_outcome,'RECONCILIATION_FAILED');
   assert.equal(r.verdict,options.endpoint?'FAIL':'UNKNOWN');
   assert.equal(adapter.journal.balance().global_remaining_micro_usd,12000);
   assert.equal(provider.calls,1);
  },{provider:new MockProvider(options)});
 }
});

test('per-case hash chain forks detected and externally supplied head checked',()=>harness(async({adapter,dir})=>{
 const a=await adapter.call(makeEnvelope(1),payload);
 const b=await adapter.call(makeEnvelope(2),payload);
 const checkpoint=adapter.journal.checkpoint();
 assert.equal(b.prev_receipt_sha256,a.receipt_sha256);
 assert.equal(adapter.journal.receipts('case-ci-001',checkpoint.case_heads['case-ci-001']).length,2);
 assert.throws(()=>adapter.journal.receipts('case-ci-001','f'.repeat(64)),/EXTERNAL_ANCHOR_MISMATCH/);
 const path=join(dir,'case-case-ci-001.jsonl');const old=readFileSync(path,'utf8');
 writeFileSync(path,old.replace('mock-kimi','model-swapped'), 'utf8');
 assert.throws(()=>adapter.journal.receipts('case-ci-001'),/RECEIPT_CHAIN_BROKEN/);
}));

test('journal is fail-closed across processes and rejects tampered event bytes',()=>harness(async({adapter,dir})=>{
 assert.throws(()=>new Journal({dir,budget}),/EXCLUSIVE_WRITER_LOCK_HELD/);
 await adapter.call(makeEnvelope(1),payload);
 const old=readFileSync(join(dir,'events.jsonl'),'utf8');
 writeFileSync(join(dir,'events.jsonl'),old.replace('RESERVED','RESERVEx'), 'utf8');
 assert.throws(()=>adapter.journal.load(),/LEDGER_CHAIN_BROKEN/);
}));

test('circuit breaker opens, allows a half-open probe, and resets after success',()=>{
 let now=0;
 const b=new Breaker({threshold:2,window_ms:100,open_ms:50,clock:()=>now});
 b.allow();b.failure();now=5;b.allow();b.failure();
 assert.throws(()=>b.allow(),/CIRCUIT_OPEN/);
 now=60;b.allow();assert.throws(()=>b.allow(),/CIRCUIT_HALF_OPEN_BUSY/);b.success();b.allow();
});

test('canonical JSON key order deterministic, fractional floats rejected, zero SHA vector',()=>{
 assert.equal(canonical({b:2,a:1}),canonical({a:1,b:2}));
 assert.equal(hash({b:2,a:1}),hash({a:1,b:2}));
 assert.throws(()=>canonical({temperature:0.7}),/NONCANONICAL_NUMBER/);
 assert.equal(hash({a:1}).length,64);
});

test('schemas require scope boundaries and all are parseable',()=>{
 for(const f of ['invocation','budget','price','receipt']){
   const schema=JSON.parse(readFileSync(new URL(`../schema/${f}.schema.json`,import.meta.url)));
   assert.equal(schema.additionalProperties,false);
   assert.ok(schema.required.length>=10);
 }
 const schema=JSON.parse(readFileSync(new URL('../schema/invocation.schema.json',import.meta.url)));
 for(const field of ['payment','wallet_signing','price_schedule_sha256','idempotency_key','global_cap_micro_usd','caller_identity'])assert.ok(schema.required.includes(field));
});
