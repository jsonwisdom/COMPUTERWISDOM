#!/usr/bin/env python3
"""Structural boundary verifier for the Air University -> DELTA crosswalk fixture.

This verifier checks the constitutional and cross-field invariants used by the
repository fixture. It does not claim to be a complete Draft-07 JSON Schema
implementation.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path("schemas/jaywisdom/au_delta_crosswalk.v1_0.schema.json")
FIXTURE_PATH = Path("fixtures/jaywisdom/challenge/AIR_UNIVERSITY_DELTA_CROSSWALK_V1_0.json")

EXPECTED_INVARIANTS = {
    "DELTA_NEQ_TRUTH": True,
    "DELTA_NEQ_CAUSATION": True,
    "DELTA_NEQ_AUTHORITY": True,
    "DICE_NEQ_VERDICT_GENERATOR": True,
    "HUMAN_RETAINS_CONSEQUENTIAL_AUTHORITY": True,
}


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    schema = load(SCHEMA_PATH)
    fixture = load(FIXTURE_PATH)
    errors: list[str] = []

    if schema.get("$schema") != "http://json-schema.org/draft-07/schema#":
        errors.append("SCHEMA_DIALECT_MISMATCH")

    class_size_schema = (
        schema.get("properties", {})
        .get("institution_observation", {})
        .get("properties", {})
        .get("observed_features", {})
        .get("properties", {})
        .get("class_size_observed", {})
    )
    any_of = class_size_schema.get("anyOf", [])
    if not any(option.get("type") == "null" for option in any_of):
        errors.append("CLASS_SIZE_NULL_NOT_ALLOWED")
    if not any(option.get("type") == "integer" for option in any_of):
        errors.append("CLASS_SIZE_INTEGER_NOT_ALLOWED")

    observation = fixture.get("institution_observation", {})
    observed_features = observation.get("observed_features", {})
    if observed_features.get("class_size_observed") is not None:
        errors.append("FIXTURE_CLASS_SIZE_MUST_REMAIN_UNOBSERVED")
    if not observation.get("source_reference"):
        errors.append("SOURCE_REFERENCE_MISSING")

    component = fixture.get("delta_component", {})
    if component.get("participant_count_conceptual") != 10:
        errors.append("CONCEPTUAL_PARTICIPANT_COUNT_CHANGED")

    boundary = fixture.get("boundary", {})
    expected_boundary = {
        "class_size_10_is_conceptual": True,
        "official_affiliation_claimed": False,
        "institutional_adoption_proven": False,
        "dice_verdict_authority": False,
        "human_consequential_authority": True,
    }
    for key, value in expected_boundary.items():
        if boundary.get(key) is not value:
            errors.append(f"BOUNDARY_MISMATCH:{key}")

    adoption = fixture.get("adoption_state", {})
    if adoption.get("status") != "NOT_ESTABLISHED":
        errors.append("ADOPTION_STATE_PROMOTION_VIOLATION")

    authority = fixture.get("authority_state", {})
    expected_authority = {
        "authority_created": False,
        "interception_authority": False,
        "official_affiliation_claimed": False,
    }
    for key, value in expected_authority.items():
        if authority.get(key) is not value:
            errors.append(f"AUTHORITY_MISMATCH:{key}")

    if fixture.get("constitutional_invariants") != EXPECTED_INVARIANTS:
        errors.append("CONSTITUTIONAL_INVARIANTS_MISMATCH")

    components = component.get("components", [])
    required_names = {
        "FREEZE_SCENARIO",
        "DICE_LEAHPRIME",
        "DISCUSSION_CELL",
        "ZIGGY",
        "GIRL_MATH",
        "PASS_GAP_CONFLICT_HOLD",
        "DELTA",
        "DEBRIEF",
    }
    names = {item.get("name") for item in components if isinstance(item, dict)}
    if names != required_names:
        errors.append("DELTA_COMPONENT_SET_MISMATCH")

    ok = not errors
    output = {
        "verifier": "AU_DELTA_CROSSWALK_VERIFIER_V1_0",
        "status": "PASS_WITH_BOUNDARY" if ok else "FAIL",
        "schema_dialect_checked": True,
        "full_schema_validation": False,
        "class_size_observed": observed_features.get("class_size_observed"),
        "participant_count_conceptual": component.get("participant_count_conceptual"),
        "institutional_adoption_proven": boundary.get("institutional_adoption_proven"),
        "official_affiliation_claimed": boundary.get("official_affiliation_claimed"),
        "authority_created": authority.get("authority_created"),
        "errors": errors,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
