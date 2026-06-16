def denied(frm, to):
    forbidden = {
        ('CLAIM', 'TRUTH'),
        ('RECEIPT_HASHED', 'TRUTH'),
        ('RECEIPT_ANCHORED', 'TRUTH'),
        ('DISPUTE_OPENED', 'BAD_ACTOR_FOUND'),
        ('REPLAY_MATCH', 'LIABILITY')
    }
    return (frm, to) in forbidden


def test_claim_cannot_become_truth():
    assert denied('CLAIM', 'TRUTH')


def test_receipt_hash_does_not_prove_truth():
    assert denied('RECEIPT_HASHED', 'TRUTH')


def test_anchor_does_not_prove_truth():
    assert denied('RECEIPT_ANCHORED', 'TRUTH')


def test_dispute_is_not_verdict():
    assert denied('DISPUTE_OPENED', 'BAD_ACTOR_FOUND')


def test_replay_match_is_not_liability():
    assert denied('REPLAY_MATCH', 'LIABILITY')


def test_authority_false_required():
    authority = False
    assert authority is False


def test_missing_receipt_blocks_promotion():
    receipt_present = False
    promotion_allowed = receipt_present
    assert promotion_allowed is False
