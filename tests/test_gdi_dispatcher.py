# tests/test_gdi_dispatcher.py
"""GDI Dispatcher Harness V0.1.

Validates pure dispatch behavior for multiple coordinator events.
"""

import copy

from gdi_dispatcher import dispatch_events


def test_dispatcher_preserves_order_and_calls_coordinator(monkeypatch):
    events = [
        {"candidate_goblin": "g1", "candidate_path": ["a"]},
        {"candidate_goblin": "g2", "candidate_path": ["b"]},
    ]
    calls = []

    def fake_coordinate(event):
        calls.append(copy.deepcopy(event))
        return {
            "report_type": "gdi_witness_observation",
            "candidate_goblin": event["candidate_goblin"],
            "candidate_path": event["candidate_path"],
            "witness": "GC-010",
            "mode": "witness_only",
            "authority": False,
        }

    monkeypatch.setattr("gdi_dispatcher.coordinate_event", fake_coordinate)

    reports = dispatch_events(events)

    assert len(calls) == 2
    assert calls[0]["candidate_goblin"] == "g1"
    assert calls[1]["candidate_goblin"] == "g2"

    assert reports[0]["candidate_goblin"] == "g1"
    assert reports[1]["candidate_goblin"] == "g2"

    for report in reports:
        assert report["report_type"] == "gdi_witness_observation"
        assert report["witness"] == "GC-010"
        assert report["mode"] == "witness_only"
        assert report["authority"] is False


def test_dispatcher_does_not_mutate_input(monkeypatch):
    event = {"candidate_goblin": "g", "candidate_path": ["x"]}
    original = copy.deepcopy(event)

    def fake_coordinate(coordinated_event):
        return {
            "report_type": "gdi_witness_observation",
            "candidate_goblin": coordinated_event["candidate_goblin"],
            "candidate_path": coordinated_event["candidate_path"],
            "witness": "GC-010",
            "mode": "witness_only",
            "authority": False,
        }

    monkeypatch.setattr("gdi_dispatcher.coordinate_event", fake_coordinate)

    dispatch_events([event])

    assert event == original
