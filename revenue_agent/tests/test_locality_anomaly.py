import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from anomaly.baseline import BaselineStore, ImmutableStoreConflict, SnapshotStore
from anomaly.engine import LocalityAnomalyEngine
from anomaly.signals import NWSWeatherAlertsSignal
from anomaly.validator import LocalityAnomalyValidator
from decomposition.agent import decompose_claim
from replay.handoff import run_replay_handoff

BASELINE = "6caa38221c9f509c3ebe895a1c9ec0b45b9d2f93"
LOCALITY = "R2-COUNTY042"
WINDOW = "24h"
OBSERVATION_SCHEMA = json.loads(
    (ROOT / "schemas" / "anomaly_observation.schema.json").read_text(encoding="utf-8")
)
RECEIPT_SCHEMA = json.loads(
    (ROOT / "schemas" / "receipt.schema.json").read_text(encoding="utf-8")
)


class FakeSignals:
    def __init__(self, signals=None):
        self.calls = 0
        self.signals = signals or [
            {
                "what": "weather_alert",
                "when": "2026-08-08T18:00:00+00:00",
                "value": 1.0,
                "confidence": 0.9,
                "severity": "MEDIUM",
                "sources": ["nws:sha256:" + "a" * 64],
            }
        ]

    def fetch_all(self, locality, time_window):
        assert locality == LOCALITY
        assert time_window == WINDOW
        self.calls += 1
        return copy.deepcopy(self.signals)


def make_engine(tmp_path, signals=None):
    provider = FakeSignals(signals)
    snapshots = SnapshotStore(tmp_path / "snapshots")
    baselines = BaselineStore(tmp_path / "baselines")
    engine = LocalityAnomalyEngine(provider, snapshots, baselines)
    return engine, provider, snapshots, baselines


def locality_work_order():
    work_order = decompose_claim(
        "Locality-scoped replay fixture",
        parent_id="fixture_parent",
        token_weight=42.0,
    )[0]
    work_order["locality"] = LOCALITY
    work_order["time_window"] = WINDOW
    return work_order


def freeze_default(engine, baselines):
    engine.capture_snapshot(LOCALITY, WINDOW, BASELINE)
    baselines.put(LOCALITY, WINDOW, BASELINE, {"weather_alert": 0.0})


def test_no_pii_in_observations(tmp_path):
    engine, _, _, baselines = make_engine(tmp_path)
    freeze_default(engine, baselines)
    report = engine.analyze(LOCALITY, WINDOW, BASELINE)

    assert report["locality"] == LOCALITY
    for observation in report["observations"]:
        jsonschema.Draft7Validator(OBSERVATION_SCHEMA).validate(observation)
        rendered = json.dumps(observation, sort_keys=True).lower()
        assert "person" not in rendered
        assert "address" not in rendered
        assert "headline" not in rendered
        assert "description" not in rendered
        assert observation["where"] == LOCALITY


def test_replay_is_deterministic_from_frozen_snapshot(tmp_path):
    engine, provider, _, baselines = make_engine(tmp_path)
    freeze_default(engine, baselines)

    first = engine.analyze(LOCALITY, WINDOW, BASELINE)
    second = engine.analyze(LOCALITY, WINDOW, BASELINE)

    assert first == second
    assert first["snapshot_digest"] == second["snapshot_digest"]
    assert first["baseline_digest"] == second["baseline_digest"]
    assert provider.calls == 1


def test_capture_snapshot_never_refetches_same_key(tmp_path):
    engine, provider, _, _ = make_engine(tmp_path)
    first = engine.capture_snapshot(LOCALITY, WINDOW, BASELINE)
    second = engine.capture_snapshot(LOCALITY, WINDOW, BASELINE)

    assert provider.calls == 1
    assert first == second


def test_snapshot_store_is_immutable(tmp_path):
    _, _, snapshots, _ = make_engine(tmp_path)
    signals_a = [
        {
            "what": "weather_alert",
            "when": "2026-08-08T18:00:00+00:00",
            "value": 1.0,
            "confidence": 0.9,
            "severity": "LOW",
            "sources": ["nws:sha256:" + "a" * 64],
        }
    ]
    signals_b = copy.deepcopy(signals_a)
    signals_b[0]["severity"] = "HIGH"

    snapshots.put(LOCALITY, WINDOW, BASELINE, signals_a)
    with pytest.raises(ImmutableStoreConflict):
        snapshots.put(LOCALITY, WINDOW, BASELINE, signals_b)


