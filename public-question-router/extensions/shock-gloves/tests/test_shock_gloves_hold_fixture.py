#!/usr/bin/env python3
"""Fail-closed regression checks for the Shock Gloves supply-chain fixture."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "Q-20260818-001.shock-gloves.json"
SCHEMA = ROOT / "schemas" / "shock_gloves_supply_chain_receipt.v0_1.schema.json"


def main() -> int:
    receipt = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert schema["title"] == "Shock Gloves Supply-Chain Receipt v0.1"
    assert receipt["authority_created"] is False
    assert receipt["replay_state"] == "HOLD"
    assert receipt["record_onion_state"] == "HOLD"
    assert receipt["power_onion_state"] == "HOLD"

    device = receipt["device_identity"]
    assert device["status"] == "HOLD"
    assert device["manufacturer"] is None
    assert device["model"] is None
    assert device["sku"] is None

    # General technology-class and appropriation receipts must not promote a
    # product-specific acquisition/deployment/use claim.
    assert receipt["appropriation_edge"]["status"] == "SOURCE_BOUND"
    assert receipt["procurement_edge"]["status"] == "HOLD"
    assert receipt["acquisition_edge"]["status"] == "HOLD"
    assert receipt["deployment_edge"]["status"] == "HOLD"
    assert receipt["use_edge"]["status"] == "HOLD"
    assert receipt["oversight_edge"]["status"] == "HOLD"

    presidential = receipt["presidential_nexus"]
    assert presidential["office_holder"] == "Donald J. Trump"
    assert presidential["specific_action"] is None
    assert presidential["claimed_authority"] is None
    assert presidential["status"] == "HOLD"

    missing = set(receipt["missing_edges"])
    required_missing = {
        "DEVICE_MANUFACTURER",
        "DEVICE_MODEL",
        "DEVICE_SKU",
        "CONTRACT_OR_AWARD",
        "PURCHASE_ORDER_OR_INVOICE",
        "DEPLOYMENT_POLICY",
        "USE_EVENT",
        "SPECIFIC_PRESIDENTIAL_ACTION_IF_ANY",
    }
    assert required_missing <= missing

    print("shock-gloves fail-closed fixture: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
