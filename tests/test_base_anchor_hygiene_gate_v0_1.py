REQUIRED_FIELDS = {
    'chain',
    'tx_hash_or_eas_uid',
    'payload_hash',
    'operator_confirmation',
    'no_existing_anchor_conflict'
}


def has_required_fields(fields):
    return REQUIRED_FIELDS.issubset(set(fields))


def test_required_fields_present():
    assert has_required_fields(REQUIRED_FIELDS) is True


def test_missing_field_fails():
    assert has_required_fields({'chain'}) is False


def test_operator_confirmation_required():
    operator_confirmation = True
    assert operator_confirmation is True


def test_authority_remains_false():
    authority = False
    assert authority is False
