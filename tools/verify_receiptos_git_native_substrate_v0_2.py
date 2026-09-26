#!/usr/bin/env python3
"""Machine regression for ReceiptOS Git-native substrate v0.2."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "receiptos_git_native_reverse_replay_v0_2.py"
SCHEMA_PATH = HERE.parent / "schemas" / "receiptos" / "git_native_semantic_envelope_v0_2.schema.json"


def load_engine():
    spec = importlib.util.spec_from_file_location("receiptos_git_native_v02", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load v0.2 engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(args, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(args)}\n"
            f"{completed.stderr.decode(errors='replace')}"
        )
    return completed.stdout.decode().strip()


def commit_env(epoch: int) -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "ReceiptOS v0.2 Regression",
        "GIT_AUTHOR_EMAIL": "receiptos-v02@example.invalid",
        "GIT_AUTHOR_DATE": f"@{epoch} +0000",
        "GIT_COMMITTER_NAME": "ReceiptOS v0.2 Regression",
        "GIT_COMMITTER_EMAIL": "receiptos-v02@example.invalid",
        "GIT_COMMITTER_DATE": f"@{epoch} +0000",
    })
    return env


def write_and_commit(repo: Path, message: str, epoch: int) -> str:
    run(repo, "git", "add", "-A")
    run(repo, "git", "commit", "--quiet", "-m", message, env=commit_env(epoch))
    return run(repo, "git", "rev-parse", "HEAD")


def schema_structure_assertions(schema: dict) -> dict[str, bool]:
    required = set(schema.get("required", []))
    props = schema.get("properties", {})
    binding_required = set(props.get("binding", {}).get("required", []))
    semantic_required = set(props.get("semantic", {}).get("required", []))
    return {
        "schema_id_v0_2": schema.get("$id") == "https://jsonwisdom.example/schemas/receiptos/git-native-semantic-envelope-v0.2.schema.json",
        "schema_const_v0_2": props.get("schema", {}).get("const") == "RECEIPTOS_GIT_NATIVE_SEMANTIC_ENVELOPE_V0_2",
        "authority_created_required": "authority_created" in required and props.get("authority_created", {}).get("const") is False,
        "merge_authorized_required": "merge_authorized" in required and props.get("merge_authorized", {}).get("const") is False,
        "native_binding_fields_present": {
            "git_object_format", "git_blob_oids", "git_tree_oid", "git_commit_oid",
            "git_parent_oids", "git_ref_observed", "target_path", "content_sha256",
        }.issubset(binding_required),
        "semantic_fields_present": {
            "claim_class", "evidence_class", "source_binding", "authority_state",
            "consent_state", "replay_disposition",
        }.issubset(semantic_required),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    engine = load_engine()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema_assertions = schema_structure_assertions(schema)

    with tempfile.TemporaryDirectory(prefix="receiptos-v02-") as tmp:
        root = Path(tmp)
        repo = root / "repo"
        semantic_dir = root / "semantic"
        repo.mkdir()
        semantic_dir.mkdir()

        run(repo, "git", "init", "--quiet", "-b", "base")
        run(repo, "git", "config", "user.name", "ReceiptOS v0.2 Regression")
        run(repo, "git", "config", "user.email", "receiptos-v02@example.invalid")

        target = "memory/state.txt"
        target_file = repo / target
        target_file.parent.mkdir(parents=True)
        target_file.write_text("season-0\n", encoding="utf-8")
        base_commit = write_and_commit(repo, "base state", 1787300000)

        run(repo, "git", "switch", "--quiet", "-c", "path-a")
        target_file.write_text("season-1\n", encoding="utf-8")
        path_a_commit = write_and_commit(repo, "path a final", 1787300010)
        path_a_tree = run(repo, "git", "show", "-s", "--format=%T", path_a_commit)
        path_a_blob = run(repo, "git", "rev-parse", f"{path_a_commit}:{target}")

        run(repo, "git", "switch", "--quiet", "-c", "path-b", base_commit)
        event_file = repo / "event_history.txt"
        event_file.write_text("ROUTE_REQUESTED\nCONSENT_CHECKED\nROUTE_BLOCKED\n", encoding="utf-8")
        path_b_history_commit = write_and_commit(repo, "path b recorded history", 1787300020)
        event_file.unlink()
        target_file.write_text("season-1\n", encoding="utf-8")
        path_b_commit = write_and_commit(repo, "path b final", 1787300030)
        path_b_tree = run(repo, "git", "show", "-s", "--format=%T", path_b_commit)

        run(repo, "git", "switch", "--quiet", "path-a")
        payload = target_file.read_bytes()
        portable_sha = "sha256:" + hashlib.sha256(payload).hexdigest()
        parents = run(repo, "git", "show", "-s", "--format=%P", path_a_commit).split()
        envelope = {
            "schema": "RECEIPTOS_GIT_NATIVE_SEMANTIC_ENVELOPE_V0_2",
            "receipt_id": "V02_SYNTHETIC_PATH_A_PASS",
            "binding": {
                "git_object_format": run(repo, "git", "rev-parse", "--show-object-format"),
                "git_blob_oids": [path_a_blob],
                "git_tree_oid": path_a_tree,
                "git_commit_oid": path_a_commit,
                "git_parent_oids": parents,
                "git_ref_observed": "refs/heads/path-a",
                "git_tag_oid": None,
                "target_path": target,
                "content_sha256": portable_sha,
            },
            "semantic": {
                "claim_class": "SYNTHETIC_REGRESSION",
                "evidence_class": "OBSERVED",
                "source_binding": ["synthetic:v0.2-regression"],
                "authority_state": "NONE",
                "consent_state": "NOT_APPLICABLE",
                "replay_disposition": "PASS",
            },
            "witness": {
                "alms_entry": "synthetic:entry-0",
                "alms_merkle_root": "synthetic:not-verified",
                "alms_inclusion_proof": {"path": []},
            },
            "authority_created": False,
            "merge_authorized": False,
        }
        (semantic_dir / "pass.json").write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        pass_result = engine.find_out(repo, "path-a", target, semantic_dir)

        conflict = json.loads(json.dumps(envelope))
        conflict["receipt_id"] = "V02_SYNTHETIC_PATH_A_HOLD"
        conflict["semantic"]["replay_disposition"] = "HOLD"
        (semantic_dir / "conflict.json").write_text(json.dumps(conflict, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        conflict_result = engine.find_out(repo, "path-a", target, semantic_dir)
        (semantic_dir / "conflict.json").unlink()

        missing_result = engine.find_out(repo, "path-a", "memory/missing.txt", semantic_dir)

        divergence_rows = pass_result.get("divergence", {}).get("same_tree_different_commit_refs", [])
        path_b_rows = [row for row in divergence_rows if row.get("ref") == "refs/heads/path-b"]
        previous = pass_result.get("previous_state", [])

        assertions = {
            **schema_assertions,
            "same_final_tree_different_commit_history_fixture": path_a_tree == path_b_tree and path_a_commit != path_b_commit,
            "path_b_history_parent_recorded": run(repo, "git", "show", "-s", "--format=%P", path_b_commit) == path_b_history_commit,
            "find_out_pass": pass_result.get("disposition") == "PASS",
            "current_blob_bound": pass_result.get("current_state", {}).get("blob_oid") == path_a_blob,
            "portable_sha256_bound": pass_result.get("current_state", {}).get("content_sha256") == portable_sha,
            "previous_parent_observed": len(previous) == 1 and previous[0].get("commit_oid") == base_commit,
            "same_tree_different_history_detected": bool(path_b_rows),
            "non_linear_relation_detected": bool(path_b_rows) and path_b_rows[0].get("relation") == "NON_LINEAR_SAME_TREE_DIFFERENT_HISTORY",
            "exact_receipt_bound": len(pass_result.get("receipts", {}).get("exact_current_bindings", [])) == 1,
            "witness_presence_not_promoted": pass_result.get("witness", {}).get("verification_scope") == "PRESENCE_ONLY_V0_2",
            "conflicting_receipts_yield_conflict": conflict_result.get("disposition") == "CONFLICT",
            "missing_path_yields_reject": missing_result.get("disposition") == "REJECT",
            "authority_remains_false": pass_result.get("authority_created") is False and conflict_result.get("authority_created") is False,
            "merge_remains_false": pass_result.get("merge_authorized") is False and conflict_result.get("merge_authorized") is False,
        }
        passed = all(assertions.values())

        receipt = {
            "schema": "RECEIPTOS_GIT_NATIVE_SUBSTRATE_V0_2_MACHINE_RECEIPT",
            "status": "PASS" if passed else "FAIL",
            "fixture": {
                "base_commit": base_commit,
                "path_a_commit": path_a_commit,
                "path_a_tree": path_a_tree,
                "path_a_blob": path_a_blob,
                "path_b_history_commit": path_b_history_commit,
                "path_b_commit": path_b_commit,
                "path_b_tree": path_b_tree,
                "portable_content_sha256": portable_sha,
            },
            "assertions": assertions,
            "find_out_pass_disposition": pass_result.get("disposition"),
            "find_out_conflict_disposition": conflict_result.get("disposition"),
            "find_out_missing_disposition": missing_result.get("disposition"),
            "laws": [
                "SAME_TREE_OID != SAME_COMMIT_OID",
                "SAME_STATE != SAME_HISTORY",
                "SEMANTIC_ENVELOPE_BINDS != SEMANTIC_ENVELOPE_REPLACES_GIT",
                "EARLIEST_REACHABLE_PATH_CHANGE != GLOBAL_INTRODUCTION_PROOF",
                "LOCAL_REF_SCAN != GLOBAL_REF_COMPLETENESS",
                "WITNESS_PRESENT != WITNESS_VERIFIED",
                "FIND_OUT_PATH != IDENTITY_RESOLUTION",
                "REPLAY_RESULT != AUTHORITY",
            ],
            "network_required": False,
            "openai_required": False,
            "authority_created": False,
            "merge_authorized": False,
        }

        rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
        print(rendered, end="")
        if args.receipt_out:
            args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
            args.receipt_out.write_text(rendered, encoding="utf-8")
        return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