def test_validator_ignores_attention_score():
    validator = LocalityAnomalyValidator()
    work_order = {"locality": LOCALITY, "time_window": WINDOW}
    report = {
        "source": "locality_anomaly",
        "engine_version": "v0.1",
        "locality": LOCALITY,
        "time_window": WINDOW,
        "snapshot_digest": "a" * 64,
        "baseline_digest": "b" * 64,
        "observations": [
            {
                "where": LOCALITY,
                "when": "2026-08-08T18:00:00+00:00",
                "what": "weather_alert",
                "baseline": 0.0,
                "delta": 1.0,
                "corroboration": 3,
                "confidence": 0.9,
                "severity": "HIGH",
                "sources": ["nws:sha256:" + "a" * 64],
                "attention_score": 999999,
            }
        ],
    }

    result = validator.validate(work_order, [report])

    assert result["status"] == "FAIL"
    assert "attention_score" not in json.dumps(result, sort_keys=True)


def test_mismatched_report_is_indeterminate():
    validator = LocalityAnomalyValidator()
    work_order = {"locality": LOCALITY, "time_window": WINDOW}
    report = {
        "source": "locality_anomaly",
        "engine_version": "v0.1",
        "locality": "R2-COUNTY999",
        "time_window": WINDOW,
        "snapshot_digest": "a" * 64,
        "baseline_digest": "b" * 64,
        "observations": [],
    }

    result = validator.validate(work_order, [report])
    assert result["status"] == "INDETERMINATE"
    assert "details" not in result


def test_locality_without_frozen_report_is_indeterminate():
    result = LocalityAnomalyValidator().validate(
        {"locality": LOCALITY, "time_window": WINDOW},
        [],
    )
    assert result["status"] == "INDETERMINATE"
    assert result["score"] == 0.5


def test_handoff_binds_locality_report_without_core_false_anomaly(tmp_path):
    engine, _, _, baselines = make_engine(tmp_path)
    freeze_default(engine, baselines)
    work_order = locality_work_order()

    receipt = run_replay_handoff(
        work_order,
        BASELINE,
        locality_engine=engine,
    )

    details = receipt["semantic_validation"]["details"]
    assert details["dimensions"]["locality_anomaly"]["status"] == "PASS"
    assert details["anomaly_report"]["source"] == "locality_anomaly"
    assert receipt["anomalies"] == []
    assert "authority_created" not in receipt
    jsonschema.Draft202012Validator(RECEIPT_SCHEMA).validate(receipt)


def test_severe_locality_signal_fails_dimension_not_authority(tmp_path):
    severe = [
        {
            "what": "weather_alert",
            "when": "2026-08-08T18:00:00+00:00",
            "value": 1.0,
            "confidence": 0.95,
            "severity": "HIGH",
            "sources": [
                "nws:sha256:" + "a" * 64,
                "nws:sha256:" + "b" * 64,
            ],
        }
    ]
    engine, _, _, baselines = make_engine(tmp_path, severe)
    freeze_default(engine, baselines)

    receipt = run_replay_handoff(
        locality_work_order(),
        BASELINE,
        locality_engine=engine,
    )

    details = receipt["semantic_validation"]["details"]
    assert details["dimensions"]["locality_anomaly"]["status"] == "FAIL"
    assert receipt["semantic_validation"]["result"] == "FAIL"
    assert "authority_created" not in receipt


def test_non_locality_work_order_preserves_original_dimension_set():
    work_order = decompose_claim(
        "Replay fixture claim",
        parent_id="fixture_parent",
        token_weight=42.0,
    )[0]
    receipt = run_replay_handoff(work_order, BASELINE)

    assert set(receipt["semantic_validation"]["details"]["dimensions"]) == {
        "dependency",
        "range",
        "schema",
    }
    assert "anomaly_report" not in receipt["semantic_validation"]["details"]


def test_nws_fetcher_strips_raw_free_text_and_sets_required_headers():
    payload = {
        "features": [
            {
                "id": "https://api.weather.gov/alerts/example",
                "properties": {
                    "sent": "2026-08-08T18:00:00+00:00",
                    "severity": "Severe",
                    "certainty": "Likely",
                    "headline": "Private-looking free text must not survive",
                    "description": "123 Example Street and a person's name",
                    "areaDesc": "Named place that must not survive",
                },
            }
        ]
    }
    seen = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(payload).encode("utf-8")

    def opener(request, timeout):
        seen["url"] = request.full_url
        seen["headers"] = dict(request.header_items())
        seen["timeout"] = timeout
        return Response()

    signal = NWSWeatherAlertsSignal(
        {LOCALITY: {"nws_zone": "MNC145"}},
        opener=opener,
    )
    observations = signal.fetch_all(LOCALITY, WINDOW)

    assert "zone=MNC145" in seen["url"]
    assert any(key.lower() == "user-agent" for key in seen["headers"])
    assert observations[0]["what"] == "weather_alert"
    assert observations[0]["severity"] == "HIGH"
    assert observations[0]["confidence"] == 0.9
    rendered = json.dumps(observations, sort_keys=True)
    assert "Private-looking" not in rendered
    assert "123 Example Street" not in rendered
    assert "Named place" not in rendered
