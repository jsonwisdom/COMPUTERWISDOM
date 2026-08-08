from __future__ import annotations

import math
from typing import Any, Dict, List

VALIDATOR_VERSION = "v0.2"


def aggregate_results(
    validator_results: List[Dict[str, Any]],
    anomalies: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Aggregate dimensions into a bounded informational RMS score.

    The aggregate score is observability only. It MUST NOT be used for routing,
    execution authority, verification authority, or receipt authority.
    """
    normalized: List[Dict[str, Any]] = []
    seen_names = set()

    for result in validator_results:
        name = result.get("name")
        status = result.get("status")
        score = result.get("score")
        if not isinstance(name, str) or not name:
            raise ValueError("validator result name must be a non-empty string")
        if name in seen_names:
            raise ValueError(f"duplicate validator result name: {name}")
        if status not in {"PASS", "FAIL", "INDETERMINATE"}:
            raise ValueError(
                f"validator {name} status must be PASS, FAIL, or INDETERMINATE"
            )
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise ValueError(f"validator {name} score must be numeric")
        if not math.isfinite(float(score)) or not 0.0 <= float(score) <= 1.0:
            raise ValueError(f"validator {name} score must be finite and bounded [0, 1]")
        seen_names.add(name)
        normalized.append(result)

    scores = [float(result["score"]) for result in normalized]
    if scores:
        aggregate_score = min(
            1.0,
            max(0.0, math.sqrt(sum(score**2 for score in scores) / len(scores))),
        )
    else:
        aggregate_score = 0.0

    high_severity_anomalies = [
        anomaly for anomaly in anomalies if anomaly.get("severity") == "HIGH"
    ]
    failed_validators = [
        result for result in normalized if result.get("status") == "FAIL"
    ]
    indeterminate_validators = [
        result for result in normalized if result.get("status") == "INDETERMINATE"
    ]

    if high_severity_anomalies:
        overall_status = "ANOMALY"
    elif failed_validators:
        overall_status = "FAIL"
    elif indeterminate_validators:
        overall_status = "INDETERMINATE"
    elif aggregate_score < 0.5:
        overall_status = "INDETERMINATE"
    else:
        overall_status = "PASS"

    dimensions = {
        result["name"]: {
            "status": result["status"],
            "score": result["score"],
            **({"reason": result["reason"]} if result.get("reason") else {}),
        }
        for result in sorted(normalized, key=lambda item: item["name"])
    }

    return {
        "overall_status": overall_status,
        "dimensions": dimensions,
        "anomalies": anomalies,
        "aggregate_score": round(aggregate_score, 4),
        "validator_version": VALIDATOR_VERSION,
    }
