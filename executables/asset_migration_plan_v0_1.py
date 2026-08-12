#!/usr/bin/env python3
"""Build a fail-closed migration plan from a COMPUTERWISDOM asset inventory.

This planner never moves files. It binds tracked source paths to Git blob SHAs
and emits review/HOLD records for candidate canonicalization.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

CANONICAL_ROOTS = {
    "executables": "executables",
    "fixtures": "fixtures",
    "instruments": "instruments",
    "proofs": "proofs",
    "whitepapers": "whitepapers",
}


def git_blob_sha(repo_root: Path, rel_path: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "-s", "--", rel_path],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    first = proc.stdout.splitlines()[0].split()
    return first[1] if len(first) >= 2 else None


def build_plan(inventory: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    plan = []
    for record in inventory.get("records", []):
        buried_classes = sorted(
            cls for cls, status in record.get("status_by_class", {}).items()
            if status == "BURIED_CANDIDATE"
        )
        if not buried_classes:
            continue

        source_path = record["path"]
        blob = git_blob_sha(repo_root, source_path)
        source_name = Path(source_path).name

        if len(buried_classes) != 1:
            target_class = None
            target_path = None
            state = "HOLD_MULTI_CLASS"
        else:
            target_class = buried_classes[0]
            target_path = f"{CANONICAL_ROOTS[target_class]}/{source_name}"
            if blob is None:
                state = "HOLD_SOURCE_BLOB_UNKNOWN"
            elif (repo_root / target_path).exists() and target_path != source_path:
                state = "HOLD_TARGET_COLLISION"
            else:
                state = "REVIEW_REQUIRED"

        plan.append({
            "source_path": source_path,
            "source_blob_sha": blob,
            "classification_candidates": record.get("classification_candidates", []),
            "buried_classes": buried_classes,
            "target_class": target_class,
            "suggested_target_path": target_path,
            "state": state,
            "dependencies_updated": False,
            "semantic_review_passed": False,
            "tests_passed": False,
            "move_authorized": False,
        })

    counts: dict[str, int] = {}
    for item in plan:
        counts[item["state"]] = counts.get(item["state"], 0) + 1

    return {
        "schema": "computerwisdom.asset_migration_plan.v0.1",
        "source_inventory_schema": inventory.get("schema"),
        "plan": plan,
        "summary": {"candidate_count": len(plan), "state_counts": counts},
        "moves_performed": False,
        "authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    result = build_plan(inventory, args.repo_root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
