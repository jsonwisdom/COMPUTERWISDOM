#!/usr/bin/env python3
"""Mechanical verifier for Jason's Dice 12 Justice Audit Lanes v0.1."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "fixtures/jaywisdom/fraud_ledger/JASONS_DICE_12_JUSTICE_LANES_V0_1.json"


def main() -> int:
    doc = json.loads(MAPPING.read_text(encoding="utf-8"))
    errors: list[str] = []

    if doc.get("format") != "JASONS_DICE_12_JUSTICE_LANES_V0.1":
        errors.append("FORMAT_INVALID")
    if doc.get("classification") != "PRECOMMITTED_RANDOMIZED_AUDIT_LANE_MAP":
        errors.append("CLASSIFICATION_INVALID")
    if doc.get("lane_count") != 12:
        errors.append("LANE_COUNT_INVALID")
    if doc.get("authority_created") is not False:
        errors.append("AUTHORITY_CREATED_MUST_BE_FALSE")

    dice = doc.get("dice", {})
    if dice.get("ordered_pair_required") is not True or dice.get("sum_is_not_used") is not True:
        errors.append("ORDERED_PAIR_RULE_INVALID")
    if dice.get("outcome_count") != 36:
        errors.append("OUTCOME_COUNT_INVALID")

    lanes = doc.get("lanes", [])
    lane_numbers = [x.get("lane") for x in lanes]
    if sorted(lane_numbers) != list(range(1, 13)):
        errors.append("LANE_IDS_NOT_EXACT_1_TO_12")
    if len({x.get("id") for x in lanes}) != 12:
        errors.append("LANE_NAMES_NOT_UNIQUE")

    mapping = doc.get("mapping", [])
    if len(mapping) != 36:
        errors.append("MAPPING_LENGTH_NOT_36")

    observed_pairs = set()
    counts = Counter()
    for row in mapping:
        a, b, lane = row.get("die_a"), row.get("die_b"), row.get("lane")
        pair = (a, b)
        if not (isinstance(a, int) and 1 <= a <= 6 and isinstance(b, int) and 1 <= b <= 6):
            errors.append(f"PAIR_OUT_OF_RANGE:{pair}")
            continue
        if pair in observed_pairs:
            errors.append(f"PAIR_DUPLICATED:{pair}")
        observed_pairs.add(pair)
        expected_lane = ((((a - 1) * 6) + b - 1) % 12) + 1
        if lane != expected_lane:
            errors.append(f"LANE_BINDING_MISMATCH:{pair}:{lane}!={expected_lane}")
        counts[lane] += 1

    expected_pairs = {(a, b) for a in range(1, 7) for b in range(1, 7)}
    if observed_pairs != expected_pairs:
        errors.append("NOT_ALL_36_ORDERED_PAIRS_PRESENT")
    if any(counts[lane] != 3 for lane in range(1, 13)):
        errors.append(f"UNEQUAL_LANE_COUNTS:{dict(sorted(counts.items()))}")

    fairness = doc.get("fairness", {})
    required_false = ["roll_selects_verdict", "roll_selects_guilt", "roll_creates_authority"]
    if fairness.get("mapping_frozen_before_roll") is not True:
        errors.append("PRECOMMITMENT_NOT_LOCKED")
    if fairness.get("roll_selects_lane_only") is not True:
        errors.append("ROLL_SCOPE_INVALID")
    for key in required_false:
        if fairness.get(key) is not False:
            errors.append(f"{key.upper()}_MUST_BE_FALSE")

    required_laws = {
        "RANDOMNESS_SELECTS_AUDIT_LANE_ONLY",
        "AUDIT_LANE != VERDICT",
        "ROLL != EVIDENCE",
        "ROLL != GUILT",
        "ROLL != AUTHORITY",
        "PASS != CLAIM_IS_TRUE",
        "PRECOMMITMENT_PRECEDES_SELECTION",
    }
    if not required_laws.issubset(set(doc.get("laws", []))):
        errors.append("REQUIRED_LAWS_MISSING")

    result = {
        "verifier": "JASONS_DICE_12_JUSTICE_LANES_VERIFIER_V0_1",
        "status": "PASS_WITH_BOUNDARY" if not errors else "FAIL",
        "ordered_outcomes_checked": len(observed_pairs),
        "lanes_checked": len(lanes),
        "outcomes_per_lane": {str(i): counts[i] for i in range(1, 13)},
        "equal_lane_probability": not errors and all(counts[i] == 3 for i in range(1, 13)),
        "lane_probability": "1/12" if not errors else "NOT_VERIFIED",
        "randomness_selects_lane_only": True,
        "randomness_quality_proven": False,
        "verdict_generated_by_dice": False,
        "guilt_generated_by_dice": False,
        "authority_created": False,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
