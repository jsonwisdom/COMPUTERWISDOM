import pytest

from revenue_agent.prompt.digest import compute_exchange_digest
from revenue_agent.prompt.parser import ParseError, parse_model_response


def _valid_response(confidence: str = "0.85") -> str:
    return f"""[MODEL ANSWER]
The answer.

[EVIDENCE / REASONING SUMMARY]
The evidence summary.

[CONFIDENCE]
{confidence}"""


def test_valid_full_response():
    assert parse_model_response(_valid_response(), "model-a") == {
        "answer": "The answer.",
        "summary": "The evidence summary.",
        "confidence": 0.85,
        "model_id": "model-a",
    }


def test_missing_section_raises():
    raw = "[MODEL ANSWER]\nA\n[CONFIDENCE]\n0.5"
    with pytest.raises(ParseError, match="summary"):
        parse_model_response(raw, "model-a")


def test_empty_section_raises():
    raw = "[MODEL ANSWER]\n[EVIDENCE / REASONING SUMMARY]\nS\n[CONFIDENCE]\n0.5"
    with pytest.raises(ParseError, match="answer"):
        parse_model_response(raw, "model-a")


def test_invalid_confidence_format():
    with pytest.raises(ParseError, match="invalid confidence format"):
        parse_model_response(_valid_response("high"), "model-a")


@pytest.mark.parametrize("confidence", ["-0.01", "1.01"])
def test_confidence_out_of_range(confidence):
    with pytest.raises(ParseError, match=r"out of range \[0.0, 1.0\]"):
        parse_model_response(_valid_response(confidence), "model-a")


def test_inline_confidence():
    raw = _valid_response().replace("[CONFIDENCE]\n0.85", "[CONFIDENCE] 0.9")
    assert parse_model_response(raw, "model-a")["confidence"] == 0.9


def test_whitespace_normalization():
    spaced = """  [MODEL ANSWER]  
  The answer.  

 [EVIDENCE / REASONING SUMMARY]
 The evidence summary. 

 [CONFIDENCE]  0.85  """
    assert parse_model_response(spaced, "model-a") == parse_model_response(
        _valid_response(), "model-a"
    )


@pytest.mark.parametrize("raw_output", [None, 7, {}, []])
def test_non_string_input_raises(raw_output):
    with pytest.raises(ParseError, match="empty or non-string output"):
        parse_model_response(raw_output, "model-a")


def test_field_names_match_digest():
    parsed = parse_model_response(_valid_response(), "model-a")
    digest_input = {
        "answer": parsed["answer"],
        "evidence_summary": parsed["summary"],
        "confidence": parsed["confidence"],
        "model_id": parsed["model_id"],
    }
    assert set(parsed) == {"answer", "summary", "confidence", "model_id"}
    assert len(compute_exchange_digest("prompt", digest_input)) == 64


@pytest.mark.parametrize(
    "header", ["[CONFIDENCE:] 0.9", "[CONFIDENCE (0-1)] 0.9"]
)
def test_confidence_prefix_variants(header):
    raw = _valid_response().replace("[CONFIDENCE]\n0.85", header)
    assert parse_model_response(raw, "model-a")["confidence"] == 0.9
