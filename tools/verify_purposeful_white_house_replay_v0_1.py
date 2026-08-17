#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_EDGES = [
    "public_need",
    "legal_authority",
    "declared_purpose",
    "resources",
    "execution",
    "measurable_result",
    "public_receipt",
    "correction_or_appeal",
]

FORBIDDEN_KEYS = {
    "president_name",
    "political_party",
    "candidate_score",
    "personality_score",
    "approval_score",
    "hero",
    "villain",
}


def contains_forbidden_key(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_KEYS:
                return True
            if contains_forbidden_key(child):
                return True
    elif isinstance(value, list):
        return any(contains_forbidden_key(v) for v in value)
    return False


def classify(record):
    if not isinstance(record, dict):
        return "REJECTED"
    if record.get("subject") != "PRESIDENCY":
        return "REJECTED"
    if record.get("public_purpose_audit") is not True:
        return "REJECTED"
    if record.get("authority_created") is not False:
        return "REJECTED"
    if record.get("party_score") is not None:
        return "REJECTED"
    if record.get("president_score") is not None:
        return "REJECTED"
    if contains_forbidden_key(record):
        return "REJECTED"

    trace = record.get("forward_trace")
    if not isinstance(trace, dict):
        return "GAP"

    if any(edge not in trace for edge in REQUIRED_EDGES):
        return "GAP"

    statuses = []
    for edge in REQUIRED_EDGES:
        payload = trace.get(edge)
        if not isinstance(payload, dict):
            return "GAP"
        statuses.append(payload.get("status"))

    # Deterministic precedence after envelope validation.
    if "CONFLICT" in statuses:
        return "CONFLICT"
    if "GAP" in statuses:
        return "GAP"
    if record.get("reverse_trace_complete") is not True:
        return "GAP"
    if "HOLD" in statuses:
        return "HOLD"

    allowed_complete = {"SOURCE_BOUND", "NOT_REQUIRED"}
    if all(status in allowed_complete for status in statuses):
        return "REPLAYABLE"

    return "REJECTED"


def main(path):
    suite = json.loads(Path(path).read_text(encoding="utf-8"))
    vectors = suite.get("vectors", [])
    failures = []

    for vector in vectors:
        actual = classify(vector.get("record"))
        expected = vector.get("expected")
        ok = actual == expected
        print(f"{vector.get('id')}: expected={expected} actual={actual} {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(vector.get("id"))

    print(f"TOTAL={len(vectors)} PASS={len(vectors) - len(failures)} FAIL={len(failures)}")
    print("party_score_none_enforced=true")
    print("president_score_none_enforced=true")
    print("authority_created_false_enforced=true")
    print("semantic_type=BOUNDED_PUBLIC_PURPOSE_EVIDENCE_DISPOSITION")

    return 1 if failures else 0


if __name__ == "__main__":
    fixture = sys.argv[1] if len(sys.argv) > 1 else "fixtures/jaywisdom/fraud_ledger/PURPOSEFUL_WHITE_HOUSE_REPLAY_TEST_VECTORS_V0_1.json"
    raise SystemExit(main(fixture))
