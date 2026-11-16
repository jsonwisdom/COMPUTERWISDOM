import test from "node:test";
import assert from "node:assert/strict";
import { readPinnedFixture, sha256, FIXTURE_SHA256, validateReplaySelection } from "../lib/evidence.js";
const bytes=readPinnedFixture(), fixture=JSON.parse(bytes.toString("utf8"));
const archive=(replay=fixture,digest=FIXTURE_SHA256)=>validateReplaySelection(replay,"archived-seven-turn",digest);
const local=(replay=fixture,digest=sha256(JSON.stringify(replay)))=>validateReplaySelection(replay,"browser-local",digest);
test("pinned fixture matches exact archived uploaded bytes",()=>{
 assert.equal(sha256(bytes),FIXTURE_SHA256);
});
test("explicit archived fixture selection verifies full seven-turn replay",()=>{
 const result=archive();
 assert.equal(result.ok,true,result.reason);
 assert.equal(result.rules.turns,7);
 assert.equal(result.rules.final.points,110);
 assert.equal(result.rules.final.trust,47);
});
test("archived selection rejects altered metadata even when arithmetic remains valid",()=>{
 const changed=structuredClone(fixture);changed.exportedAt="2099-01-01T00:00:00Z";
 assert.equal(archive(changed).ok,false);
});
test("archived selection rejects forged points",()=>{
 const changed=structuredClone(fixture);changed.state.points=999;
 assert.equal(archive(changed).ok,false);
});
test("archived selection rejects wrong claimed source digest",()=>{
 assert.equal(archive(fixture,"a".repeat(64)).ok,false);
});
test("explicit browser-local snapshot can be selected with its own digest",()=>{
 const result=local();assert.equal(result.ok,true,result.reason);assert.equal(result.source,"browser-local");
});
test("browser-local snapshot rejects stale or spoofed digest",()=>{
 assert.equal(local(fixture,"b".repeat(64)).ok,false);
});
test("implicit or missing source selection is denied",()=>{
 assert.equal(validateReplaySelection(fixture,undefined,undefined).ok,false);
});
