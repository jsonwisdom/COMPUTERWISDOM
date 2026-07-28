#!/usr/bin/env python3
"""Reconcile live GitHub inventory against the frozen historical 75/3/72 scope baseline."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "knowledge-management" / "config" / "repository-estate-baseline.json"
REGISTRY = ROOT / "knowledge-management" / "generated" / "repository-registry.json"
OUT_JSON = ROOT / "knowledge-management" / "generated" / "repository-estate-reconciliation.json"
OUT_MD = ROOT / "knowledge-management" / "generated" / "repository-estate-reconciliation.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    baseline = load(CONFIG)
    registry = load(REGISTRY)

    live_repositories = registry.get("repositories", [])
    live_names = {row.get("repository") for row in live_repositories if row.get("repository")}
    anchors = set(baseline["trinity_anchors"])
    live_anchor_names = sorted(live_names & anchors)
    live_non_anchor_names = sorted(live_names - anchors)

    expected = baseline["baseline_counts"]
    member_manifest = baseline["non_anchor_member_manifest"]

    reconciliation = {
        "schema": "JSONWisdom-Repository-Estate-Reconciliation",
        "version": "1.0.0",
        "baseline": {
            "repositories_observed": expected["repositories_observed"],
            "trinity_anchors": expected["trinity_anchors"],
            "non_anchor_estate": expected["non_anchor_estate"],
        },
        "live_inventory": {
            "inventory_mode": registry.get("inventory_mode"),
            "repositories_observed": len(live_names),
            "trinity_anchors_observed": len(live_anchor_names),
            "non_anchor_repositories_observed": len(live_non_anchor_names),
        },
        "anchor_presence": {
            "expected": sorted(anchors),
            "observed": live_anchor_names,
            "missing": sorted(anchors - live_names),
        },
        "original_72_member_manifest": {
            "status": member_manifest["status"],
            "captured_members": len(member_manifest.get("members", [])),
            "identity_reconciliation_possible": member_manifest["status"] == "CAPTURED",
        },
        "count_drift": {
            "total": len(live_names) - expected["repositories_observed"],
            "non_anchor": len(live_non_anchor_names) - expected["non_anchor_estate"],
            "interpretation": "DRIFT_REQUIRES_RECONCILIATION" if len(live_names) != expected["repositories_observed"] else "COUNT_MATCH_ONLY",
        },
        "portfolio_completion": {
            "status": "NOT_ESTABLISHED",
            "reason": "The original 72 repository names have not yet been captured as an evidence-backed baseline manifest.",
        },
        "boundaries": [
            "Live inventory does not rewrite the historical 75/3/72 baseline.",
            "Count equality alone does not establish member identity or audit completion.",
            "Canon-chain PASS is not portfolio completion.",
            "No repository is removed from scope by inference.",
            "authority=false",
        ],
        "authority": False,
    }

    OUT_JSON.write_text(json.dumps(reconciliation, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Repository Estate Reconciliation",
        "",
        "## Frozen historical scope",
        "",
        f"- Repositories observed: **{expected['repositories_observed']}**",
        f"- Trinity anchors: **{expected['trinity_anchors']}**",
        f"- Original non-anchor estate: **{expected['non_anchor_estate']}**",
        "",
        "## Live inventory",
        "",
        f"- Repositories observed now: **{len(live_names)}**",
        f"- Trinity anchors observed now: **{len(live_anchor_names)}**",
        f"- Non-anchor repositories observed now: **{len(live_non_anchor_names)}**",
        "",
        "## Constitutional status",
        "",
        "- Original 72-member name manifest: **NOT YET CAPTURED**",
        "- Portfolio completion: **NOT ESTABLISHED**",
        "- Canon-chain PASS: **component evidence only**",
        "- `authority: false`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
