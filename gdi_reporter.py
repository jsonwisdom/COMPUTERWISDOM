"""GDI Reporter V0.1.

Minimal witness-only formatter for GDI Scanner receipts.

Boundary:
- Pure functions only.
- No I/O.
- No git operations.
- No network operations.
- No anchoring.
- No blocking or mutation.
- No timestamps, hashes, IDs, confidence scores, or new evidence.
- GC-010 remains witness-only.
- Authority is always false.
"""

ALLOWED_RECEIPT_FIELDS = frozenset(
    {
        "candidate_goblin",
        "candidate_path",
        "witness",
        "authority",
    }
)

FORBIDDEN_EMIT_FIELDS = frozenset(
    {
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
    }
)


def _strip_forbidden_fields(data):
    """Return a shallow copy without forbidden emission fields."""
    if not isinstance(data, dict):
        return {}

    return {key: value for key, value in data.items() if key not in FORBIDDEN_EMIT_FIELDS}


def _allow_receipt_fields(data):
    """Return only fields permitted for neutral witness reporting."""
    return {key: value for key, value in data.items() if key in ALLOWED_RECEIPT_FIELDS}


def observe_receipt(receipt):
    """Observe an existing scanner receipt without creating new evidence."""
    cleaned = _strip_forbidden_fields(receipt)
    observed = _allow_receipt_fields(cleaned)

    return {
        "candidate_goblin": observed.get("candidate_goblin", "GC-010"),
        "candidate_path": observed.get("candidate_path", ["GC-010"]),
        "witness": "GC-010",
        "authority": False,
    }


def format_witness_report(observed):
    """Format observed scanner receipt fields into a neutral witness report."""
    cleaned = _strip_forbidden_fields(observed)
    report = _allow_receipt_fields(cleaned)

    return {
        "report_type": "gdi_witness_observation",
        "candidate_goblin": report.get("candidate_goblin", "GC-010"),
        "candidate_path": report.get("candidate_path", ["GC-010"]),
        "witness": "GC-010",
        "mode": "witness_only",
        "authority": False,
    }


def emit_observation(receipt):
    """Public API: format an existing scanner receipt as a witness report."""
    observed = observe_receipt(receipt)
    return format_witness_report(observed)


__all__ = [
    "ALLOWED_RECEIPT_FIELDS",
    "FORBIDDEN_EMIT_FIELDS",
    "emit_observation",
]
