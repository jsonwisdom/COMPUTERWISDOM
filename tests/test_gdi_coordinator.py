# tests/test_gdi_coordinator.py
"""GDI Coordinator Harness V0.1.

Validates flat witness-only output schema.
"""

from gdi_coordinator import coordinate_event


def test_coordinator_flat_witness_schema():
    event = {
        "event_type": "symptom",
        "event": "coordinator_test",
    }

    report = coordinate_event(event)

    assert report["report_type"] == "gdi_witness_observation"
    assert report["witness"] == "GC-010"
    assert report["mode"] == "witness_only"
    assert report["authority"] is False
    assert "candidate_goblin" in report
    assert "candidate_path" in report


def test_coordinator_strips_forbidden_fields():
    event = {
        "event_type": "symptom",
        "severity": "high",
        "judgment": "bad",
        "block": True,
        "diagnosis": "forbidden",
    }

    report = coordinate_event(event)
    report_str = str(report).lower()

    forbidden = ["severity", "judgment", "block", "diagnosis"]
    for field in forbidden:
        assert field not in report_str


def test_coordinator_neutral_on_unroutable():
    report = coordinate_event({"random": "noise"})

    assert report["report_type"] == "gdi_witness_observation"
    assert report["candidate_goblin"] == "GC-010"
    assert report["candidate_path"] == ["GC-010"]
    assert report["witness"] == "GC-010"
    assert report["mode"] == "witness_only"
    assert report["authority"] is False


def test_coordinator_does_not_mutate_input():
    event = {"event_type": "observation", "payload": "original"}
    original = dict(event)

    coordinate_event(event)

    assert event == original
