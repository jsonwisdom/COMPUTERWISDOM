from revenue_agent.prompt.hook import canonical_query_receipt


RAW = """[MODEL ANSWER]
A

[EVIDENCE / REASONING SUMMARY]
S

[CONFIDENCE] 0.5"""


def test_hook_is_deterministic_and_authority_free():
    kwargs = dict(
        question="Q",
        known_facts=["B", "A", "A"],
        unknowns=["U"],
        constraints=["C"],
        raw_model_output=RAW,
        model_id="M",
    )
    first = canonical_query_receipt(**kwargs)
    second = canonical_query_receipt(**kwargs)
    assert first == second
    assert first["known_facts"] == ["A", "B"]
    assert first["model_response"]["evidence_summary"] == "S"
    assert first["authority_created"] is False
    assert first["consensus"] is None
    assert len(first["exchange_digest"]) == 64


def test_hook_digest_changes_when_model_output_changes():
    first = canonical_query_receipt("Q", [], [], [], RAW, "M")
    changed = RAW.replace("[MODEL ANSWER]\nA", "[MODEL ANSWER]\nB")
    second = canonical_query_receipt("Q", [], [], [], changed, "M")
    assert first["exchange_digest"] != second["exchange_digest"]
