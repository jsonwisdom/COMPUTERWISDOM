#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
INDEX_PATH = ROOT / "missions" / "_MISSION_INDEX.json"
SUBDIRS = [
    "control/state",
    "control/handoffs",
    "sources",
    "corpus/raw",
    "receipts",
    "manifests",
    "analysis",
    "schemas",
    "tests",
]


def ensure(path, dry_run=False):
    if dry_run:
        print(f"WOULD_CREATE {path.relative_to(ROOT)}")
        return
    path.mkdir(parents=True, exist_ok=True)


def main():
    ap = argparse.ArgumentParser(description="Create mission directory skeletons without overwriting existing artifacts.")
    ap.add_argument("--include-review", action="store_true", help="Also scaffold entries flagged REVIEW_REQUIRED.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    doc = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    entries = doc["entries"] if isinstance(doc, dict) else doc
    missions = {}
    for e in entries:
        mid = e.get("MISSION_ID")
        if not mid or mid == "UNKNOWN":
            continue
        if e.get("REVIEW_REQUIRED") and not args.include_review:
            continue
        missions.setdefault(mid, e)

    scaffold_root = ROOT / "missions" / "_SCAFFOLD_v0.1"
    ensure(scaffold_root, args.dry_run)

    for mid, entry in sorted(missions.items()):
        base = ROOT / "missions" / mid
        ensure(base, args.dry_run)
        for rel in SUBDIRS:
            d = base / rel
            ensure(d, args.dry_run)
            if not args.dry_run:
                keep = d / ".gitkeep"
                if not any(d.iterdir()):
                    keep.touch()

        readme = base / "README.md"
        if args.dry_run:
            if not readme.exists():
                print(f"WOULD_CREATE {readme.relative_to(ROOT)}")
            continue
        if not readme.exists():
            readme.write_text(
                f"# {mid}\n\n"
                f"Canonical mission scaffold.\n\n"
                f"- Artifact class: `{entry.get('ARTIFACT_CLASS', 'UNKNOWN')}`\n"
                f"- Initial source branch: `{entry.get('BRANCH', 'UNKNOWN')}`\n"
                f"- Initial source SHA: `{entry.get('SOURCE_SHA', 'UNKNOWN')}`\n"
                f"- Migration status: `NOT_STARTED`\n"
                f"- Authority created: `FALSE`\n\n"
                "## Boundary\n\n"
                "Scaffolding does not copy evidence, promote claims, create authority, or delete source branches.\n",
                encoding="utf-8",
            )

    print(f"Mission scaffolds selected: {len(missions)}")


if __name__ == "__main__":
    main()
