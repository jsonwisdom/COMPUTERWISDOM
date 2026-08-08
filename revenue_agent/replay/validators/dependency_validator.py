from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

from replay.validators.base import Validator


def _canonical_work_order_hash(work_order: Dict[str, Any]) -> str:
    payload = json.dumps(
        work_order,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class DependencyValidator(Validator):
    """Bind replay evidence refs to the immutable work order and baseline context."""

    name = "dependency"

    def __init__(self, evidence_refs: List[str], baseline_anchor: str) -> None:
        self.evidence_refs = evidence_refs
        self.baseline_anchor = baseline_anchor

    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        del observed_outputs

        if (
            not isinstance(self.baseline_anchor, str)
            or len(self.baseline_anchor) != 40
            or any(ch not in "0123456789abcdef" for ch in self.baseline_anchor)
        ):
            return self.result("FAIL", 0.0, "Baseline anchor is not a full lowercase git SHA.")

        if not isinstance(self.evidence_refs, list) or not self.evidence_refs:
            return self.result("FAIL", 0.0, "Replay evidence_refs are missing.")
        if any(not isinstance(ref, str) or not ref for ref in self.evidence_refs):
            return self.result("FAIL", 0.0, "Replay evidence_refs contain an invalid reference.")

        expected = f"trace:sha256:{_canonical_work_order_hash(work_order)}"
        if expected not in self.evidence_refs:
            return self.result(
                "FAIL",
                0.0,
                "Replay evidence does not contain the canonical work-order trace hash.",
            )

        return self.result(
            "PASS",
            1.0,
            "Evidence refs exist and the trace hash matches the canonical work order; "
            "baseline anchor format is valid.",
        )
