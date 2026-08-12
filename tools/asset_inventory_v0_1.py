#!/usr/bin/env python3
"""Read-only COMPUTERWISDOM asset topology inventory.

This tool emits classification *candidates*. It never moves files and never
promotes a label into evidence or authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

CANONICAL_ROOTS = {
    "executables": "executables",
    "fixtures": "fixtures",
    "instruments": "instruments",
    "proofs": "proofs",
    "whitepapers": "whitepapers",
}

SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
EXEC_SUFFIXES = {".sh", ".ps1", ".bat", ".cmd", ".py"}
EXEC_PATH_HINTS = {"scripts", "tools", "bin", "cli"}
INSTRUMENT_HINTS = (
    "auditor",
    "audit",
    "validator",
    "validate",
    "verifier",
    "verify",
    "evaluator",
    "scanner",
    "router",
    "meter",
)
PROOF_HINTS = ("proof", "attestation", "verifier_chain", "verification_result")
WHITEPAPER_HINTS = ("whitepaper", "white_paper", "white-paper")


def _first_line(path: Path) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return handle.readline(256)
    except OSError:
        return ""


def classify(path: Path, root: Path) -> list[str]:
    rel = path.relative_to(root)
    posix = rel.as_posix().lower()
    name = path.name.lower()
    parts = {part.lower() for part in rel.parts}
    classes: set[str] = set()

    if "fixture" in posix or "fixtures" in parts:
        classes.add("fixtures")

    if any(hint in posix for hint in PROOF_HINTS) or "proofs" in parts:
        classes.add("proofs")

    if any(hint in posix for hint in WHITEPAPER_HINTS) or "whitepapers" in parts:
        classes.add("whitepapers")

    if any(hint in name for hint in INSTRUMENT_HINTS) or "instruments" in parts:
        classes.add("instruments")

    if path.suffix.lower() in EXEC_SUFFIXES:
        shebang = _first_line(path).startswith("#!")
        hinted_path = bool(parts & EXEC_PATH_HINTS)
        hinted_name = any(token in name for token in ("run", "cli", "verify", "validate", "audit", "replay"))
        if shebang or hinted_path or hinted_name or "executables" in parts:
            classes.add("executables")

    return sorted(classes)


def inventory(root: Path) -> dict:
    records = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        classes = classify(path, root)
        if not classes:
            continue
        statuses = {}
        for asset_class in classes:
            canonical_root = CANONICAL_ROOTS[asset_class]
            statuses[asset_class] = (
                "CANONICAL" if rel.parts and rel.parts[0] == canonical_root else "BURIED_CANDIDATE"
            )
        records.append(
            {
                "path": rel.as_posix(),
                "classification_candidates": classes,
                "status_by_class": statuses,
            }
        )

    buried = sum(
        1
        for record in records
        if "BURIED_CANDIDATE" in record["status_by_class"].values()
    )
    return {
        "schema": "computerwisdom.asset_inventory.v0.1",
        "root": str(root),
        "records": records,
        "summary": {
            "candidate_files": len(records),
            "buried_candidate_files": buried,
        },
        "moves_performed": False,
        "authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--fail-on-buried", action="store_true")
    args = parser.parse_args()

    report = inventory(Path(args.root).resolve())
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.fail_on_buried and report["summary"]["buried_candidate_files"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
