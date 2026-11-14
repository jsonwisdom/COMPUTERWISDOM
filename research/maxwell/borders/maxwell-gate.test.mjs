import test from "node:test";
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {BORDER,inspectOne,inspectBatch,shannonBits} from "./maxwell-gate.mjs";
const source_text="MN classroom fixture source, no external fetch.";
const sha256=createHash("sha256").update(source_text).digest("hex");
const record={scope:"US-MN-EDUCATION",kind:"classroom_fixture",claim:"Verify the example",
 source_uri:"https://example.org/mn",observed_at:"2026-11-14T23:00:00Z",source_text,sha256};
test("all outbound authority disabled",()=>{for(const k of ["network","crawler","cron","write","publish","wallet","payment","authority"])assert.equal(BORDER[k],false);assert.equal(BORDER.maxHops,0)});
test("valid bytes are bounded only",async()=>{const x=await inspectOne(record);assert.equal(x.state,"BOUND_READ_ONLY");assert.equal(x.source_authenticated,false);assert.equal(x.escalation,false)});
test("no cross-border scope or personal data",async()=>{assert.equal((await inspectOne({...record,scope:"GLOBAL"})).state,"REJECT");assert.equal((await inspectOne({...record,contains_pii:true})).state,"REJECT")});
test("missing and conflicting receipts stay unresolved",async()=>{assert.equal((await inspectOne({...record,sha256:undefined})).state,"HOLD");assert.equal((await inspectOne({...record,source_text:"other"})).state,"CONFLICT")});
test("limits and Shannon model",async()=>{assert.equal((await inspectBatch(Array(51).fill(record))).state,"REJECT");assert.equal((await inspectOne({...record,source_text:"x".repeat(32769)})).state,"REJECT");assert.equal(shannonBits([.5,.5]),1);assert.equal(shannonBits([1,0]),0)});
