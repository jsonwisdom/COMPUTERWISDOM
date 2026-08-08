from __future__ import annotations

from typing import Any, Dict, Optional

from anomaly.baseline import BaselineMissing, SnapshotMissing
from anomaly.engine import BaselineIncomplete, LocalityAnomalyEngine
from anomaly.validator import LocalityAnomalyValidator
from replay.aggregator import aggregate_results
from replay.anomaly_detector import detect_anomalies
from replay.executor import run_replay
from replay.receipt_builder import build_receipt
from replay.semantic_validator import SemanticValidator
from replay.validators import DependencyValidator, RangeValidator, SchemaValidator


def _is_locality_report(output: Any) -> bool:
    return isinstance(output, dict) and output.get("source") == "locality_anomaly"


def _quadratic_family_validation(
    work_order: Dict[str, Any],
    baseline_anchor: str,
    observed_outputs: list,
    evidence_refs: list,
) -> tuple[Dict[str, Any], list]:
    core_outputs = [output for output in observed_outputs if not _is_locality_report(output)]
    validators = [
        SchemaValidator(),
        DependencyValidator(evidence_refs, baseline_anchor),
        RangeValidator(),
    ]
    if work_order.get("locality"):
        validators.append(LocalityAnomalyValidator())

    validator_results = []
    locality_report = None
    for validator in validators:
        target_outputs = (
            observed_outputs if validator.name == "locality_anomaly" else core_outputs
        )
        result = validator.validate(work_order, target_outputs)
        if result.get("name") != validator.name:
            raise ValueError(
                f"validator identity mismatch: expected {validator.name!r}, "
                f"got {result.get('name')!r}"
            )
        if validator.name == "locality_anomaly" and isinstance(result.get("details"), dict):
            locality_report = result["details"]
        validator_results.append(result)

    anomalies = detect_anomalies(
        work_order,
        core_outputs,
        evidence_refs,
        baseline_anchor,
    )
    details = aggregate_results(validator_results, anomalies)
    if locality_report is not None:
        details["anomaly_report"] = locality_report

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
    locality_engine: Optional[LocalityAnomalyEngine] = None,
) -> Dict[str, Any]:
    """Execute deterministic replay, validate it, and return a receipt only.

    RePlay never performs live locality acquisition. A locality engine may analyze
    a previously frozen snapshot; missing frozen evidence becomes INDETERMINATE.
    """
    replay_result = run_replay(work_order, baseline_anchor)
    observed_outputs = list(replay_result["observed_outputs"])

    locality = work_order.get("locality")
    time_window = work_order.get("time_window")
    if validator is None and locality and time_window and locality_engine is not None:
        try:
            observed_outputs.append(
                locality_engine.analyze(locality, time_window, baseline_anchor)
            )
        except (SnapshotMissing, BaselineMissing, BaselineIncomplete):
            pass

    if validator is None:
        semantic_validation, anomalies = _quadratic_family_validation(
            work_order,
            baseline_anchor,
            observed_outputs,
            replay_result["evidence_refs"],
        )
    else:
        semantic_validation = validator.validate(
            work_order,
            observed_outputs,
            replay_result["evidence_refs"],
        )
        anomalies = []

    if semantic_validation.get("result") not in {"PASS", "FAIL"}:
        raise ValueError("semantic validator result must be PASS or FAIL")

    return build_receipt(
        work_order=work_order,
        baseline_anchor=baseline_anchor,
        observed_outputs=observed_outputs,
        evidence_refs=replay_result["evidence_refs"],
        execution_trace=replay_result["execution_trace"],
        semantic_validation=semantic_validation,
        anomalies=anomalies,
    )
