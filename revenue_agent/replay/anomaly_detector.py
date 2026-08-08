from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

ANOMALY_TYPES = {
    "missing_required_field",
    "unexpected_output_shape",
    "temporal_drift",
    "evidence_mismatch",
    "logical_contradiction",
}

_REQUIRED_OBSERVED_FIELDS = {
    "work_order_id",
    "claim_text",
    "verification_status",
    "authority_created",
}
_TEMPORAL_KEYS = {"timestamp", "created_at", "updated_at"}


def _canonical_work_order_hash(work_order: Dict[str, Any]) -> str:
    payload = json.dumps(
        work_order,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _anomaly(
    anomaly_type: str,
    severity: str,
    description: str,
    *,
    field: str | None = None,
    expected: Any = None,
    actual: Any = None,
) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "type": anomaly_type,
        "severity": severity,
        "description": description,
    }
    if field is not None:
        item["field"] = field
    if expected is not None:
        item["expected"] = expected
    if actual is not None:
        item["actual"] = actual
    return item


def detect_anomalies(
    work_order: Dict[str, Any],
    observed_outputs: List[Dict[str, Any]],
    evidence_refs: List[str],
    baseline_anchor: str,
) -> List[Dict[str, Any]]:
    """Return structured anomalies as evidence; anomalies do not create authority."""
    anomalies: List[Dict[str, Any]] = []

    if not isinstance(observed_outputs, list):
        return [
            _anomaly(
                "unexpected_output_shape",
                "HIGH",
                "Observed outputs are not a list.",
                field="observed_outputs",
                expected="array",
                actual=type(observed_outputs).__name__,
            )
        ]

    for index, output in enumerate(observed_outputs):
        if not isinstance(output, dict):
            anomalies.append(
                _anomaly(
                    "unexpected_output_shape",
                    "HIGH",
                    "Observed output is not an object.",
                    field=f"observed_outputs[{index}]",
                    expected="object",
                    actual=type(output).__name__,
                )
            )
            continue

        for field in sorted(_REQUIRED_OBSERVED_FIELDS - set(output)):
            anomalies.append(
                _anomaly(
                    "missing_required_field",
                    "HIGH",
                    f"Observed output is missing required field '{field}'.",
                    field=f"observed_outputs[{index}].{field}",
                    expected="present",
                    actual="missing",
                )
            )

        if output.get("authority_created") is not False:
            anomalies.append(
                _anomaly(
                    "logical_contradiction",
                    "HIGH",
                    "Replay output attempted to create or omit the frozen authority boundary.",
                    field=f"observed_outputs[{index}].authority_created",
                    expected=False,
                    actual=output.get("authority_created"),
                )
            )

        if output.get("verification_status") not in {None, "UNVERIFIED"}:
            anomalies.append(
                _anomaly(
                    "logical_contradiction",
                    "HIGH",
                    "Replay output promoted verification status without a separate authority path.",
                    field=f"observed_outputs[{index}].verification_status",
                    expected="UNVERIFIED",
                    actual=output.get("verification_status"),
                )
            )

        for key in sorted(_TEMPORAL_KEYS.intersection(output)):
            anomalies.append(
                _anomaly(
                    "temporal_drift",
                    "LOW",
                    "Timestamp-like replay output detected in a deterministic receipt surface.",
                    field=f"observed_outputs[{index}].{key}",
                    expected="no temporal field",
                    actual=output.get(key),
                )
            )

    expected_evidence = f"trace:sha256:{_canonical_work_order_hash(work_order)}"
    if not isinstance(evidence_refs, list) or expected_evidence not in evidence_refs:
        anomalies.append(
            _anomaly(
                "evidence_mismatch",
                "HIGH",
                "Canonical work-order trace evidence is missing or mismatched.",
                field="evidence_refs",
                expected=expected_evidence,
                actual=evidence_refs,
            )
        )

    if (
        not isinstance(baseline_anchor, str)
        or len(baseline_anchor) != 40
        or any(ch not in "0123456789abcdef" for ch in baseline_anchor)
    ):
        anomalies.append(
            _anomaly(
                "evidence_mismatch",
                "HIGH",
                "Baseline anchor is not a full lowercase git SHA.",
                field="baseline_anchor",
                expected="40-character lowercase git SHA",
                actual=baseline_anchor,
            )
        )

    return anomalies
