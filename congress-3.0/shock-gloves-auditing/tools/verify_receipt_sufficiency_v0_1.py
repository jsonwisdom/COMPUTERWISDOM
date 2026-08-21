#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "RECEIPT_SUFFICIENCY_TEST_VECTORS_V0_1.json"


def classify(case):
    if case.get("claim_contradicted_by_bound_source"):
        return "REJECT"
    if case.get("timestamp_conflict"):
        return "CONFLICT"
    if not case.get("trigger_bound") or not case.get("duty_source_bound"):
        return "HOLD"

    required = set(case.get("required_elements", []))
    response = set(case.get("response_elements", []))
    if not required.issubset(response):
        return "HOLD"

    if case.get("contempt_asserted"):
        review_gates = [
            "court_with_authority_bound",
            "lawful_order_bound",
            "notice_or_knowledge_bound",
            "disobedience_evidence_bound",
            "procedural_path_bound",
        ]
        if not all(case.get(gate, False) for gate in review_gates):
            return "HOLD"
        # Even complete audit predicates cannot turn this software into a court.
        return "HOLD"

    return "PASS"


def main():
    suite = json.loads(FIXTURES.read_text())
    failures = []
    results = []
    for vector in suite["vectors"]:
        actual = classify(vector["case"])
        results.append({"id": vector["id"], "expected": vector["expected"], "actual": actual})
        if actual != vector["expected"]:
            failures.append(results[-1])

    print(json.dumps({
        "suite": suite["suite"],
        "result": "PASS" if not failures else "FAIL",
        "vectors": results,
        "boundaries": {
            "legal_violation_proven": False,
            "contempt_found": False,
            "physical_enforcement": False,
            "authority_created": False,
        },
    }, indent=2))

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
