import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from decomposition.agent import decompose_claim
from replay.handoff import run_replay_handoff
from replay.receipt_builder import sha256_json
from replay.semantic_validator import SemanticValidator

BASELINE = "c44fd4423ec412de811edbc8e41f7781bc880cea"
RECEIPT_SCHEMA = json.loads(
    (ROOT / "schemas" / "receipt.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = jsonschema.Draft202012Validator(RECEIPT_SCHEMA)


def sample_work_order():
    return decompose_claim(
        "Replay fixture claim",
        parent_id="fixture_parent",
        token_weight=42.0,
    )[0]


def test_replay_is_deterministic():
    """Same work order + baseline + implementation -> identical receipt digest."""
    work_order = sample_work_order()

    receipt1 = run_replay_handoff(work_order, BASELINE)
    receipt2 = run_replay_handoff(work_order, BASELINE)

    assert receipt1["receipt_digest"] == receipt2["receipt_digest"]
    assert receipt1["execution_trace"]["seed"] == receipt2["execution_trace"]["seed"]
    assert (
        receipt1["execution_trace"]["implementation_hash"]
        == receipt2["execution_trace"]["implementation_hash"]
    )


def test_receipt_validates_against_schema():
    receipt = run_replay_handoff(sample_work_order(), BASELINE)
    VALIDATOR.validate(receipt)


def test_authority_never_created_by_handoff():
    receipt = run_replay_handoff(sample_work_order(), BASELINE)
    assert "authority_created" not in receipt
    assert receipt["semantic_validation"]["result"] in {"PASS", "FAIL"}


def test_stub_pass_does_not_claim_semantic_correctness():
    receipt = run_replay_handoff(sample_work_order(), BASELINE)
    assert receipt["semantic_validation"]["result"] == "PASS"
    assert "semantic correctness is not asserted" in receipt["semantic_validation"]["reason"]
    assert "Evidence refs bound: 1" in receipt["semantic_validation"]["reason"]


def test_receipt_digest_covers_execution_trace_and_validation():
    receipt = run_replay_handoff(sample_work_order(), BASELINE)
    digest = receipt.pop("receipt_digest")
    assert digest == sha256_json(receipt)


def test_baseline_changes_seed_and_receipt_digest():
    work_order = sample_work_order()
    receipt1 = run_replay_handoff(work_order, BASELINE)
    receipt2 = run_replay_handoff(work_order, "a" * 40)

    assert receipt1["execution_trace"]["seed"] != receipt2["execution_trace"]["seed"]
    assert receipt1["receipt_digest"] != receipt2["receipt_digest"]


def test_work_order_hash_is_canonical_across_key_order():
    work_order = sample_work_order()
    reversed_work_order = dict(reversed(list(work_order.items())))

    receipt1 = run_replay_handoff(work_order, BASELINE)
    receipt2 = run_replay_handoff(reversed_work_order, BASELINE)

    assert (
        receipt1["execution_trace"]["work_order_hash"]
        == receipt2["execution_trace"]["work_order_hash"]
    )
    assert receipt1["receipt_digest"] == receipt2["receipt_digest"]


def test_joy_work_order_identifier_is_forward_compatible():
    work_order = sample_work_order()
    work_order["work_order_id"] = "JOY-CD8D67E3"

    receipt = run_replay_handoff(work_order, BASELINE)

    assert receipt["work_order_id"] == "JOY-CD8D67E3"
    VALIDATOR.validate(receipt)


class FailingValidator(SemanticValidator):
    def validate(self, work_order, observed_outputs, evidence_refs):
        assert work_order
        assert observed_outputs
        assert evidence_refs
        return {"result": "FAIL", "reason": "Deliberate test failure."}


def test_fail_validation_is_recorded_not_promoted_to_authority():
    receipt = run_replay_handoff(
        sample_work_order(),
        BASELINE,
        validator=FailingValidator(),
    )

    assert receipt["semantic_validation"]["result"] == "FAIL"
    assert "authority_created" not in receipt
    VALIDATOR.validate(receipt)
