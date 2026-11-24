"""CI-FIRST evidence continuity decision engine. Stdlib only; no external writes.

A previous PASS is scoped to its exact claim and test. Neither a digest alone
nor an earlier reported PASS is automatically cryptographic identity proof.
"""
import hashlib
import json
from pathlib import Path

VALID = {
    "UNKNOWN_NOT_SEARCHED", "UNKNOWN_NOT_VERIFIED",
    "PASS_PREVIOUSLY_VERIFIED", "CONFLICT", "FAIL",
}


def fingerprint(data):
    return hashlib.sha256(data).hexdigest()


def reconcile(claim_id, receipts, searched_sources, expected_scope=None):
    """Return a reasoned decision without silently converting absence to failure.

    Receipt fields: claim_id, scope, status, source, test_id, evidence_sha256.
    For PASS, this *reuses* only pre-existing reported test results; it does
    not itself reproduce cryptographic assertions or certify provenance.
    """
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise ValueError("claim_id required")
    if not isinstance(receipts, list) or not isinstance(searched_sources, list):
        raise ValueError("receipts and searched_sources must be lists")
    matching = [r for r in receipts if isinstance(r, dict)
                and r.get("claim_id") == claim_id
                and (expected_scope is None or r.get("scope") == expected_scope)]
    for r in matching:
        if r.get("status") not in VALID:
            raise ValueError("unknown receipt status")
    statuses = {r["status"] for r in matching}
    identities = {(r.get("scope"), r.get("test_id"), r.get("evidence_sha256"))
                  for r in matching if r["status"] == "PASS_PREVIOUSLY_VERIFIED"}
    observed = {r["status"] for r in matching
                if r["status"] in {"PASS_PREVIOUSLY_VERIFIED", "FAIL", "CONFLICT"}}
    if "CONFLICT" in observed or ({"FAIL", "PASS_PREVIOUSLY_VERIFIED"} <= observed):
        status, reason = "CONFLICT", "contradictory_receipts_require_reconciliation"
    elif "FAIL" in observed:
        status, reason = "FAIL", "prior_test_failure_in_requested_scope"
    elif "PASS_PREVIOUSLY_VERIFIED" in observed:
        if any(not all(isinstance(r.get(k), str) and r[k].strip()
                       for k in ("source", "test_id", "scope", "evidence_sha256"))
               for r in matching if r["status"] == "PASS_PREVIOUSLY_VERIFIED"):
            status, reason = "UNKNOWN_NOT_VERIFIED", "pass_receipt_missing_provenance_fields"
        elif len(identities) > 1:
            status, reason = "CONFLICT", "distinct_pass_receipts_require_scope_review"
        else:
            status, reason = "PASS_PREVIOUSLY_VERIFIED", "prior_scoped_test_result_reused_not_rerun"
    elif matching or searched_sources:
        status, reason = "UNKNOWN_NOT_VERIFIED", "searched_but_no_scoped_pass"
    else:
        status, reason = "UNKNOWN_NOT_SEARCHED", "no_evidence_search_recorded"
    return {
        "claim_id": claim_id,
        "scope": expected_scope,
        "status": status,
        "reason": reason,
        "matching_receipts": len(matching),
        "searched_sources": sorted(set(searched_sources)),
        "external_verification_performed": False,
        "new_authority_granted": False,
    }


def main():
    # Synthetic demonstration only; no network or wallet calls.
    sample = reconcile("example", [], [], "demo")
    print(json.dumps(sample, sort_keys=True))


if __name__ == "__main__":
    main()
