#!/usr/bin/env python3
"""Deterministic structural verifier for DELTA Work Replay v0.1.

This verifier checks that the DELTA training sidecar preserves its declared
work-training, institutional, evidence, causation, and authority boundaries.
It does not prove substantive mission suitability or institutional adoption.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DELTA = Path("fixtures/jaywisdom/challenge/DELTA_WORK_REPLAY_V0_1.json")
GAME = Path("fixtures/jaywisdom/challenge/LEAHPRIME_DICE_GAME_V0_1.json")

EXPECTED_LOOP = [
    "FREEZE_BEFORE_STATE",
    "ROLL_OR_SELECT_BOUNDED_SCENARIO",
    "DICE_LEAHPRIME_PRESENTS_SCENARIO",
    "ZIGGY_CHALLENGES_CLAIMS_AND_MISSING_EDGES",
    "GIRLMATH_CHECKS_EVIDENCE_DENOMINATOR",
    "CLASSIFY_PASS_GAP_CONFLICT_OR_HOLD",
    "RECEIPTOS_RECORDS_EVENTS",
    "REPLAY_REPRODUCES_BINDINGS",
    "DELTA_COMPARES_BEFORE_AND_AFTER",
    "HUMAN_DECIDES_ANY_CONSEQUENTIAL_ACTION",
]

EXPECTED_AXES = [
    "OBSERVATION_STATE",
    "EVIDENCE_STATE",
    "CLAIM_STATE",
    "GAP_STATE",
    "CONFLICT_STATE",
    "BOUNDARY_PRESERVATION_STATE",
    "DECISION_READINESS_STATE",
    "AUTHORITY_STATE",
]

EXPECTED_OUTPUTS = [
    "NO_DELTA",
    "DELTA_OBSERVED",
    "DELTA_GAP_OPENED",
    "DELTA_GAP_CLOSED_WITH_RECEIPT",
    "DELTA_CONFLICT_OPENED",
    "DELTA_CONFLICT_RESOLVED_WITH_RECEIPT",
    "DELTA_BOUNDARY_VIOLATION",
    "HOLD_INSUFFICIENT_REPLAY",
]

EXPECTED_PROFILES = [
    "AFRL_STYLE_RESEARCH_ASSURANCE",
    "USAF_STYLE_OPERATIONAL_TRAINING",
    "USSF_STYLE_CONTESTED_DATA",
    "AETC_STYLE_INSTRUCTION",
    "MAXWELL_STYLE_PME",
    "AIR_UNIVERSITY_STYLE_SYSTEMS_EDUCATION",
]

EXPECTED_ALLOWED = [
    "EVIDENCE_TYPE_MATCH",
    "VERIFICATION_RESULT",
    "RULE_SCOPE_BINDING",
    "EDGE_LOCAL_RECEIPT",
]

EXPECTED_FORBIDDEN = [
    "DICE_ROLL",
    "PLAYER_SCORE",
    "VOTE_COUNT",
    "POPULARITY",
    "DELTA_MAGNITUDE",
    "INSTITUTION_NAME",
    "ACTOR_ROLE",
]

EXPECTED_LAWS = [
    "DELTA != TRUTH",
    "DELTA != CAUSATION",
    "DELTA != AUTHORITY",
    "CHANGE_DETECTED != CHANGE_EXPLAINED",
    "SCORE_DELTA != EVIDENCE_DELTA",
    "TRAINING_CONTEXT != INSTITUTIONAL_ENDORSEMENT",
    "DICE = SCENARIO_SELECTOR",
    "DICE != VERDICT_GENERATOR",
    "GAMEPLAY != AUTHORITY",
    "HUMAN_RETAINS_CONSEQUENTIAL_AUTHORITY",
]


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    delta = load(DELTA)
    game = load(GAME)
    errors = []

    if delta.get("format") != "JSONWISDOM_DELTA_WORK_REPLAY_V0.1":
        errors.append("DELTA_FORMAT_INVALID")
    if delta.get("classification") != "SYNTHETIC_WORK_TRAINING_ORCHESTRATOR":
        errors.append("DELTA_CLASSIFICATION_INVALID")
    if delta.get("base_game") != game.get("game_id"):
        errors.append("BASE_GAME_BINDING_MISMATCH")
    if delta.get("delta_meaning") != "OBSERVED_CHANGE_BETWEEN_FROZEN_BEFORE_AND_AFTER_STATES":
        errors.append("DELTA_MEANING_INVALID")

    if delta.get("loop") != EXPECTED_LOOP:
        errors.append("DELTA_LOOP_MISMATCH")
    if delta.get("delta_axes") != EXPECTED_AXES:
        errors.append("DELTA_AXES_MISMATCH")
    if delta.get("delta_outputs") != EXPECTED_OUTPUTS:
        errors.append("DELTA_OUTPUTS_MISMATCH")

    profiles = [item.get("profile") for item in delta.get("work_context_profiles", [])]
    if profiles != EXPECTED_PROFILES:
        errors.append("WORK_CONTEXT_PROFILE_MISMATCH")

    boundary = delta.get("institutional_boundary", {})
    required_false = [
        "official_affiliation_claimed",
        "institutional_adoption_claimed",
        "institutional_endorsement_claimed",
        "real_mission_authority_created",
        "personnel_decision_use_authorized",
    ]
    if any(boundary.get(key) is not False for key in required_false):
        errors.append("INSTITUTIONAL_BOUNDARY_VIOLATION")

    gate = delta.get("promotion_gate", {})
    if gate.get("allowed_inputs") != EXPECTED_ALLOWED:
        errors.append("DELTA_ALLOWED_INPUTS_MISMATCH")
    if gate.get("forbidden_inputs") != EXPECTED_FORBIDDEN:
        errors.append("DELTA_FORBIDDEN_INPUTS_MISMATCH")

    if delta.get("laws") != EXPECTED_LAWS:
        errors.append("DELTA_LAWS_MISMATCH")
    if delta.get("verification_state") != "STRUCTURAL_VERIFIER_WIRED":
        errors.append("DELTA_VERIFIER_STATE_MISMATCH")
    if delta.get("verifier") != str(Path("tools/verify_delta_work_replay_v0_1.py")):
        errors.append("DELTA_VERIFIER_PATH_MISMATCH")
    if delta.get("workflow") != str(Path(".github/workflows/mind-the-gap-challenge-v0-1.yml")):
        errors.append("DELTA_WORKFLOW_PATH_MISMATCH")
    if delta.get("authority_created") is not False:
        errors.append("AUTHORITY_CREATED_MUST_BE_FALSE")

    ok = not errors
    out = {
        "verifier": "DELTA_WORK_REPLAY_VERIFIER_V0_1",
        "status": "PASS_WITH_BOUNDARY" if ok else "FAIL",
        "artifact_id": delta.get("artifact_id"),
        "profiles_checked": EXPECTED_PROFILES,
        "delta_axes_checked": EXPECTED_AXES,
        "boundaries": {
            "delta_is_not_truth": True,
            "delta_is_not_causation": True,
            "delta_is_not_authority": True,
            "training_context_is_not_institutional_endorsement": True,
            "human_retains_consequential_authority": True,
            "substantive_mission_suitability_proven": False,
            "institutional_adoption_proven": False,
        },
        "errors": errors,
        "authority_created": False,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
