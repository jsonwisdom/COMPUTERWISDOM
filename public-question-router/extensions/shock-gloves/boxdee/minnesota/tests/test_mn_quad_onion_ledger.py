#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "mn_quad_onion_ledger.v0_1.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "MN_QUAD_ONION_LEDGER_HOLD_0001.json"

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
ledger = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

assert schema["properties"]["schema"]["const"] == "boxd.mn_quad_onion_ledger.v0_1"
assert ledger["schema"] == "boxd.mn_quad_onion_ledger.v0_1"
assert ledger["jurisdiction"] == "MN"
assert ledger.get("authority_created") is False
assert ledger.get("legal_finding_created") is False

required_top = set(schema["required"])
assert required_top.issubset(ledger), required_top - set(ledger)

source_ids = {r["source_id"] for r in ledger["source_receipts"]}
assert len(source_ids) == len(ledger["source_receipts"]), "duplicate source_id"

for bucket in (
    "onion_1_criminal_receipts",
    "onion_2_payment_control_edges",
    "onion_3_financial_rail_edges",
    "onion_4_oversight_recovery_edges",
):
    for obj in ledger[bucket]:
        refs = set(obj.get("source_receipt_ids", []))
        assert refs, f"{bucket} object missing source receipts: {obj}"
        assert refs <= source_ids, f"unbound source receipt(s): {refs - source_ids}"

# Allegation cannot be promoted to a plea/conviction-bound state.
for receipt in ledger["onion_1_criminal_receipts"]:
    if receipt["adjudication_status"] == "CHARGED":
        assert receipt["state"] not in {"PASS_CASE_BOUND"}, receipt

# Naming a financial rail does not create institutional wrongdoing.
finding_ids = {f["finding_id"] for f in ledger["institution_findings"]}
for edge in ledger["onion_3_financial_rail_edges"]:
    if edge.get("institution_wrongdoing_claimed"):
        fid = edge.get("institution_finding_id")
        assert fid, f"wrongdoing claim lacks finding id: {edge['edge_id']}"
        assert fid in finding_ids, f"finding not present: {fid}"
    else:
        assert edge.get("institution_finding_id") is None, edge["edge_id"]

# Cross-onion references must resolve to known ledger object IDs.
known_ids = set()
for receipt in ledger["onion_1_criminal_receipts"]:
    known_ids.add(receipt["case_id"])
for bucket in (
    "onion_2_payment_control_edges",
    "onion_3_financial_rail_edges",
    "onion_4_oversight_recovery_edges",
):
    known_ids.update(obj["edge_id"] for obj in ledger[bucket])

for edge in ledger["cross_onion_edges"]:
    assert set(edge["from_ids"]) <= known_ids, edge
    assert set(edge["to_ids"]) <= known_ids, edge

# LeeLoo is fail-closed: any HOLD/partial onion or cross-edge prevents PASS.
disposition = ledger["boxd_disposition"]
partial_or_hold = any(disposition[key] != "PASS" for key in ("o1", "o2", "o3", "o4"))
blocked_cross_edge = any(edge["state"] != "PASS" for edge in ledger["cross_onion_edges"])
if partial_or_hold or blocked_cross_edge:
    assert disposition["leeloo_multi_pass"] != "MULTI_PASS_PASS"

assert disposition["leeloo_multi_pass"] == "MULTI_PASS_HOLD"
assert ledger["institution_findings"] == []
assert "FOLLOW_THE_MONEY_WITHOUT_PROMOTING_THE_RAIL_INTO_THE_CRIME" in ledger["membranes"]

print("Minnesota Quad Onion ledger fixture: PASS (fail-closed HOLD preserved)")
