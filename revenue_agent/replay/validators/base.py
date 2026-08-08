from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Validator(ABC):
    """Strict plugin contract for non-authoritative validation dimensions."""

    name: str = "base"
    version: str = "v0.2"

    @abstractmethod
    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Return a dimension result with this exact semantic shape:

        {
            "name": str,          # must equal self.name
            "status": "PASS" | "FAIL",
            "score": float,       # bounded [0, 1]
            "reason": str,        # optional but recommended
        }

        A validator result is evidence/observability only. It creates no authority.
        """
        raise NotImplementedError

    def result(self, status: str, score: float, reason: str = "") -> Dict[str, Any]:
        if status not in {"PASS", "FAIL"}:
            raise ValueError("validator status must be PASS or FAIL")
        bounded = min(1.0, max(0.0, float(score)))
        result: Dict[str, Any] = {
            "name": self.name,
            "status": status,
            "score": bounded,
        }
        if reason:
            result["reason"] = reason
        return result
