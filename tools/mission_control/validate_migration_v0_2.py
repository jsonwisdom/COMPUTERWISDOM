#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
RECEIPT_GLOB = "missions/*/receipts/migration-v0.2/*.provenance.json"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(sha, path):
    return subprocess.check_output(["git", "show", f"{sha}:{path}"], cwd=ROOT)


def main():
    receipts = sorted(ROOT.glob(RECEIPT_GLOB))
    errors = []
    checked_files = 0

    for receipt_path in receipts:
        r = json.loads(receipt_path.read_text(encoding="utf-8"))
        label = str(receipt_path.relative_to(ROOT))
        if r.get("EVENT") != "COPY_HASH_VERIFIED":
            errors.append(f"{label}: unexpected EVENT")
        if r.get("AUTHORITY_CREATED") is not False or r.get("AUTHORITY_GRANT") is not None:
            errors.append(f"{label}: provenance receipt must not grant authority")
        if r.get("ORIGINAL_BRANCH_DELETED") is not False:
            errors.append(f"{label}: original branch deletion recorded")

        sha = r.get("SOURCE_SHA")
        dest_root = ROOT / r.get("DESTINATION_ROOT", "")
        if not dest_root.resolve().is_relative_to(ROOT.resolve()):
            errors.append(f"{label}: destination escapes repository root")
            continue

        for f in r.get("FILES", []):
            member = f.get("source_member")
            expected = f.get("sha256")
            pp = PurePosixPath(member or "")
            if not member or pp.is_absolute() or ".." in pp.parts:
                errors.append(f"{label}: unsafe source_member {member}")
                continue
            dest = dest_root / Path(*pp.parts)
            if not dest.is_file():
                errors.append(f"{label}: missing destination file {dest.relative_to(ROOT)}")
                continue
            dest_hash = sha256_file(dest)
            if dest_hash != expected:
                errors.append(f"{label}: destination hash mismatch {dest.relative_to(ROOT)}")
            try:
                source_hash = sha256_bytes(git_blob(sha, member))
            except subprocess.CalledProcessError:
                errors.append(f"{label}: source blob not resolvable {sha}:{member}")
                continue
            if source_hash != expected:
                errors.append(f"{label}: source hash mismatch {sha}:{member}")
            checked_files += 1

    print(f"receipts={len(receipts)} files_checked={checked_files} errors={len(errors)}")
    for e in errors:
        print(f"ERROR {e}")
    if not receipts:
        print("NO_MIGRATION_RECEIPTS_FOUND")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
