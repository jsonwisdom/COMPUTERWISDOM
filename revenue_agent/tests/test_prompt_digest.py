from revenue_agent.prompt.digest import compute_exchange_digest


def _response(evidence_summary: str = "S") -> dict:
    return {
        "answer": "A",
        "evidence_summary": evidence_summary,
        "confidence": 0.5,
        "model_id": "M",
    }


def test_digest_deterministic_for_identical_exchange():
    prompt = "P"
    assert compute_exchange_digest(prompt, _response()) == compute_exchange_digest(prompt, _response())


def test_digest_changes_when_evidence_summary_changes():
    prompt = "P"
    assert compute_exchange_digest(prompt, _response("S1")) != compute_exchange_digest(prompt, _response("S2"))


def test_digest_model_response_key_order_independent():
    prompt = "P"
    r1 = {"answer": "A", "evidence_summary": "S", "confidence": 0.5, "model_id": "M"}
    r2 = {"model_id": "M", "confidence": 0.5, "evidence_summary": "S", "answer": "A"}
    assert compute_exchange_digest(prompt, r1) == compute_exchange_digest(prompt, r2)
