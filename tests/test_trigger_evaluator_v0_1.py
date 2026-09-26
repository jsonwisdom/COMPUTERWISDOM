"""
tests/test_trigger_evaluator_v0_1.py
Three-state test vectors for watch_trigger_engine_v0_1
Enforces strict binary: MAINTAIN / OBSERVE / TRANSITION_READY
"""

import json
from pathlib import Path

import jsonschema
import pytest

from tools.trigger_evaluator_v0_1 import TriggerEvaluationRejected, TriggerEvaluator

trigger_schema = {}
receipt_schema = {}

evaluator = TriggerEvaluator(trigger_schema, receipt_schema)

_TRIGGER_SCHEMA = json.loads(Path("schemas/trigger_v0_1.schema.json").read_text(encoding="utf-8"))
_RECEIPT_SCHEMA = json.loads(Path("schemas/watch_receipt_v0_1.schema.json").read_text(encoding="utf-8"))
_VALID_HASH = "sha256:" + ("b" * 64)


def test_maintain_no_receipt():
    trigger = {
        "watch_id": "TEST_WATCH",
        "trigger_id": "TEST_TRIGGER",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "state_transition": {"from_level": 2, "to_level": 3},
    }
    receipt = {
        "source_domain": "example.com",
        "artifact_type": "other",
        "verified": False,
    }
    result = evaluator.evaluate(trigger, receipt)
    assert result["status"] == "MAINTAIN"
    assert result["state_transition"] is False


def test_observe_unverified_receipt():
    trigger = {
        "watch_id": "TEST_WATCH",
        "trigger_id": "TEST_TRIGGER",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "state_transition": {"from_level": 2, "to_level": 3},
    }
    receipt = {
        "source_domain": "example.gov",
        "artifact_type": "press_release",
        "verified": False,
    }
    result = evaluator.evaluate(trigger, receipt)
    assert result["status"] == "OBSERVE"
    assert result["state_transition"] is False


def test_transition_ready_verified_match():
    trigger = {
        "watch_id": "TEST_WATCH",
        "trigger_id": "TEST_TRIGGER",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "state_transition": {"from_level": 2, "to_level": 3},
    }
    receipt = {
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "verified": True,
        "verifier": "human",
    }
    result = evaluator.evaluate(trigger, receipt)
    assert result["status"] == "TRANSITION_READY"
    assert result["state_transition"] is True
    assert result["from_level"] == 2
    assert result["to_level"] == 3


def _schema_conforming_pair():
    trigger = {
        "watch_id": "WATCH_INT_001",
        "trigger_id": "TRIGGER_INT_001",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "state_transition": {"from_level": 2, "to_level": 3},
        "authority": False,
    }
    receipt = {
        "watch_id": "WATCH_INT_001",
        "trigger_id": "TRIGGER_INT_001",
        "collected_at": "2026-06-03T10:00:00Z",
        "source_url": "https://example.gov/omb-memo-001",
        "source_domain": "example.gov",
        "artifact_type": "omb_memo",
        "hash": _VALID_HASH,
        "verified": True,
        "verifier": "human",
        "authority": False,
    }
    return trigger, receipt


def _reject(trigger, receipt, match):
    with pytest.raises(TriggerEvaluationRejected, match=match):
        evaluator.evaluate(trigger, receipt)


@pytest.mark.parametrize("side", ["trigger", "receipt"])
def test_reject_authority_true(side):
    trigger, receipt = _schema_conforming_pair()
    target = trigger if side == "trigger" else receipt
    target["authority"] = True
    _reject(trigger, receipt, "authority")


@pytest.mark.parametrize("mutation", ["missing", "empty", "invalid"])
@pytest.mark.parametrize("side", ["trigger", "receipt", "both"])
def test_reject_missing_domain(mutation, side):
    trigger, receipt = _schema_conforming_pair()
    targets = []
    if side in ("trigger", "both"):
        targets.append(trigger)
    if side in ("receipt", "both"):
        targets.append(receipt)
    for target in targets:
        if mutation == "missing":
            target.pop("source_domain")
        elif mutation == "empty":
            target["source_domain"] = ""
        elif mutation == "invalid":
            target["source_domain"] = "not a host"
        else:
            raise AssertionError(mutation)
    _reject(trigger, receipt, "source_domain")


@pytest.mark.parametrize("mutation", ["missing", "empty", "null"])
@pytest.mark.parametrize("side", ["trigger", "receipt", "both"])
def test_reject_missing_artifact_type(mutation, side):
    trigger, receipt = _schema_conforming_pair()
    targets = []
    if side in ("trigger", "both"):
        targets.append(trigger)
    if side in ("receipt", "both"):
        targets.append(receipt)
    for target in targets:
        if mutation == "missing":
            target.pop("artifact_type")
        elif mutation == "empty":
            target["artifact_type"] = ""
        elif mutation == "null":
            target["artifact_type"] = None
        else:
            raise AssertionError(mutation)
    _reject(trigger, receipt, "artifact_type")


