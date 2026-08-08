from __future__ import annotations

import math
from typing import Any, Dict, List

from replay.validators.base import Validator


class RangeValidator(Validator):
    """Sanity-check observed numeric values without letting token weight decide truth."""

    name = "range"

    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        del work_order
        invalid_fields: List[str] = []

        def walk(value: Any, path: str = "") -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    child_path = f"{path}.{key}" if path else key
                    if key == "quadratic_weight":
                        continue
                    walk(child, child_path)
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    walk(child, f"{path}[{index}]")
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if not math.isfinite(float(value)):
                    invalid_fields.append(path)

        walk(observed_outputs)

        if invalid_fields:
            return self.result(
                "FAIL",
                0.0,
                "Non-finite numeric observations at: " + ", ".join(sorted(invalid_fields)),
            )

        return self.result(
            "PASS",
            1.0,
            "Observed numeric values are finite; quadratic_weight is intentionally ignored "
            "for pass/fail.",
        )
