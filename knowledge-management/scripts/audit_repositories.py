#!/usr/bin/env python3
"""Build a read-only, metadata-bounded live repository registry after all estate gates pass."""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OWNER = os.environ.get("JSONWISDOM_OWNER", "jsonwisdom")
TOKEN = os.environ.get("GH_TOKEN", "")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "knowledge-management" / "generated"

TRINITY = {"AL": "proof", "COMPUTERWISDOM": "memory", "JOY": "meaning"}
SIGNALS = {
    "proof": ["proof", "receipt", "replay", "verify", "audit", "evidence", "provenance"],
    "memory": ["knowledge", "memory", "index", "portal", "computerwisdom", "registry"],
    "meaning": ["joy", "family", "wisdom", "legacy", "consent", "story"],
    "specification": ["spec", "schema", "protocol", "rfc", "constitution"],
}


def api(path: str) -> Any:
    if not TOKEN:
        raise SystemExit("ESTATE_AUDIT_PAT_REQUIRED")
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "jsonwisdom-trinity-audit")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def discover_repositories() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    page = 1
    while True:
        query = urllib.parse.urlencode({
            "affiliation": "owner", "visibility": "all", "sort": "full_name",
            "per_page": "100", "page": str(page),
        })
        batch = api(f"/user/repos?{query}")
        if not isinstance(batch, list):
            raise SystemExit("AUTHENTICATED_REPOSITORY_RESPONSE_NOT_LIST")
        rows.extend(row for row in batch if row.get("owner", {}).get("login", "").lower() == OWNER.lower())
        if len(batch) < 100:
            break
        page += 1
    return rows


def classify(repo: dict[str, Any]) -> tuple[str, str, list[str]]:
    name = repo.get("name", "")
    if name in TRINITY:
        return "trinity_root", TRINITY[name], [f"Exact Trinity repository: {name}"]
    if repo.get("private"):
        return "unknown", "unassigned", ["Private descriptive metadata redacted; no semantic classification performed"]
    text = " ".join([name, repo.get("description") or "", " ".join(repo.get("topics") or [])]).lower()
    scores: Counter[str] = Counter()
    evidence: list[str] = []
    for role, terms in SIGNALS.items():
        for term in terms:
            if term in text:
                scores[role] += 1
                evidence.append(f"Matched metadata signal '{term}' for {role}")
    if repo.get("archived"):
        return "archive", "unassigned", ["GitHub archived flag is true"]
    if not scores:
        return "unknown", "unassigned", ["No sufficient public metadata signal found"]
    role, top = scores.most_common(1)[0]
    if sum(1 for score in scores.values() if score == top) > 1:
        return "unknown", "unassigned", ["Ambiguous top metadata signals"] + evidence[:8]
    return role, {"proof": "proof", "memory": "memory", "meaning": "meaning"}.get(role, "cross_trinity"), evidence[:8]


def main() -> None:
    repos = discover_repositories()
    records: list[dict[str, Any]] = []
    for repo in sorted(repos, key=lambda item: item.get("name", "").lower()):
        role, leg, evidence = classify(repo)
        private = bool(repo.get("private"))
        record = {
            "repository": repo["full_name"],
            "repository_id": repo.get("id"),
            "visibility": "private" if private else repo.get("visibility", "public"),
            "archived": bool(repo.get("archived")),
            "updated_at": repo.get("updated_at"),
            "classification": {
                "role": role,
                "trinity_leg": leg,
                "state": "observed" if role != "unknown" else "unknown",
                "evidence": evidence,
            },
            "private_metadata_redacted": private,
            "authority": False,
        }
        if not private:
            record["description"] = repo.get("description")
            record["topics"] = repo.get("topics") or []
            record["default_branch"] = repo.get("default_branch")
        records.append(record)

    generated_at = datetime.now(timezone.utc).isoformat()
    registry = {
        "schema": "JSONWisdom-Trinity-Repository-Registry",
        "version": "1.0.0",
        "generated_at": generated_at,
        "owner": OWNER,
        "inventory_mode": "authenticated-owner-inventory",
        "repository_count": len(records),
        "content_fields_collected": False,
        "inventory_completeness_claimed": False,
        "repositories": records,
        "authority": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "repository-registry.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    (OUT / "repository-audit.md").write_text(
        "# JSONWisdom Live Repository Registry\n\n"
        f"- Generated: `{generated_at}`\n"
        f"- Repositories observed: **{len(records)}**\n"
        "- Endpoint: **authenticated `/user/repos` filtered by exact owner**\n"
        "- Commit messages, PR titles, and bodies collected: **no**\n"
        "- Private descriptive metadata: **redacted**\n"
        "- Inventory completeness claimed: **no**\n"
        "- `authority: false`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
