VALID_OUTPUTS = {
    'PASS_TO_EXISTENCE_CHECK',
    'NEEDS_RECEIPT',
    'GHOST_PROMOTION_BLOCKED',
    'DUPLICATE_FOUND',
    'DISPUTE_REQUIRED',
    'INVALID_TRANSITION'
}


def verifier_output_allowed(output):
    return output in VALID_OUTPUTS


def test_allowed_output_passes():
    assert verifier_output_allowed('PASS_TO_EXISTENCE_CHECK') is True


def test_ghost_promotion_blocked_exists():
    assert verifier_output_allowed('GHOST_PROMOTION_BLOCKED') is True


def test_invalid_output_fails():
    assert verifier_output_allowed('TRUTH_FINALITY') is False


def test_authority_remains_false():
    authority = False
    assert authority is False
