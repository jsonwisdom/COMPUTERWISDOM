#!/usr/bin/env python3
"""
Root Law behavior fixture runner scaffold.

Status: draft scaffold.
Authority: false.

Default behavior emits the baseline fixture_suite_result.v0_1 receipt only.
Phase 3 pattern observation is experimental and opt-in via --emit-patterns.

By default this script does not write generated receipts to the working tree.
Use --write-receipt when an explicit local receipt artifact is desired.
"""

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "fixtures" / "root_law" / "behavior_contract_v0_1"
RECEIPT_DIR = ROOT / "receipts" / "root_law" / "fixture_runs"
REASON_CODE_MAP_PATH = ROOT / "schemas" / "root_law" / "reason_code_failure_family_map.v0_1.json"
PATTERN_WINDOW_SIZE = 10
PATTERN_THRESHOLDS = {
    "LINEAGE_REPEAT": 3,
    "DOMAIN_REPEAT": 3,
    "HASH_SHAPE_REPEAT": 3,
}

FIXTURE_BATCH = [
    "G1_FULL_VALID_LATTICE.json",
    "G5A_MISSING_PARENT_REFERENCE.json",
    "G5B_PARENT_NOT_IN_LOCAL_STORE.json",
    "G5C_SCHEMA_HASH_MISMATCH.json",
    "G5_ORPHANED_PARENT.json",
    "G5D_WRONG_DOMAIN.json",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def base_actual(verdict: str, reason_code: str, failure_class: str = "NONE", **diagnostic) -> dict:
    return {
        "verdict": verdict,
        "reason_code": reason_code,
        "failure_class": failure_class,
        "constitutional_compliance": True,
        "memory_update": False,
        "diagnostic": diagnostic,
    }


def evaluate_fixture(fixture: dict) -> dict:
    fixture_id = fixture["fixture_id"]
    proposed = fixture["input"]["proposed_receipt"]
    local_store = fixture["input"].get("local_store_state", {})
    parent_cid = proposed.get("parent_cid")
    available_cids = set(local_store.get("available_cids", []))

    if fixture_id == "G1_FULL_VALID_LATTICE":
        if parent_cid in available_cids and proposed.get("authority") is False:
            return base_actual("ALLOW", "SUCCESS")
        return base_actual("DENY", "INVALID_VALID_LATTICE", "LINEAGE_FAILURE")

    if fixture_id == "G5A_MISSING_PARENT_REFERENCE":
        if parent_cid is None:
            return base_actual(
                "VETO",
                "MISSING_PARENT_REFERENCE",
                "LINEAGE_FAILURE",
                parent_cid_present=False,
            )

    if fixture_id == "G5B_PARENT_NOT_IN_LOCAL_STORE":
        if parent_cid not in available_cids:
            return base_actual(
                "VETO",
                "PARENT_NOT_IN_LOCAL_STORE",
                "LINEAGE_FAILURE",
                parent_cid=parent_cid,
                parent_found=False,
            )

    if fixture_id == "G5C_SCHEMA_HASH_MISMATCH":
        schema_hash = proposed.get("schema_hash")
        expected_schema_hash = fixture["input"].get("expected_schema_hash")
        if schema_hash != expected_schema_hash:
            return base_actual(
                "VETO",
                "SCHEMA_HASH_MISMATCH",
                "LINEAGE_FAILURE",
                observed_schema_hash=schema_hash,
                expected_schema_hash=expected_schema_hash,
            )

    if fixture_id == "G5_ORPHANED_PARENT":
        if parent_cid not in available_cids:
            return base_actual(
                "VETO",
                "ORPHANED_RECEIPT",
                "LINEAGE_FAILURE",
                parent_cid=parent_cid,
                parent_found=False,
            )

    if fixture_id == "G5D_WRONG_DOMAIN":
        cid_domain_map = local_store.get("cid_domain_map", {})
        observed_domain = cid_domain_map.get(parent_cid)
        expected_domain = proposed.get("expected_domain")
        if parent_cid in available_cids and observed_domain != expected_domain:
            return base_actual(
                "VETO",
                "DOMAIN_BOUNDARY_VIOLATION",
                "LINEAGE_FAILURE",
                parent_found=True,
                observed_domain=observed_domain,
                expected_domain=expected_domain,
            )

    return base_actual("DENY", "FIXTURE_NOT_IMPLEMENTED", "INVALID_TRANSITION")


def run_fixture(path: Path) -> dict:
    fixture = load_json(path)
    fixture_id = fixture["fixture_id"]
    actual = evaluate_fixture(fixture)
    expected = fixture["expected_outcome"]
    passed = (
        actual.get("verdict") == expected.get("verdict")
        and actual.get("reason_code") == expected.get("reason_code")
        and actual.get("failure_class") == expected.get("failure_class", actual.get("failure_class"))
        and actual.get("memory_update") == expected.get("memory_update", actual.get("memory_update"))
    )

    return {
        "fixture_id": fixture_id,
        "path": str(path.relative_to(ROOT)),
        "expected": expected,
        "actual": actual,
        "pass": passed,
        "authority": False,
    }


def build_receipt() -> dict:
    fixture_paths = [FIXTURE_DIR / name for name in FIXTURE_BATCH]
    results = [run_fixture(path) for path in fixture_paths]
    suite_pass = all(result["pass"] for result in results)

    return {
        "artifact": "fixture_suite_result.v0_1",
        "suite_id": "ROOT_LAW_BEHAVIOR_FIXTURES_G1",
        "runner_state": "DRAFT_G1_G5_CALIBRATION",
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "fixture_results": results,
        "suite_result": "PASS" if suite_pass else "FAIL",
        "constitutional_lock": False,
        "authority": False,
    }


def load_reason_code_map() -> dict:
    family_map_doc = load_json(REASON_CODE_MAP_PATH)
    return family_map_doc["mapping"]


def build_packet_observations(fixture_results: list[dict], family_map: dict) -> list[dict]:
    observations = []
    for index, result in enumerate(fixture_results, start=1):
        reason_code = result["actual"]["reason_code"]
        if reason_code not in family_map:
            raise ValueError(f"Unmapped reason_code: {reason_code}")
        mapping = family_map[reason_code]
        observations.append(
            {
                "packet_sequence_id": index,
                "fixture_id": result["fixture_id"],
                "reason_codes": [reason_code],
                "families": [mapping["family"]],
                "pattern_triggers": [bool(mapping["pattern_trigger"])],
                "authority": False,
            }
        )
    return observations


def build_pattern_results(packet_observations: list[dict]) -> list[dict]:
    window = packet_observations[-PATTERN_WINDOW_SIZE:]
    family_counter: Counter[str] = Counter()

    for packet in window:
        for family, trigger in zip(packet["families"], packet["pattern_triggers"]):
            if trigger and family != "NONE":
                family_counter[family] += 1

    families_to_report = sorted(set(PATTERN_THRESHOLDS) | set(family_counter))
    return [
        {
            "pattern_family": family,
            "observed_count": int(family_counter.get(family, 0)),
            "threshold": int(PATTERN_THRESHOLDS.get(family, 3)),
            "pattern_detected": int(family_counter.get(family, 0)) >= int(PATTERN_THRESHOLDS.get(family, 3)),
            "success_masking": False,
            "authority": False,
        }
        for family in families_to_report
    ]


def build_pattern_observation_receipt(baseline_receipt: dict) -> dict:
    family_map = load_reason_code_map()
    packet_observations = build_packet_observations(baseline_receipt["fixture_results"], family_map)
    return {
        "artifact": "pattern_observation_receipt.v0_1",
        "receipt_id": "pattern-observation-draft-001",
        "run_id": "root-law-fixture-run-draft",
        "batch_id": baseline_receipt["runner_state"],
        "timestamp_utc": baseline_receipt["timestamp_utc"],
        "corpus_window": {
            "mode": "last_N_packets",
            "window_size": PATTERN_WINDOW_SIZE,
            "sequence_scope": "runner_level_within_declared_test_corpus",
        },
        "reason_code_map_ref": str(REASON_CODE_MAP_PATH.relative_to(ROOT)),
        "threshold_policy_ref": "inline:draft:LINEAGE_REPEAT=3,DOMAIN_REPEAT=3,HASH_SHAPE_REPEAT=3",
        "packet_observations": packet_observations,
        "pattern_results": build_pattern_results(packet_observations),
        "memory_update": False,
        "reputation_system": False,
        "quarantine": False,
        "authority": False,
    }


def write_receipt(receipt: dict) -> Path:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / "fixture_suite_result.v0_1.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Root Law behavior fixtures.")
    parser.add_argument(
        "--write-receipt",
        action="store_true",
        help="Write fixture_suite_result.v0_1.json into receipts/root_law/fixture_runs/.",
    )
    parser.add_argument(
        "--emit-patterns",
        action="store_true",
        help="Emit passive Phase 3 pattern_observation_receipt.v0_1 alongside the baseline receipt.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = build_receipt()

    if args.emit_patterns:
        receipt["pattern_observation_receipt"] = build_pattern_observation_receipt(receipt)

    if args.write_receipt:
        receipt_path = write_receipt(receipt)
        receipt["written_receipt_path"] = str(receipt_path.relative_to(ROOT))

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["suite_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
