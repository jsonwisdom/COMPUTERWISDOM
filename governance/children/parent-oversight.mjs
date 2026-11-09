// CI-FIRST parent oversight for publicly existing family-labeled repositories.
// These are protected project lanes, NOT assertions about a person's age,
// consent, guardianship or relationship. No I/O, network, wallet or CI writes.
import {createHash} from "node:crypto";
import {readFileSync} from "node:fs";
const REGISTRY_FILE = new URL("./registry.v1.json", import.meta.url);
export const loadRegistry = () => JSON.parse(readFileSync(REGISTRY_FILE, "utf8"));
const allowedActions = new Set(["inventory", "observe", "replay", "compare", "draft"]);
const requestKeys = new Set(["child_id", "action", "channel", "source_sha256", "source_url"]);
const sha = /^sha256:[0-9a-f]{64}$/;
const github = /^https:\/\/github\.com\/jsonwisdom\/[A-Za-z0-9_.-]+(?:\/(?:blob|tree|pull|issues|commit)\/[A-Za-z0-9_./-]+)?$/;
const result = (status, decision, reason, child_id = null) =>
 Object.freeze({status, decision, reason, child_id, authority_created: false, payment_authorized: false, publication_authorized: false});
function sorted(x) {
 if (Array.isArray(x)) return x.map(sorted);
 if (x && typeof x === "object") return Object.fromEntries(Object.entries(x).sort(([a],[b]) => a.localeCompare(b)).map(([k,v])=>[k,sorted(v)]));
 return x;
}
export const sha256Receipt = x => "sha256:" + createHash("sha256").update(JSON.stringify(sorted(x)), "utf8").digest("hex");
export function validateRegistry(r) {
 if (!r || r.schema !== "computerwisdom.parent-child-oversight.registry.v1" || r.parent_repo !== "jsonwisdom/COMPUTERWISDOM" ||
     r.authority_created !== false || r.canon !== false) return false;
 const c = r.machine_controls;
 if (!c || c.cross_rail_bridge_enabled !== false || c.mutations_enabled !== false ||
     c.child_fund_access_enabled !== false || c.child_identity_publication_enabled !== false || c.parent_approval_automated !== false) return false;
 if (!Array.isArray(r.family_repos) || r.family_repos.length !== 6) return false;
 const ids = new Set();
 for (const n of r.family_repos) {
   if (!n || typeof n.id !== "string" || typeof n.repository !== "string" ||
       n.id !== "FAMILY_" + n.repository.split("/")[1] || !n.repository.startsWith("jsonwisdom/") ||
       n.github_repo_exist_readback !== true || n.private_person_data_authorized !== false ||
       n.publication_authorized !== false || n.authority_created !== false || ids.has(n.id)) return false;
   ids.add(n.id);
 }
 const permitted = ["FAMILY_JAYCEE","FAMILY_HEIDEE","FAMILY_LEEANN","FAMILY_MARYDEE","FAMILY_GAGA","FAMILY_GRAMMY"];
 if (permitted.some(id=>!ids.has(id))) return false;
 if (r.protected_lane_index?.repository !== "jsonwisdom/JOY" ||
     r.protected_lane_index?.not_a_guardian_consent_receipt !== true) return false;
 if (r.unverified_separate_family_repo?.state !== "UNKNOWN_REPO_NOT_FOUND") return false;
 return true;
}
/** Structural check only. PASS here means an offline draft is well formed. */
export function evaluateChildProposal(registry, proposal) {
 if (!validateRegistry(registry)) return result("FAIL","HOLD","PARENT_REGISTRY_INVALID");
 if (!proposal || typeof proposal !== "object" || Array.isArray(proposal))
   return result("FAIL","HOLD","CHILD_PROPOSAL_INVALID");
 for (const k of Object.keys(proposal))
   if (!requestKeys.has(k)) return result("FAIL","HOLD","EXTRA_OR_PRIVATE_FIELD_FORBIDDEN",proposal.child_id ?? null);
 const child = registry.family_repos.find(x=>x.id === proposal.child_id) ||
   (proposal.child_id === "JOY_PROTECTED_LANES" ? registry.protected_lane_index : null);
 if (!child) return result("FAIL","HOLD","UNREGISTERED_CHILD",proposal.child_id ?? null);
 if (!allowedActions.has(proposal.action)) return result("FAIL","HOLD","MUTATING_OR_UNKNOWN_ACTION_FORBIDDEN",proposal.child_id);
 if (!["none","ethereum","base"].includes(proposal.channel)) return result("FAIL","HOLD","CROSS_RAIL_OR_UNKNOWN_CHANNEL_FORBIDDEN",proposal.child_id);
 if (proposal.channel !== "none" && proposal.action === "draft")
   return result("FAIL","HOLD","CHAIN_BOUND_DRAFT_REQUIRES_PARENT_REVIEW",proposal.child_id);
 if (typeof proposal.source_sha256 !== "string" || !sha.test(proposal.source_sha256))
   return result("UNKNOWN","HOLD","SOURCE_BYTES_NOT_VERIFIED",proposal.child_id);
 if (typeof proposal.source_url !== "string" || !github.test(proposal.source_url))
   return result("UNKNOWN","HOLD","GITHUB_SOURCE_NOT_VERIFIED",proposal.child_id);
 // This code never checks an external source or approves a human/guardian.
 return result("PASS","DRAFT_REVIEW_ONLY","STRUCTURAL_RECEIPT_NOT_PARENT_APPROVAL",proposal.child_id);
}
/** No data supplied by a child, AI or agent can itself establish parent permission. */
export function assessParentApproval(_candidate) {
 return result("UNKNOWN","HOLD","INDEPENDENT_HUMAN_OVERSIGHT_NOT_VERIFIED");
}
/** Called by future dual-chain bridge adapters. Always fail closed until separately implemented and reviewed. */
export function requireDualRailRelease() {
 throw new Error("CI_FIRST_PARENT_HOLD: parent oversight, child privacy, ENS control and live settlement not certified");
}
