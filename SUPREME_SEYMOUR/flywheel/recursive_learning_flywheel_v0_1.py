#!/usr/bin/env python3
"""Supreme Seymour Recursive Learning Flywheel v0.1

Read-only GitHub estate observer.
- Enumerates jsonwisdom public repositories.
- Compares current heads to the checked-in Master Room snapshot index.
- Emits delta artifacts only.
- Never commits, merges, emails, writes Drive, or promotes authority.

AUTHORITY_CREATED = false
FINAL_DECISION = JASON
"""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASELINE = ROOT / "MASTER_ROOM" / "SNAPSHOT_INDEX_V1.json"
OUTDIR = ROOT / "build" / "supreme-seymour-flywheel"
OWNER = os.environ.get("FLYWHEEL_OWNER", "jsonwisdom")
TOKEN = os.environ.get("GH_TOKEN", "")
API = "https://api.github.com"


def api_get(path: str):
    req = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
            "User-Agent": "supreme-seymour-flywheel-v0-1",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def list_public_repos():
    repos = []
    page = 1
    while True:
        batch = api_get(f"/users/{OWNER}/repos?type=public&per_page=100&page={page}&sort=full_name")
        if not batch:
            break
        repos.extend(x for x in batch if not x.get("private", False))
        if len(batch) < 100:
            break
        page += 1
    return repos


def head_sha(repo_full_name: str, default_branch: str):
    try:
        obj = api_get(f"/repos/{repo_full_name}/commits/{default_branch}")
        return obj.get("sha")
    except urllib.error.HTTPError as e:
        if e.code in (404, 409, 422):
            return None
        raise


def main():
    observed_at = dt.datetime.now(dt.timezone.utc).isoformat()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    baseline_rows = {x["repo"]: x for x in baseline.get("repos", [])}

    live_repos = list_public_repos()
    live_names = {x["full_name"] for x in live_repos}
    deltas = []
    unchanged = []
    unknowns = []

    for repo in live_repos:
        full = repo["full_name"]
        branch = repo.get("default_branch")
        base = baseline_rows.get(full)
        current = head_sha(full, branch) if branch else None

        if base is None:
            deltas.append({
                "repo": full,
                "delta_class": "STRUCTURE_DELTA",
                "reason": "REPO_NOT_IN_BASELINE",
                "baseline_head": None,
                "current_head": current,
                "default_branch": branch,
            })
            continue

        prior = base.get("head_commit")
        if prior == current:
            unchanged.append(full)
        else:
            deltas.append({
                "repo": full,
                "delta_class": "VERSION_DELTA",
                "reason": "HEAD_CHANGED" if prior and current else "HEAD_RESOLUTION_CHANGED",
                "baseline_head": prior,
                "current_head": current,
                "default_branch": branch,
            })

        if current is None:
            unknowns.append({
                "repo": full,
                "unknown": "CURRENT_HEAD_UNRESOLVED",
                "blocking": False,
            })

    for full, base in baseline_rows.items():
        if full not in live_names:
            deltas.append({
                "repo": full,
                "delta_class": "ABSENCE_CLAIM_DELTA",
                "reason": "NOT_IN_CURRENT_PUBLIC_ENUMERATION",
                "baseline_head": base.get("head_commit"),
                "current_head": None,
                "note": "Enumeration miss is not deletion proof.",
            })

    report = {
        "schema": "SUPREME_SEYMOUR_RECURSIVE_LEARNING_FLYWHEEL_REPORT_V0_1",
        "observed_at": observed_at,
        "owner": OWNER,
        "operator": "JASON",
        "authority_created": False,
        "canon": False,
        "mode": "READ_ONLY_DELTA_OBSERVER",
        "baseline": {
            "path": "MASTER_ROOM/SNAPSHOT_INDEX_V1.json",
            "observed_at": baseline.get("observed_at"),
            "public_repo_count": baseline.get("public_repo_count"),
        },
        "live": {
            "public_repo_count": len(live_repos),
            "delta_count": len(deltas),
            "unchanged_count": len(unchanged),
            "unknown_count": len(unknowns),
        },
        "deltas": deltas,
        "unknowns": unknowns,
        "invariants": [
            "DELTA != WRONGDOING",
            "SEARCH_MISS != NONEXISTENCE",
            "HEAD_CHANGED != PURPOSE_CHANGED",
            "REPO_EXISTENCE != PURPOSE",
            "AUTHORITY_CREATED = FALSE",
            "FINAL_DECISION = JASON",
        ],
        "delivery_contract": {
            "github_artifact": True,
            "drive_checkpoint_required": True,
            "gmail_delivery_required": True,
            "email_payload_class": ["INSTRUCTION", "UPDATE", "MANUAL"],
            "email_body_should_link_to_drive": True,
            "github_workflow_may_send_email": False,
            "reason": "Gmail/Drive delivery remains a separate authenticated operator-facing rail.",
        },
    }

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "flywheel-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Supreme Seymour Recursive Learning Flywheel v0.1",
        "",
        f"- Observed: {observed_at}",
        f"- Public repos: **{len(live_repos)}**",
        f"- Deltas: **{len(deltas)}**",
        f"- Unchanged: **{len(unchanged)}**",
        f"- Unknowns: **{len(unknowns)}**",
        "- Authority created: **false**",
        "- Final decision: **Jason**",
        "",
        "## Delta queue",
        "",
    ]
    if deltas:
        for d in deltas:
            md.append(f"- `{d['repo']}`: {d['delta_class']} — {d['reason']}")
    else:
        md.append("- No head-level delta observed.")

    md += [
        "",
        "## Delivery boundary",
        "",
        "This workflow does not email and does not write Google Drive.",
        "Its artifact is input to the separate operator-delivery rail:",
        "",
        "`GitHub artifact → Drive checkpoint/manual → Gmail link → Jason`",
        "",
        "No material delta may silently become purpose, authority, or action.",
    ]
    (OUTDIR / "flywheel-summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
