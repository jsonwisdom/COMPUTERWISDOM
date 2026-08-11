#!/usr/bin/env python3
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
INDEX = ROOT / "missions" / "_MISSION_INDEX.json"
PLAN = ROOT / "missions" / "_MIGRATION_PLAN_v0.2.json"
ALLOWED_DESTINATION_SUBDIRS = {
    "control/state", "control/handoffs", "sources", "corpus/raw",
    "receipts", "manifests", "analysis", "schemas", "tests"
}
SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")


def git_ok(*args):
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_row(e):
    errors = []
    if e.get("MIGRATION_STATUS") != "REVIEWED":
        errors.append("MIGRATION_STATUS must be REVIEWED")
    if e.get("REVIEW_REQUIRED") is not False:
        errors.append("REVIEW_REQUIRED must be false")
    if e.get("AUTHORITY_CREATED") is not False:
        errors.append("AUTHORITY_CREATED must remain false")
    if e.get("MISSION_ID") in (None, "", "UNKNOWN"):
        errors.append("MISSION_ID must be explicit")
    if e.get("CLASSIFICATION_AMBIGUOUS") is True:
        errors.append("CLASSIFICATION_AMBIGUOUS must be false")

    artifact_id = e.get("ARTIFACT_ID")
    if not artifact_id or artifact_id == "UNSPLIT_BRANCH_TIP" or not SAFE_ID.fullmatch(artifact_id):
        errors.append("ARTIFACT_ID must be explicit and filesystem-safe")

    source_paths = e.get("SOURCE_PATHS")
    if not isinstance(source_paths, list) or not source_paths:
        errors.append("SOURCE_PATHS must be a non-empty explicit list")
        source_paths = []

    if e.get("DESTINATION_SUBDIR") not in ALLOWED_DESTINATION_SUBDIRS:
        errors.append("DESTINATION_SUBDIR is not approved")

    expected = f"missions/{e.get('MISSION_ID')}/"
    if e.get("CANONICAL_DESTINATION") != expected:
        errors.append(f"CANONICAL_DESTINATION must equal {expected}")

    sha = e.get("SOURCE_SHA")
    if not sha or not git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
        errors.append("SOURCE_SHA is not a resolvable commit")

    normalized = []
    for p in source_paths:
        if not isinstance(p, str):
            errors.append(f"SOURCE_PATH must be a string: {p!r}")
            continue
        pp = PurePosixPath(p)
        if p in ("", ".") or pp.is_absolute() or ".." in pp.parts:
            errors.append(f"unsafe SOURCE_PATH: {p}")
            continue
        norm = pp.as_posix().rstrip("/")
        normalized.append(norm)
        if sha and not git_ok("cat-file", "-e", f"{sha}:{norm}"):
            errors.append(f"SOURCE_PATH not found at SOURCE_SHA: {norm}")

    if len(normalized) != len(set(normalized)):
        errors.append("SOURCE_PATHS contains duplicates")
    for i, a in enumerate(normalized):
        ap = PurePosixPath(a)
        for b in normalized[i + 1:]:
            bp = PurePosixPath(b)
            if ap in bp.parents or bp in ap.parents:
                errors.append(f"SOURCE_PATHS overlap: {a} <-> {b}")

    return errors


def destination_string(e):
    return f"{e['CANONICAL_DESTINATION']}{e['DESTINATION_SUBDIR']}/{e['ARTIFACT_ID']}/"


def reviewed_rows(doc):
    rows = []
    blocked = []
    destinations = {}
    for e in doc.get("entries", []):
        if e.get("MIGRATION_STATUS") != "REVIEWED":
            continue
        errors = validate_row(e)
        if not errors:
            dest = destination_string(e)
            prior = destinations.get(dest)
            if prior is not None:
                errors.append(f"destination collides with {prior}")
            else:
                destinations[dest] = f"{e.get('DISCOVERY_ID')}::{e.get('ARTIFACT_ID')}"
        if errors:
            blocked.append({"DISCOVERY_ID": e.get("DISCOVERY_ID"), "ARTIFACT_ID": e.get("ARTIFACT_ID"), "errors": errors})
        else:
            rows.append(e)
    return rows, blocked


def write_plan(doc, rows, blocked):
    plan = {
        "PLAN_VERSION": "0.2",
        "GENERATED_AT_UTC": datetime.now(timezone.utc).isoformat(),
        "INDEX_REGISTRY_VERSION": doc.get("REGISTRY_VERSION"),
        "INDEX_MIGRATION_AUTHORIZED": doc.get("MIGRATION_AUTHORIZED"),
        "AUTHORITY_CREATED": False,
        "eligible_count": len(rows),
        "blocked_count": len(blocked),
        "eligible": [
            {
                "DISCOVERY_ID": e["DISCOVERY_ID"],
                "ARTIFACT_ID": e["ARTIFACT_ID"],
                "MISSION_ID": e["MISSION_ID"],
                "BRANCH": e["BRANCH"],
                "SOURCE_SHA": e["SOURCE_SHA"],
                "SOURCE_PATHS": e["SOURCE_PATHS"],
                "DESTINATION": destination_string(e),
            }
            for e in rows
        ],
        "blocked": blocked,
    }
    PLAN.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return plan


def safe_members(tf):
    members = []
    for m in tf.getmembers():
        p = PurePosixPath(m.name)
        if p.is_absolute() or ".." in p.parts:
            raise RuntimeError(f"unsafe archive member: {m.name}")
        if not (m.isdir() or m.isfile()):
            raise RuntimeError(f"unsupported archive member type: {m.name}")
        members.append(m)
    return members


