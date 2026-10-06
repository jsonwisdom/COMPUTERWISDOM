#!/usr/bin/env python3
"""Structural verifier for the Dice LeahPrime gamification sidecar.

This verifier checks project invariants and exact binding to the already-frozen
Mind the Gap dice mapping. It is not a general Draft 2020-12 schema engine.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = Path("schemas/jaywisdom/gamification_membrane.v0_1.schema.json")
GAME = Path("fixtures/jaywisdom/challenge/LEAHPRIME_DICE_GAME_V0_1.json")
MAPPING = Path("fixtures/jaywisdom/challenge/MIND_THE_GAP_DICE_V0_1.json")

EXPECTED_ARENAS = {
    "MIND_THE_GAP",
    "CLAIM_EVIDENCE",
    "DELTA_QUADRATIC_VOTING",
    "PARTICIPANT_VECTOR",
    "FAMILY_MAP",
    "RESUME_GITHUB",
    "DELTA_REPLAY",
}
EXPECTED_ALLOWED = ["EVIDENCE_TYPE_MATCH", "VERIFICATION_RESULT", "RULE_SCOPE_BINDING"]
EXPECTED_FORBIDDEN = ["DICE_ROLL", "PLAYER_SCORE", "VOTE_COUNT", "POPULARITY"]


def raw(path: Path) -> bytes:
    return (ROOT / path).read_bytes()


def doc(path: Path):
    return json.loads(raw(path).decode("utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    schema = doc(SCHEMA)
    game = doc(GAME)
    mapping_bytes = raw(MAPPING)
    mapping = json.loads(mapping_bytes.decode("utf-8"))
    errors = []

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("SCHEMA_DIALECT_INVALID")

    if game.get("format") != "JSONWISDOM_GAMIFICATION_MEMBRANE_V0.1":
        errors.append("GAME_FORMAT_INVALID")
    if game.get("classification") != "SYNTHETIC_GAME_LAYER":
        errors.append("GAME_CLASSIFICATION_INVALID")

    base = game.get("base_mapping", {})
    if base.get("mapping_id") != mapping.get("mapping_id"):
        errors.append("MAPPING_ID_MISMATCH")
    if base.get("path") != str(MAPPING):
        errors.append("MAPPING_PATH_MISMATCH")
    if base.get("sha256") != sha(mapping_bytes):
        errors.append("MAPPING_SHA256_MISMATCH")

    roles = game.get("roles", {})
    expected_roles = {
        "dice_leahprime": "SCENARIO_PRESENTER",
        "ziggy": "ADVERSARIAL_QUESTIONER",
        "girlmath": "EVIDENCE_DENOMINATOR_AUDITOR",
        "receiptos": "EVENT_RECORDER",
        "human": "CONSEQUENTIAL_AUTHORITY",
    }
    if roles != expected_roles:
        errors.append("ROLE_BOUNDARY_MISMATCH")

    arenas = game.get("arenas", [])
    if set(arenas) != EXPECTED_ARENAS or len(arenas) != len(EXPECTED_ARENAS):
        errors.append("ARENA_SET_MISMATCH")

    scoring = game.get("scoring", {})
    if scoring.get("score_changes_epistemic_state") is not False:
        errors.append("SCORE_PROMOTION_VIOLATION")
    if scoring.get("overclaim_penalty", 1) >= 0:
        errors.append("OVERCLAIM_PENALTY_INVALID")

    gate = game.get("promotion_gate", {})
    if gate.get("allowed_inputs") != EXPECTED_ALLOWED:
        errors.append("PROMOTION_ALLOWED_INPUTS_MISMATCH")
    if gate.get("forbidden_inputs") != EXPECTED_FORBIDDEN:
        errors.append("PROMOTION_FORBIDDEN_INPUTS_MISMATCH")

    laws = game.get("laws", {})
    if not laws or not all(value is True for value in laws.values()):
        errors.append("GAME_LAW_DISABLED")

    if game.get("win_condition") != "MAXIMIZE_CORRECT_CLASSIFICATION_WITHOUT_OVERCLAIM":
        errors.append("WIN_CONDITION_INVALID")
    if game.get("authority_created") is not False:
        errors.append("AUTHORITY_CREATED_MUST_BE_FALSE")

    ok = not errors
    out = {
        "verifier": "LEAHPRIME_DICE_GAME_VERIFIER_V0_1",
        "status": "PASS_WITH_BOUNDARY" if ok else "FAIL",
        "game_id": game.get("game_id"),
        "mapping_sha256": sha(mapping_bytes),
        "arenas_checked": sorted(EXPECTED_ARENAS),
        "promotion_inputs": EXPECTED_ALLOWED,
        "forbidden_promotion_inputs": EXPECTED_FORBIDDEN,
        "boundaries": {
            "dice_selects_scenario_not_verdict": True,
            "player_score_does_not_create_evidence": True,
            "quadratic_votes_are_priority_only": True,
            "story_does_not_promote_history": True,
            "gameplay_does_not_create_authority": True,
            "draft_2020_12_declared": True,
            "full_schema_validation": False,
        },
        "errors": errors,
        "authority_created": False,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
