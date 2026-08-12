#!/usr/bin/env python3
"""Read-only COMPUTERWISDOM asset inventory v0.2.

Adds native-home exemptions and content-aware whitepaper candidates while
keeping every classification review-only and non-authoritative.
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
INSTRUMENT_HINTS = ("auditor", "audit", "validator", "validate", "verifier", "verify", "evaluator", "scanner", "router", "meter")
PROOF_HINTS = ("proof", "verifier_chain", "verification_result")
WHITEPAPER_HINTS = ("whitepaper", "white_paper", "white-paper")
WHITEPAPER_CONTENT_HINTS = ("abstract", "methodology", "methods", "findings", "conclusion", "references", "research", "architecture")
NATIVE_HOME_RULES = (
    ((".github", "workflows"), "instruments"),
    (("tests",), "executables"),
)


def _first_line(path: Path) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return handle.readline(256)
    except OSError:
        return ""


def _sample_text(path: Path, limit: int = 32768) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit].lower()
    except OSError:
        return ""


def classify(path: Path, root: Path) -> tuple[list[str], dict[str, list[str]]]:
    rel = path.relative_to(root)
    posix = rel.as_posix().lower()
    name = path.name.lower()
    parts = {part.lower() for part in rel.parts}
    classes: set[str] = set()
    basis: dict[str, list[str]] = {}

    def add(asset_class: str, reason: str) -> None:
        classes.add(asset_class)
        basis.setdefault(asset_class, []).append(reason)

    if "fixture" in posix or "fixtures" in parts:
        add("fixtures", "path_or_name_fixture_hint")

    if any(hint in posix for hint in PROOF_HINTS) or "proofs" in parts:
        add("proofs", "explicit_proof_hint")

    if any(hint in posix for hint in WHITEPAPER_HINTS) or "whitepapers" in parts:
        add("whitepapers", "explicit_whitepaper_hint")
    elif path.suffix.lower() in {".md", ".markdown"}:
        text = _sample_text(path)
        score = sum(1 for hint in WHITEPAPER_CONTENT_HINTS if hint in text)
        if score >= 3:
            add("whitepapers", f"content_whitepaper_score:{score}")

    if any(hint in name for hint in INSTRUMENT_HINTS) or "instruments" in parts:
        add("instruments", "instrument_name_or_root_hint")

    if path.suffix.lower() in EXEC_SUFFIXES:
        shebang = _first_line(path).startswith("#!")
        hinted_path = bool(parts & EXEC_PATH_HINTS)
        hinted_name = any(token in name for token in ("run", "cli", "verify", "validate", "audit", "replay"))
        if shebang or hinted_path or hinted_name or "executables" in parts:
            add("executables", "runnable_or_command_hint")

    return sorted(classes), basis


def _native_home(rel: Path, asset_class: str) -> bool:
    parts = tuple(part.lower() for part in rel.parts)
    for prefix, native_class in NATIVE_HOME_RULES:
        if native_class == asset_class and parts[: len(prefix)] == prefix:
            return True
    return False


def inventory(root: Path) -> dict:
    records = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        classes, basis = classify(path, root)
        if not classes:
            continue
        statuses = {}
        for asset_class in classes:
            if rel.parts and rel.parts[0].lower() == CANONICAL_ROOTS[asset_class]:
                status = "CANONICAL"
            elif _native_home(rel, asset_class):
                status = "NATIVE_HOME"
            else:
                status = "BURIED_CANDIDATE"
            statuses[asset_class] = status
        records.append({
            "path": rel.as_posix(),
            "classification_candidates": classes,
            "classification_basis": basis,
            "status_by_class": statuses,
        })

    buried = sum(1 for record in records if "BURIED_CANDIDATE" in record["status_by_class"].values())
    return {
        "schema": "computerwisdom.asset_inventory.v0.2",
        "root": str(root),
        "records": records,
        "summary": {"candidate_files": len(records), "buried_candidate_files": buried},
        "classification_requires_review": True,
        "moves_performed": False,
        "authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    print(json.dumps(inventory(Path(args.root).resolve()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