def stage_row(e, stage_root):
    stage_name = f"{e['DISCOVERY_ID'][:12]}-{e['ARTIFACT_ID']}"
    artifact_stage = stage_root / stage_name
    artifact_stage.mkdir(parents=True, exist_ok=False)
    cmd = ["git", "archive", "--format=tar", e["SOURCE_SHA"], "--", *e["SOURCE_PATHS"]]
    archive_bytes = subprocess.check_output(cmd, cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as tf:
        members = safe_members(tf)
        files = []
        for m in members:
            target = artifact_stage / Path(*PurePosixPath(m.name).parts)
            if m.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(m)
            if src is None:
                raise RuntimeError(f"could not extract {m.name}")
            with src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)
            files.append({"source_member": m.name, "sha256": sha256_file(target), "size": target.stat().st_size})
    files.sort(key=lambda x: x["source_member"])
    return artifact_stage, files


def destination_root(e):
    return ROOT / e["CANONICAL_DESTINATION"] / e["DESTINATION_SUBDIR"] / e["ARTIFACT_ID"]


def preflight_destination(stage, dest):
    for src in stage.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(stage)
        target = dest / rel
        if target.exists() and (not target.is_file() or sha256_file(target) != sha256_file(src)):
            raise RuntimeError(f"destination collision with different content: {target}")


def copy_stage(stage, dest):
    for src in stage.rglob("*"):
        rel = src.relative_to(stage)
        target = dest / rel
        if src.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def verify_destination(stage, dest):
    for src in stage.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(stage)
        target = dest / rel
        if not target.is_file():
            raise RuntimeError(f"destination verification missing file: {target}")
        if sha256_file(target) != sha256_file(src):
            raise RuntimeError(f"destination verification hash mismatch: {target}")


def receipt_stable_fields(e, files):
    return {
        "RECEIPT_VERSION": "0.2",
        "EVENT": "COPY_HASH_VERIFIED",
        "DISCOVERY_ID": e["DISCOVERY_ID"],
        "ARTIFACT_ID": e["ARTIFACT_ID"],
        "MISSION_ID": e["MISSION_ID"],
        "ORIGINAL_BRANCH": e["BRANCH"],
        "SOURCE_SHA": e["SOURCE_SHA"],
        "SOURCE_PATHS": e["SOURCE_PATHS"],
        "DESTINATION_SUBDIR": e["DESTINATION_SUBDIR"],
        "DESTINATION_ROOT": str(destination_root(e).relative_to(ROOT)).replace(os.sep, "/"),
        "FILES": files,
        "AUTHORITY_CREATED": False,
        "AUTHORITY_GRANT": None,
        "ORIGINAL_BRANCH_DELETED": False,
    }


def write_receipt(e, files):
    receipt_dir = ROOT / e["CANONICAL_DESTINATION"] / "receipts" / "migration-v0.2"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / f"{e['ARTIFACT_ID']}.provenance.json"
    stable = receipt_stable_fields(e, files)

    if receipt_path.exists():
        existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        existing_stable = {k: existing.get(k) for k in stable}
        if existing_stable != stable:
            raise RuntimeError(f"receipt already exists with different provenance: {receipt_path}")
        return receipt_path

    receipt = {"COPIED_AT_UTC": datetime.now(timezone.utc).isoformat(), **stable}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt_path


def execute(rows):
    completed = []
    with tempfile.TemporaryDirectory(prefix="cw-migrate-v0-2-") as td:
        stage_root = Path(td)
        staged = []
        for e in rows:
            stage, files = stage_row(e, stage_root)
            dest = destination_root(e)
            preflight_destination(stage, dest)
            staged.append((e, stage, files, dest))
        for e, stage, files, dest in staged:
            copy_stage(stage, dest)
            verify_destination(stage, dest)
            receipt = write_receipt(e, files)
            completed.append({"ARTIFACT_ID": e["ARTIFACT_ID"], "destination": str(dest.relative_to(ROOT)), "receipt": str(receipt.relative_to(ROOT))})
    return completed


def main():
    ap = argparse.ArgumentParser(description="Plan or execute provenance-preserving mission copies.")
    ap.add_argument("--execute", action="store_true", help="Execute eligible reviewed copies. Default is plan-only.")
    args = ap.parse_args()

    doc = json.loads(INDEX.read_text(encoding="utf-8"))
    rows, blocked = reviewed_rows(doc)
    plan = write_plan(doc, rows, blocked)
    print(f"Plan: eligible={plan['eligible_count']} blocked={plan['blocked_count']} -> {PLAN}")

    if blocked:
        print("Fail-closed: at least one REVIEWED row is invalid.")
        raise SystemExit(2)
    if not args.execute:
        print("PLAN_ONLY: no files copied; no authority created.")
        return

    gates = {
        "INDEX_MIGRATION_AUTHORIZED": doc.get("MIGRATION_AUTHORIZED") is True,
        "ENV_CW_MIGRATION_AUTHORIZED": os.environ.get("CW_MIGRATION_AUTHORIZED") == "TRUE",
        "EXECUTE_FLAG": args.execute,
    }
    failed = [k for k, v in gates.items() if not v]
    if failed:
        raise SystemExit("Execution denied; unsatisfied gates: " + ", ".join(failed))
    if not rows:
        raise SystemExit("Execution denied; zero reviewed migration rows")

    completed = execute(rows)
    print(f"COPIED_HASH_VERIFIED={len(completed)}")
    print("AUTHORITY_CREATED=FALSE")
    print("ORIGINAL_BRANCHES_DELETED=FALSE")


if __name__ == "__main__":
    main()
