#!/usr/bin/env python3
"""Build a read-only, evidence-linked Trinity registry for JSONWisdom repositories."""

from __future__ import annotations

import json
import os
import re
import urllib.error
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

TRINITY = {
    "AL": "proof",
    "COMPUTERWISDOM": "memory",
    "JOY": "meaning",
}

SIGNALS = {
    "proof": ["proof", "receipt", "replay", "verify", "audit", "evidence", "provenance", "attestation", "alms", "risk", "detector"],
    "memory": ["knowledge", "memory", "index", "portal", "computerwisdom", "registry", "graph", "map", "discovery", "crawler"],
    "meaning": ["joy", "family", "wisdom", "legacy", "consent", "story", "sophia", "grammy", "papa", "sister", "daughter"],
    "base_substrate": ["base", "eas", "ens", "chainlink", "contract"],
    "zora_distribution": ["zora", "mint", "contentcoin", "market snapshot"],
    "minnesota_fixture": ["minnesota", "mn-", "st. cloud", "civic", "court", "ago"],
    "agent_runtime": ["agent", "copilot", "mcp", "chatkit"],
    "specification": ["spec", "schema", "protocol", "rfc", "constitution"],
}


def api(path: str) -> Any:
    url = path if path.startswith("https://") else f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "jsonwisdom-trinity-audit")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in {404, 409, 422}:
            return None
        raise


