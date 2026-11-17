import test from "node:test";
import assert from "node:assert/strict";
import {loadRegistry, validateRegistry, evaluateChildProposal, assessParentApproval, requireDualRailRelease, sha256Receipt} from "./parent-oversight.mjs";
const registry=loadRegistry();
const baseline={child_id:"FAMILY_HEIDEE",action:"observe",channel:"none",source_sha256:"sha256:"+"a".repeat(64),source_url:"https://github.com/jsonwisdom/HEIDEE"};
test("six already verified family-labeled repos only; public-safe JOY lane",()=> {
 assert.equal(validateRegistry(registry),true);
 assert.deepEqual(registry.family_repos.map(x=>x.repository).sort(),["jsonwisdom/GAGA","jsonwisdom/GRAMMY","jsonwisdom/HEIDEE","jsonwisdom/JAYCEE","jsonwisdom/LEEANN","jsonwisdom/MARYDEE"].sort());
 assert.equal(registry.protected_lane_index.repository,"jsonwisdom/JOY");
});
test("no private child data in permitted proposal schema",()=> {
 const r=evaluateChildProposal(registry,{...baseline,age:10});
 assert.equal(r.status,"FAIL");assert.equal(r.decision,"HOLD");
});
test("source provenance must be a digest and an allowed GitHub URL",()=> {
 assert.equal(evaluateChildProposal(registry,{...baseline,source_sha256:null}).status,"UNKNOWN");
 assert.equal(evaluateChildProposal(registry,{...baseline,source_url:"https://example.org/child"}).status,"UNKNOWN");
});
test("structural PASS is only a review draft; never authority",()=> {
 const r=evaluateChildProposal(registry,baseline);
 assert.equal(r.status,"PASS");assert.equal(r.decision,"DRAFT_REVIEW_ONLY");
 assert.equal(r.authority_created,false);assert.equal(r.payment_authorized,false);assert.equal(r.publication_authorized,false);
});
test("unknown family repository and fabricated permissions are denied",()=> {
 assert.equal(evaluateChildProposal(registry,{...baseline,child_id:"FAMILY_BRIANNA"}).status,"FAIL");
 assert.equal(evaluateChildProposal(registry,{...baseline,parent_approved:true}).status,"FAIL");
});
test("no child publication, wallet, trade, transfer, deploy, merge, attest or signing",()=> {
 for (const action of ["publish","send","wallet_sign","settle","trade","transfer","deploy","merge","attest","resolver_write","unknown"]) {
   const r=evaluateChildProposal(registry,{...baseline,action});
   assert.equal(r.status,"FAIL",action);
 }
});
test("cross-chain or unknown networks blocked even for observer",()=> {
 for(const channel of ["ethereum+base","eip155:8453/eip155:1","cross-chain","other"]) {
  assert.equal(evaluateChildProposal(registry,{...baseline,channel}).status,"FAIL",channel);
 }
 assert.equal(evaluateChildProposal(registry,{...baseline,channel:"base",action:"draft"}).status,"FAIL");
});
test("machine cannot grant parent or guardian approval by flag",()=> {
 for(const v of [true,{approved:true},{approved:true,guardian:true},null])
   assert.deepEqual([assessParentApproval(v).status,assessParentApproval(v).decision],["UNKNOWN","HOLD"]);
});
test("all receipts deterministic and no runtime authority path",()=> {
 assert.equal(sha256Receipt({b:1,a:{y:2,x:3}}),sha256Receipt({a:{x:3,y:2},b:1}));
 assert.throws(()=>requireDualRailRelease(),/CI_FIRST_PARENT_HOLD/);
});
test("changes that enable authority or remove child privacy invalidate registry",()=> {
 assert.equal(validateRegistry({...registry,authority_created:true}),false);
 assert.equal(validateRegistry({...registry,machine_controls:{...registry.machine_controls,child_fund_access_enabled:true}}),false);
 assert.equal(validateRegistry({...registry,family_repos:registry.family_repos.slice(0,5)}),false);
});
