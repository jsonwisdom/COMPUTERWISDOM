from __future__ import annotations

from typing import Any, Dict

from revenue_agent.prompt.digest import compute_exchange_digest
from revenue_agent.prompt.engine import build_canonical_prompt
from revenue_agent.prompt.parser import parse_model_response


HOOK_VERSION = "CANONICAL_QUERY_HOOK_V0_1"


def canonical_query_receipt(
    question: str,
    known_facts: list[str],
    unknowns: list[str],
    constraints: list[str],
    raw_model_output: str,
    model_id: str,
) -> Dict[str, Any]:
    """Build a deterministic prompt-exchange receipt for downstream replay/game use.

    This function does not call a model, create consensus, authorize execution,
    or promote any claim. It only canonicalizes a supplied exchange.
    """
    prompt = build_canonical_prompt(question, known_facts, unknowns, constraints)
    parsed = parse_model_response(raw_model_output, model_id)
    digest_input = {
        "answer": parsed["answer"],
        "evidence_summary": parsed["summary"],
        "confidence": parsed["confidence"],
        "model_id": parsed["model_id"],
    }
    return {
        "hook_version": HOOK_VERSION,
        "spine_version": "v0.1",
        "question": question.strip(),
        "known_facts": sorted({item.strip() for item in known_facts if item.strip()}),
        "unknowns": sorted({item.strip() for item in unknowns if item.strip()}),
        "constraints": sorted({item.strip() for item in constraints if item.strip()}),
        "model_response": digest_input,
        "exchange_digest": compute_exchange_digest(prompt, digest_input),
        "authority_created": False,
        "consensus": None,
    }
