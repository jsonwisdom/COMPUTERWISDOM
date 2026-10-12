#!/usr/bin/env python3
"""Quadratic priority allocator for PublicProof.

This module does NOT vote on candidate preference, guilt, truth, or election outcomes.
It allocates a fixed public attention budget across claims that participants want
independently verified next.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_BUDGET = 100
FORBIDDEN_DIMENSIONS = {
    "candidate_preference",
    "candidate_score",
    "party_preference",
    "party_score",
    "guilt",
    "truth_vote",
    "election_vote",
}


def ballot_cost(allocations: dict[str, int]) -> int:
    """Quadratic cost: sum(q_j^2) across claim-priority allocations."""
    return sum(q * q for q in allocations.values())


def validate_ballot(ballot: dict, allowed_claims: set[str], budget: int) -> None:
    forbidden = FORBIDDEN_DIMENSIONS.intersection(ballot)
    if forbidden:
        raise ValueError(f"forbidden political/verdict dimensions: {sorted(forbidden)}")

    allocations = ballot.get("allocations", {})
    if not isinstance(allocations, dict):
        raise ValueError("allocations must be an object mapping claim_id -> nonnegative integer")

    for claim_id, q in allocations.items():
        if claim_id not in allowed_claims:
            raise ValueError(f"unknown claim_id: {claim_id}")
        if isinstance(q, bool) or not isinstance(q, int) or q < 0:
            raise ValueError(f"allocation for {claim_id} must be a nonnegative integer")

    cost = ballot_cost(allocations)
    if cost > budget:
        raise ValueError(f"ballot exceeds budget: cost={cost}, budget={budget}")


def aggregate(doc: dict) -> dict:
    if doc.get("purpose") != "VERIFICATION_PRIORITY_ONLY":
        raise ValueError("purpose must be VERIFICATION_PRIORITY_ONLY")

    budget = doc.get("budget_per_participant", DEFAULT_BUDGET)
    if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
        raise ValueError("budget_per_participant must be a positive integer")

    claims = doc.get("claims", [])
    allowed_claims = {c["id"] for c in claims}
    status_by_claim = {c["id"]: c.get("status") for c in claims}
    totals: dict[str, int] = defaultdict(int)
    costs: dict[str, int] = {}

    ballots = doc.get("ballots", [])
    seen_participants: set[str] = set()
    for ballot in ballots:
        participant = ballot.get("participant_id")
        if not participant or not isinstance(participant, str):
            raise ValueError("each ballot requires participant_id")
        if participant in seen_participants:
            raise ValueError(f"duplicate participant_id: {participant}")
        seen_participants.add(participant)

        validate_ballot(ballot, allowed_claims, budget)
        allocations = ballot.get("allocations", {})
        costs[participant] = ballot_cost(allocations)
        for claim_id, q in allocations.items():
            totals[claim_id] += q

    matrix = [
        {
            "claim_id": claim_id,
            "evidence_status": status_by_claim[claim_id],
            "priority_votes": totals.get(claim_id, 0),
        }
        for claim_id in sorted(allowed_claims)
    ]
    matrix.sort(key=lambda row: (-row["priority_votes"], row["claim_id"]))

    return {
        "mode": doc.get("mode"),
        "purpose": "VERIFICATION_PRIORITY_ONLY",
        "budget_per_participant": budget,
        "participants": len(ballots),
        "ballot_costs": costs,
        "priority_matrix": matrix,
        "changes_evidence_status": False,
        "changes_candidate_score": False,
        "changes_election_result": False,
        "authority_created": False,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: quadratic_priority.py <matrix.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    doc = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(aggregate(doc), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
