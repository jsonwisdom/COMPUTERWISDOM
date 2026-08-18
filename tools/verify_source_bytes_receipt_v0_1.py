#!/usr/bin/env python3
"""Deterministic synthetic verifier for SOURCE_BYTES_RECEIPT_V0.1.

This tool classifies byte-observation receipts only. It does not fetch live URLs,
authenticate institutional identity, prove content assertions, or create authority.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SEMANTIC_TYPE = "BOUNDED_SOURCE_BYTES_RECEIPT_DISPOSITION"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "fixtures/jaywisdom/source_bytes/SOURCE_BYTES_RECEIPT_TEST_VECTORS_V0_1.json"


def valid_sha(value):
    return value is None or (isinstance(value, str) and SHA256_RE.fullmatch(value) is not None)


def classify(vector):
    # Any attempt to widen byte evidence into identity, guilt, truth, or an
    # untyped external PROVEN result is rejected at the presentation boundary.
    if vector.get("attempt_claim"):
        return "REJECTED"

    observed = vector.get("observed_sha256")
    expected = vector.get("expected_sha256")
    byte_length = vector.get("byte_length")
    fetch_status = vector.get("fetch_status")
    comparison = vector.get("comparison")

    if not valid_sha(observed) or not valid_sha(expected):
        return "REJECTED"

    if fetch_status == "ERROR":
        return "REJECTED"

    if fetch_status == "NOT_FETCHED":
        return "HOLD"

    if fetch_status != "FETCHED":
        return "REJECTED"

    if observed is None or byte_length is None or not isinstance(byte_length, int) or byte_length < 0:
        return "REJECTED"

    if comparison == "MISMATCH":
        return "REJECTED"

    if comparison == "MATCH":
        if expected is None or observed != expected:
            return "REJECTED"
        return "PROVEN"

    if comparison == "NO_REFERENCE":
        if expected is not None:
            return "REJECTED"
        return "PROVEN"

    return "REJECTED"


def run_self_test():
    data = json.loads(VECTORS.read_text(encoding="utf-8"))
    results = []
    passed = 0

    for vector in data["vectors"]:
        observed = classify(vector)
        expected = vector["expected_disposition"]
        ok = observed == expected
        passed += int(ok)
        results.append({
            "id": vector["id"],
            "expected": expected,
            "observed": observed,
            "pass": ok,
        })

    summary = {
        "verifier": "SOURCE_BYTES_RECEIPT_V0.1",
        "semantic_type": SEMANTIC_TYPE,
        "observer_result": {
            "semantic_type": SEMANTIC_TYPE,
            "value": "PROVEN" if passed == len(results) else "REJECTED",
            "rendering": "SOURCE_BYTES_BOUNDARY_TESTS_PASS" if passed == len(results) else "SOURCE_BYTES_BOUNDARY_TESTS_FAIL",
        },
        "passed": passed,
        "failed": len(results) - passed,
        "source_bytes_authenticated_proves_world_fact": False,
        "source_identity_authenticated": False,
        "claim_verified": False,
        "live_fetch_performed": False,
        "model_execution_performed": False,
        "authority_created": False,
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["failed"] == 0 else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(run_self_test())
    parser.error("Only --self-test is supported in v0.1; live fetching is intentionally out of scope.")


if __name__ == "__main__":
    main()
