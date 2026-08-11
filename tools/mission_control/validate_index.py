#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
INDEX = ROOT / "missions" / "_MISSION_INDEX.json"
REQUIRED = {
    "MISSION_ID", "CURRENT_LOCATION", "BRANCH", "ARTIFACT_CLASS",
    "CURRENT_STATE", "CANONICAL_DESTINATION", "SOURCE_SHA",
    "MIGRATION_STATUS", "AUTHORITY_CREATED"
}


def git_ok(*args):
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def main():
    doc = json.loads(INDEX.read_text(encoding="utf-8"))
    entries = doc.get("entries", [])
    errors = []
    warnings = []

    if doc.get("MIGRATION_AUTHORIZED") is not False:
        errors.append("MIGRATION_AUTHORIZED must remain false during registry/scaffold phase")
    if doc.get("AUTHORITY_CREATED") is not False:
        errors.append("Top-level AUTHORITY_CREATED must remain false during discovery")

    seen = set()
    for i, e in enumerate(entries):
        missing = REQUIRED - set(e)
        if missing:
            errors.append(f"entry[{i}] missing {sorted(missing)}")
        key = (e.get("BRANCH"), e.get("SOURCE_SHA"))
        if key in seen:
            errors.append(f"duplicate branch/SHA entry: {key}")
        seen.add(key)
        sha = e.get("SOURCE_SHA")
        if sha and not git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
            errors.append(f"source SHA not resolvable: {sha} ({e.get('BRANCH')})")
        if e.get("AUTHORITY_CREATED") is not False:
            errors.append(f"authority unexpectedly true: {e.get('BRANCH')}")
        if e.get("MISSION_ID") == "UNKNOWN":
            warnings.append(f"unclassified: {e.get('BRANCH')}")
        if e.get("REVIEW_REQUIRED"):
            warnings.append(f"review required: {e.get('BRANCH')}")

    print(f"entries={len(entries)} errors={len(errors)} warnings={len(warnings)}")
    for x in errors:
        print(f"ERROR {x}")
    for x in warnings[:100]:
        print(f"WARN  {x}")
    if len(warnings) > 100:
        print(f"WARN  ... {len(warnings)-100} additional warnings suppressed")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
