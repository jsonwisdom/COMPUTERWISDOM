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
        """Return non-authoritative PASS, FAIL, or INDETERMINATE evidence."""
        raise NotImplementedError

    def result(self, status: str, score: float, reason: str = "") -> Dict[str, Any]:
        if status not in {"PASS", "FAIL", "INDETERMINATE"}:
            raise ValueError("validator status must be PASS, FAIL, or INDETERMINATE")
        bounded = min(1.0, max(0.0, float(score)))
        result: Dict[str, Any] = {
            "name": self.name,
            "status": status,
            "score": bounded,
        }
        if reason:
            result["reason"] = reason
        return result
