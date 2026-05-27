#!/usr/bin/env python3
"""Verify federal-adjacent surfaces remain observer-only.

This guard enforces the COMPUTERWISDOM constitutional membrane:
federal adjacency is allowed; federal authority cosplay is not.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

COVERED_PARTS = (
    "federal",
    "white-house-ai",
    "whitehouse",
    "white_house",
)

TEXT_EXTENSIONS = {
    ".json",
    ".md",
    ".yml",
    ".yaml",
    ".txt",
}

OBSERVER_MODES = {
    "observer",
    "READ_ONLY_PUBLIC_OBSERVER",
    "EVIDENCE_ONLY",
    "CONCEPTUAL_ONLY",
}

BOUNDARIES = {
    "OBSERVER_IS_NOT_OFFICE",
    "REGISTRY_IS_NOT_GOVERNMENT_AUTHORITY",
    "PROCESS_VERIFIED_NOT_GOVERNMENT_AUTHORITY",
}

FORBIDDEN_PATTERNS = [
    r"\bofficial\s+white\s+house\b",
    r"\bauthorized\s+by\s+the\s+white\s+house\b",
    r"\bendorsed\s+by\s+the\s+white\s+house\b",
    r"\bfederal\s+authority\s+granted\b",
    r"\bexecutive\s+authority\b",
    r"\bexecutive\s+function\b",
    r"\bDOJ\s+authorized\b",
    r"\bPam\s+Bondi\s+authorized\b",
    r"\bgovernment\s+approved\b",
    r"\bofficial\s+channel\b",
    r"\boffice\s+of\s+(the\s+)?(white\s+house|president|attorney\s+general)\b",
]

ALLOWED_NEUTRALIZERS = [
    "authority\": false",
    "authority: false",
    "authority\": \"NONE\"",
    "authority: NONE",
    "government_endorsement\": false",
    "government_endorsement: FALSE",
    "CONCEPTUAL_ONLY",
    "OBSERVER_IS_NOT_OFFICE",
    "REGISTRY_IS_NOT_GOVERNMENT_AUTHORITY",
    "PROCESS_VERIFIED_NOT_GOVERNMENT_AUTHORITY",
    "READ_ONLY_PUBLIC_OBSERVER",
]


def is_covered(path: Path) -> bool:
    lowered = [part.lower() for part in path.parts]
    return any(part in lowered for part in COVERED_PARTS)


def iter_files(root: Path):
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix in TEXT_EXTENSIONS and is_covered(path):
            yield path


def flatten_values(obj: Any):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield str(key), value
            yield from flatten_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from flatten_values(value)


def has_value(obj: Any, expected: str) -> bool:
    expected_l = expected.lower()
    for _, value in flatten_values(obj):
        if isinstance(value, str) and value.lower() == expected_l:
            return True
    return False


def check_json(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return failures

    serialized = json.dumps(data, sort_keys=True)

    if re.search(r'"authority"\s*:\s*true\b', serialized, re.I):
        failures.append("authority:true is forbidden")

    if re.search(r'"government_endorsement"\s*:\s*true\b', serialized, re.I):
        failures.append("government_endorsement:true is forbidden")

    has_authority_false = re.search(r'"authority"\s*:\s*false\b', serialized, re.I)
    has_authority_none = re.search(r'"authority"\s*:\s*"NONE"', serialized, re.I)
    has_is_federal_false = re.search(r'"is_federal_authority"\s*:\s*false\b', serialized, re.I)

    if not (has_authority_false or has_authority_none or has_is_federal_false):
        failures.append("missing authority:false, authority:NONE, or is_federal_authority:false")

    if not any(has_value(data, mode) for mode in OBSERVER_MODES):
        failures.append("missing observer-only mode")

    if not any(has_value(data, boundary) for boundary in BOUNDARIES):
        failures.append("missing observer boundary")

    return failures


def check_text(path: Path, text: str) -> list[str]:
    failures: list[str] = []

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, re.I):
            if not any(neutralizer in text for neutralizer in ALLOWED_NEUTRALIZERS):
                failures.append(f"forbidden authority-cosplay phrase matched: {pattern}")

    if path.suffix in {".md", ".yml", ".yaml"}:
        lower = text.lower()
        mentions_federal_claim = any(token in lower for token in ["white house", "whitehouse", "federal", "doj", "pam bondi"])
        if mentions_federal_claim:
            has_boundary = any(boundary in text for boundary in BOUNDARIES)
            has_authority_boundary = any(neutralizer in text for neutralizer in ALLOWED_NEUTRALIZERS)
            if not has_boundary:
                failures.append("federal-adjacent text missing observer boundary")
            if not has_authority_boundary:
                failures.append("federal-adjacent text missing explicit no-authority boundary")

    return failures


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    failures: dict[str, list[str]] = {}

    for path in iter_files(root):
        text = path.read_text(errors="ignore")
        path_failures = []
        path_failures.extend(check_json(path, text))
        path_failures.extend(check_text(path, text))
        if path_failures:
            failures[str(path)] = path_failures

    if failures:
        print("FAIL: federal observer membrane violations detected")
        for path, reasons in failures.items():
            print(f"\n{path}")
            for reason in reasons:
                print(f"  - {reason}")
        return 1

    print("PASS: federal observer membrane holds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
