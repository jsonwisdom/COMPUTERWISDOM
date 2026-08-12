#!/usr/bin/env python3
"""CrissCross Auditor v0.1: test whether retained evidence uniquely recovers a claim."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def evidence_projection(case: dict, fields: list[str]) -> dict:
    return {field: case.get(field) for field in fields}


def audit(payload: dict) -> dict:
    claim_field = payload["claim_field"]
    evidence_fields = list(payload["evidence_fields"])
    cases = list(payload["cases"])

    groups: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        projection = evidence_projection(case, evidence_fields)
        encoded = canonical_json(projection).encode("utf-8")
        fingerprint = hashlib.sha256(encoded).hexdigest()
        groups[fingerprint].append(
            {
                "case_id": case.get("case_id"),
                "claim": case.get(claim_field),
                "evidence": projection,
            }
        )

    collisions = []
    for fingerprint, members in sorted(groups.items()):
        distinct_claims = sorted({canonical_json(member["claim"]) for member in members})
        if len(distinct_claims) > 1:
            collisions.append(
                {
                    "evidence_sha256": fingerprint,
                    "distinct_claims": [json.loads(value) for value in distinct_claims],
                    "cases": [member["case_id"] for member in members],
                }
            )

    return {
        "schema": "computerwisdom.crisscross_audit.v0.1",
        "claim_field": claim_field,
        "evidence_fields": evidence_fields,
        "case_count": len(cases),
        "collision_count": len(collisions),
        "collisions": collisions,
        "claim_recoverable": len(collisions) == 0,
        "label_not_evidence": True,
        "external_action_performed": False,
        "authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CrissCross vector JSON")
    parser.add_argument("--require-recoverable", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = audit(payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.require_recoverable and not result["claim_recoverable"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
