from __future__ import annotations

from typing import Any, Dict, Optional

from replay.executor import run_replay
from replay.receipt_builder import build_receipt
from replay.semantic_validator import SemanticValidator, StubValidator


def run_replay_handoff(
    work_order: Dict[str, Any],
    baseline_anchor: str,
    validator: Optional[SemanticValidator] = None,
) -> Dict[str, Any]:
    """Execute deterministic replay, validate it, and return a receipt only."""
    replay_result = run_replay(work_order, baseline_anchor)
    semantic_validator = validator or StubValidator()
    semantic_validation = semantic_validator.validate(
        work_order,
        replay_result["observed_outputs"],
        replay_result["evidence_refs"],
    )

    if semantic_validation.get("result") not in {"PASS", "FAIL"}:
        raise ValueError("semantic validator result must be PASS or FAIL")

    return build_receipt(
        work_order=work_order,
        baseline_anchor=baseline_anchor,
        observed_outputs=replay_result["observed_outputs"],
        evidence_refs=replay_result["evidence_refs"],
        execution_trace=replay_result["execution_trace"],
        semantic_validation=semantic_validation,
    )
