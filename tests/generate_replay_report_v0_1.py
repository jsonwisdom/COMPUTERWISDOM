"""Generate replay_report.json for classification validator kernel v0.1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from validator.classification_validator_kernel_v0_1 import validate, validate_sequence  # noqa: E402

FIXTURE_DIR = ROOT / "fixtures"
REPORT_PATH = ROOT / "replay_report.json"

FIXTURES = [
    "001_full_valid_lattice.json",
    "002_bad_authority_true.json",
    "003_bad_hash_format.json",
    "004_invalid_transition_skip.json",
    "005_orphaned_parent.json",
    "006_truth_claim_decision.json",
]


def load_fixture(name: str) -> dict:
    with (FIXTURE_DIR / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def run_fixture(fixture: dict) -> dict:
    if "receipts" in fixture:
        actual = validate_sequence(fixture["receipts"])
    elif "ledger_seed" in fixture:
        ledger = {item["receipt_id"]: item for item in fixture["ledger_seed"]}
        actual = validate(fixture["receipt"], ledger)
    else:
        actual = validate(fixture["receipt"], {})

    verdict, reason_code, gate_triggered = actual
    expected = fixture["expected"]
    passed = (
        verdict == expected["verdict"]
        and reason_code == expected["reason_code"]
        and gate_triggered == expected["gate_triggered"]
    )
    return {
        "fixture_id": fixture["fixture_id"],
        "expected": expected,
        "actual": {
            "verdict": verdict,
            "reason_code": reason_code,
            "gate_triggered": gate_triggered,
        },
        "passed": passed,
    }


def main() -> int:
    results = [run_fixture(load_fixture(name)) for name in FIXTURES]
    passed = sum(1 for item in results if item["passed"])
    report = {
        "report_metadata": {
            "artifact": "classification_validator_kernel_v0_1",
            "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "contract": "validator_behavior_contract_v0_1",
            "authority": False,
        },
        "summary": {
            "total_fixtures": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "alignment_score": f"{passed}/{len(results)}",
        },
        "results": results,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