def test_reject_verified_string_true():
    trigger, receipt = _schema_conforming_pair()
    receipt["verified"] = "true"
    _reject(trigger, receipt, "verified")


def test_reject_verified_int_one():
    trigger, receipt = _schema_conforming_pair()
    receipt["verified"] = 1
    _reject(trigger, receipt, "verified")


def test_reject_null_receipt():
    trigger, _receipt = _schema_conforming_pair()
    _reject(trigger, None, "receipt must be an object")


def test_reject_list_receipt():
    trigger, _receipt = _schema_conforming_pair()
    _reject(trigger, [], "receipt must be an object")


def test_reject_null_trigger():
    _trigger, receipt = _schema_conforming_pair()
    _reject(None, receipt, "trigger must be an object")


def test_reject_list_trigger():
    _trigger, receipt = _schema_conforming_pair()
    _reject([], receipt, "trigger must be an object")


@pytest.mark.parametrize(
    "state_transition",
    [
        pytest.param(None, id="null"),
        pytest.param([], id="list"),
        pytest.param({"from_level": 2}, id="missing-to-level"),
        pytest.param({"from_level": "2", "to_level": "3"}, id="string-levels"),
        pytest.param({"from_level": 2, "to_level": 3, "extra": 1}, id="extra-field"),
        pytest.param({"from_level": -1, "to_level": 2}, id="negative-level"),
        pytest.param({"from_level": True, "to_level": 3}, id="bool-level"),
        pytest.param({"from_level": 2.0, "to_level": 3}, id="float-level"),
    ],
)
def test_reject_invalid_state_transition(state_transition):
    trigger, receipt = _schema_conforming_pair()
    trigger["state_transition"] = state_transition
    _reject(trigger, receipt, "state_transition")


def test_reject_same_level_transition():
    trigger, receipt = _schema_conforming_pair()
    trigger["state_transition"] = {"from_level": 2, "to_level": 2}
    jsonschema.validate(instance=trigger, schema=_TRIGGER_SCHEMA)
    _reject(trigger, receipt, "same-level")


def test_reject_downgrade_transition():
    trigger, receipt = _schema_conforming_pair()
    trigger["state_transition"] = {"from_level": 3, "to_level": 2}
    jsonschema.validate(instance=trigger, schema=_TRIGGER_SCHEMA)
    _reject(trigger, receipt, "downgrade")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("collected_at", "2026-06-03"),
        ("collected_at", "not-a-date"),
        ("source_url", "example.gov/doc"),
        ("source_url", "not a uri"),
    ],
)
def test_reject_invalid_receipt_format(field, value):
    trigger, receipt = _schema_conforming_pair()
    receipt[field] = value
    _reject(trigger, receipt, field)


@pytest.mark.parametrize(
    "hash_value",
    ["not-a-hash", "sha256:" + ("a" * 63), "sha256:" + ("g" * 64)],
)
def test_reject_invalid_hash(hash_value):
    trigger, receipt = _schema_conforming_pair()
    receipt["hash"] = hash_value
    _reject(trigger, receipt, "hash")


@pytest.mark.parametrize(
    ("side", "trigger_id"),
    [("trigger", ""), ("trigger", 123), ("receipt", ""), ("receipt", 123)],
)
def test_reject_invalid_trigger_identifier(side, trigger_id):
    trigger, receipt = _schema_conforming_pair()
    target = trigger if side == "trigger" else receipt
    target["trigger_id"] = trigger_id
    _reject(trigger, receipt, "trigger_id")


@pytest.mark.parametrize(
    ("side", "field"),
    [
        ("trigger", "trigger_id"),
        ("trigger", "state_transition"),
        ("receipt", "verified"),
    ],
)
def test_reject_missing_required_fields(side, field):
    trigger, receipt = _schema_conforming_pair()
    target = trigger if side == "trigger" else receipt
    target.pop(field)
    _reject(trigger, receipt, field)


def test_supplied_schema_rejects_missing_hash():
    trigger, receipt = _schema_conforming_pair()
    receipt.pop("hash")
    strict = TriggerEvaluator({}, _RECEIPT_SCHEMA)
    with pytest.raises(TriggerEvaluationRejected, match="hash"):
        strict.evaluate(trigger, receipt)


def test_supplied_schema_rejects_missing_authority():
    trigger, receipt = _schema_conforming_pair()
    trigger.pop("authority")
    strict = TriggerEvaluator(_TRIGGER_SCHEMA, {})
    with pytest.raises(TriggerEvaluationRejected, match="authority"):
        strict.evaluate(trigger, receipt)


def test_schema_conforming_verified_receipt_is_transition_ready():
    trigger, receipt = _schema_conforming_pair()
    jsonschema.validate(instance=trigger, schema=_TRIGGER_SCHEMA)
    jsonschema.validate(instance=receipt, schema=_RECEIPT_SCHEMA)
    result = evaluator.evaluate(trigger, receipt)
    assert result["status"] == "TRANSITION_READY"
    assert result["state_transition"] is True
    assert result["from_level"] == 2
    assert result["to_level"] == 3
    assert result["authority"] is False
