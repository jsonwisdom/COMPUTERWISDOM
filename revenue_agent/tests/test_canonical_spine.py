import json
from pathlib import Path

import jsonschema
import pytest

from revenue_agent.prompt.digest import compute_exchange_digest
from revenue_agent.prompt.engine import build_canonical_prompt
from revenue_agent.prompt.parser import ParseError, parse_model_response


QUESTION = "What caused the 2023 St. Cloud power outage?"
KNOWN_FACTS = [
    "Transformer failure at Substation 7",
    "Occurred 2023-11-15T14:30:00Z",
]
UNKNOWNS = ["Root cause of transformer failure", "Maintenance history"]
CONSTRAINTS = [
    "Use only public utility reports",
    "No speculation beyond evidence",
]

# Synthetic frozen model output used only to qualify the deterministic spine.
# Its substantive claims are not asserted as real-world facts by this test.
MOCK_MODEL_RESPONSE = """[MODEL ANSWER]
The 2023 St. Cloud power outage was caused by a catastrophic transformer failure 
at Substation 7 due to insulation degradation from prolonged moisture exposure.

[EVIDENCE / REASONING SUMMARY]
Public utility report PU-2023-1142 documents insulation resistance testing showing 
values below threshold for 6 months prior to failure. Weather records confirm 
above-average precipitation in the preceding quarter. No maintenance was scheduled 
despite flagged test results.

[CONFIDENCE] 0.82"""

EXPECTED_DIGEST = "a4bcb83d5cc5f4daa995b18a397d63eae1d7988ad3d0c2538612e2a52ed9baa3"
SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "prompt_receipt.schema.json"


def _exchange():
    prompt = build_canonical_prompt(QUESTION, KNOWN_FACTS, UNKNOWNS, CONSTRAINTS)
    parsed = parse_model_response(MOCK_MODEL_RESPONSE, "mock-model-v1")
    digest_input = {
        "answer": parsed["answer"],
        "evidence_summary": parsed["summary"],
        "confidence": parsed["confidence"],
        "model_id": parsed["model_id"],
    }
    return prompt, parsed, compute_exchange_digest(prompt, digest_input)


class TestCanonicalSpineEndToEnd:
    def test_deterministic_prompt_construction(self):
        p1 = build_canonical_prompt(QUESTION, KNOWN_FACTS, UNKNOWNS, CONSTRAINTS)
        p2 = build_canonical_prompt(QUESTION, KNOWN_FACTS, UNKNOWNS, CONSTRAINTS)
        p3 = build_canonical_prompt(
            QUESTION,
            list(reversed(KNOWN_FACTS)) + [KNOWN_FACTS[0]],
            UNKNOWNS,
            CONSTRAINTS,
        )
        assert p1 == p2 == p3

    def test_parser_extracts_correct_fields(self):
        _, parsed, _ = _exchange()
        assert parsed["model_id"] == "mock-model-v1"
        assert "transformer failure" in parsed["answer"].lower()
        assert "insulation resistance" in parsed["summary"].lower()
        assert parsed["confidence"] == pytest.approx(0.82)

    def test_digest_is_stable_for_frozen_exchange(self):
        _, _, digest = _exchange()
        assert digest == EXPECTED_DIGEST

    def test_receipt_validates_against_frozen_schema(self):
        _, parsed, digest = _exchange()
        receipt = {
            "spine_version": "v0.1",
            "question": QUESTION,
            "known_facts": sorted(KNOWN_FACTS),
            "unknowns": sorted(UNKNOWNS),
            "constraints": sorted(CONSTRAINTS),
            "model_responses": [
                {
                    "model_id": parsed["model_id"],
                    "answer": parsed["answer"],
                    "evidence_summary": parsed["summary"],
                    "confidence": parsed["confidence"],
                }
            ],
            "exchange_digest": digest,
            "timestamp": "2026-08-09T00:00:00Z",
        }
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(instance=receipt, schema=schema)

    def test_malformed_response_rejected(self):
        bad = "[MODEL ANSWER]\nSome answer\n[EVIDENCE / REASONING SUMMARY]\nS\n[CONFIDENCE] not-a-number"
        with pytest.raises(ParseError, match="invalid confidence"):
            parse_model_response(bad, "bad-model")

    def test_missing_evidence_summary_rejected(self):
        no_summary = "[MODEL ANSWER]\nAnswer here.\n[CONFIDENCE] 0.5"
        with pytest.raises(ParseError, match="missing or empty required sections.*summary"):
            parse_model_response(no_summary, "incomplete-model")
