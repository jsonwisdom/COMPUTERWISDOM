# tests/test_scanner_reporter_integration.py

from gdi_scanner import scan
from gdi_reporter import emit_observation


FORBIDDEN_REPORT_FIELDS = {
    "truth_claim",
    "liability_claim",
    "adjudication_claim",
    "verified_truth",
    "final_diagnosis",
    "must_block",
    "judge",
    "block",
    "blame",
    "verify_truth",
    "state_mutation",
    "blocking_action",
    "anchored",
    "eas_uid",
    "tx_hash",
    "analysis",
    "judgment",
    "diagnosis",
    "recommendation",
    "action",
    "confidence",
    "timestamp",
    "observed_at",
    "receipt_id",
    "event_hash",
    "severity",
}


def test_scanner_reporter_pipeline_preserves_witness_only_boundary():
    event = {
        "event": "branch_rejected_direct_write",
        "severity": "low",
        "truth_claim": "forbidden",
        "recommendation": "forbidden",
    }

    scanner_receipt = scan(event)
    report = emit_observation(scanner_receipt)

    assert report == {
        "report_type": "gdi_witness_observation",
        "candidate_goblin": "GC-009",
        "candidate_path": ["GC-009", "GC-010"],
        "witness": "GC-010",
        "mode": "witness_only",
        "authority": False,
    }


def test_reporter_strips_forbidden_fields_from_receipt_like_input():
    receipt = {
        "candidate_goblin": "GC-009",
        "candidate_path": ["GC-009", "GC-010"],
        "witness": "GC-010",
        "authority": False,
        "severity": "low",
        "diagnosis": "forbidden",
        "recommendation": "forbidden",
        "truth_claim": "forbidden",
        "tx_hash": "forbidden",
    }

    report = emit_observation(receipt)
    report_text = str(report).lower()

    for field in FORBIDDEN_REPORT_FIELDS:
        assert field not in report
        assert field.lower() not in report_text

    assert report["witness"] == "GC-010"
    assert report["mode"] == "witness_only"
    assert report["authority"] is False


def test_pipeline_defaults_to_gc_010_for_unknown_event():
    scanner_receipt = scan({"event": "unknown"})
    report = emit_observation(scanner_receipt)

    assert report["candidate_goblin"] == "GC-010"
    assert report["candidate_path"] == ["GC-010"]
    assert report["witness"] == "GC-010"
    assert report["authority"] is False


def test_pipeline_does_not_mutate_inputs():
    event = {"event": "hash_mismatch", "severity": "low"}
    original_event = dict(event)

    scanner_receipt = scan(event)
    original_receipt = dict(scanner_receipt)

    emit_observation(scanner_receipt)

    assert event == original_event
    assert scanner_receipt == original_receipt
