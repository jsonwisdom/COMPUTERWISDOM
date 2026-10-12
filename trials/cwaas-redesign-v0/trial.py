#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def canonical_sha256(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def evaluate(case):
    facts = case["facts"]
    if facts.get("requested_action") in {"EXECUTE", "PUBLISH", "DISCLOSE_RAW"} and not facts.get("current_epoch_authorized"):
        state = "HOLD_AUTHORIZATION_REQUIRED"
    elif facts.get("challenge_consumed"):
        state = "CHALLENGE_REPLAY"
    elif facts.get("document_rejected") and not facts.get("reason_code"):
        state = "DOCUMENT_REJECTED_REASON_PENDING"
    elif facts.get("document_uploaded") and not facts.get("document_accepted"):
        state = "EXCEPTION_EVIDENCE_PENDING"
    elif facts.get("historical_pass") and facts.get("live_state") == "UNKNOWN":
        state = "HOLD_LIVE_STATE_UNKNOWN"
    else:
        state = "HOLD_UNCLASSIFIED"

    receipt = {
        "case_id": case["case_id"],
        "state": state,
        "execution_allowed": False,
        "facts_promoted": 0,
        "authority_created": False,
        "input_sha256": canonical_sha256(facts),
    }
    receipt["receipt_sha256"] = canonical_sha256(receipt)
    return receipt


def main():
    cases = json.loads((ROOT / "cases.json").read_text())
    results = []
    for case in cases:
        receipt = evaluate(case)
        passed = receipt["state"] == case["expected_state"]
        results.append({"case_id": case["case_id"], "pass": passed, "receipt": receipt})
    summary = {"passed": sum(r["pass"] for r in results), "total": len(results), "results": results}
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if summary["passed"] == summary["total"] else 1)


if __name__ == "__main__":
    main()

