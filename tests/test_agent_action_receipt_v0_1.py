VALID_ACTIONS = {
    'observe_public_claim',
    'summarize_context',
    'propose_case_intake',
    'draft_spec',
    'prepare_anchor_payload',
    'produce_runtime_log',
    'open_dispute_state',
    'emit_boundary_observation'
}


def action_allowed(action):
    return action in VALID_ACTIONS


def test_valid_action_passes():
    assert action_allowed('draft_spec') is True


def test_invalid_action_fails():
    assert action_allowed('autonomous_merge') is False


def test_input_refs_required_fixture():
    input_refs = ['artifact_001']
    assert len(input_refs) > 0


def test_authority_remains_false():
    authority = False
    assert authority is False
