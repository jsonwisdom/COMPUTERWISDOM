import test from "node:test";
import assert from "node:assert/strict";

// Immutable staging deployment of JOSHUA owner-enforcement build.
// Read-only network tests: do not use a real wallet or any credential.
const origin="https://joshua-war-room-q8e2x5w6r-jsonwisdoms-projects.vercel.app";
test("GET owner attestation is not allowed",async()=>{
 const r=await fetch(origin+"/api/auth?mode=attest");
 assert.equal(r.status,405);
});
test("unverified POST owner attestation is denied",async()=>{
 const r=await fetch(origin+"/api/auth?mode=attest",{
  method:"POST",headers:{"Content-Type":"application/json","Origin":origin},
  body:JSON.stringify({action:"attest-replay",replay:{case:"CW-JOSHUA-STACK-001",simulation:"fictional",state:{}}})
 });
 const data=await r.json();
 assert.equal(r.status,403);assert.match(data.error,/OWNER_DENIED/);
});
test("cross-origin POST is forbidden",async()=>{
 const r=await fetch(origin+"/api/auth?mode=attest",{
  method:"POST",headers:{"Content-Type":"application/json","Origin":"https://example.invalid"},
  body:JSON.stringify({action:"attest-replay",replay:{}})
 });
 assert.equal(r.status,403);
});
test("unauthenticated session returns false",async()=>{
 const r=await fetch(origin+"/api/auth?mode=session");
 assert.equal(r.status,200);assert.equal((await r.json()).authenticated,false);
});
