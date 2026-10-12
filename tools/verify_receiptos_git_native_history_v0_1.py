#!/usr/bin/env python3
"""ReceiptOS v0.1 Git-native same-state/different-history regression."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile

FINAL_STATE = b'{"consent":"HOLD","content":"Meet me by the pink tree.","delivered":false}'
EVENT_HISTORY = b'{"events":["ROUTE_REQUESTED","CONSENT_CHECKED","ROUTE_BLOCKED"]}'
EXPECTED_STATE_SHA256 = "30cc29ff65e9f94595a0c1c0e35ad4e58692d1dea4c4ed4badf83719435cfdd9"


def run(cwd: Path, *args: str, stdin: bytes | None = None, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(args)}\n"
            f"stdout={completed.stdout.decode(errors='replace')}\n"
            f"stderr={completed.stderr.decode(errors='replace')}"
        )
    return completed.stdout.decode().strip()


def git_object(cwd: Path, payload: bytes) -> str:
    return run(cwd, "git", "hash-object", "-w", "--stdin", stdin=payload)


def git_tree(cwd: Path, entries: list[tuple[str, str]]) -> str:
    body = "".join(f"100644 blob {oid}\t{name}\n" for name, oid in sorted(entries)).encode()
    return run(cwd, "git", "mktree", stdin=body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="receiptos-git-native-") as tmp:
        repo = Path(tmp)
        run(repo, "git", "init", "--quiet")
        run(repo, "git", "config", "user.name", "ReceiptOS Regression")
        run(repo, "git", "config", "user.email", "receiptos-regression@example.invalid")

        object_format = run(repo, "git", "rev-parse", "--show-object-format")
        git_version = run(repo, "git", "--version")

        state_blob = git_object(repo, FINAL_STATE)
        events_blob = git_object(repo, EVENT_HISTORY)

        final_tree = git_tree(repo, [("state.json", state_blob)])
        event_tree = git_tree(repo, [("event_history.json", events_blob), ("state.json", state_blob)])

        fixed_env = os.environ.copy()
        fixed_env.update(
            {
                "GIT_AUTHOR_NAME": "ReceiptOS Regression",
                "GIT_AUTHOR_EMAIL": "receiptos-regression@example.invalid",
                "GIT_AUTHOR_DATE": "@1787292000 +0000",
                "GIT_COMMITTER_NAME": "ReceiptOS Regression",
                "GIT_COMMITTER_EMAIL": "receiptos-regression@example.invalid",
                "GIT_COMMITTER_DATE": "@1787292000 +0000",
            }
        )

        history_commit_b = run(
            repo,
            "git",
            "commit-tree",
            event_tree,
            "-m",
            "Path B recorded event history",
            env=fixed_env,
        )

        final_commit_a = run(
            repo,
            "git",
            "commit-tree",
            final_tree,
            "-m",
            "Final state",
            env=fixed_env,
        )
        final_commit_b = run(
            repo,
            "git",
            "commit-tree",
            final_tree,
            "-p",
            history_commit_b,
            "-m",
            "Final state",
            env=fixed_env,
        )

        tree_a = run(repo, "git", "show", "-s", "--format=%T", final_commit_a)
        tree_b = run(repo, "git", "show", "-s", "--format=%T", final_commit_b)
        parents_a = run(repo, "git", "show", "-s", "--format=%P", final_commit_a)
        parents_b = run(repo, "git", "show", "-s", "--format=%P", final_commit_b)

        state_sha256 = hashlib.sha256(FINAL_STATE).hexdigest()

        assertions = {
            "portable_state_sha256_matches_existing_receiptos_vector": state_sha256 == EXPECTED_STATE_SHA256,
            "same_final_tree_oid": tree_a == tree_b == final_tree,
            "different_final_commit_oid": final_commit_a != final_commit_b,
            "path_a_has_no_parent": parents_a == "",
            "path_b_parent_is_recorded_history": parents_b == history_commit_b,
        }
        passed = all(assertions.values())

        receipt = {
            "schema": "RECEIPTOS_GIT_NATIVE_HISTORY_V0_1",
            "status": "PASS" if passed else "FAIL",
            "git_version": git_version,
            "git_object_format": object_format,
            "python_version": platform.python_version(),
            "portable_state_sha256": f"sha256:{state_sha256}",
            "expected_portable_state_sha256": f"sha256:{EXPECTED_STATE_SHA256}",
            "git_blob_oid_state": state_blob,
            "git_blob_oid_event_history": events_blob,
            "git_tree_oid_final": final_tree,
            "git_tree_oid_event_history": event_tree,
            "git_commit_oid_path_a_final": final_commit_a,
            "git_commit_oid_path_b_history": history_commit_b,
            "git_commit_oid_path_b_final": final_commit_b,
            "assertions": assertions,
            "laws": [
                "SAME_TREE_OID != SAME_COMMIT_OID",
                "SAME_STATE != SAME_HISTORY",
                "GIT_COMMIT != FACT_TRUE",
                "GIT_DATE != TRUSTED_TIME",
            ],
            "network_required": False,
            "openai_required": False,
            "merge_authorized": False,
            "authority_created": False,
        }

        rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
        print(rendered, end="")

        if args.receipt_out:
            args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
            args.receipt_out.write_text(rendered, encoding="utf-8")

        return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
