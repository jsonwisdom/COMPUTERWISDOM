#!/usr/bin/env python3
"""Validate a SINGLE shared ledger without causing promotion or mutation."""
import copy
import datetime as dt
import json
import pathlib
import sys

LEDGER = pathlib.Path(__file__).resolve().parents[1] / "docs/hold_ledger/HOLD_LEDGER_V0_1.json"
BUCKETS = {"PRIVACY", "INTEGRITY", "LEGAL", "TECHNICAL", "PROCESS"}
COORDINATION = {"HOLD", "STOP_TRIAGE", "RELEASE_REVIEW", "ARCHIVED", "ABANDONED", "CLOSED_VERIFIED", "MERGED_IMPORTED"}
TERMINAL = {"ARCHIVED", "ABANDONED", "CLOSED_VERIFIED", "MERGED_IMPORTED"}


def check_date(value):
    if value is None:
        return True
    try:
        return isinstance(value, str) and dt.date.fromisoformat(value).isoformat() == value
    except (ValueError, TypeError):
        return False


def validate(doc):
    errors = []
    if doc.get("schema") != "JSONWISDOM_HOLD_LEDGER_V0_1":
        errors.append("SCHEMA_MISMATCH")
    if doc.get("policy_id") != "NO_UNRECEIPTED_PROMOTION_V0_1":
        errors.append("POLICY_MISMATCH")
    if doc.get("canonical_home") != "docs/hold_ledger/HOLD_LEDGER_V0_1.json":
        errors.append("CANONICAL_HOME_MISMATCH")
    for key in ("authority_created", "canon", "automatic_disposition"):
        if doc.get(key) is not False:
            errors.append("FALSE_BOUNDARY:" + key)
    if not check_date(doc.get("as_of")) or doc.get("as_of") is None:
        errors.append("BAD_SNAPSHOT_DATE")
    cadence = doc.get("weekly_review_policy", {})
    if cadence.get("cadence") != "WEEKLY" or cadence.get("auto_disposition") is not False:
        errors.append("CADENCE_RULE")
    if type(cadence.get("unassigned_escalation_cycles")) is not int or cadence["unassigned_escalation_cycles"] < 2:
        errors.append("ESCALATION_RULE")
    if type(cadence.get("stale_days")) is not int or cadence["stale_days"] < 7:
        errors.append("STALE_RULE")
    entries = doc.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["NO_ENTRIES"]
    ids, pairs = set(), set()
    for idx, item in enumerate(entries):
        prefix = f"ROW_{idx + 1}:"
        if not isinstance(item, dict):
            errors.append(prefix + "NOT_OBJECT")
            continue
        uid = item.get("id")
        if not isinstance(uid, str) or not uid:
            errors.append(prefix + "NO_ID")
        elif uid in ids:
            errors.append(prefix + "DUPLICATE_ID")
        ids.add(uid)
        repository, case = item.get("repo"), item.get("case_key")
        if not isinstance(repository, str) or not repository.startswith("jsonwisdom/"):
            errors.append(prefix + "BAD_REPO")
        if not isinstance(case, str) or not case:
            errors.append(prefix + "BAD_CASE")
        ident = (repository, case)
        if ident in pairs:
            errors.append(prefix + "DUPLICATE_CASE")
        pairs.add(ident)
        if item.get("bucket") not in BUCKETS:
            errors.append(prefix + "INVALID_BUCKET")
        if not isinstance(item.get("evidence_needed"), str) or not item["evidence_needed"].strip():
            errors.append(prefix + "UNBOUNDED_CRITERION")
        if not isinstance(item.get("release_path"), str) or not item["release_path"].strip():
            errors.append(prefix + "UNBOUND_RELEASE_PATH")
        if not isinstance(item.get("source_url"), str) or not item["source_url"].startswith("https://github.com/jsonwisdom/"):
            errors.append(prefix + "INVALID_SOURCE_URL")
        if not isinstance(item.get("source_blob_sha"), str) or len(item["source_blob_sha"]) != 40 or any(ch not in "0123456789abcdef" for ch in item["source_blob_sha"]):
            errors.append(prefix + "INVALID_SOURCE_SHA")
        for field in ("opened_at", "source_record_date", "last_reviewed_at"):
            if not check_date(item.get(field)) or (field == "last_reviewed_at" and item.get(field) is None):
                errors.append(prefix + "INVALID_DATE:" + field)
        owner = item.get("evidence_owner")
        assignment = item.get("owner_assignment_receipt")
        owned = isinstance(owner, str) and bool(owner.strip()) and isinstance(assignment, str) and bool(assignment.strip())
        criterion = isinstance(item.get("evidence_needed"), str) and bool(item["evidence_needed"].strip())
        status = item.get("status")
        if status not in COORDINATION:
            errors.append(prefix + "BAD_STATUS")
        if status == "HOLD" and not (owned and criterion):
            errors.append(prefix + "HOLD_WITHOUT_OWNER_OR_CRITERION")
        if status == "STOP_TRIAGE" and owned and criterion:
            errors.append(prefix + "TRIAGE_WITHOUT_MISSING_FIELD")
        if status in TERMINAL and not item.get("disposition_authorization"):
            errors.append(prefix + "TERMINAL_WITHOUT_HUMAN_RECEIPT")
        if status == "RELEASE_REVIEW" and not (owned and criterion and item.get("verified_release_receipt")):
            errors.append(prefix + "UNVERIFIED_RELEASE_REVIEW")
        value = item.get("cost_per_day_usd")
        if value is not None and (type(value) not in (int, float) or value < 0 or not item.get("cost_basis")):
            errors.append(prefix + "COST_UNGROUNDED")
        if value is None and item.get("cost_basis") is not None:
            errors.append(prefix + "COST_BASIS_WITHOUT_VALUE")
    return errors


def self_test(doc):
    assert not validate(doc), validate(doc)
    altered = copy.deepcopy(doc)
    altered["entries"][0]["status"] = "HOLD"
    assert any("HOLD_WITHOUT_OWNER" in x for x in validate(altered))
    altered = copy.deepcopy(doc)
    altered["entries"][0]["status"] = "ARCHIVED"
    assert any("TERMINAL_WITHOUT_HUMAN_RECEIPT" in x for x in validate(altered))
    altered = copy.deepcopy(doc)
    altered["entries"][0]["cost_per_day_usd"] = 0
    assert any("COST_UNGROUNDED" in x for x in validate(altered))
    altered = copy.deepcopy(doc)
    altered["entries"][0]["status"] = "RELEASE_REVIEW"
    assert any("UNVERIFIED_RELEASE_REVIEW" in x for x in validate(altered))
    altered = copy.deepcopy(doc)
    altered["entries"][1]["id"] = altered["entries"][0]["id"]
    assert any("DUPLICATE_ID" in x for x in validate(altered))
    print("HOLD_LEDGER_SELF_TEST=PASS")


def main():
    try:
        doc = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("HOLD_LEDGER=FAIL", str(exc))
        return 1
    errors = validate(doc)
    if errors:
        print(json.dumps({"hold_ledger": "FAIL", "errors": errors}, sort_keys=True))
        return 1
    if "--self-test" in sys.argv:
        self_test(doc)
    counts = {x: sum(r["status"] == x for r in doc["entries"]) for x in COORDINATION}
    print(json.dumps({"hold_ledger": "PASS", "scope": doc["scope"], "entries": len(doc["entries"]),
                      "statuses": counts, "promotion": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
