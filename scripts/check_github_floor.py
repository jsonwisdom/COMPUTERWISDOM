#!/usr/bin/env python3
"""Read-only validation of a current-state consolidation HOLD checkpoint.

Validation PASS means the guardrail input is coherent, not that migration occurred.
"""
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = BASE / "docs/github_floor/JSONWISDOM_CURRENT_ESTATE_SNAPSHOT_V0_1.json"
SHA256 = re.compile(r"^[a-f0-9]{64}$")
GIT_SHA = re.compile(r"^[a-f0-9]{40}$")


def validate(m):
    errors = []
    expected = {
        "schema": "JSONWISDOM_CURRENT_ESTATE_SNAPSHOT_V0_1",
        "mode": "REVIEW_ONLY",
        "status": "HOLD",
        "source_owner": "jsonwisdom",
        "target_repository": "jsonwisdom/COMPUTERWISDOM",
        "source_kind": "CURRENT_GITHUB_REPOSITORY_ENUMERATION",
        "historical_manifest_equivalence": False,
        "historical_identity_manifest_status": "UNRESOLVED_SEPARATE_P0_PROCEDURE",
        "private_to_public_allowed": False,
        "source_repositories_mutated": False,
        "git_default_branch_mutated": False,
        "canon": False,
        "authority_created": False,
        "human_decision": "PENDING",
    }
    for key, value in expected.items():
        if m.get(key) != value or type(m.get(key)) is not type(value):
            errors.append("INVALID_FIELD:" + key)
    totals = m.get("totals")
    if not isinstance(totals, dict):
        errors.append("TOTALS_MISSING")
        totals = {}
    for key in ("owned", "public", "private", "empty", "public_nonempty"):
        if type(totals.get(key)) is not int or totals[key] < 0:
            errors.append("INVALID_TOTAL:" + key)
    if not any(e.startswith("INVALID_TOTAL") for e in errors):
        if totals["owned"] != totals["public"] + totals["private"]:
            errors.append("INCOHERENT_VISIBILITY_TOTAL")
        if totals["empty"] > totals["owned"] or totals["public_nonempty"] > totals["public"]:
            errors.append("INCOHERENT_SIZE_TOTAL")
    entries = m.get("migrated_files")
    if not isinstance(entries, list):
        errors.append("MIGRATED_FILES_NOT_LIST")
        entries = []
    if type(m.get("migrated_file_count")) is not int or m["migrated_file_count"] != len(entries):
        errors.append("COPY_COUNT_MISMATCH")
    seen = set()
    for index, item in enumerate(entries):
        if not isinstance(item, dict):
            errors.append("INVALID_ENTRY:" + str(index))
            continue
        path = item.get("destination_path", "")
        bits = path.split("/") if isinstance(path, str) else []
        if len(bits) < 4 or bits[:2] != ["imports", "repositories"] or any(
            b in ("", ".", "..") for b in bits
        ) or "\\" in path:
            errors.append("UNSAFE_PATH:" + str(index))
        else:
            folded = path.casefold()
            if folded in seen:
                errors.append("PATH_COLLISION:" + str(index))
            seen.add(folded)
        if item.get("source_visibility") != "public":
            errors.append("PUBLIC_BOUNDARY:" + str(index))
        if item.get("privacy_license_review") != "PASS":
            errors.append("CONTENT_REVIEW_MISSING:" + str(index))
        if not (isinstance(item.get("source_repo"), str) and
                item["source_repo"].startswith("jsonwisdom/")):
            errors.append("SOURCE_SCOPE:" + str(index))
        if not isinstance(item.get("source_path"), str) or not item["source_path"]:
            errors.append("SOURCE_PATH:" + str(index))
        if not GIT_SHA.fullmatch(str(item.get("source_blob_sha", ""))):
            errors.append("SOURCE_SHA:" + str(index))
        if not SHA256.fullmatch(str(item.get("destination_sha256", ""))):
            errors.append("DESTINATION_DIGEST:" + str(index))
        if not item.get("witness_receipt_id"):
            errors.append("WITNESS_MISSING:" + str(index))
    return errors


def self_test():
    fixture = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert not validate(fixture), "baseline checkpoint must be coherent"
    altered = dict(fixture)
    altered["historical_manifest_equivalence"] = True
    assert "INVALID_FIELD:historical_manifest_equivalence" in validate(altered)
    altered = dict(fixture)
    altered["totals"] = dict(fixture["totals"], private=0)
    assert "INCOHERENT_VISIBILITY_TOTAL" in validate(altered)
    altered = dict(fixture)
    altered["migrated_files"] = [{"destination_path": "imports/repositories/demo/a.txt",
                                 "source_visibility": "private"}]
    altered["migrated_file_count"] = 1
    assert any(e.startswith("PUBLIC_BOUNDARY") for e in validate(altered))
    print("SELF_TEST=PASS")


def main():
    if not MANIFEST.is_file():
        print("RECOVERY_FLOOR=FAIL reason=MISSING_MANIFEST")
        return 1
    try:
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print("RECOVERY_FLOOR=FAIL reason=INVALID_INPUT", str(error))
        return 1
    errors = validate(m)
    if errors:
        print(json.dumps({"recovery_floor": "FAIL", "errors": errors}, sort_keys=True))
        return 1
    if "--self-test" in sys.argv:
        self_test()
    print(json.dumps({"recovery_floor": "PASS", "migration_status": "HOLD",
                      "copied_files": len(m["migrated_files"]),
                      "authority_created": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
