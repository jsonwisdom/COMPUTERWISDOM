from __future__ import annotations

import hashlib
import json
import math
import os
import random
from pathlib import Path
from typing import Any, Dict

from decomposition.agent import decompose_claim

REPLAY_RUNNER_VERSION = "REPLAY_RUNNER_V0_1"


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _implementation_hash() -> str:
    """Bind the trace to the replay executor and decomposition implementation."""
    executor_bytes = Path(__file__).read_bytes()
    decomposition_bytes = Path(decompose_claim.__code__.co_filename).read_bytes()
    material = b"REPLAY_EXECUTOR\0" + executor_bytes + b"\0DECOMPOSITION\0" + decomposition_bytes
    return _sha256_bytes(material)


def _validate_inputs(work_order: Dict[str, Any], baseline_anchor: str) -> None:
    if not isinstance(work_order, dict):
        raise TypeError("work_order must be a dict")

    work_order_id = work_order.get("work_order_id")
    if not isinstance(work_order_id, str) or not work_order_id.strip():
        raise ValueError("work_order_id must be a non-empty string")

    claim_text = work_order.get("claim_text")
    if not isinstance(claim_text, str) or not claim_text.strip():
        raise ValueError("claim_text must be a non-empty string")

    parent_id = work_order.get("parent_id")
    if parent_id is not None and (not isinstance(parent_id, str) or not parent_id.strip()):
        raise ValueError("parent_id must be null or a non-empty string")

    weight = work_order.get("quadratic_weight")
    if not isinstance(weight, (int, float)) or isinstance(weight, bool):
        raise TypeError("quadratic_weight must be a finite non-negative number")
    if not math.isfinite(float(weight)) or float(weight) < 0:
        raise ValueError("quadratic_weight must be a finite non-negative number")

    if not isinstance(baseline_anchor, str) or len(baseline_anchor) != 40:
        raise ValueError("baseline_anchor must be a full 40-character git SHA")
    if any(ch not in "0123456789abcdef" for ch in baseline_anchor):
        raise ValueError("baseline_anchor must be a lowercase hexadecimal git SHA")


def run_replay(work_order: Dict[str, Any], baseline_anchor: str) -> Dict[str, Any]:
    """
    Deterministically replay decomposition from an immutable work-order input.

    v0.1 freezes Python's pseudo-random source for current pure replay code and
    records both a deterministic seed and an implementation hash. The
    implementation hash makes later code drift visible instead of allowing a
    changed runner to masquerade as the same replay.
    """
    _validate_inputs(work_order, baseline_anchor)

    work_order_hash = _sha256_bytes(_canonical_json_bytes(work_order))
    seed_material = f"{work_order['work_order_id']}:{baseline_anchor}".encode("utf-8")
    seed = int(hashlib.sha256(seed_material).hexdigest()[:8], 16)

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    observed_outputs = decompose_claim(
        work_order["claim_text"],
        parent_id=work_order.get("parent_id"),
        token_weight=float(work_order["quadratic_weight"]),
    )

    execution_trace = {
        "seed": seed,
        "work_order_hash": work_order_hash,
        "implementation_hash": _implementation_hash(),
    }

    return {
        "observed_outputs": observed_outputs,
        "evidence_refs": [f"trace:sha256:{work_order_hash}"],
        "execution_trace": execution_trace,
    }
