from __future__ import annotations

from typing import Any, Dict, Optional

from replay.aggregator import aggregate_results
from replay.anomaly_detector import detect_anomalies
from replay.executor import run_replay
from replay.receipt_builder import build_receipt
from replay.semantic_validator import SemanticValidator
from replay.validators import DependencyValidator, RangeValidator, SchemaValidator


def _quadratic_family_validation(
    work_order: Dict[str, Any],
    baseline_anchor: str,
    observed_outputs: list,
    evidence_refs: list,
) -> tuple[Dict[str, Any], list]:
    validators = [
        SchemaValidator(),
        DependencyValidator(evidence_refs, baseline_anchor),
        RangeValidator(),
    ]
    validator_results = []
    for validator in validators:
        result = validator.validate(work_order, observed_outputs)
        if result.get("name") != validator.name:
            raise ValueError(
                f"validator identity mismatch: expected {validator.name!r}, "
                f"got {result.get('name')!r}"
            )
        validator_results.append(result)

    anomalies = detect_anomalies(
        work_order,
        observed_outputs,
        evidence_refs,
        baseline_anchor,
    )
    details = aggregate_results(validator_results, anomalies)
    failed_validators = [
        result for result in validator_results if result.get("status") == "FAIL"
    ]
    semantic_result = "FAIL" if failed_validators else "PASS"

    return (
        {
            "result": semantic_result,
            "reason": (
                "Quadratic Family v0.2 completed as a non-authoritative observability "
                f"surface; overall_status={details['overall_status']}."
            ),
            "details": details,
        },
        anomalies,
    )


def run_replay_handoff(
    work_order: Dict[str, Any],
    baseline_anchor: str,
    validator: Optional[SemanticValidator] = None,
) -> Dict[str, Any]:
    """Execute deterministic replay, validate it, and return a receipt only."""
    replay_result = run_replay(work_order, baseline_anchor)

    if validator is None:
        semantic_validation, anomalies = _quadratic_family_validation(
            work_order,
            baseline_anchor,
            replay_result["observed_outputs"],
            replay_result["evidence_refs"],
        )
    else:
        semantic_validation = validator.validate(
            work_order,
            replay_result["observed_outputs"],
            replay_result["evidence_refs"],
        )
        anomalies = []

    if semantic_validation.get("result") not in {"PASS", "FAIL"}:
        raise ValueError("semantic validator result must be PASS or FAIL")

    return build_receipt(
        work_order=work_order,
        baseline_anchor=baseline_anchor,
        observed_outputs=replay_result["observed_outputs"],
        evidence_refs=replay_result["evidence_refs"],
        execution_trace=replay_result["execution_trace"],
        semantic_validation=semantic_validation,
        anomalies=anomalies,
    )
