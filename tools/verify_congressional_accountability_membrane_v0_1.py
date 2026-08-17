#!/usr/bin/env python3
"""Fail-closed verifier for Jason's Congressional Accountability Membrane v0.1."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "fixtures/jaywisdom/fraud_ledger/CONGRESSIONAL_ACCOUNTABILITY_MEMBRANE_TEST_VECTORS_V0_1.json"
LANES = (
    "STATUTORY_AUTHORITY", "BILL_STATUS", "AUTHORIZATION", "APPROPRIATION",
    "COMMITTEE_JURISDICTION", "REQUIRED_CONGRESSIONAL_NOTICE", "HEARING_TESTIMONY",
    "COMMITTEE_REPORT", "IG_AUDIT", "TRANSPARENCY_PUBLIC_REPORTING",
    "DOJ_FBI_REFERRAL_OR_RESPONSE", "JUDICIAL_FISA_CONSTITUTIONAL_REVIEW",
)
FORBIDDEN = (
    "agency_action_lawful", "underlying_claim_true", "fraud_proven",
    "guilt_established", "congressional_endorsement",
    "government_authority_created", "authority_created",
)


def evaluate(record: dict) -> dict:
    rejected, holds = [], []
    document = record.get("document") or {}
    url, sha = document.get("url"), document.get("sha256")
    if not url:
        holds.append("SOURCE_URL_MISSING")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
        rejected.append("SOURCE_SHA256_INVALID")

    enacted = False
    if document.get("bill_status") == "ENACTED":
        if document.get("document_type") != "PUBLIC_LAW":
            rejected.append("ENACTED_REQUIRES_PUBLIC_LAW_DOCUMENT")
        elif not document.get("public_law_number") or not document.get("enacted_at"):
            holds.append("ENACTMENT_RECEIPT_INCOMPLETE")
        else:
            enacted = True

    for field in FORBIDDEN:
        if field == "authority_created":
            value = record.get(field)
        else:
            value = (record.get("claims") or {}).get(field)
        if value is not False:
            rejected.append(f"SEMANTIC_PROMOTION_BLOCKED:{field}")

    claims = record.get("claims") or {}
    if claims.get("enacted_law") is not enacted:
        rejected.append("ENACTED_LAW_DERIVATION_MISMATCH")

    lanes = record.get("lanes") or {}
    if set(lanes) != set(LANES):
        rejected.append("TWELVE_LANES_REQUIRED")

    result = "REJECTED" if rejected else "HOLD" if holds else "PROVEN"
    return {
        "observer_result": result,
        "semantic_type": "BOUNDED_CONGRESSIONAL_EVIDENCE_GATE_DISPOSITION",
        "enacted_law": enacted,
        "rejected_reasons": sorted(rejected),
        "hold_reasons": sorted(holds),
        "underlying_claim_true": False,
        "fraud_proven": False,
        "guilt_established": False,
        "congressional_endorsement": False,
        "government_authority_created": False,
        "authority_created": False,
    }


def build(vector: dict) -> dict:
    lanes = {name: {"status": "NOT_EVALUATED", "evidence_refs": []} for name in LANES}
    if vector.get("set_lane"):
        lanes[vector["set_lane"]] = {"status": "SUPPORTED", "evidence_refs": ["SYNTHETIC_SOURCE"]}
    claims = {
        "enacted_law": vector["expected_enacted"],
        "agency_action_lawful": False,
        "underlying_claim_true": False,
        "fraud_proven": False,
        "guilt_established": False,
        "congressional_endorsement": False,
        "government_authority_created": False,
    }
    if vector.get("attempt_claim"):
        claims[vector["attempt_claim"]] = True
    return {
        "record_id": vector["id"],
        "document": {
            "document_type": vector["document_type"],
            "url": vector.get("url", "https://example.invalid/congressional-source"),
            "sha256": vector.get("sha256", "a" * 64),
            "observed_at": "2026-08-17T00:00:00Z",
            "bill_status": vector["bill_status"],
            **({"public_law_number": vector["public_law_number"]} if vector.get("public_law_number") else {}),
            **({"enacted_at": vector["enacted_at"]} if vector.get("enacted_at") else {}),
        },
        "lanes": lanes,
        "claims": claims,
        "authority_created": False,
    }


def self_test() -> int:
    vectors = json.loads(VECTORS.read_text(encoding="utf-8"))["vectors"]
    results, failed = [], []
    for vector in vectors:
        receipt = evaluate(build(vector))
        ok = receipt["observer_result"] == vector["expected_result"] and receipt["enacted_law"] == vector["expected_enacted"]
        row = {"id": vector["id"], "expected": vector["expected_result"], "observed": receipt["observer_result"], "pass": ok}
        results.append(row)
        if not ok:
            failed.append(row)
    summary = {
        "verifier": "CONGRESSIONAL_ACCOUNTABILITY_MEMBRANE_V0.1",
        "passed": len(results) - len(failed), "failed": len(failed),
        "introduced_bill_is_law": False, "passed_house_is_law": False,
        "committee_report_is_law": False,
        "observer_result_proves_underlying_claim": False,
        "authority_created": False, "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.record:
        parser.error("--record is required unless --self-test is used")
    print(json.dumps(evaluate(json.loads(args.record.read_text(encoding="utf-8"))), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
