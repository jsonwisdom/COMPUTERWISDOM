VALID_TRANSITIONS = {
    ("DRAFT", "UNDER_REVIEW"),
    ("UNDER_REVIEW", "GOVERNANCE_CHECK"),
    ("GOVERNANCE_CHECK", "APPROVED"),
    ("APPROVED", "IN_PROGRESS"),
    ("IN_PROGRESS", "MERGED"),
    ("UNDER_REVIEW", "REJECTED"),
    ("GOVERNANCE_CHECK", "REJECTED"),
    ("MERGED", "REPLAY"),
    ("DRAFT", "DISPUTED"),
    ("UNDER_REVIEW", "DISPUTED"),
    ("GOVERNANCE_CHECK", "DISPUTED")
}


def transition_allowed(from_state, to_state):
    return (from_state, to_state) in VALID_TRANSITIONS


def emit_receipt(from_state, to_state, reason):
    if not transition_allowed(from_state, to_state):
        return {
            "authority": False,
            "allowed": False,
            "from_state": from_state,
            "to_state": "DISPUTED",
            "reason": "INVALID_TRANSITION_BLOCKED",
            "invariant": "NO_SILENT_CATEGORY_PROMOTION"
        }

    return {
        "authority": False,
        "allowed": True,
        "from_state": from_state,
        "to_state": to_state,
        "reason": reason,
        "invariant": "NO_SILENT_CATEGORY_PROMOTION"
    }


def test_valid_transition_passes():
    receipt = emit_receipt("DRAFT", "UNDER_REVIEW", "human_request")
    assert receipt["allowed"] is True
    assert receipt["authority"] is False


def test_invalid_transition_blocks_to_disputed():
    receipt = emit_receipt("DRAFT", "MERGED", "ghost_bypass")
    assert receipt["allowed"] is False
    assert receipt["to_state"] == "DISPUTED"


def test_no_authority_upgrade():
    receipt = emit_receipt("APPROVED", "IN_PROGRESS", "implementation_start")
    assert receipt["authority"] is False
