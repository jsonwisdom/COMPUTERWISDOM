#!/usr/bin/env python3
"""Deterministic evidence scorer for PublicProof fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

WEIGHTS = {
    "primary_government_record": 100,
    "full_original_video": 80,
    "independent_corroboration": 60,
    "complete_contextual_quote": 40,
    "campaign_party_assertion": 10,
    "cropped_viral_clip": 0,
    "unsupported_accusation": -50,
    "proven_fabrication": -100,
}

ALLOWED_STATUS = {
    "VERIFIED",
    "FALSE",
    "HOLD",
    "VIDEO_NEEDED",
    "NOT_PROVEN",
    "NOT_ESTABLISHED",
}

FORBIDDEN_SCORE_FIELDS = {"party", "political_party", "office", "candidate_identity"}


def validate(doc: dict) -> None:
    scoring = doc.get("scoring", {})
    bad = FORBIDDEN_SCORE_FIELDS.intersection(scoring)
    if bad:
        raise ValueError(f"forbidden identity-based scoring fields: {sorted(bad)}")

    for claim in doc.get("claims", []):
        status = claim.get("status")
        if status not in ALLOWED_STATUS:
            raise ValueError(f"invalid claim status {status!r}: {claim.get('id')}")

    for item in doc.get("evidence", []):
        kind = item.get("type")
        if kind not in WEIGHTS:
            raise ValueError(f"unknown evidence type {kind!r}: {item.get('id')}")
        if item.get("points") != WEIGHTS[kind]:
            raise ValueError(
                f"noncanonical points for {item.get('id')}: "
                f"expected {WEIGHTS[kind]}, got {item.get('points')}"
            )


def score(doc: dict) -> dict:
    validate(doc)
    evidence = doc.get("evidence", [])
    total = sum(item["points"] for item in evidence)
    return {
        "game": doc.get("game"),
        "round_id": doc.get("round_id"),
        "evidence_count": len(evidence),
        "evidence_score": total,
        "claim_states": {c["id"]: c["status"] for c in doc.get("claims", [])},
        "party_scoring": False,
        "authority_created": False,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: publicproof.py <fixture.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    doc = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(score(doc), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
