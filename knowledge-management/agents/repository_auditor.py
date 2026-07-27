#!/usr/bin/env python3
"""Machine-speed, evidence-bounded repository inventory and Trinity routing.

This first agentic slice uses GitHub metadata only. It never claims semantic certainty
from a repository name, size, or visibility. Ambiguous repositories remain UNKNOWN.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

OWNER = os.environ.get("GITHUB_OWNER", "jsonwisdom")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path("knowledge-management/generated")
API = "https://api.github.com"

TRINITY_RULES = {
    "AL": [r"\bal\b", r"alms", r"verify", r"proof", r"receipt", r"replay", r"audit", r"risk", r"detector"],
    "COMPUTERWISDOM": [r"computerwisdom", r"index", r"portal", r"registry", r"knowledge", r"agent", r"server", r"software"],
    "JOY": [r"\bjoy\b", r"family", r"wisdom", r"legacy", r"memory", r"braelee", r"breann", r"destinee", r"grammy", r"grandaddy", r"heidee", r"jaycee", r"leeann", r"marydee", r"papa", r"uncled"],
}

DOMAIN_RULES = {
    "X402": [r"x402", r"payment"],
    "BASE": [r"\bbase\b", r"eas", r"8453", r"basenames"],
    "EAS": [r"\beas\b", r"attestation"],
    "ENS": [r"\bens\b", r"jaywisdom\.eth", r"jaywisdom\.base\.eth"],
    "ZORA": [r"zora", r"contentcoin", r"mint"],
    "MINNESOTA": [r"minnesota", r"\bmn\b", r"st\. cloud", r"waite park"],
    "REPLAYOS": [r"replayos", r"replay-membrane"],
    "RECEIPTOS": [r"receiptos", r"receipts-engine", r"receipt"],
}

SENSITIVE_NAME_PATTERNS = [r"private", r"secret", r"stash", r"key", r"wallet", r"seed"]


def request_json(path: str, params: dict[str, str] | None = None) -> Any:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "jsonwisdom-repository-audit",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {exc.code}: {body}") from exc


def list_repositories() -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        batch = request_json(
            f"/users/{OWNER}/repos",
            {"per_page": "100", "page": str(page), "type": "owner", "sort": "full_name"},
        )
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def matches(patterns: list[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]


def classify(repo: dict[str, Any]) -> dict[str, Any]:
    text = " ".join(
        str(value or "")
        for value in [repo.get("name"), repo.get("description"), " ".join(repo.get("topics") or [])]
    )

    trinity_evidence = {
        leg: matches(patterns, text) for leg, patterns in TRINITY_RULES.items()
    }
    ranked = sorted(trinity_evidence.items(), key=lambda item: len(item[1]), reverse=True)
    primary = ranked[0][0] if ranked and len(ranked[0][1]) >= 2 else "UNKNOWN"
    confidence = "PARTIAL" if primary != "UNKNOWN" else "UNKNOWN"

    domains = [name for name, patterns in DOMAIN_RULES.items() if matches(patterns, text)]
    sensitive_name = bool(matches(SENSITIVE_NAME_PATTERNS, text))

    visibility = "PRIVATE" if repo.get("private") else "PUBLIC"
    security = "REVIEW_REQUIRED" if sensitive_name else "NO_SECRET_SIGNAL_FROM_METADATA"
    if visibility == "PRIVATE":
        security = "PRIVATE_CONTENT_NOT_EXPORTED"

    evidence = {
        "source": "GitHub repository metadata API",
        "observed_fields": [
            "full_name", "visibility", "archived", "fork", "default_branch",
            "created_at", "updated_at", "pushed_at", "topics", "description"
        ],
        "semantic_contents_reviewed": False,
        "trinity_rule_matches": trinity_evidence,
    }

    return {
        "repository": repo["full_name"],
        "repository_id": repo["id"],
        "visibility": visibility,
        "archived": bool(repo.get("archived")),
        "fork": bool(repo.get("fork")),
        "default_branch": repo.get("default_branch"),
        "description": repo.get("description"),
        "topics": repo.get("topics") or [],
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "trinity": {
            "primary": primary,
            "confidence": confidence,
            "requires_semantic_audit": True,
        },
        "domains": sorted(domains),
        "security": security,
        "evidence": evidence,
        "authority": False,
    }


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def write_json(name: str, value: Any) -> None:
    path = OUT / name
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    observed_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    repos = list_repositories()
    records = [classify(repo) for repo in repos]

    public_records = [record for record in records if record["visibility"] == "PUBLIC"]
    private_index = [
        {
            "repository": record["repository"],
            "visibility": "PRIVATE",
            "content_exported": False,
            "security": record["security"],
            "authority": False,
        }
        for record in records if record["visibility"] == "PRIVATE"
    ]
    unknown = [record["repository"] for record in records if record["trinity"]["primary"] == "UNKNOWN"]

    inventory = {
        "schema": "JSONWisdom-Repository-Inventory",
        "version": "0.1.0",
        "owner": OWNER,
        "observed_at": observed_at,
        "repository_count": len(records),
        "records": records,
        "authority": False,
    }
    receipt = {
        "schema": "JSONWisdom-Audit-Receipt",
        "version": "0.1.0",
        "observed_at": observed_at,
        "owner": OWNER,
        "repository_count": len(records),
        "public_count": len(public_records),
        "private_count": len(private_index),
        "unknown_count": len(unknown),
        "inventory_sha256": hashlib.sha256(canonical_bytes(inventory)).hexdigest(),
        "limitations": [
            "Metadata-only classification",
            "Repository size excluded from importance and routing",
            "Private repository contents not exported",
            "No legal identity or wallet ownership claims",
            "No EAS, ENS, Base, X402, or Zora success claim without separate receipts",
        ],
        "authority": False,
    }

    write_json("repository-inventory.json", inventory)
    write_json("public-registry.json", {"observed_at": observed_at, "records": public_records, "authority": False})
    write_json("private-registry.json", {"observed_at": observed_at, "records": private_index, "authority": False})
    write_json("unknown-repositories.json", {"observed_at": observed_at, "repositories": unknown, "authority": False})
    write_json("audit-receipt.json", receipt)

    (OUT / "resume.md").write_text(
        "# JSONWisdom Agentic Audit Resume\n\n"
        f"Observed: `{observed_at}`\n\n"
        f"Repositories inventoried: **{len(records)}**\n\n"
        f"Public: **{len(public_records)}**  \nPrivate: **{len(private_index)}**  \n"
        f"Trinity role still UNKNOWN: **{len(unknown)}**\n\n"
        "Next action: semantic agents inspect README, PR lineage, workflows, and canonical manifests for UNKNOWN and PARTIAL records.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
