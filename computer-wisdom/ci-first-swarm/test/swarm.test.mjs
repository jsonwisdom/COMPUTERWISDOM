import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runSwarm,verifyReceipt} from '../src/swarm.mjs';
import {sha256} from '../src/contracts.mjs';
const fixture=JSON.parse(readFileSync(new URL('../fixtures/io-worker-separation.json',import.meta.url),'utf8'));
test('eight real role handlers, two-stage synthesis and independent supervisor',async()=>{
 const r=await runSwarm(fixture);
 assert.equal(r.agents,8);assert.deepEqual(r.agent_order,['intake','provenance','mathematics','contradiction','safety','replay','synthesis','supervisor']);
 assert.equal(r.verdict,'FAIL');assert.equal(r.production_verification,'UNKNOWN');assert.equal(r.model_api_calls,0);
 assert.equal(r.authority_created,false);assert.equal(r.payment,false);assert.equal(r.deployment,false);
 assert.equal(r.handoffs.find(x=>x.agent==='mathematics').findings[0].verdict,'FAIL');
 assert.equal(r.handoffs.find(x=>x.agent==='mathematics').findings[1].verdict,'PASS');
 assert.equal(r.handoffs.find(x=>x.agent==='mathematics').findings[2].verdict,'UNKNOWN');
 assert.ok(verifyReceipt(r,fixture));
});
test('exact byte deterministic across 1 and 4 concurrent workers',async()=>{
 const a=await runSwarm(fixture,{concurrency:4}),b=await runSwarm(fixture,{concurrency:4}),c=await runSwarm(fixture,{concurrency:1});
 assert.deepEqual(a,b);assert.deepEqual(a.handoffs,c.handoffs);
 assert.notEqual(a.sha256,c.sha256); // actual concurrency belongs in receipt
});
test('fail closed if input source SHA-256 diverges',async()=>{
 const corrupted=structuredClone(fixture);corrupted.evidence[0].content+='tampered';
 const r=await runSwarm(corrupted);
 assert.equal(r.handoffs.find(x=>x.agent==='provenance').verdict,'FAIL');
 assert.equal(r.handoffs.find(x=>x.agent==='supervisor').verdict,'FAIL');
});
test('fail closed if supervisor receives a forged hash',async()=>{
 const r=await runSwarm(fixture);r.handoffs[0].findings[0].verdict='PASS_INVENTED';
 assert.throws(()=>verifyReceipt(r,fixture),/RECEIPT_HASH_MISMATCH/);
});
test('reject authority, online mode and excessive concurrency',async()=>{
 const v=structuredClone(fixture);v.authority_created=true;
 await assert.rejects(runSwarm(v),/AUTHORITY_BOUNDARY/);
 const w=structuredClone(fixture);w.mode='live';
 await assert.rejects(runSwarm(w),/OFFLINE_ONLY/);
 await assert.rejects(runSwarm(fixture,{concurrency:300}),/CONCURRENCY_CAP/);
});
test('all facts sourced and explicit decisions reasoned',async()=>{
 const r=await runSwarm(fixture);
 assert.ok(r.memory.facts.length>=2);
 assert.ok(r.memory.facts.every(x=>typeof x.source_id==='string'));
 assert.ok(r.memory.decisions.every(x=>typeof x.rationale==='string'));
 assert.ok(r.memory.open_questions.length>=1);
});
test('independent SHA test vector',()=>{
 assert.equal(sha256(''), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
});
