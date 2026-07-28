#!/usr/bin/env python3
"""Fail-honest capability gate for estate-wide GitHub inventory access."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "knowledge-management" / "generated"
TOKEN_GATE = OUT / "repository-estate-token-gate.json"
OWNER = os.environ.get("JSONWISDOM_OWNER", "jsonwisdom")
TOKEN = os.environ.get("ESTATE_AUDIT_PAT", "")
API = "https://api.github.com"
ANCHORS = {f"{OWNER}/AL", f"{OWNER}/COMPUTERWISDOM", f"{OWNER}/JOY"}


def request(path: str) -> tuple[Any, dict[str, str]]:
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "jsonwisdom-estate-token-gate")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as response:
        headers = {key.lower(): value for key, value in response.headers.items()}
        return json.load(response), headers


def paginate_owned() -> tuple[list[dict[str, Any]], dict[str, str]]:
    rows: list[dict[str, Any]] = []
    headers: dict[str, str] = {}
    page = 1
    while True:
        path = "/user/repos?" + urllib.parse.urlencode({
            "affiliation": "owner", "visibility": "all", "sort": "full_name",
            "per_page": "100", "page": str(page),
        })
        batch, headers = request(path)
        if not isinstance(batch, list):
            raise RuntimeError("AUTHENTICATED_REPOSITORY_RESPONSE_NOT_LIST")
        rows.extend(row for row in batch if row.get("owner", {}).get("login", "").lower() == OWNER.lower())
        if len(batch) < 100:
            break
        page += 1
    return rows, headers


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    observed_login: str | None = None
    oauth_scopes: list[str] = []
    visible_anchors: list[str] = []

    if not TOKEN:
        errors.append("ESTATE_AUDIT_PAT_MISSING")
    else:
        try:
            user, headers = request("/user")
            observed_login = user.get("login") if isinstance(user, dict) else None
            oauth_scopes = sorted(scope.strip() for scope in headers.get("x-oauth-scopes", "").split(",") if scope.strip())
            repos, _ = paginate_owned()
            names = {row.get("full_name") for row in repos if row.get("full_name")}
            visible_anchors = sorted(names & ANCHORS)
            if observed_login and observed_login.lower() != OWNER.lower():
                errors.append("TOKEN_OWNER_MISMATCH")
            if "repo" not in oauth_scopes:
                errors.append("OWNER_WIDE_PRIVATE_COVERAGE_NOT_PROVABLE")
            if set(visible_anchors) != ANCHORS:
                errors.append("TRINITY_ANCHOR_VISIBILITY_INCOMPLETE")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError, json.JSONDecodeError):
            errors.append("ESTATE_AUDIT_PAT_CAPABILITY_CHECK_FAILED")

    authorized = not errors
    receipt = {
        "schema": "JSONWisdom-Repository-Estate-Token-Gate",
        "version": "1.0.0",
        "owner": OWNER,
        "state": "INVENTORY_AUTHORIZED" if authorized else "BLOCKED",
        "errors": errors,
        "token_present": bool(TOKEN),
        "observed_login": observed_login,
        "oauth_scopes_observed": oauth_scopes,
        "required_scope": "repo",
        "visible_trinity_anchors": visible_anchors,
        "inventory_authorized": authorized,
        "inventory_completeness_claimed": False,
        "authority": False,
    }
    TOKEN_GATE.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("true" if authorized else "false")


if __name__ == "__main__":
    main()
