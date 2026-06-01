"""GDI Scanner V0.1.

Minimal observation-only scanner module for Goblin Court replay symptoms.

Boundary:
- Pure functions only.
- No I/O.
- No git operations.
- No network operations.
- No anchoring.
- No blocking or mutation.
- GC-010 remains witness-only.
- Authority is always false.
"""

ALLOWED_GOBLINS = frozenset(
    {
        "GC-001",
        "GC-002",
        "GC-003",
        "GC-004",
        "GC-005",
        "GC-006",
        "GC-007",
        "GC-008",
        "GC-009",
        "GC-010",
    }
)

FORBIDDEN_FIELDS = frozenset(
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
    }
)

_SYMPTOM_TO_GOBLIN = {
    "repo_root_mismatch": "GC-001",
    "uncommitted_change": "GC-002",
    "missing_receipt": "GC-003",
    "schema_gap": "GC-004",
    "chain_id_mismatch": "GC-005",
    "artifact_missing": "GC-006",
    "hash_mismatch": "GC-007",
    "replay_gap": "GC-008",
    "branch_rejected_direct_write": "GC-009",
    "cascade_witness": "GC-010",
}


def _candidate_goblin(event):
    """Return a bounded candidate goblin without claiming diagnosis."""
    if not isinstance(event, dict):
        return "GC-010"

    symptom = event.get("event") or event.get("symptom") or event.get("type")
    candidate = _SYMPTOM_TO_GOBLIN.get(symptom, "GC-010")

    if candidate not in ALLOWED_GOBLINS:
        return "GC-010"

    return candidate


def _candidate_path(candidate):
    """Return a candidate path with GC-010 as witness-only cascade observer."""
    if candidate == "GC-010":
        return ["GC-010"]

    return [candidate, "GC-010"]


def _strip_forbidden_fields(output):
    """Remove forbidden fields if future edits accidentally introduce them."""
    return {key: value for key, value in output.items() if key not in FORBIDDEN_FIELDS}


def scan(event):
    """Observe an event and emit bounded candidate replay metadata.

    This function does not verify truth, assign liability, adjudicate blame,
    block execution, mutate state, perform I/O, use git, access networks,
    or anchor anything.
    """
    candidate = _candidate_goblin(event)
    output = {
        "candidate_goblin": candidate,
        "candidate_path": _candidate_path(candidate),
        "witness": "GC-010",
        "authority": False,
    }
    return _strip_forbidden_fields(output)


__all__ = ["ALLOWED_GOBLINS", "FORBIDDEN_FIELDS", "scan"]
