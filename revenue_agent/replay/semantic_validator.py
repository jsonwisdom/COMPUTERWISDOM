from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SemanticValidator(ABC):
    @abstractmethod
    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
        evidence_refs: List[str],
    ) -> Dict[str, str]:
        """Validate replay outputs while binding the decision to evidence refs."""
        raise NotImplementedError


class StubValidator(SemanticValidator):
    """v0.1 pipeline validator. PASS means handoff executed, not semantic truth."""

    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
        evidence_refs: List[str],
    ) -> Dict[str, str]:
        del work_order, observed_outputs
        return {
            "result": "PASS",
            "reason": (
                "Stub validator (v0.1): replay pipeline completed; semantic correctness "
                f"is not asserted. Evidence refs bound: {len(evidence_refs)}."
            ),
        }
