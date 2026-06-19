import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "ers.v0_1.schema.json"
EXAMPLES_DIR = ROOT / "examples"

EXPECTED_SCHEMA_VERSION = "ERS_V0_1"
EXPECTED_CONSTITUTIONAL_ROOT = "808f2b1c6c339eb46e68a2161da3cca22f7b0eeb"
EXPECTED_AUTHORITY = False
EXPECTED_AUTHORITY_BOUNDARY = "NONE"

REPLAY_CRITICAL_FIELDS = {
    "artifact_id",
    "artifact_type",
    "timestamp",
    "lineage_root",
    "constitutional_root",
    "schema_version",
    "hash",
}

GOVERNANCE_FIELDS = {
    "authority",
    "authority_boundary",
}

EXAMPLE_FILES = [
    "event_example.json",
    "observation_example.json",
    "dispute_example.json",
    "adjudication_example.json",
    "protocol_example.json",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_schema_declares_required_replay_and_governance_fields():
    schema = load_json(SCHEMA_PATH)
    required = set(schema["required"])

    assert REPLAY_CRITICAL_FIELDS.issubset(required)
    assert GOVERNANCE_FIELDS.issubset(required)

    assert schema["properties"]["schema_version"]["const"] == EXPECTED_SCHEMA_VERSION
    assert schema["properties"]["constitutional_root"]["const"] == EXPECTED_CONSTITUTIONAL_ROOT
    assert schema["properties"]["authority"]["const"] is EXPECTED_AUTHORITY
    assert schema["properties"]["authority_boundary"]["const"] == EXPECTED_AUTHORITY_BOUNDARY


def test_examples_validate_against_schema():
    schema = load_json(SCHEMA_PATH)
    validator = jsonschema.Draft202012Validator(schema)

    for filename in EXAMPLE_FILES:
        artifact = load_json(EXAMPLES_DIR / filename)
        errors = sorted(validator.iter_errors(artifact), key=lambda error: error.path)
        assert not errors, f"{filename} failed ERS_V0_1 schema validation: {errors}"


def test_examples_preserve_replay_and_governance_boundary():
    for filename in EXAMPLE_FILES:
        artifact = load_json(EXAMPLES_DIR / filename)

        for field in REPLAY_CRITICAL_FIELDS:
            assert field in artifact, f"{filename} missing replay-critical field: {field}"

        for field in GOVERNANCE_FIELDS:
            assert field in artifact, f"{filename} missing governance field: {field}"

        assert artifact["schema_version"] == EXPECTED_SCHEMA_VERSION
        assert artifact["constitutional_root"] == EXPECTED_CONSTITUTIONAL_ROOT
        assert artifact["authority"] is EXPECTED_AUTHORITY
        assert artifact["authority_boundary"] == EXPECTED_AUTHORITY_BOUNDARY
