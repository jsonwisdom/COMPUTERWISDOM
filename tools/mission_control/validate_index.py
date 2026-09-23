#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
INDEX = ROOT / "missions" / "_MISSION_INDEX.json"
REQUIRED = {
    "DISCOVERY_ID", "ARTIFACT_ID", "MISSION_ID", "CURRENT_LOCATION",
    "BRANCH", "ARTIFACT_CLASS", "CURRENT_STATE", "CANONICAL_DESTINATION",
    "DESTINATION_SUBDIR", "SOURCE_SHA", "SOURCE_PATHS", "MIGRATION_STATUS",
    "AUTHORITY_CREATED", "REVIEW_REQUIRED", "CLASSIFICATION_AMBIGUOUS"
}
ALLOWED_PRE_MIGRATION_STATUS = {"PENDING_REVIEW", "REVIEWED"}
ALLOWED_DESTINATION_SUBDIRS = {
    "control/state", "control/handoffs", "sources", "corpus/raw",
    "receipts", "manifests", "analysis", "schemas", "tests"
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
        errors.append("Top-level AUTHORITY_CREATED must remain false during discovery/scaffold phase")

    seen_discovery_artifact = set()
    for i, e in enumerate(entries):
        missing = REQUIRED - set(e)
        if missing:
            errors.append(f"entry[{i}] missing {sorted(missing)}")
            continue

        key = (e.get("DISCOVERY_ID"), e.get("ARTIFACT_ID"))
        if key in seen_discovery_artifact:
            errors.append(f"duplicate discovery/artifact entry: {key}")
        seen_discovery_artifact.add(key)

        sha = e.get("SOURCE_SHA")
        if sha and not git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
            errors.append(f"source SHA not resolvable: {sha} ({e.get('BRANCH')})")

        if e.get("AUTHORITY_CREATED") is not False:
            errors.append(f"authority unexpectedly true: {e.get('BRANCH')}::{e.get('ARTIFACT_ID')}")

        status = e.get("MIGRATION_STATUS")
        if status not in ALLOWED_PRE_MIGRATION_STATUS:
            errors.append(f"invalid pre-migration status {status}: {e.get('BRANCH')}")

        if e.get("MISSION_ID") == "UNKNOWN":
            warnings.append(f"unclassified: {e.get('BRANCH')}")
            if e.get("REVIEW_REQUIRED") is not True:
                errors.append(f"UNKNOWN entry must require review: {e.get('BRANCH')}")

        if e.get("CLASSIFICATION_AMBIGUOUS") and e.get("REVIEW_REQUIRED") is not True:
            errors.append(f"ambiguous entry must require review: {e.get('BRANCH')}")

        if status == "REVIEWED":
            if e.get("REVIEW_REQUIRED") is True:
                errors.append(f"REVIEWED entry still marked review-required: {e.get('BRANCH')}")
            if e.get("ARTIFACT_ID") == "UNSPLIT_BRANCH_TIP":
                errors.append(f"REVIEWED entry must have explicit ARTIFACT_ID: {e.get('BRANCH')}")
            if not isinstance(e.get("SOURCE_PATHS"), list) or not e.get("SOURCE_PATHS"):
                errors.append(f"REVIEWED entry requires explicit SOURCE_PATHS: {e.get('BRANCH')}::{e.get('ARTIFACT_ID')}")
            if e.get("DESTINATION_SUBDIR") not in ALLOWED_DESTINATION_SUBDIRS:
                errors.append(f"REVIEWED entry requires approved DESTINATION_SUBDIR: {e.get('BRANCH')}::{e.get('ARTIFACT_ID')}")
            if not e.get("CANONICAL_DESTINATION"):
                errors.append(f"REVIEWED entry requires canonical destination: {e.get('BRANCH')}::{e.get('ARTIFACT_ID')}")

        if e.get("REVIEW_REQUIRED"):
            warnings.append(f"review required: {e.get('BRANCH')}::{e.get('ARTIFACT_ID')}")

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
