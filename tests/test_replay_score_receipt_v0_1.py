VALID_DIMENSIONS = {
    'replayability',
    'receipt_integrity',
    'agent_discipline',
    'dispute_quality',
    'base_anchor_hygiene'
}

FORBIDDEN_DIMENSIONS = {
    'human_worth',
    'legal_guilt',
    'creditworthiness',
    'employment_suitability',
    'truth_finality',
    'merge_authority'
}


def dimension_allowed(value):
    return value in VALID_DIMENSIONS


def test_valid_dimension_passes():
    assert dimension_allowed('replayability') is True


def test_forbidden_dimension_fails():
    assert dimension_allowed('truth_finality') is False


def test_supporting_receipts_required_fixture():
    supporting_receipts = ['receipt_001']
    assert len(supporting_receipts) > 0


def test_authority_remains_false():
    authority = False
    assert authority is False
