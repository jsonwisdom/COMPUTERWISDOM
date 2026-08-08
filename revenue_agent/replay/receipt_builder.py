from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Dict, List

from replay.executor import REPLAY_RUNNER_VERSION

RECEIPT_VERSION = "REPLAY_HANDOFF_V0_1"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def receipt_digest_payload(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Return the digest-bound payload with informational aggregate score removed."""
    payload = copy.deepcopy(receipt)
    payload.pop("receipt_digest", None)
    details = payload.get("semantic_validation", {}).get("details")
    if isinstance(details, dict):
        details.pop("aggregate_score", None)
    return payload


def build_receipt(
    work_order: Dict[str, Any],
    baseline_anchor: str,
    observed_outputs: List[Dict[str, Any]],
    evidence_refs: List[str],
    execution_trace: Dict[str, Any],
    semantic_validation: Dict[str, Any],
    anomalies: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    """Build an immutable replay receipt with no authority claim.

    Validator dimensions and anomaly evidence are digest-bound. The quadratic
    aggregate_score is deliberately excluded because it is informational only.
    """
    receipt: Dict[str, Any] = {
        "receipt_version": RECEIPT_VERSION,
        "work_order_id": work_order["work_order_id"],
        "parent_id": work_order.get("parent_id"),
        "work_order_sha256": sha256_json(work_order),
        "baseline_anchor": baseline_anchor,
        "input_claim_sha256": hashlib.sha256(
            work_order["claim_text"].encode("utf-8")
        ).hexdigest(),
        "quadratic_weight": float(work_order["quadratic_weight"]),
        "replay_runner_version": REPLAY_RUNNER_VERSION,
        "observed_outputs": observed_outputs,
        "evidence_refs": evidence_refs,
        "execution_trace": execution_trace,
        "semantic_validation": semantic_validation,
        "anomalies": anomalies or [],
    }
    receipt["receipt_digest"] = sha256_json(receipt_digest_payload(receipt))
    return receipt
