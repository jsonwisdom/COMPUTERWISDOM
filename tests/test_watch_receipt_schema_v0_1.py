"""
tests/test_watch_receipt_schema_v0_1.py
Schema validation vectors for watch_receipt_v0_1.schema.json
"""

import json
import jsonschema
import pytest
from pathlib import Path

SCHEMA_PATH = Path("schemas/watch_receipt_v0_1.schema.json")
with open(SCHEMA_PATH) as f:
    RECEIPT_SCHEMA = json.load(f)


def test_valid_unverified_observe_receipt():
    receipt = {
        "watch_id": "WATCH_001",
        "trigger_id": "TRIGGER_001",
        "collected_at": "2026-06-03T10:00:00Z",
        "source_url": "https://example.gov/doc",
        "source_domain": "example.gov",
        "artifact_type": "press_release",
        "hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "verified": False,
        "verifier": None,
        "authority": False,
    }
    jsonschema.validate(instance=receipt, schema=RECEIPT_SCHEMA)


def test_invalid_authority_true_receipt():
    receipt = {
        "watch_id": "WATCH_001",
        "trigger_id": "TRIGGER_001",
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
