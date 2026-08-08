import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from matrix.router import POLICY_DIGEST, project_anomaly_observation, route, route_anomaly_report

OBSERVATION_VALIDATOR = jsonschema.Draft7Validator(
    json.loads((ROOT / "schemas" / "routing_observation.schema.json").read_text())
)
RECEIPT_VALIDATOR = jsonschema.Draft7Validator(
    json.loads((ROOT / "schemas" / "routing_receipt.schema.json").read_text())
)


def routing_observation():
    return {
        "where": "R2-COUNTY042",
        "what": "weather_alert",
        "severity_score": 0.6,
        "digest": "a" * 64,
    }


def anomaly_observation():
    return {
        "where": "R2-COUNTY042",
        "when": "2026-08-08T18:00:00+00:00",
        "what": "weather_alert",
        "baseline": 0.0,
        "delta": 1.0,
        "corroboration": 2,
        "confidence": 0.9,
        "severity": "HIGH",
        "sources": ["nws:sha256:" + "a" * 64],
    }


@pytest.mark.parametrize(
    "bad_where",
    ["123 Main St", "R6-PERSON007", "R2-COUNTY042/ADDRESS1", "47.1,-94.2"],
)
def test_router_rejects_person_or_non_ring_scope(bad_where):
    observation = routing_observation()
    observation["where"] = bad_where
    with pytest.raises(ValueError):
        route(observation)


def test_closed_input_rejects_metadata_leakage():
    observation = routing_observation()
    observation["person_name"] = "prohibited"
    with pytest.raises(ValueError):
        route(observation)
    assert list(OBSERVATION_VALIDATOR.iter_errors(observation))


def test_routing_is_deterministic_and_schema_valid():
    first = route(routing_observation())
    second = route(copy.deepcopy(routing_observation()))
    assert first == second
    assert first["policy_digest"] == POLICY_DIGEST
    assert first["authority_created"] is False
    RECEIPT_VALIDATOR.validate(first)


def test_consequential_class_requires_human_authorization():
    observation = routing_observation()
    observation.update(what="infrastructure_outage", severity_score=1.0)
    receipt = route(observation)
    assert receipt["routing_class"] == "RESOURCE_COORDINATION"
    assert receipt["human_authorization_required"] is True
    assert receipt["authority_created"] is False


def test_projection_binds_full_anomaly_observation():
    first = project_anomaly_observation(anomaly_observation())
    changed = anomaly_observation()
    changed["confidence"] = 0.8
    second = project_anomaly_observation(changed)
    assert first["digest"] != second["digest"]
    OBSERVATION_VALIDATOR.validate(first)


def test_report_routing_is_order_independent():
    first = anomaly_observation()
    second = anomaly_observation()
    second.update(what="traffic_disruption", severity="MEDIUM")
    report = {"source": "locality_anomaly", "observations": [first, second]}
    reversed_report = {"source": "locality_anomaly", "observations": [second, first]}
    assert route_anomaly_report(report) == route_anomaly_report(reversed_report)


def test_no_receipt_can_contain_authority_true():
    receipts = route_anomaly_report(
        {"source": "locality_anomaly", "observations": [anomaly_observation()]}
    )
    assert receipts
    assert all(receipt["authority_created"] is False for receipt in receipts)
