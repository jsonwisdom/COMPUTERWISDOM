#!/usr/bin/env python3
"""MASTER_ROOM deterministic repo router v1.

Read-only. Loads the public repo registry and routes a repo/object without
executing connectors or granting machine authority.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "PUBLIC_REPO_REGISTRY_V1.json"

def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def route(repo: str, action: str = "inspect") -> dict:
    data = load_registry()
    row = next((x for x in data["rows"] if x["repo"] == repo), None)
    if row is None:
        return {
            "repo": repo,
            "action": action,
            "terminal": "UNKNOWN",
            "route": "JASON_OPERATOR",
            "reason": "REPO_NOT_IN_PUBLIC_REGISTRY",
            "machine_authority_created": False,
        }
    if row["purpose_status"] != "VERIFIED_FROM_CURRENT_PUBLIC_TEXT":
        return {
            "repo": repo,
            "action": action,
            "purpose_status": row["purpose_status"],
            "terminal": "HOLD",
            "route": "JASON_OPERATOR_PURPOSE_GATE",
            "reason": "PURPOSE_NOT_PROVEN",
            "machine_authority_created": False,
        }
    return {
        "repo": repo,
        "action": action,
        "purpose": row["purpose"],
        "purpose_source": row["purpose_source"],
        "terminal": "PASS_FOR_ROUTING_ONLY",
        "route": row["master_room_route"],
        "machine_authority_created": False,
        "note": "Routing pass is not execution, promotion, legal authority, or proof of operator identity.",
    }

def status() -> dict:
    data = load_registry()
    rows = data["rows"]
    seated = sum(x["purpose_status"] == "VERIFIED_FROM_CURRENT_PUBLIC_TEXT" for x in rows)
    return {
        "object": "MASTER_ROOM_STATUS_V1",
        "public_repos": len(rows),
        "purpose_seated": seated,
        "purpose_unresolved": len(rows) - seated,
        "fan_out": "OFF",
        "operator_gate": data["operator_gate"],
        "machine_authority_created": False,
    }

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    r = sub.add_parser("route")
    r.add_argument("repo")
    r.add_argument("--action", default="inspect")
    args = p.parse_args()
    out = status() if args.cmd == "status" else route(args.repo, args.action)
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
