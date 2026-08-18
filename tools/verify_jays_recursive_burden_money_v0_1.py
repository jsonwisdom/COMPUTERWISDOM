#!/usr/bin/env python3
"""Deterministic fail-closed verifier for Jay's Recursive Burden / Dirty Math kernel v0.1."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "fixtures/jaywisdom/fraud_ledger/JAYS_RECURSIVE_BURDEN_MONEY_TEST_VECTORS_V0_1.json"

MONEY_STATES = (
    "REQUEST", "AUTHORIZATION", "APPROPRIATION", "APPORTIONMENT", "ALLOTMENT",
    "OBLIGATION", "OUTLAY", "EXPENDITURE_RESULT", "AUDITED_RESULT",
)
GATES = ("source", "authority", "action", "receipt", "replay")
VALID_GATE_STATES = {"VERIFIED", "MISSING", "DISAGREES", "CONTRADICTED", "NOT_APPLICABLE"}


def evaluate(record: dict) -> dict:
    holds, conflicts, rejects, signals = [], [], [], []
    if record.get("authority_created") is not False:
        rejects.append("AUTHORITY_CREATION_BLOCKED")

    money = record.get("money_object") or {}
    value = money.get("value")
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        rejects.append("MONEY_VALUE_INVALID")
    if money.get("currency") != "USD":
        rejects.append("CURRENCY_NOT_USD")
    if money.get("state") not in MONEY_STATES:
        holds.append("MONEY_STATE_REQUIRED")
    for field in ("account", "program", "fiscal_year", "authority_ref", "source_ref", "receipt_ref"):
        if not money.get(field):
            holds.append(f"MONEY_{field.upper()}_MISSING")

    recursion = record.get("recursion")
    if not isinstance(recursion, list) or not recursion:
        holds.append("RECURSION_CHAIN_MISSING")
        recursion = []
    for i, node in enumerate(recursion):
        if node.get("depth") != i:
            rejects.append(f"RECURSION_DEPTH_INVALID:{i}")
        if not node.get("claim_ref"):
            holds.append(f"CLAIM_REF_MISSING:{i}")
        for gate in GATES:
            gate_obj = node.get(gate) or {}
            gate_state = gate_obj.get("status")
            if gate_state not in VALID_GATE_STATES:
                rejects.append(f"GATE_STATE_INVALID:{i}:{gate}")
            elif gate_state == "MISSING":
                holds.append(f"GATE_MISSING:{i}:{gate}")
            elif gate_state == "DISAGREES":
                conflicts.append(f"GATE_DISAGREES:{i}:{gate}")
            elif gate_state == "CONTRADICTED":
                rejects.append(f"GATE_CONTRADICTED:{i}:{gate}")
            elif gate_state == "VERIFIED" and not gate_obj.get("ref"):
                holds.append(f"GATE_REF_MISSING:{i}:{gate}")
        if i < len(recursion) - 1:
            expected = recursion[i + 1].get("claim_ref")
            if node.get("terminal") is True:
                rejects.append(f"EARLY_TERMINAL:{i}")
            if node.get("receipt_claim_ref") != expected:
                rejects.append(f"RECURSIVE_RECEIPT_BINDING_INVALID:{i}")
        elif node.get("terminal") is not True:
            holds.append("FINAL_TERMINAL_MARKER_MISSING")

    observations = record.get("state_observations") or []
    by_state, value_to_states = {}, {}
    for obs in observations:
        state, value = obs.get("state"), obs.get("value")
        if state not in MONEY_STATES:
            rejects.append("OBSERVATION_STATE_INVALID")
            continue
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            rejects.append("OBSERVATION_VALUE_INVALID")
            continue
        by_state.setdefault(state, set()).add(value)
        value_to_states.setdefault(value, set()).add(state)
    for state, values in by_state.items():
        if len(values) > 1:
            conflicts.append(f"SAME_STATE_VALUE_CONFLICT:{state}")
    for value, states in value_to_states.items():
        if len(states) > 1:
            signals.append(f"SAME_NUMBER_DIFFERENT_STATE:{value}")
            rows = [o for o in observations if o.get("value") == value and o.get("state") in states]
            if any(o.get("reconciled") is not True for o in rows):
                holds.append("STATE_COLLAPSE_TRACE_REQUIRED")

    top_down, bottom_up = record.get("top_down"), record.get("bottom_up")
    if not isinstance(top_down, list) or not top_down:
        holds.append("TOP_DOWN_REPLAY_MISSING")
    if not isinstance(bottom_up, list) or not bottom_up:
        holds.append("BOTTOM_UP_REPLAY_MISSING")
    if isinstance(top_down, list) and top_down and isinstance(bottom_up, list) and bottom_up:
        if list(reversed(top_down)) != bottom_up:
            conflicts.append("TOP_DOWN_BOTTOM_UP_MISMATCH")

    if record.get("attempt_state_promotion") is True:
        rejects.append("MONEY_STATE_PROMOTION_BLOCKED")

    status = "REJECT" if rejects else "CONFLICT" if conflicts else "HOLD" if holds else "PASS"
    return {
        "status": status,
        "semantic_type": "BOUNDED_RECURSIVE_MONEY_EVIDENCE_DISPOSITION",
        "dirty_math_signal": bool(signals),
        "signals": sorted(set(signals)),
        "hold_reasons": sorted(set(holds)),
        "conflict_reasons": sorted(set(conflicts)),
        "reject_reasons": sorted(set(rejects)),
        "fraud_proven": False,
        "intent_proven": False,
        "misconduct_proven": False,
        "authority_created": False,
    }


def gate(status="VERIFIED", ref="BOUND"):
    return {"status": status, **({"ref": ref} if ref is not None else {})}


def base_record() -> dict:
    return {
        "format": "JAYS_RECURSIVE_BURDEN_MONEY_CLAIM_V0.1",
        "claim_id": "C0",
        "claim_text": "$10B obligated",
        "money_object": {
            "value": 10_000_000_000, "currency": "USD", "state": "OBLIGATION",
            "account": "A1", "program": "P1", "fiscal_year": "FY2026",
            "authority_ref": "LAW1", "source_ref": "S1", "receipt_ref": "R1",
        },
        "recursion": [{
            "depth": 0, "claim_ref": "C0", "source": gate(ref="S0"),
            "authority": gate(ref="A0"), "action": gate(ref="X0"),
            "receipt": gate(ref="R0"), "replay": gate(ref="RP0"), "terminal": True,
        }],
        "state_observations": [{
            "value": 10_000_000_000, "state": "OBLIGATION",
            "source_ref": "S1", "reconciled": True,
        }],
        "top_down": ["LAW1", "MONEY1", "PROGRAM1", "TX1", "R1"],
        "bottom_up": ["R1", "TX1", "PROGRAM1", "MONEY1", "LAW1"],
        "authority_created": False,
    }


def build(vector: dict) -> dict:
    record = base_record()
    if vector.get("drop_money_field"):
        record["money_object"].pop(vector["drop_money_field"], None)
    if "money_value" in vector:
        record["money_object"]["value"] = vector["money_value"]
        record["state_observations"][0]["value"] = vector["money_value"]
    for gate_name, gate_state in (vector.get("gate_overrides") or {}).items():
        record["recursion"][0][gate_name] = gate(gate_state, ref=f"{gate_name.upper()}_REF")
    if "state_observations" in vector:
        record["state_observations"] = copy.deepcopy(vector["state_observations"])
    if "bottom_up" in vector:
        record["bottom_up"] = list(vector["bottom_up"])
    if vector.get("attempt_state_promotion"):
        record["attempt_state_promotion"] = True
    if vector.get("recursive_binding_invalid"):
        first = copy.deepcopy(record["recursion"][0])
        first["terminal"] = False
        first["receipt_claim_ref"] = "WRONG"
        second = copy.deepcopy(record["recursion"][0])
        second["depth"] = 1
        second["claim_ref"] = "C1"
        record["recursion"] = [first, second]
    return record


def self_test() -> int:
    vectors = json.loads(VECTORS.read_text(encoding="utf-8"))["vectors"]
    rows, failed = [], []
    for vector in vectors:
        receipt = evaluate(build(vector))
        ok = (
            receipt["status"] == vector["expected_status"]
            and receipt["dirty_math_signal"] == vector.get("expected_dirty_math_signal", False)
        )
        row = {"id": vector["id"], "expected": vector["expected_status"], "observed": receipt["status"], "pass": ok}
        rows.append(row)
        if not ok:
            failed.append(row)
    print(json.dumps({
        "verifier": "JAYS_RECURSIVE_BURDEN_MONEY_V0.1",
        "passed": len(rows) - len(failed),
        "failed": len(failed),
        "dirty_math_means_corruption": False,
        "same_number_different_state_means_same_fact": False,
        "authority_created": False,
        "results": rows,
    }, indent=2, sort_keys=True))
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.record:
        parser.error("--record is required unless --self-test is used")
    print(json.dumps(evaluate(json.loads(args.record.read_text(encoding="utf-8"))), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
