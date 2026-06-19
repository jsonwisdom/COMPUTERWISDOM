# tests/test_gdi_orchestrator.py
"""GDI Orchestrator Harness V0.1.

Validates single public entrypoint forwarding to dispatcher.
"""

import copy

from gdi_orchestrator import run_gdi_pipeline


def test_orchestrator_returns_dispatcher_output_unchanged(monkeypatch):
    events = [
        {"event": "one"},
        {"event": "two"},
    ]
    expected = [
        {
            "report_type": "gdi_witness_observation",
            "candidate_goblin": "GC-010",
            "candidate_path": ["GC-010"],
            "witness": "GC-010",
            "mode": "witness_only",
            "authority": False,
        },
        {
            "report_type": "gdi_witness_observation",
            "candidate_goblin": "GC-009",
            "candidate_path": ["GC-009", "GC-010"],
            "witness": "GC-010",
            "mode": "witness_only",
            "authority": False,
        },
    ]

    def fake_dispatch(dispatched_events):
        assert dispatched_events == events
        return expected

    monkeypatch.setattr("gdi_orchestrator.dispatch_events", fake_dispatch)

    assert run_gdi_pipeline(events) == expected


def test_orchestrator_returns_empty_list_for_none(monkeypatch):
    def fake_dispatch(dispatched_events):
        raise AssertionError("dispatcher must not be called for None")

    monkeypatch.setattr("gdi_orchestrator.dispatch_events", fake_dispatch)

    assert run_gdi_pipeline(None) == []


def test_orchestrator_normalizes_iterable_without_mutating_events(monkeypatch):
    event = {"event": "branch_rejected_direct_write"}
    original = copy.deepcopy(event)
    captured = []

    def event_iterable():
        yield event

    def fake_dispatch(dispatched_events):
        captured.extend(dispatched_events)
        return [
            {
                "report_type": "gdi_witness_observation",
                "candidate_goblin": "GC-009",
                "candidate_path": ["GC-009", "GC-010"],
                "witness": "GC-010",
                "mode": "witness_only",
                "authority": False,
            }
        ]

    report = run_gdi_pipeline(event_iterable())

    assert event == original
    assert captured == [event]
    assert report[0]["witness"] == "GC-010"
    assert report[0]["authority"] is False
