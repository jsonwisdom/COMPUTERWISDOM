"""
tests/test_trigger_evaluator_receipt_integration_v0_1.py
Integration tests for watch_receipt_v0_1.schema.json + tools/trigger_evaluator_v0_1.py
"""

import json
import jsonschema
import pytest
from pathlib import Path
from tools.trigger_evaluator_v0_1 import TriggerEvaluator

SCHEMA_PATH = Path("schemas/watch_receipt_v0_1.schema.json")
with open(SCHEMA_PATH) as f:
    RECEIPT_SCHEMA = json.load(f)


def test_schema_valid_unverified_receipt_evaluates_observe():
    receipt = {
        "watch_id": "WATCH_INT_001",
        "trigger_id": "TRIGGER_INT_001",
        "collected_at": "2026-06-03T10:00:00Z",
        "source_url": "https://example.gov/doc",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "verified": False,
        "verifier": None,
        "authority": False,
    }
    trigger = {
        "trigger_id": "TRIGGER_INT_001",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "state_transition": {"from_level": 2, "to_level": 3},
    }

    jsonschema.validate(instance=receipt, schema=RECEIPT_SCHEMA)
    evaluator = TriggerEvaluator({}, RECEIPT_SCHEMA)
    result = evaluator.evaluate(trigger, receipt)

    assert result["status"] == "OBSERVE"
    assert result["state_transition"] is False
    assert result["authority"] is False


def test_schema_valid_verified_matching_receipt_evaluates_transition_ready():
    receipt = {
        "watch_id": "WATCH_INT_001",
        "trigger_id": "TRIGGER_INT_001",
        "collected_at": "2026-06-03T10:00:00Z",
        "source_url": "https://example.gov/omb-memo-001",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "hash": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "verified": True,
        "verifier": "human",
        "authority": False,
    }
    trigger = {
        "trigger_id": "TRIGGER_INT_001",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "state_transition": {"from_level": 2, "to_level": 3},
    }

    jsonschema.validate(instance=receipt, schema=RECEIPT_SCHEMA)
    evaluator = TriggerEvaluator({}, RECEIPT_SCHEMA)
    result = evaluator.evaluate(trigger, receipt)

    assert result["status"] == "TRANSITION_READY"
    assert result["state_transition"] is True
    assert result["authority"] is False


def test_schema_invalid_authority_true_rejected_before_evaluator():
    receipt = {
        "watch_id": "WATCH_INT_001",
        "trigger_id": "TRIGGER_INT_001",
        "collected_at": "2026-06-03T10:00:00Z",
        "source_url": "https://example.gov/doc",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "hash": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "verified": True,
        "verifier": "human",
        "authority": True,
    }

    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(instance=receipt, schema=RECEIPT_SCHEMA)
