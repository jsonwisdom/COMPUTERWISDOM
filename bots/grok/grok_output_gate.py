#!/usr/bin/env python3
"""Fail-closed output gate for the bounded Grok reviewer bot."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

GATE_ID = "GROK_OUTPUT_GATE_V0_1"
ALLOWED_INPUTS = {
    "REVIEW_FINDINGS": "review_findings",
    "NONBINDING_RECOMMENDATION": "nonbinding_recommendation",
}


def _normalized_key(key: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(key).lower())


def _find_forbidden(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if _normalized_key(key) == "finalverdict":
                found.append(child_path)
            else:
                found.extend(_find_forbidden(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_forbidden(child, f"{path}[{index}]"))
    return found


def _strip_forbidden(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_forbidden(child)
            for key, child in value.items()
            if _normalized_key(key) != "finalverdict"
        }
    if isinstance(value, list):
        return [_strip_forbidden(child) for child in value]
    return value


def gate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise ValueError("input must be a JSON object")

    receipt = candidate.get("batch_receipt_id")
    receipt_present = isinstance(receipt, str) and bool(receipt.strip())
    result: dict[str, Any] = {
        "gate": GATE_ID,
        "status": "REVIEW_READY_FOR_HUMAN" if receipt_present else "HOLD_REVIEW_ONLY",
        "batch_receipt_id": receipt.strip() if receipt_present else None,
        "removed_fields": _find_forbidden(candidate),
        "grok_can_verify_self_as_final": False,
        "build_blocking": False,
        "authority_created": False,
    }

    for source, target in ALLOWED_INPUTS.items():
        if source in candidate:
            result[target] = _strip_forbidden(candidate[source])
        elif target in candidate:
            result[target] = _strip_forbidden(candidate[target])

    return result


def main() -> int:
    try:
        candidate = json.load(sys.stdin)
        output = gate(candidate)
    except (json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"gate": GATE_ID, "status": "REJECT_INVALID_INPUT", "error": str(exc)}, separators=(",", ":")))
        return 2

    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
