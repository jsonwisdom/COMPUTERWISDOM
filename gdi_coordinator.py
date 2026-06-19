"""GDI Coordinator V0.1.

Minimal routing-only coordinator for the GDI observational pipeline.

Boundary:
- Pure routing only.
- No I/O.
- No git operations.
- No network operations.
- No anchoring.
- No blocking or mutation.
- No analysis, judgment, diagnosis, or recommendations.
- Scanner and Reporter are treated as black boxes.
- GC-010 remains witness-only.
- Authority is always false.
"""

from gdi_reporter import emit_observation
from gdi_scanner import scan

ALLOWED_EVENT_FIELDS = frozenset(
    {
        "event",
        "symptom",
        "type",
        "description",
        "source",
    }
)

FORBIDDEN_COORDINATION_FIELDS = frozenset(
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
    }
)


def _strip_forbidden_fields(data):
    """Return a shallow copy without forbidden coordination fields."""
    if not isinstance(data, dict):
        return {}

    return {
        key: value
        for key, value in data.items()
        if key not in FORBIDDEN_COORDINATION_FIELDS
    }


def _is_routable_event(event):
    """Return whether an event can be mechanically routed, not whether it should be."""
    if not isinstance(event, dict):
        return False

    cleaned = _strip_forbidden_fields(event)
    return any(field in cleaned for field in ALLOWED_EVENT_FIELDS)


def _empty_observation():
    """Return a neutral non-blocking observation for unroutable inputs."""
    return {
        "report_type": "gdi_witness_observation",
        "candidate_goblin": "GC-010",
        "candidate_path": ["GC-010"],
        "witness": "GC-010",
        "mode": "witness_only",
        "authority": False,
    }


def coordinate_event(event):
    """Route an event through scanner and reporter without making decisions."""
    if not _is_routable_event(event):
        return _empty_observation()

    routed_event = _strip_forbidden_fields(event)
    scanner_receipt = scan(routed_event)
    return emit_observation(scanner_receipt)


__all__ = [
    "ALLOWED_EVENT_FIELDS",
    "FORBIDDEN_COORDINATION_FIELDS",
    "coordinate_event",
]
