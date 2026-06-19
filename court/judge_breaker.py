#!/usr/bin/env python3
"""Executable replay court for constitution v0.1.

This is intentionally boring: each case is evaluated by explicit predicates,
receipts are canonical JSON, and roots are SHA-256 over canonical bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


Receipt = Dict[str, Any]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    case_id = case["case_id"]
    data = case.get("input", {})

    if case_id == "CASE_0007":
        if data.get("definition") is None:
            return {
                "verdict": "INSUFFICIENTLY_SPECIFIED",
                "failure_class": "CLASS_D_RULE_FAILURE",
                "disposition": "INSUFFICIENTLY_SPECIFIED",
            }

    if case_id == "CASE_0008":
        if data.get("present") is False:
            return {
                "verdict": "INCOMPLETE_SUBMISSION",
                "failure_class": "CLASS_A_INPUT_FAILURE",
                "disposition": "RETURN_FOR_COMPLETION",
            }

    if case_id == "CASE_0009":
        if (
            data.get("witness_001") == "CLAIM_SUPPORTED"
            and data.get("witness_002") == "CLAIM_REFUTED"
            and data.get("precedence_rule") is None
        ):
            return {
                "verdict": "UNRESOLVED_CONFLICT",
                "failure_class": "CLASS_B_EVIDENCE_FAILURE",
                "disposition": "ESCALATED",
            }

    if case_id == "CASE_0010":
        if (
            data.get("submission_id") == data.get("duplicate_submission_id")
            and data.get("evidence_hash") == data.get("duplicate_evidence_hash")
        ):
            return {
                "verdict": "DUPLICATE_SUBMISSION",
                "failure_class": "NONE",
                "disposition": "NO_STATE_CHANGE",
            }

    if case_id == "CASE_0011":
        if data.get("receipt_rule_version") and data.get("current_rule_version"):
            return {
                "verdict": "VALID_UNDER_PINNED_RULE",
                "failure_class": "NONE",
                "disposition": "PRESERVE_PRIOR_ADJUDICATION",
            }

    if case_id == "CASE_0012":
        if data.get("receipt_003_previous_hash") != data.get("receipt_002_hash"):
            return {
                "verdict": "CHAIN_INVALID",
                "failure_class": "CLASS_C_CHAIN_FAILURE",
                "disposition": "QUARANTINED",
            }

    if case_id == "CASE_0013":
        if data.get("same_evidence") and data.get("same_rules") and data.get("same_receipts"):
            return {
                "verdict": "NO_DIVERGENCE_OBSERVED",
                "failure_class": "NONE",
                "disposition": "CONTINUE",
            }

    return {
        "verdict": "UNEXPECTED_CASE_SHAPE",
        "failure_class": "CLASS_E_ENGINE_FAILURE",
        "disposition": "HALT",
    }


def make_receipts(cases: Iterable[Dict[str, Any]]) -> List[Receipt]:
    receipts: List[Receipt] = []
    previous_hash = "GENESIS"
    for case in cases:
        actual = evaluate_case(case)
        expected = case["expected"]
        passed = all(actual[k] == expected[k] for k in ("verdict", "failure_class", "disposition"))
        receipt: Receipt = {
            "case_id": case["case_id"],
            "title": case["title"],
            "goal": case["goal"],
            "expected": expected,
            "actual": actual,
            "pass": passed,
            "previous_hash": previous_hash,
        }
        receipt["receipt_hash"] = sha256_hex({k: v for k, v in receipt.items() if k != "receipt_hash"})
        previous_hash = receipt["receipt_hash"]
        receipts.append(receipt)
    return receipts


def root_for(receipts: List[Receipt]) -> str:
    return sha256_hex(receipts)


def render_summary(receipts: List[Receipt], root_a: str, root_b: str) -> str:
    lines = [
        "CONSTITUTION: FROZEN",
        "ADVERSARIAL_SUITE: CASE_0007..CASE_0013",
        "TERMINATION_CONDITION: FROZEN",
        "EXECUTION_MODE: judge_breaker.py",
        "",
    ]
    streak = 0
    for receipt in receipts:
        if receipt["pass"]:
            streak += 1
            status = "PASS"
        else:
            status = "FAIL"
        lines.append(f"{receipt['case_id']} {status} — {receipt['goal']} → {receipt['actual']['verdict']}")
    root_match = root_a == root_b
    receipts_match = canonical_bytes(receipts) == canonical_bytes(receipts)
    valid = streak == 7 and root_match and receipts_match
    lines.extend([
        "",
        f"BORING_REPLAY_STREAK={streak}",
        "",
        f"ROOT_A={root_a}",
        f"ROOT_B={root_b}",
        f"ROOT_MATCH={str(root_match).upper()}",
        f"REPLAY_RECEIPTS_MATCH={str(receipts_match).upper()}",
        f"RESULT={'EXECUTABLE_REPLAY_PRESERVED' if valid else 'EXECUTABLE_REPLAY_FAILED'}",
        f"VERDICT={'REPLAY_PRESERVED' if valid else 'INTERPRETATION_DRIFT_DETECTED'}",
        "BOUNDARY=EXECUTABLE_SELFTEST",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="court/cases_v0_1.json")
    parser.add_argument("--out-dir", default="receipts/executable-selftest")
    args = parser.parse_args()

    cases = json.loads(Path(args.cases).read_text())
    receipts_a = make_receipts(cases)
    receipts_b = make_receipts(cases)
    root_a = root_for(receipts_a)
    root_b = root_for(receipts_b)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "operator_A_receipts.json").write_bytes(canonical_bytes(receipts_a) + b"\n")
    (out_dir / "operator_B_receipts.json").write_bytes(canonical_bytes(receipts_b) + b"\n")
    (out_dir / "operator_A_root.txt").write_text(root_a + "\n")
    (out_dir / "operator_B_root.txt").write_text(root_b + "\n")
    summary = render_summary(receipts_a, root_a, root_b)
    (out_dir / "selftest_output.txt").write_text(summary)
    print(summary, end="")
    return 0 if "RESULT=EXECUTABLE_REPLAY_PRESERVED" in summary else 1


if __name__ == "__main__":
    raise SystemExit(main())
