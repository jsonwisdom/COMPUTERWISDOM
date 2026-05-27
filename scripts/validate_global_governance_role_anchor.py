#!/usr/bin/env python3
"""
validate_global_governance_role_anchor.py

Global governance role-collapse validator for COMPUTERWISDOM.

Purpose:
- Enforce temporal governance role boundaries.
- Reject role-collapse between CURRENT_OFFICE_HOLDER, CANDIDATE, NOMINEE, and SUCCESSOR_ELECT.
- Require jurisdiction + office + person + role_status + as_of + sources.

Boundary:
- This script validates structure and explicit role fields.
- It does not determine who holds office.
- It does not claim state authority.
- It does not write to AL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

REQUIRED_FIELDS = [
    "anchor_id",
    "as_of",
    "jurisdiction",
    "office",
    "person",
    "role_status",
    "sources",
    "boundary",
]

VALID_ROLE_STATUS = {
    "CURRENT_OFFICE_HOLDER",
    "CANDIDATE",
    "NOMINEE",
    "SUCCESSOR_ELECT",
    "FORMER_OFFICE_HOLDER",
    "UNKNOWN",
}

BOUNDARY = "CANDIDATE_NOMINEE_SUCCESSOR_ELECT_NOT_CURRENT_OFFICE_HOLDER"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROMOTION_WORDS = [
    "candidate",
    "nominee",
    "front-runner",
    "frontrunner",
    "likely successor",
    "favorite to succeed",
    "running to succeed",
    "successor-elect",
]


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}")


def text_surface(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False).lower()


def validate_anchor(path: Path, obj: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    for field in REQUIRED_FIELDS:
        if field not in obj:
            errors.append(f"{path}: missing required field: {field}")

    if errors:
        return errors

    if obj.get("anchor_id") != "GLOBAL_GOVERNANCE_ROLE_ANCHOR_V1":
        errors.append(f"{path}: anchor_id must be GLOBAL_GOVERNANCE_ROLE_ANCHOR_V1")

    if not isinstance(obj.get("as_of"), str) or not DATE_RE.match(obj["as_of"]):
        errors.append(f"{path}: as_of must be YYYY-MM-DD")

    for field in ["jurisdiction", "office", "person"]:
        if not isinstance(obj.get(field), str) or not obj[field].strip():
            errors.append(f"{path}: {field} must be non-empty string")

    role_status = obj.get("role_status")
    if role_status not in VALID_ROLE_STATUS:
        errors.append(f"{path}: invalid role_status: {role_status}")

    if obj.get("boundary") != BOUNDARY:
        errors.append(f"{path}: boundary must be {BOUNDARY}")

    sources = obj.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{path}: sources must be non-empty array")
    elif not all(isinstance(src, str) and src.startswith(("http://", "https://")) for src in sources):
        errors.append(f"{path}: every source must be http(s) URL string")

    surface = text_surface(obj)
    if role_status == "CURRENT_OFFICE_HOLDER" and any(word in surface for word in PROMOTION_WORDS):
        errors.append(
            f"{path}: role-collapse risk: CURRENT_OFFICE_HOLDER claim contains candidate/nominee/successor language"
        )

    if role_status in {"CANDIDATE", "NOMINEE", "SUCCESSOR_ELECT"}:
        if obj.get("election_date") is None:
            errors.append(f"{path}: {role_status} requires election_date")

    return errors


def iter_paths(inputs: Iterable[str]) -> Iterable[Path]:
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            yield from sorted(p.rglob("*.json"))
        else:
            yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate global governance role anchors.")
    parser.add_argument("paths", nargs="+", help="JSON files or directories to validate")
    args = parser.parse_args()

    all_errors: List[str] = []
    checked = 0

    for path in iter_paths(args.paths):
        obj = read_json(path)
        # Only validate explicit governance role anchor objects.
        if obj.get("anchor_id") != "GLOBAL_GOVERNANCE_ROLE_ANCHOR_V1":
            continue
        checked += 1
        all_errors.extend(validate_anchor(path, obj))

    if all_errors:
        print(json.dumps({
            "validator": "GLOBAL_GOVERNANCE_ROLE_COLLAPSE_GUARD_V1",
            "status": "FAIL",
            "checked": checked,
            "errors": all_errors,
        }, indent=2), file=sys.stderr)
        return 1

    print(json.dumps({
        "validator": "GLOBAL_GOVERNANCE_ROLE_COLLAPSE_GUARD_V1",
        "status": "PASS",
        "checked": checked,
        "boundary": BOUNDARY,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
