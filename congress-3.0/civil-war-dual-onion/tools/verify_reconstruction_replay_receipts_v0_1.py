#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "alabama-live-constitution" / "alison-legislative-teacher-civil-war" / "reconstruction-replay"

REQUIRED = [
    "schema", "receipt_id", "PRIOR_STATE", "ACTOR", "CLAIMED_AUTHORITY",
    "PRIMARY_SOURCE", "DATE", "ACTION", "FEDERAL_STATE_RELATION",
    "SUPERSESSION_EVENT", "NEXT_STATE", "CONTRADICTORY_SOURCE",
    "BOXD_RECEIPT", "boundaries"
]
TERMINALS = {"PASS", "HOLD", "CONFLICT", "REJECT"}


def load(name):
    return json.loads((R / name).read_text())


def verify_receipt(receipt):
    missing = [k for k in REQUIRED if k not in receipt]
    assert not missing, f"missing fields: {missing}"
    assert receipt["schema"] == "reconstruction_replay_receipt.v0_1"
    assert receipt["BOXD_RECEIPT"]["terminal"] in TERMINALS
    b = receipt["boundaries"]
    assert b["source_bound_not_authority_validated"] is True
    assert b["later_supersession_not_retroactive_fact_rewrite"] is True
    assert b["authority_created"] is False
    if receipt["BOXD_RECEIPT"]["authority_validated"]:
        raise AssertionError("authority validation is outside v0.1 receipt scope")


def verify_pass_source_bound(receipt, expected_id):
    assert receipt["receipt_id"] == expected_id
    assert receipt["BOXD_RECEIPT"]["terminal"] == "PASS"
    assert receipt["BOXD_RECEIPT"]["source_bound"] is True
    assert receipt["BOXD_RECEIPT"]["authority_validated"] is False
    assert receipt["BOXD_RECEIPT"]["raw_bytes_frozen"] is False
    assert receipt["BOXD_RECEIPT"]["sha256_computed"] is False


def main():
    template = load("RECONSTRUCTION_REPLAY_RECEIPT_TEMPLATE_V0_1.json")
    r001 = load("RECONSTRUCTION_REPLAY_RECEIPT_001.json")
    r002 = load("RECONSTRUCTION_REPLAY_RECEIPT_002.json")
    rail = load("RECONSTRUCTION_REPLAY_RAIL_V0_1.json")

    verify_receipt(template)
    verify_receipt(r001)
    verify_receipt(r002)

    assert template["BOXD_RECEIPT"]["terminal"] == "HOLD"
    assert template["BOXD_RECEIPT"]["source_bound"] is False

    verify_pass_source_bound(r001, "RECONSTRUCTION_REPLAY_RECEIPT_001")
    verify_pass_source_bound(r002, "RECONSTRUCTION_REPLAY_RECEIPT_002")
    assert "1867 Reconstruction Acts" in r002["SUPERSESSION_EVENT"]
    assert "Receipt 003" in r002["NEXT_STATE"]

    slots = rail["slots"]
    assert len(slots) == 13
    expected = [f"RECONSTRUCTION_REPLAY_RECEIPT_{i:03d}" for i in range(1, 14)]
    assert [s["id"] for s in slots] == expected
    assert slots[0]["state"] == "PASS_SOURCE_BOUND_AUTHORITY_NOT_VALIDATED"
    assert slots[1]["state"] == "PASS_SOURCE_BOUND_AUTHORITY_NOT_VALIDATED"
    assert all(s["state"] == "HOLD_TEMPLATE_ONLY" for s in slots[2:])
    assert rail["authority_created"] is False

    print("RECONSTRUCTION_REPLAY_RECEIPT_TEMPLATE=PASS")
    print("RECONSTRUCTION_REPLAY_RECEIPT_001=PASS_SOURCE_BOUND_AUTHORITY_NOT_VALIDATED")
    print("RECONSTRUCTION_REPLAY_RECEIPT_002=PASS_SOURCE_BOUND_AUTHORITY_NOT_VALIDATED")
    print("RECONSTRUCTION_REPLAY_SLOTS=13")
    print("RECONSTRUCTION_REPLAY_RECEIPTS_003_013=HOLD_TEMPLATE_ONLY")


if __name__ == "__main__":
    main()
