#!/usr/bin/env python3
"""
Root Law behavior fixture runner scaffold.

Status: draft scaffold.
Authority: false.

This runner currently materializes the G5 orphaned-parent gate and emits a
fixture_suite_result draft receipt. Full JCS hashing and full G1-G6 coverage
must be added before constitutional lock.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "fixtures" / "root_law" / "behavior_contract_v0_1"
RECEIPT_DIR = ROOT / "receipts" / "root_law" / "fixture_runs"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_g5_orphaned_parent(fixture: dict) -> dict:
    proposed = fixture["input"]["proposed_receipt"]
    local_store = fixture["input"]["local_store_state"]

    parent_cid = proposed.get("parent_cid")
    available_cids = set(local_store.get("available_cids", []))

    if parent_cid not in available_cids:
        return {
            "verdict": "VETO",
            "reason_code": "ORPHANED_RECEIPT",
            "constitutional_compliance": True,
        }

    return {
        "verdict": "ALLOW",
        "reason_code": "SUCCESS",
        "constitutional_compliance": True,
    }


def run_fixture(path: Path) -> dict:
    fixture = load_json(path)
    fixture_id = fixture["fixture_id"]

    if fixture_id == "G5_ORPHANED_PARENT":
        actual = evaluate_g5_orphaned_parent(fixture)
    else:
        actual = {
            "verdict": "DENY",
            "reason_code": "FIXTURE_NOT_IMPLEMENTED",
            "constitutional_compliance": False,
        }

    expected = fixture["expected_outcome"]
    passed = (
        actual.get("verdict") == expected.get("verdict")
        and actual.get("reason_code") == expected.get("reason_code")
    )

    return {
        "fixture_id": fixture_id,
        "path": str(path.relative_to(ROOT)),
        "expected": expected,
        "actual": actual,
        "pass": passed,
        "authority": False,
    }


def main() -> int:
    fixture_paths = [FIXTURE_DIR / "G5_ORPHANED_PARENT.json"]
    results = [run_fixture(path) for path in fixture_paths]
    suite_pass = all(result["pass"] for result in results)

    receipt = {
        "artifact": "fixture_suite_result.v0_1",
        "suite_id": "ROOT_LAW_BEHAVIOR_FIXTURES_G1",
        "runner_state": "DRAFT_G5_ONLY",
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "fixture_results": results,
        "suite_result": "PASS" if suite_pass else "FAIL",
        "constitutional_lock": False,
        "authority": False,
    }

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / "fixture_suite_result.v0_1.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if suite_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
