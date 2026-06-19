"""
tests/test_trigger_evaluator_v0_1.py
Three-state test vectors for watch_trigger_engine_v0_1
Enforces strict binary: MAINTAIN / OBSERVE / TRANSITION_READY
"""

from tools.trigger_evaluator_v0_1 import TriggerEvaluator

trigger_schema = {}
receipt_schema = {}

evaluator = TriggerEvaluator(trigger_schema, receipt_schema)


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
