import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {auditRegistry,inspectClockFixture} from "../tools/fullmath_guard_v0_1.mjs";
const base=new URL("../",import.meta.url),load=p=>JSON.parse(readFileSync(new URL(p,base),"utf8"));
const registry=load("receipts/MINNESOTA_REPLAY_VALIDATION_REGISTRY_V0_1.json");
const fixture=load("fixtures/MNK_003_SYNTHETIC_CLOCK_DEMO_V0_1.json");
const copy=x=>JSON.parse(JSON.stringify(x));
test("registry receipts 0001-0003 have 8 distinct gates and parent HOLD",()=>{const r=auditRegistry(registry);assert.equal(r.status,"CONSISTENT_METADATA_ONLY");assert.equal(r.exercised,8);assert.equal(r.unexercised,5);assert.equal(r.coverage_percent,61.5385);assert.equal(r.parent_disposition,"HOLD");assert.equal(r.independent_reexecution,false);});
test("registry contradictory count is CONFLICT",()=>{const x=copy(registry);x.cumulative_gate_state.distinct_exercised=7;assert.equal(auditRegistry(x).status,"CONFLICT");});
test("unexpected gate id is CONFLICT",()=>{const x=copy(registry);x.receipts[2].exercised.push("MNK-999");assert.equal(auditRegistry(x).status,"CONFLICT");});
test("synthetic clock example cannot change validation coverage",()=>{const r=inspectClockFixture(fixture);assert.equal(r.status,"SIMULATION_PASS");assert.equal(r.real_mn_gate_exercised,false);assert.equal(r.coverage_increment,0);});
test("synthetic inverted document clock is CONFLICT",()=>{const x=copy(fixture);x.clocks.document_time="2026-09-30T12:00:00Z";assert.equal(inspectClockFixture(x).status,"CONFLICT");});
test("missing clock means HOLD",()=>{const x=copy(fixture);delete x.clocks.event_time;assert.equal(inspectClockFixture(x).status,"HOLD");});
test("missing ordering rules means HOLD",()=>{const x=copy(fixture);x.expected_order=[];assert.equal(inspectClockFixture(x).status,"HOLD");});
test("fixture cannot claim proof admission",()=>{const x=copy(fixture);x.proof_admission=true;assert.equal(inspectClockFixture(x).status,"HOLD");});
test("real-event fixture cannot be smuggled through synthetic gate",()=>{const x=copy(fixture);x.classification="PUBLIC_CASE";assert.equal(inspectClockFixture(x).status,"HOLD");});

test("four classroom demo is offline, explicitly non-authoritative",()=>{
 const html=readFileSync(new URL("classes-with-glasses/the-art-of-learing-demo.html",base),"utf8");
 for(const room of ["Learing the Law","Learing the Press","Minnesota Math Algorithms","Applied Wisdom"])assert.ok(html.includes(room));
 assert.equal((html.match(/room:"/g)||[]).length,4);
 assert.ok(html.includes("LOCAL_PRACTICE_ONLY"));
 assert.ok(html.includes("authority_created:false"));
 assert.doesNotMatch(html,/fetch\\s*\\(/);
 assert.doesNotMatch(html,/<script[^>]+src=/);
});
