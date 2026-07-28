#!/usr/bin/env python3
"""Validate estate gate, hold, token, registry, and reconciliation artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "knowledge-management" / "generated"
FORBIDDEN_TEXT_KEYS = {"message", "title", "body"}


def load(name: str) -> dict[str, Any]:
    path = OUT / name
    if not path.exists():
        raise SystemExit(f"MISSING_ARTIFACT:{name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"ARTIFACT_NOT_OBJECT:{name}")
    return value


def require(value: dict[str, Any], expected: dict[str, type], name: str) -> None:
    for key, kind in expected.items():
        if key not in value:
            raise SystemExit(f"MISSING_FIELD:{name}:{key}")
        if not isinstance(value[key], kind):
            raise SystemExit(f"INVALID_FIELD_TYPE:{name}:{key}")
    if value.get("authority") is not False:
        raise SystemExit(f"AUTHORITY_NOT_FALSE:{name}")


def scan_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_TEXT_KEYS:
                raise SystemExit(f"FORBIDDEN_PRIVATE_TEXT_KEY:{path}.{key}")
            scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden(child, f"{path}[{index}]")


def validate_hold() -> None:
    gate = load("repository-estate-gate.json")
    require(gate, {
        "schema": str, "version": str, "state": str, "manifest_present": bool,
        "manifest_valid": bool, "errors": list, "live_inventory_executed": bool,
        "reconciliation_authorized": bool, "identity_claims_authorized": bool,
        "authority": bool,
    }, "gate")
    if gate["reconciliation_authorized"] is False:
        hold = load("repository-estate-hold.json")
        require(hold, {
            "schema": str, "version": str, "state": str, "reason": str,
            "errors": list, "count_state": str, "identity_state": str,
            "evidence_state": str, "live_inventory_executed": bool,
            "reconciliation_status": str, "reconciliation_authorized": bool,
            "authority": bool,
        }, "hold")
        if hold["live_inventory_executed"] or hold["reconciliation_authorized"]:
            raise SystemExit("HOLD_BOUNDARY_VIOLATION")
    scan_forbidden(gate)


def validate_authorized() -> None:
    validate_hold()
    token = load("repository-estate-token-gate.json")
    require(token, {
        "schema": str, "version": str, "owner": str, "state": str,
        "errors": list, "token_present": bool, "oauth_scopes_observed": list,
        "required_scope": str, "visible_trinity_anchors": list,
        "inventory_authorized": bool, "inventory_completeness_claimed": bool,
        "authority": bool,
    }, "token-gate")
    if token["inventory_authorized"] is not True:
        raise SystemExit("INVENTORY_NOT_AUTHORIZED")

    registry = load("repository-registry.json")
    require(registry, {
        "schema": str, "version": str, "generated_at": str, "owner": str,
        "inventory_mode": str, "repository_count": int,
        "content_fields_collected": bool, "inventory_completeness_claimed": bool,
        "repositories": list, "authority": bool,
    }, "registry")
    if registry["content_fields_collected"] or registry["inventory_completeness_claimed"]:
        raise SystemExit("REGISTRY_OVERCLAIM")
    scan_forbidden(registry)
    for row in registry["repositories"]:
        if row.get("visibility") == "private":
            if row.get("private_metadata_redacted") is not True:
                raise SystemExit("PRIVATE_METADATA_NOT_REDACTED")
            for key in ("description", "topics", "default_branch", "observations"):
                if key in row:
                    raise SystemExit(f"PRIVATE_FIELD_EXPORTED:{key}")

    reconciliation = load("repository-estate-reconciliation.json")
    require(reconciliation, {
        "schema": str, "version": str, "status": str,
        "historical_manifest": dict, "matched": list,
        "missing_or_renamed_unresolved": list,
        "added_or_renamed_unresolved": list,
        "classification_boundary": str, "portfolio_completion": str,
        "authority": bool,
    }, "reconciliation")
    scan_forbidden(reconciliation)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("hold", "authorized"), required=True)
    args = parser.parse_args()
    validate_hold() if args.mode == "hold" else validate_authorized()
    print("VALID")


if __name__ == "__main__":
    main()
