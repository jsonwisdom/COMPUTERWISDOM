#!/usr/bin/env python3
"""Five-invariant validator for INTERNAL_RULES_SCHISM_POC_0001.

This validates specimen integrity only. PASS does not verify the underlying
legal proposition while primary source bytes remain unavailable.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

NONE = type(None)
REQUIRED_PATH_TYPES = {
    "poc_id": str,
    "rule_id": str,
    "version_id": str,
    "state": str,
    "source_attestation": dict,
    "source_attestation.publisher": str,
    "source_attestation.canonical_url": (str, NONE),
    "source_attestation.retrieved_at": (str, NONE),
    "source_attestation.media_type": (str, NONE),
    "source_attestation.byte_length": (int, NONE),
    "source_attestation.sha256": (str, NONE),
    "source_attestation.redirect_chain": list,
    "source_attestation.etag": (str, NONE),
    "source_attestation.last_modified": (str, NONE),
    "source_attestation.retrieval_method": (str, NONE),
    "source_attestation.primary_source_verified": bool,
    "source_attestation.notes": str,
    "dates": dict,
    "dates.issued_at": (str, NONE),
    "dates.effective_from": (str, NONE),
    "dates.applicability_start": (str, NONE),
    "scope": dict,
    "unknown_scope_factors": dict,
    "authority_scope": str,
    "court_binding": bool,
    "congress_binding": bool,
    "authority_created": bool,
    "parent_version": str,
    "parent_version_verified": bool,
    "supersedes": list,
    "delta": dict,
    "delta.delta_id": str,
    "delta.status": str,
    "delta.operation": str,
    "delta.subject": str,
    "delta.dimension": str,
    "delta.before": str,
    "delta.after": str,
    "delta.conditions_added": list,
    "delta.conditions_removed": list,
    "delta.source_span": (str, NONE),
    "delta.confidence": (int, float),
    "precedent_match": dict,
    "queries": dict,
    "ci_certificate": dict,
    "ci_certificate.primary_object": str,
    "ci_certificate.source_bytes": str,
    "ci_certificate.source_sha256": str,
    "ci_certificate.version_parent": str,
    "ci_certificate.issued_at": str,
    "ci_certificate.applicability_start": str,
    "ci_certificate.machine_delta": str,
    "ci_certificate.scope_expansion": str,
    "ci_certificate.precedent_graph": str,
    "ci_certificate.tension": str,
    "ci_certificate.automatic_reliance": str,
    "ci_certificate.recommended_action": str,
    "ci_certificate.final_state": str,
    "ci_certificate.epistemic_gate": str,
    "epistemic_status": dict,
    "epistemic_status.primary_source": str,
    "epistemic_status.dates": dict,
    "epistemic_status.scope": str,
    "epistemic_status.delta": str,
    "epistemic_status.precedent_match": str,
}


def _lookup(obj: dict, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(dotted)
        cur = cur[part]
    return cur


def _schema_ok(obj: dict) -> bool:
    try:
        return all(isinstance(_lookup(obj, path), types) for path, types in REQUIRED_PATH_TYPES.items())
    except KeyError:
        return False


def _date(value):
    return dt.date.fromisoformat(value) if value else None


def validate(obj: dict, raw: bytes) -> dict:
    att = obj["source_attestation"]
    dates = obj["dates"]
    delta = obj["delta"]
    cert = obj["ci_certificate"]

    checks = {
        "schema_validation": _schema_ok(obj),
        "hash_invariant": not (att.get("sha256") is None and att.get("primary_source_verified") is True),
        "date_logic": (
            _date(dates.get("applicability_start")) is None
            or _date(dates.get("issued_at")) is None
            or _date(dates.get("applicability_start")) <= _date(dates.get("issued_at"))
        ),
        "delta_coherence": (
            delta.get("operation") != "EXPAND_SCOPE"
            or (
                isinstance(delta.get("after"), str)
                and bool(delta["after"].strip())
                and isinstance(delta.get("conditions_added"), list)
                and len(delta["conditions_added"]) > 0
            )
        ),
        "ci_cascade": not (
            att.get("primary_source_verified") is False
            and cert.get("final_state") not in {"HOLD_PRIMARY_BYTES", "FETCH_PRIMARY_SOURCE"}
        ),
    }

    return {
        "validator": "computerwisdom.internal_rules_schism.poc_validator.v0.1",
        "poc_id": obj.get("poc_id"),
        "specimen_sha256": hashlib.sha256(raw).hexdigest(),
        "checks": {name: ("PASS" if ok else "FAIL") for name, ok in checks.items()},
        "integrity_gate": "PASS" if all(checks.values()) else "FAIL",
        "rule_verification": cert.get("final_state"),
        "primary_source_verified": att.get("primary_source_verified"),
        "authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rule", type=Path)
    args = parser.parse_args()
    raw = args.rule.read_bytes()
    obj = json.loads(raw)
    result = validate(obj, raw)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["integrity_gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
