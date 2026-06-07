#!/usr/bin/env python3
"""Validate HANDSHAKE conformance vectors.

This runner is intentionally small and dependency-free.
It checks expected validator outputs without generating authority.
"""

import json
import sys
from pathlib import Path

EXPECTED = {
    "HANDSHAKE/004-moment-to-story-example.json": "admissible",
    "HANDSHAKE/005-expression-only-example.json": "expression_only",
    "HANDSHAKE/006-narrative-missing-receipt.json": "invalid",
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"FAIL {path}: invalid JSON: {exc}") from exc


def validate_vector(path: Path, expected_verdict: str) -> tuple[bool, str]:
    vector = load_json(path)
    output = vector.get("expected_validator_output", {})

    if vector.get("authority") is not False:
        return False, "top-level authority must be false"

    if output.get("authority") is not False:
        return False, "expected output authority must be false"

    actual = output.get("verdict")
    if actual != expected_verdict:
        return False, f"expected verdict {expected_verdict!r}, got {actual!r}"

    if vector.get("vector_id") == "HANDSHAKE-005":
        trace = vector.get("validator_trace", {})
        if trace.get("receipt_check") != "not_required":
            return False, "HANDSHAKE-005 receipt_check must be not_required"
        if trace.get("replay_check") != "not_required":
            return False, "HANDSHAKE-005 replay_check must be not_required"

    return True, actual


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures = []

    for relpath, expected in EXPECTED.items():
        path = root / relpath
        if not path.exists():
            failures.append(f"FAIL {relpath}: missing file")
            continue
        ok, detail = validate_vector(path, expected)
        status = "PASS" if ok else "FAIL"
        print(f"{status} {relpath}: {detail}")
        if not ok:
            failures.append(f"FAIL {relpath}: {detail}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("HANDSHAKE conformance suite PASS | authority:false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
