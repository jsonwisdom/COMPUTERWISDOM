import copy
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import replay.handoff as handoff_module
from decomposition.agent import decompose_claim
from replay.aggregator import aggregate_results
from replay.executor import run_replay
from replay.handoff import run_replay_handoff
from replay.receipt_builder import receipt_digest_payload, sha256_json
from replay.validators.schema_validator import SchemaValidator

BASELINE = "c44fd4423ec412de811edbc8e41f7781bc880cea"
UPDATED_RECEIPT_SCHEMA = json.loads(
    (ROOT / "schemas" / "receipt.schema.json").read_text(encoding="utf-8")
)


def sample_work_order(token_weight=42.0):
    work_order = decompose_claim(
        "Replay fixture claim",
        parent_id="fixture_parent",
        token_weight=token_weight,
    )[0]
    work_order["work_order_id"] = "JOY-CD8D67E3"
    return work_order


def test_existing_work_order_remains_pass():
    """JOY-CD8D67E3 remains clean under the v0.2 validator family."""
    receipt = run_replay_handoff(sample_work_order(), BASELINE)

    assert receipt["semantic_validation"]["result"] == "PASS"
    details = receipt["semantic_validation"]["details"]
    assert details["overall_status"] == "PASS"
    assert details["aggregate_score"] >= 0.9
    assert set(details["dimensions"]) == {"dependency", "range", "schema"}
    assert len(receipt["anomalies"]) == 0
    assert "authority_created" not in receipt
    jsonschema.validate(instance=receipt, schema=UPDATED_RECEIPT_SCHEMA)


def test_missing_required_field_is_anomaly_not_validator_failure(monkeypatch):
    work_order = sample_work_order()
    replay_result = copy.deepcopy(run_replay(work_order, BASELINE))
    replay_result["observed_outputs"][0].pop("authority_created")

    monkeypatch.setattr(
        handoff_module,
        "run_replay",
        lambda supplied_work_order, supplied_baseline: replay_result,
    )
    receipt = run_replay_handoff(work_order, BASELINE)

    assert receipt["semantic_validation"]["result"] == "PASS"
    assert receipt["semantic_validation"]["details"]["overall_status"] == "ANOMALY"
    assert any(
        anomaly["type"] == "missing_required_field"
        and anomaly["severity"] == "HIGH"
        for anomaly in receipt["anomalies"]
    )
    assert "authority_created" not in receipt
    jsonschema.validate(instance=receipt, schema=UPDATED_RECEIPT_SCHEMA)


def test_quadratic_weight_never_changes_validation_outcome():
    low = run_replay_handoff(sample_work_order(token_weight=0.0), BASELINE)
    high = run_replay_handoff(sample_work_order(token_weight=1_000_000.0), BASELINE)

    low_details = low["semantic_validation"]["details"]
    high_details = high["semantic_validation"]["details"]
    assert low_details["overall_status"] == high_details["overall_status"] == "PASS"
    assert low_details["aggregate_score"] == high_details["aggregate_score"]
    assert low_details["dimensions"] == high_details["dimensions"]


def test_aggregate_score_is_bounded_and_high_anomaly_overrides_status():
    result = aggregate_results(
        [
            {"name": "a", "status": "PASS", "score": 1.0},
            {"name": "b", "status": "PASS", "score": 0.0},
        ],
        [],
    )
    assert 0.0 <= result["aggregate_score"] <= 1.0
    assert result["aggregate_score"] == 0.7071

    anomalous = aggregate_results(
        [{"name": "a", "status": "FAIL", "score": 0.0}],
        [
            {
                "type": "logical_contradiction",
                "severity": "HIGH",
                "description": "Injected high severity anomaly.",
            }
        ],
    )
    assert anomalous["overall_status"] == "ANOMALY"


def test_aggregate_score_is_excluded_from_receipt_digest_only():
    receipt = run_replay_handoff(sample_work_order(), BASELINE)
    digest = receipt["receipt_digest"]

    score_only_change = copy.deepcopy(receipt)
    score_only_change["semantic_validation"]["details"]["aggregate_score"] = 0.1234
    assert sha256_json(receipt_digest_payload(score_only_change)) == digest

    dimension_change = copy.deepcopy(receipt)
    dimension_change["semantic_validation"]["details"]["dimensions"]["range"]["score"] = 0.5
    assert sha256_json(receipt_digest_payload(dimension_change)) != digest


def test_schema_validator_uses_declared_json_schema():
    validator = SchemaValidator()
    work_order = sample_work_order()
    work_order["output_schema"] = {
        "type": "object",
        "required": ["claim_text"],
        "properties": {"claim_text": {"type": "string"}},
    }

    passed = validator.validate(work_order, [{"claim_text": "ok"}])
    failed = validator.validate(work_order, [{"claim_text": 7}])

    assert passed["status"] == "PASS"
    assert passed["score"] == 1.0
    assert failed["status"] == "FAIL"
    assert failed["score"] == 0.0
