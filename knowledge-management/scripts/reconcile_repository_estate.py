#!/usr/bin/env python3
"""Gate repository-estate reconciliation on an admissible historical 72-member manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "knowledge-management" / "config" / "repository-estate-baseline.json"
MANIFEST = ROOT / "receipts" / "estate" / "ORIGINAL_72_MANIFEST_V1.json"
REGISTRY = ROOT / "knowledge-management" / "generated" / "repository-registry.json"
OUT = ROOT / "knowledge-management" / "generated"
GATE_JSON = OUT / "repository-estate-gate.json"
HOLD_JSON = OUT / "repository-estate-hold.json"
HOLD_MD = OUT / "repository-estate-hold.md"
RECON_JSON = OUT / "repository-estate-reconciliation.json"
RECON_MD = OUT / "repository-estate-reconciliation.md"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_baseline(baseline: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    counts = baseline.get("baseline_counts", {})
    if counts.get("repositories_observed") != 75:
        errors.append("BASELINE_TOTAL_NOT_75")
    if counts.get("trinity_anchors") != 3:
        errors.append("BASELINE_ANCHORS_NOT_3")
    if counts.get("non_anchor_estate") != 72:
        errors.append("BASELINE_NON_ANCHOR_NOT_72")
    if baseline.get("authority") is not False:
        errors.append("BASELINE_AUTHORITY_NOT_FALSE")
    return errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    members = manifest.get("original_72_non_anchor")
    if not isinstance(members, list):
        errors.append("ORIGINAL_72_LIST_MISSING")
    elif len(members) != 72:
        errors.append("ORIGINAL_72_COUNT_NOT_72")

    for field in (
        "capture_timestamp_utc",
        "capture_source",
        "source_artifact_hash",
        "manifest_sha256",
    ):
        if not manifest.get(field):
            errors.append(f"{field.upper()}_MISSING")

    if manifest.get("authority") is not False:
        errors.append("MANIFEST_AUTHORITY_NOT_FALSE")
    return errors


def write_gate() -> bool:
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = load(BASELINE)
    errors = validate_baseline(baseline)

    manifest_present = MANIFEST.exists()
    if manifest_present:
        try:
            manifest = load(MANIFEST)
            errors.extend(validate_manifest(manifest))
        except (OSError, json.JSONDecodeError):
            errors.append("ORIGINAL_72_MANIFEST_INVALID_JSON")

    if not manifest_present:
        errors.append("ORIGINAL_72_MANIFEST_MISSING")

    authorized = manifest_present and not errors
    gate = {
        "schema": "JSONWisdom-Repository-Estate-Gate",
        "version": "1.0.0",
        "state": "RECONCILIATION_AUTHORIZED" if authorized else "CONSTITUTIONAL_HOLD",
        "historical_baseline": {
            "repositories_observed": 75,
            "trinity_anchors": 3,
            "non_anchor_estate": 72,
        },
        "manifest_path": str(MANIFEST.relative_to(ROOT)),
        "manifest_present": manifest_present,
        "manifest_valid": manifest_present and not errors,
        "errors": errors,
        "live_inventory_executed": False,
        "reconciliation_authorized": authorized,
        "identity_claims_authorized": authorized,
        "authority": False,
    }
    GATE_JSON.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if not authorized:
        hold = {
            "schema": "JSONWisdom-Repository-Estate-Hold",
            "version": "1.0.0",
            "state": "CONSTITUTIONAL_HOLD",
            "reason": "Original 72-member historical manifest is absent or invalid.",
            "errors": errors,
            "count_state": "KNOWN_75_3_72",
            "identity_state": "UNKNOWN",
            "evidence_state": "EMPTY",
            "live_inventory_executed": False,
            "reconciliation_status": "PENDING",
            "reconciliation_authorized": False,
            "authority": False,
        }
        HOLD_JSON.write_text(json.dumps(hold, indent=2) + "\n", encoding="utf-8")
        HOLD_MD.write_text(
            "# Repository Estate Constitutional Hold\n\n"
            "- Count: **known (75 / 3 / 72)**\n"
            "- Identities: **unknown**\n"
            "- Historical manifest: **missing or invalid**\n"
            "- Live inventory executed: **no**\n"
            "- Reconciliation: **pending and unauthorized**\n"
            "- `authority: false`\n",
            encoding="utf-8",
        )
    return authorized


def reconcile() -> None:
    gate = load(GATE_JSON) if GATE_JSON.exists() else {}
    if gate.get("reconciliation_authorized") is not True:
        raise SystemExit("RECONCILIATION_NOT_AUTHORIZED")
    if not REGISTRY.exists():
        raise SystemExit("LIVE_REGISTRY_MISSING")

    baseline = load(BASELINE)
    manifest = load(MANIFEST)
    registry = load(REGISTRY)

    historical_names = manifest["original_72_non_anchor"]
    live_rows = registry.get("repositories", [])
    live_names = [row.get("repository") for row in live_rows if row.get("repository")]

    historical_set = set(historical_names)
    live_set = set(live_names)
    anchors = set(baseline["trinity_anchors"])
    live_non_anchor = live_set - anchors

    reconciliation = {
        "schema": "JSONWisdom-Repository-Estate-Reconciliation",
        "version": "1.0.0",
        "status": "IDENTITY_COMPARISON_EXECUTED",
        "historical_manifest": {
            "path": str(MANIFEST.relative_to(ROOT)),
            "member_count": len(historical_names),
            "manifest_sha256": manifest["manifest_sha256"],
        },
        "matched": sorted(historical_set & live_non_anchor),
        "missing_or_renamed_unresolved": sorted(historical_set - live_non_anchor),
        "added_or_renamed_unresolved": sorted(live_non_anchor - historical_set),
        "classification_boundary": "Rename, split, merge, visibility change, deletion, and addition require separate evidence.",
        "portfolio_completion": "NOT_ESTABLISHED",
        "authority": False,
    }
    RECON_JSON.write_text(json.dumps(reconciliation, indent=2) + "\n", encoding="utf-8")
    RECON_MD.write_text(
        "# Repository Estate Reconciliation\n\n"
        f"- Historical identities compared: **{len(historical_names)}**\n"
        f"- Exact-name matches: **{len(reconciliation['matched'])}**\n"
        f"- Missing or renamed unresolved: **{len(reconciliation['missing_or_renamed_unresolved'])}**\n"
        f"- Added or renamed unresolved: **{len(reconciliation['added_or_renamed_unresolved'])}**\n"
        "- Portfolio completion: **not established**\n"
        "- `authority: false`\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--gate-only", action="store_true")
    mode.add_argument("--reconcile", action="store_true")
    args = parser.parse_args()

    if args.gate_only:
        write_gate()
    else:
        reconcile()


if __name__ == "__main__":
    main()
