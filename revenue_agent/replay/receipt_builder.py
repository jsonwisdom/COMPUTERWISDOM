from __future__ import annotations

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


def build_receipt(
    work_order: Dict[str, Any],
    baseline_anchor: str,
    observed_outputs: List[Dict[str, Any]],
    evidence_refs: List[str],
    execution_trace: Dict[str, Any],
    semantic_validation: Dict[str, str],
) -> Dict[str, Any]:
    """Build an immutable, content-addressed replay receipt with no authority claim."""
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
    }
    receipt["receipt_digest"] = sha256_json(receipt)
    return receipt
