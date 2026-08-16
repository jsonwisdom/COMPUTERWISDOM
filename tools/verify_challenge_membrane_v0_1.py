#!/usr/bin/env python3
"""Deterministic Q1/Q2 binding verifier for MIND_THE_GAP_DICE_V0_1."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = Path("schemas/jaywisdom/challenge_membrane.v0_1.schema.json")
MAPPING = Path("fixtures/jaywisdom/challenge/MIND_THE_GAP_DICE_V0_1.json")
RECEIPTS = [
    Path("fixtures/jaywisdom/challenge/dice_receipt_pass_v0_1.json"),
    Path("fixtures/jaywisdom/challenge/dice_receipt_conflict_v0_1.json"),
    Path("fixtures/jaywisdom/challenge/dice_receipt_gap_v0_1.json"),
]
SUFFICIENCY = {"PASS": "SUFFICIENT", "CONFLICT": "CONFLICTING", "GAP": "INSUFFICIENT"}


def raw(path: Path) -> bytes:
    return (ROOT / path).read_bytes()


def doc(path: Path):
    return json.loads(raw(path).decode("utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def entry_for_roll(mapping, roll):
    matches = [x for x in mapping["mapping"] if roll in x["rolls"]]
    return matches[0] if len(matches) == 1 else None


def verify_fixture(fixture, mapping):
    errors = []
    if fixture.get("format") != "JSONWISDOM_CHALLENGE_FIXTURE_V0.1":
        errors.append("FIXTURE_FORMAT_INVALID")
    for key in ("claim_id", "challenge_id", "authority_state"):
        if fixture.get(key) != mapping.get(key):
            errors.append(f"{key.upper()}_MISMATCH")
    replay = fixture.get("replay", {})
    if replay.get("rule_version") != mapping.get("rule_version"):
        errors.append("RULE_VERSION_MISMATCH")
    if replay.get("scope") != mapping.get("scope"):
        errors.append("SCOPE_MISMATCH")

    snap = fixture.get("evidence_snapshot", {})
    payload = snap.get("payload_utf8")
    if not isinstance(payload, str):
        errors.append("SNAPSHOT_PAYLOAD_INVALID")
    else:
        b = payload.encode("utf-8")
        if snap.get("byte_length") != len(b):
            errors.append("SNAPSHOT_BYTE_LENGTH_MISMATCH")
        if snap.get("sha256") != sha(b):
            errors.append("SNAPSHOT_SHA256_MISMATCH")

    disposition = fixture.get("result", {}).get("disposition")
    if SUFFICIENCY.get(disposition) != fixture.get("response", {}).get("evidence_sufficiency"):
        errors.append("SUFFICIENCY_DISPOSITION_MISMATCH")
    if fixture.get("result", {}).get("assessment_state_changed") is not True:
        errors.append("ASSESSMENT_STATE_INVALID")
    for field in (
        "source_evidence_mutated", "claim_state_mutated", "identity_state_mutated",
        "authority_state_mutated", "authority_created",
    ):
        if fixture.get(field) is not False:
            errors.append(f"{field.upper()}_MUST_BE_FALSE")
    return errors


def verify_receipt(receipt, mapping, mapping_bytes):
    errors = []
    rm = receipt.get("mapping", {})
    if rm.get("mapping_id") != mapping.get("mapping_id") or rm.get("path") != str(MAPPING):
        errors.append("MAPPING_ID_OR_PATH_MISMATCH")
    if rm.get("sha256") != sha(mapping_bytes):
        errors.append("MAPPING_FILE_SHA256_MISMATCH")
    for key in ("claim_id", "challenge_id", "authority_state"):
        if receipt.get(key) != mapping.get(key):
            errors.append(f"{key.upper()}_MISMATCH")

    roll = receipt.get("roll", {}).get("observed_value")
    if not isinstance(roll, int) or not mapping["dice"]["minimum"] <= roll <= mapping["dice"]["maximum"]:
        return errors + ["ROLL_OUT_OF_RANGE"]
    entry = entry_for_roll(mapping, roll)
    if entry is None:
        return errors + ["MAPPING_AMBIGUOUS_OR_MISSING"]

    selection = receipt.get("selection", {})
    if not (
        selection.get("expected_snapshot_id") == entry["snapshot_id"]
        and selection.get("selected_snapshot_id") == entry["snapshot_id"]
        and selection.get("challenge_fixture_path") == entry["challenge_fixture_path"]
        and selection.get("challenge_fixture_sha256") == entry["challenge_fixture_sha256"]
        and selection.get("q1_selection_match") is True
    ):
        errors.append("MAPPING_VIOLATION")

    fixture_path = Path(entry["challenge_fixture_path"])
    fixture_bytes = raw(fixture_path)
    fixture_hash = sha(fixture_bytes)
    if fixture_hash != entry["challenge_fixture_sha256"] or fixture_hash != selection.get("challenge_fixture_sha256"):
        errors.append("CHALLENGE_FIXTURE_FILE_SHA256_MISMATCH")
    fixture = json.loads(fixture_bytes.decode("utf-8"))
    errors.extend(verify_fixture(fixture, mapping))

    replay = receipt.get("replay", {})
    snapshot = fixture["evidence_snapshot"]
    if not (
        replay.get("rule_version") == mapping["rule_version"]
        and replay.get("scope") == mapping["scope"]
        and replay.get("snapshot_sha256") == entry["snapshot_sha256"] == snapshot["sha256"]
        and replay.get("expected_disposition") == entry["expected_disposition"] == fixture["result"]["disposition"]
        and replay.get("observed_disposition") == entry["expected_disposition"]
        and replay.get("q2_replay_match") is True
    ):
        errors.append("REPLAY_VIOLATION")

    if receipt.get("response") != fixture.get("response"):
        errors.append("RESPONSE_BINDING_MISMATCH")
    if receipt.get("source_evidence_mutated") is not False or receipt.get("assessment_state_changed") is not True:
        errors.append("STATE_MUTATION_BOUNDARY_VIOLATION")
    for field in ("claim_state_mutated", "identity_state_mutated", "authority_state_mutated", "authority_created"):
        if receipt.get(field) is not False:
            errors.append(f"{field.upper()}_MUST_BE_FALSE")
    if receipt.get("roll", {}).get("randomness_quality_proven") is not False:
        errors.append("RANDOMNESS_QUALITY_OVERCLAIM")
    return errors


def main() -> int:
    schema = doc(SCHEMA)
    mapping_bytes = raw(MAPPING)
    mapping = json.loads(mapping_bytes.decode("utf-8"))
    setup_errors = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        setup_errors.append("SCHEMA_DIALECT_INVALID")
    if mapping.get("dependency_policy") != "STANDALONE_NO_REF_TO_DRAFT":
        setup_errors.append("DRAFT_DEPENDENCY_POLICY_INVALID")
    if mapping.get("authority_created") is not False:
        setup_errors.append("MAPPING_AUTHORITY_CREATED_MUST_BE_FALSE")

    loaded = [doc(p) for p in RECEIPTS]
    positive = []
    for path, receipt in zip(RECEIPTS, loaded):
        errors = verify_receipt(receipt, mapping, mapping_bytes)
        positive.append({"path": str(path), "pass": not errors, "errors": errors})

    q1_bad = copy.deepcopy(loaded[2])
    q1_bad["roll"]["observed_value"] = 5
    q1_bad["selection"]["selected_snapshot_id"] = "EVIDENCE_SNAPSHOT_A"
    q1_errors = verify_receipt(q1_bad, mapping, mapping_bytes)

    q2_bad = copy.deepcopy(loaded[2])
    q2_bad["roll"]["observed_value"] = 5
    q2_bad["replay"]["observed_disposition"] = "PASS"
    q2_errors = verify_receipt(q2_bad, mapping, mapping_bytes)

    negative = [
        {"case_id": "Q1_MAPPING_VIOLATION", "pass": "MAPPING_VIOLATION" in q1_errors, "observed_errors": q1_errors},
        {"case_id": "Q2_REPLAY_VIOLATION", "pass": "REPLAY_VIOLATION" in q2_errors, "observed_errors": q2_errors},
    ]
    ok = not setup_errors and all(x["pass"] for x in positive + negative)
    out = {
        "verifier": "MIND_THE_GAP_DICE_VERIFIER_V0_1",
        "status": "PASS_WITH_BOUNDARY" if ok else "FAIL",
        "q1": "ROLL_SELECTS_FROZEN_SNAPSHOT",
        "q2": "RULE_SCOPE_SNAPSHOT_DISPOSITION_BINDING_MATCH",
        "mapping_sha256": sha(mapping_bytes),
        "positive_results": positive,
        "negative_results": negative,
        "setup_errors": setup_errors,
        "boundaries": {
            "dice_is_scenario_selector": True,
            "dice_is_verdict_generator": False,
            "roll_observed_does_not_prove_randomness_quality": True,
            "pass_does_not_mean_claim_true": True,
            "substantive_rule_engine_proven": False,
            "schema_dialect_checked": True,
            "full_schema_validation": False,
            "replay_does_not_create_authority": True
        },
        "authority_created": False
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
