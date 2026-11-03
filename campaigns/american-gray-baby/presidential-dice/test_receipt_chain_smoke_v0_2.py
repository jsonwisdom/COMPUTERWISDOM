from receipt_chain_v0_2 import BranchType, ReplayIntegrity, Status, exact_replay_result, merkle_root_hex, namespace_for, sha256_hex


def test_exact_replay_match_keeps_evidence_state():
    integrity, state, _ = exact_replay_result(
        current_evidence_state=Status.HOLD,
        original_serialized=b"same",
        replayed_serialized=b"same",
    )
    assert integrity == ReplayIntegrity.MATCH
    assert state == Status.HOLD


def test_counterfactual_is_quarantined():
    assert namespace_for(BranchType.COUNTERFACTUAL_X) == "quarantine"


def test_merkle_is_deterministic():
    left = sha256_hex(b"left")
    right = sha256_hex(b"right")
    assert merkle_root_hex([left, right]) == merkle_root_hex([left, right])
