import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {MockProvider,Breaker} from '../src/adapter.mjs';
import {rig,makeEnvelope,payload,budget,price} from './helpers.mjs';

test('missing price schedule and stale source fail before model invocation',async()=>{
 assert.throws(()=>rig({customPrice:null}),/PRICE_SCHEMA/);
 const stale={...price,fetched_at:'2026-10-01T00:00:00.000Z'};
 const h=rig({customPrice:stale});
 try{
  const e=makeEnvelope(1,{price_schedule_sha256:(await import('../src/canonical.mjs')).hash(stale)});
  await assert.rejects(h.adapter.call(e,payload),/PRICE_FETCH_STALE/);
  assert.equal(h.provider.calls,0);
 }finally{h.cleanup()}
});

test('rejects unknown envelope fields instead of silently passing into provider',async()=>{
 const h=rig();try{
  await assert.rejects(h.adapter.call({...makeEnvelope(1),enable_payment:true},payload),/ENVELOPE_EXTRA_OR_MISSING_FIELDS/);
  assert.equal(h.provider.calls,0);
 }finally{h.cleanup()}
});

test('reservation TTL may expire while a call is dispatched; reconciliation remains possible',async()=>{
 const provider=new MockProvider();const h=rig({provider});
 try{
  const invoke=provider.invoke.bind(provider);
  provider.invoke=async(e)=>{h.setTime('2026-11-08T22:10:00.000Z');return invoke(e)};
  const r=await h.adapter.call(makeEnvelope(1),payload);
  assert.equal(r.cost_outcome,'RECONCILED');
  assert.equal(h.adapter.journal.balance().global_remaining_micro_usd,29400);
  await assert.rejects(h.adapter.releaseExpiredUndispatched('idem-mock-1'),/MAY_HAVE_DISPATCHED/);
 }finally{h.cleanup()}
});

test('manual breaker never resets itself and permits explicit reset',()=>{
 let now=0;const b=new Breaker({threshold:1,window_ms:50,open_ms:10,reset:'manual',clock:()=>now});
 b.allow();b.failure();now=60000;
 assert.throws(()=>b.allow(),/CIRCUIT_OPEN/);
 b.manualReset();b.allow();
});

test('observer failure by itself does not upgrade provider echo to VERIFIED',async()=>{
 const h=rig();try{
  const r=await h.adapter.call(makeEnvelope(1),payload);
  assert.equal(r.model_revision_verification,'unverified');
  assert.equal(r.verdict,'UNKNOWN');
  assert.equal(r.model_api_calls,0);
 }finally{h.cleanup()}
});