def paginate(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    page = 1
    separator = "&" if "?" in path else "?"
    while True:
        data = api(f"{path}{separator}per_page=100&page={page}")
        if not isinstance(data, list) or not data:
            break
        rows.extend(data)
        if len(data) < 100:
            break
        page += 1
    return rows


def discover_repositories() -> tuple[list[dict[str, Any]], str]:
    authenticated = paginate("/user/repos?affiliation=owner&sort=full_name") if TOKEN else []
    owned = [r for r in authenticated if r.get("owner", {}).get("login", "").lower() == OWNER.lower()]
    if owned:
        return owned, "authenticated-owner-inventory"
    return paginate(f"/users/{urllib.parse.quote(OWNER)}/repos?type=owner&sort=full_name"), "public-owner-inventory"


def compact_text(repo: dict[str, Any], commits: list[dict[str, Any]], pulls: list[dict[str, Any]]) -> str:
    parts = [repo.get("name", ""), repo.get("description") or "", " ".join(repo.get("topics") or [])]
    parts.extend((c.get("commit", {}).get("message") or "").splitlines()[0] for c in commits)
    parts.extend((p.get("title") or "") for p in pulls)
    return " ".join(parts).lower()


def classify(repo: dict[str, Any], commits: list[dict[str, Any]], pulls: list[dict[str, Any]]) -> tuple[str, str, list[str]]:
    name = repo.get("name", "")
    if name in TRINITY:
        return "trinity_root", TRINITY[name], [f"Exact Trinity repository: {name}"]

    text = compact_text(repo, commits, pulls)
    scores: Counter[str] = Counter()
    evidence: list[str] = []
    for role, terms in SIGNALS.items():
        for term in terms:
            if term in text:
                scores[role] += 1
                evidence.append(f"Matched signal '{term}' for {role}")

    if repo.get("archived"):
        return "archive", "unassigned", ["GitHub archived flag is true"]
    if not scores:
        if repo.get("size", 0) == 0:
            return "unknown", "unassigned", ["No semantic signal found; repository is empty"]
        return "unknown", "unassigned", ["No sufficient semantic signal found"]

    role, top = scores.most_common(1)[0]
    tied = [candidate for candidate, score in scores.items() if score == top]
    if len(tied) > 1:
        return "unknown", "unassigned", [f"Ambiguous top signals: {', '.join(sorted(tied))}"] + evidence[:8]

    leg = {"proof": "proof", "memory": "memory", "meaning": "meaning"}.get(role, "cross_trinity")
    return role, leg, evidence[:8]


def importance(repo: dict[str, Any], commits: list[dict[str, Any]], pulls: list[dict[str, Any]], role: str) -> dict[str, int]:
    # Deliberately excludes repository size.
    recent_activity = min(100, len(commits) * 15 + len(pulls) * 10)
    trinity_bonus = 100 if role == "trinity_root" else 0
    evidence_strength = min(100, 20 + len(commits) * 12 + len(pulls) * 8)
    identity = 100 if repo.get("name") in TRINITY else (70 if re.search(r"jason|jay|wisdom", repo.get("name", ""), re.I) else 20)
    return {
        "identity_relevance": max(identity, trinity_bonus),
        "recurrence": recent_activity,
        "dependency_weight": trinity_bonus,
        "human_value": 100 if role in {"trinity_root", "meaning"} else 40,
        "evidence_strength": evidence_strength,
        "active_urgency": 70 if pulls else 20,
    }


def main() -> None:
    repos, inventory_mode = discover_repositories()
    records: list[dict[str, Any]] = []

    for repo in sorted(repos, key=lambda item: item.get("name", "").lower()):
        full_name = repo["full_name"]
        commits = api(f"/repos/{full_name}/commits?per_page=5") or []
        pulls = api(f"/repos/{full_name}/pulls?state=all&sort=updated&direction=desc&per_page=5") or []
        role, leg, evidence = classify(repo, commits, pulls)
        records.append({
            "repository": full_name,
            "visibility": repo.get("visibility", "private" if repo.get("private") else "public"),
            "archived": bool(repo.get("archived")),
            "default_branch": repo.get("default_branch"),
            "description": repo.get("description"),
            "updated_at": repo.get("updated_at"),
            "classification": {
                "role": role,
                "trinity_leg": leg,
                "state": "observed" if role != "unknown" else "unknown",
                "evidence": evidence,
            },
            "importance": importance(repo, commits, pulls, role),
            "observations": {
                "recent_commits": [
                    {"sha": c.get("sha"), "message": (c.get("commit", {}).get("message") or "").splitlines()[0]}
                    for c in commits[:5]
                ],
                "recent_pull_requests": [
                    {"number": p.get("number"), "title": p.get("title"), "state": p.get("state")}
                    for p in pulls[:5]
                ],
            },
            "authority": False,
        })

    generated_at = datetime.now(timezone.utc).isoformat()
    registry = {
        "schema": "JSONWisdom-Trinity-Repository-Registry",
        "version": "0.1.0",
        "generated_at": generated_at,
        "owner": OWNER,
        "inventory_mode": inventory_mode,
        "repository_count": len(records),
        "private_repo_boundary": "Private repositories are included only when GH_TOKEN has explicit read access.",
        "trinity": {"proof": "jsonwisdom/AL", "memory": "jsonwisdom/COMPUTERWISDOM", "meaning": "jsonwisdom/JOY"},
        "rules": ["importance_not_size", "evidence_required", "unknown_is_valid", "read_only_audit", "authority_false"],
        "repositories": records,
        "authority": False,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "repository-registry.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    counts = Counter(r["classification"]["role"] for r in records)
    unknown = [r["repository"] for r in records if r["classification"]["role"] == "unknown"]
    lines = [
        "# JSONWisdom Trinity Repository Audit",
        "",
        f"Generated: `{generated_at}`",
        f"Inventory mode: `{inventory_mode}`",
        f"Repositories observed: **{len(records)}**",
        "",
        "## Trinity",
        "",
        "- **AL** — Proof",
        "- **COMPUTERWISDOM** — Memory and coordination",
        "- **JOY** — Meaning and family continuity",
        "",
        "## Classification counts",
        "",
    ]
    lines.extend(f"- `{role}`: {count}" for role, count in sorted(counts.items()))
    lines.extend(["", "## Unknown / requires human or deeper AI review", ""])
    lines.extend(f"- `{name}`" for name in unknown) if unknown else lines.append("- None")
    lines.extend([
        "",
        "## Boundaries",
        "",
        "- Repository size is recorded by GitHub but is not used in importance scoring.",
        "- This workflow performs no deletion, archival, merge, or repository mutation.",
        "- A heuristic classification is not canon; every record carries its evidence.",
        "- Private repositories require an explicitly configured read token.",
        "- `authority: false`",
    ])
    (OUT / "repository-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
