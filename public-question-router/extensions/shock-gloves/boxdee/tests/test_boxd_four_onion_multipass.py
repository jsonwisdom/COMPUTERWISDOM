#!/usr/bin/env python3
"""Fail-closed checks for BoxD Four Onion + LeeLoo Multi Pass."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "BOXD_MULTI_PASS_HOLD_0001.json"
SCHEMA = ROOT / "schemas" / "boxd_four_onion_multipass.v0_1.schema.json"


def aggregate(states: list[str]) -> str:
    if "REJECT" in states:
        return "MULTI_PASS_REJECT"
    if "CONFLICT" in states:
        return "MULTI_PASS_CONFLICT"
    if "HOLD" in states:
        return "MULTI_PASS_HOLD"
    assert states and all(state == "PASS" for state in states)
    return "MULTI_PASS_PASS"


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert schema["title"] == "BoxD Four Onion LeeLoo Multi Pass v0.1"
    assert fixture["authority_created"] is False
    assert fixture["legal_finding_created"] is False

    onion_states = [
        fixture["record_onion"]["state"],
        fixture["authority_onion"]["state"],
        fixture["execution_onion"]["state"],
        fixture["oversight_onion"]["state"],
    ]
    cross_states = [edge["state"] for edge in fixture["cross_edges"].values()]

    computed = aggregate(onion_states + cross_states)
    assert computed == fixture["multi_pass_state"] == "MULTI_PASS_HOLD"

    # Three green onions do not wash a red/unknown fourth onion.
    assert onion_states.count("PASS") == 3
    assert "HOLD" in onion_states

    # Four green onions would still fail if any join is HOLD.
    assert aggregate(["PASS", "PASS", "PASS", "PASS", "PASS", "HOLD", "PASS", "PASS"]) == "MULTI_PASS_HOLD"

    # Conflict outranks HOLD; rejection outranks all.
    assert aggregate(["PASS", "HOLD", "CONFLICT"]) == "MULTI_PASS_CONFLICT"
    assert aggregate(["PASS", "CONFLICT", "REJECT"]) == "MULTI_PASS_REJECT"

    print("BoxD four-onion LeeLoo Multi Pass fail-closed regression: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
