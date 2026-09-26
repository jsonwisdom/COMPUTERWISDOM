#!/usr/bin/env python3
"""ReceiptOS Git-native substrate v0.2: deterministic FIND OUT for repo-relative paths."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

ENGINE_VERSION = "RECEIPTOS_GIT_NATIVE_SUBSTRATE_V0_2"
ENVELOPE_SCHEMA = "RECEIPTOS_GIT_NATIVE_SEMANTIC_ENVELOPE_V0_2"
DISPOSITIONS = ("PASS", "HOLD", "CONFLICT", "REJECT")


class GitQueryError(RuntimeError):
    pass


def run(repo: Path, *args: str, check: bool = True, input_bytes: bytes | None = None) -> str:
    completed = subprocess.run(args, cwd=repo, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check and completed.returncode != 0:
        raise GitQueryError(
            f"command failed ({completed.returncode}): {' '.join(args)}\n"
            f"stdout={completed.stdout.decode(errors='replace')}\n"
            f"stderr={completed.stderr.decode(errors='replace')}"
        )
    return completed.stdout.decode(errors="replace").strip()


def git_is_ancestor(repo: Path, older: str, newer: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    return completed.returncode == 0


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def resolve_commit(repo: Path, ref: str) -> str:
    return run(repo, "git", "rev-parse", "--verify", f"{ref}^{{commit}}")


def commit_tree(repo: Path, commit: str) -> str:
    return run(repo, "git", "show", "-s", "--format=%T", commit)


def commit_parents(repo: Path, commit: str) -> list[str]:
    raw = run(repo, "git", "show", "-s", "--format=%P", commit)
    return raw.split() if raw else []


def path_entry(repo: Path, commit: str, target: str) -> dict[str, Any] | None:
    raw = run(repo, "git", "ls-tree", "-z", commit, "--", target)
    if not raw:
        return None
    for record in [r for r in raw.split("\0") if r]:
        header, path = record.split("\t", 1)
        if path == target:
            mode, obj_type, oid = header.split()
            return {"mode": mode, "type": obj_type, "oid": oid, "path": path}
    return None


def blob_bytes(repo: Path, oid: str) -> bytes:
    completed = subprocess.run(["git", "cat-file", "blob", oid], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        raise GitQueryError(completed.stderr.decode(errors="replace"))
    return completed.stdout


def changed_paths(repo: Path, commit: str) -> list[dict[str, str]]:
    raw = run(repo, "git", "diff-tree", "--root", "--no-commit-id", "--name-status", "-r", commit)
    rows: list[dict[str, str]] = []
    for line in raw.splitlines() if raw else []:
        parts = line.split("\t")
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            rows.append({"status": status, "path": parts[-1], "source_path": parts[-2]})
        elif len(parts) >= 2:
            rows.append({"status": status, "path": parts[-1]})
    return rows


def path_history(repo: Path, commit: str, target: str) -> dict[str, Any]:
    raw = run(repo, "git", "log", "--format=%H", commit, "--", target)
    commits = [x for x in raw.splitlines() if x]
    return {
        "last_changed_commit": commits[0] if commits else None,
        "earliest_path_change_reachable": commits[-1] if commits else None,
        "path_change_commit_count": len(commits),
        "introduction_proven": False,
        "boundary": "EARLIEST_REACHABLE_PATH_CHANGE != GLOBAL_INTRODUCTION_PROOF",
    }


def parent_states(repo: Path, parents: list[str], target: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for parent in parents:
        tree = commit_tree(repo, parent)
        entry = path_entry(repo, parent, target)
        row: dict[str, Any] = {
            "commit_oid": parent,
            "tree_oid": tree,
            "target_present": entry is not None,
            "target_blob_oid": None,
            "content_sha256": None,
        }
        if entry is not None and entry["type"] == "blob":
            payload = blob_bytes(repo, entry["oid"])
            row["target_blob_oid"] = entry["oid"]
            row["content_sha256"] = sha256_bytes(payload)
        out.append(row)
    return out


def visible_refs(repo: Path) -> list[tuple[str, str]]:
    raw = run(repo, "git", "for-each-ref", "--format=%(refname)%00%(objectname)", "refs/heads", "refs/remotes")
    refs: list[tuple[str, str]] = []
    for line in raw.splitlines():
        if "\0" not in line:
            continue
        refname, oid = line.split("\0", 1)
        if refname.endswith("/HEAD"):
            continue
        try:
            refs.append((refname, resolve_commit(repo, oid)))
        except GitQueryError:
            continue
    return refs


def same_tree_histories(repo: Path, current_commit: str, current_tree: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for refname, other_commit in visible_refs(repo):
        key = (refname, other_commit)
        if key in seen or other_commit == current_commit:
            continue
        seen.add(key)
        try:
            other_tree = commit_tree(repo, other_commit)
        except GitQueryError:
            continue
        if other_tree != current_tree:
            continue
        current_ancestor = git_is_ancestor(repo, current_commit, other_commit)
        other_ancestor = git_is_ancestor(repo, other_commit, current_commit)
        merge_base = run(repo, "git", "merge-base", current_commit, other_commit, check=False) or None
        relation = "LINEAR_REVISIT_SAME_TREE" if current_ancestor or other_ancestor else "NON_LINEAR_SAME_TREE_DIFFERENT_HISTORY"
        out.append({
            "ref": refname,
            "commit_oid": other_commit,
            "tree_oid": other_tree,
            "relation": relation,
            "current_is_ancestor_of_other": current_ancestor,
            "other_is_ancestor_of_current": other_ancestor,
            "merge_base": merge_base,
        })
    return sorted(out, key=lambda row: (row["ref"], row["commit_oid"]))


def envelope_errors(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["envelope must be an object"]
    if data.get("schema") != ENVELOPE_SCHEMA:
        errors.append("schema mismatch")
    if not isinstance(data.get("receipt_id"), str) or not data["receipt_id"]:
        errors.append("receipt_id required")
    if data.get("authority_created") is not False:
        errors.append("authority_created must be false")
    if data.get("merge_authorized") is not False:
        errors.append("merge_authorized must be false")
    binding = data.get("binding")
    if not isinstance(binding, dict):
        errors.append("binding object required")
    else:
        for key in ("git_object_format", "git_tree_oid", "git_commit_oid", "git_ref_observed", "target_path", "content_sha256"):
            if not isinstance(binding.get(key), str) or not binding[key]:
                errors.append(f"binding.{key} required")
        if not isinstance(binding.get("git_blob_oids"), list) or not all(isinstance(x, str) for x in binding.get("git_blob_oids", [])):
            errors.append("binding.git_blob_oids must be an array of strings")
        if not isinstance(binding.get("git_parent_oids"), list) or not all(isinstance(x, str) for x in binding.get("git_parent_oids", [])):
            errors.append("binding.git_parent_oids must be an array of strings")
        digest = binding.get("content_sha256")
        if isinstance(digest, str):
            if not (digest.startswith("sha256:") and len(digest) == 71):
                errors.append("binding.content_sha256 must be sha256:<64 hex>")
            else:
                try:
                    int(digest[7:], 16)
                except ValueError:
                    errors.append("binding.content_sha256 must be hexadecimal")
    semantic = data.get("semantic")
    if not isinstance(semantic, dict):
        errors.append("semantic object required")
    else:
        for key in ("claim_class", "evidence_class", "authority_state", "consent_state"):
            if not isinstance(semantic.get(key), str) or not semantic[key]:
                errors.append(f"semantic.{key} required")
        if semantic.get("replay_disposition") not in DISPOSITIONS:
            errors.append("semantic.replay_disposition invalid")
        source_binding = semantic.get("source_binding")
        if not isinstance(source_binding, list) or not source_binding or not all(isinstance(x, str) and x for x in source_binding):
            errors.append("semantic.source_binding must be a non-empty array of strings")
    witness = data.get("witness")
    if witness is not None and not isinstance(witness, dict):
        errors.append("witness must be an object when present")
    return errors


def load_envelopes(directory: Path | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if directory is None or not directory.exists():
        return [], []
    valid: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    for path in sorted(directory.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            invalid.append({"file": str(path), "errors": [f"json parse error: {exc}"], "target_path": None})
            continue
        errors = envelope_errors(data)
        record = {
            "file": str(path), "data": data, "errors": errors,
            "target_path": data.get("binding", {}).get("target_path") if isinstance(data, dict) else None,
        }
        (invalid if errors else valid).append(record)
    return valid, invalid


def matching_receipts(valid, invalid, target, current_commit, current_tree, current_blob, content_sha256):
    exact, target_valid_nonmatching, target_invalid = [], [], []
    for record in invalid:
        if record.get("target_path") == target:
            target_invalid.append({"file": record["file"], "errors": record["errors"]})
    for record in valid:
        data = record["data"]
        binding = data["binding"]
        if binding["target_path"] != target:
            continue
        exact_match = (
            binding["git_commit_oid"] == current_commit
            and binding["git_tree_oid"] == current_tree
            and current_blob in binding["git_blob_oids"]
            and binding["content_sha256"] == content_sha256
        )
        compact = {
            "file": record["file"],
            "receipt_id": data["receipt_id"],
            "replay_disposition": data["semantic"]["replay_disposition"],
            "claim_class": data["semantic"]["claim_class"],
            "evidence_class": data["semantic"]["evidence_class"],
            "authority_state": data["semantic"]["authority_state"],
            "consent_state": data["semantic"]["consent_state"],
            "source_binding": data["semantic"]["source_binding"],
            "witness": data.get("witness"),
            "binding_exact": exact_match,
        }
        (exact if exact_match else target_valid_nonmatching).append(compact)
    dispositions = sorted({r["replay_disposition"] for r in exact})
    if target_invalid:
        normalized, reason = "REJECT", "INVALID_TARGET_ENVELOPE"
    elif not exact:
        normalized, reason = "HOLD", "NO_EXACT_CURRENT_RECEIPT"
    elif len(dispositions) > 1:
        normalized, reason = "CONFLICT", "EXACT_RECEIPTS_DISAGREE"
    else:
        normalized, reason = dispositions[0], "EXACT_RECEIPT_DISPOSITION"
    witness_rows = []
    for receipt in exact:
        witness = receipt.get("witness")
        if witness:
            witness_rows.append({
                "receipt_id": receipt["receipt_id"],
                "alms_entry": witness.get("alms_entry"),
                "alms_merkle_root": witness.get("alms_merkle_root"),
                "alms_inclusion_proof": witness.get("alms_inclusion_proof"),
                "presence": True,
                "verification": "DECLARED_UNVERIFIED_V0_2",
            })
    return {
        "exact": sorted(exact, key=lambda x: x["receipt_id"]),
        "target_valid_nonmatching": sorted(target_valid_nonmatching, key=lambda x: x["receipt_id"]),
        "target_invalid": target_invalid,
        "normalized_disposition": normalized,
        "disposition_reason": reason,
        "witness_rows": witness_rows,
    }


def find_out(repo: Path, ref: str, target: str, semantic_dir: Path | None = None) -> dict[str, Any]:
    repo = repo.resolve()
    target = target.strip().replace("\\", "/")
    base = {
        "schema": "RECEIPTOS_GIT_NATIVE_FIND_OUT_V0_2",
        "engine": ENGINE_VERSION,
        "query": {"target_type": "PATH", "target": target, "ref_input": ref},
        "authority_created": False,
        "merge_authorized": False,
    }
    if not target or target.startswith("/") or target.startswith("../") or "/../" in target:
        return {**base, "disposition": "REJECT", "reason": "INVALID_REPO_RELATIVE_PATH"}
    try:
        current_commit = resolve_commit(repo, ref)
        object_format = run(repo, "git", "rev-parse", "--show-object-format")
        current_tree = commit_tree(repo, current_commit)
        entry = path_entry(repo, current_commit, target)
    except GitQueryError as exc:
        return {**base, "disposition": "REJECT", "reason": "REF_OR_REPOSITORY_UNRESOLVED", "error": str(exc)}
    if entry is None:
        return {
            **base,
            "current_history": {"git_object_format": object_format, "commit_oid": current_commit, "tree_oid": current_tree},
            "disposition": "REJECT", "reason": "TARGET_NOT_PRESENT_AT_REF",
        }
    if entry["type"] != "blob":
        return {**base, "disposition": "REJECT", "reason": "V0_2_TARGET_MUST_RESOLVE_TO_BLOB"}
    payload = blob_bytes(repo, entry["oid"])
    portable_sha = sha256_bytes(payload)
    parents = commit_parents(repo, current_commit)
    divergence = same_tree_histories(repo, current_commit, current_tree)
    valid, invalid = load_envelopes(semantic_dir)
    receipt_state = matching_receipts(valid, invalid, target, current_commit, current_tree, entry["oid"], portable_sha)
    return {
        **base,
        "query": {**base["query"], "ref_resolution_scope": "LOCAL_GIT_REPOSITORY"},
        "current_state": {
            "tree_oid": current_tree,
            "blob_oid": entry["oid"],
            "blob_mode": entry["mode"],
            "content_sha256": portable_sha,
            "changed_paths_at_current_commit": changed_paths(repo, current_commit),
        },
        "current_history": {
            "git_object_format": object_format,
            "commit_oid": current_commit,
            "parent_oids": parents,
            "ref_observed": ref,
            **path_history(repo, current_commit, target),
        },
        "previous_state": parent_states(repo, parents, target),
        "divergence": {
            "same_tree_different_commit_refs": divergence,
            "same_tree_different_history_detected": bool(divergence),
            "scope": "LOCAL_HEADS_AND_REMOTES_ONLY",
            "boundary": "UNSEEN_REMOTE_REF != ABSENT_HISTORY",
        },
        "receipts": {
            "exact_current_bindings": receipt_state["exact"],
            "target_valid_nonmatching": receipt_state["target_valid_nonmatching"],
            "target_invalid": receipt_state["target_invalid"],
        },
        "witness": {
            "rows": receipt_state["witness_rows"],
            "verification_scope": "PRESENCE_ONLY_V0_2",
            "boundary": "WITNESS_PRESENT != WITNESS_VERIFIED",
        },
        "boundary": [
            "GIT_COMMIT != FACT_TRUE",
            "GIT_HASH != COMPLETE_RECORD",
            "TREE_OID != CAUSATION",
            "EARLIEST_REACHABLE_PATH_CHANGE != GLOBAL_INTRODUCTION_PROOF",
            "LOCAL_REF_SCAN != GLOBAL_REF_COMPLETENESS",
            "WITNESS_PRESENT != WITNESS_VERIFIED",
            "FIND_OUT_PATH != IDENTITY_RESOLUTION",
            "MODEL_OUTPUT != RECEIPT",
            "REPLAY_RESULT != AUTHORITY",
        ],
        "disposition": receipt_state["normalized_disposition"],
        "disposition_reason": receipt_state["disposition_reason"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ReceiptOS Git-native FIND OUT v0.2")
    parser.add_argument("target", help="repo-relative path to inspect")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--semantic-dir", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = find_out(args.repo, args.ref, args.target, args.semantic_dir)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    return 0 if result.get("disposition") != "REJECT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
