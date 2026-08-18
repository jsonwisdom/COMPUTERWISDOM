#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "CITIZEN_BLOCKCHAIN_REVERSE_REPLAY_LEDGER_V0_1.json"
NEGATIVE = ROOT / "receipts" / "CITIZEN_LEDGER_ITEM_001_NEGATIVE_RPC_REPLAY_2026_08_18.json"

TERMINALS = {"PASS", "HOLD", "CONFLICT", "REJECT"}


def main():
    data = json.loads(LEDGER.read_text())
    negative = json.loads(NEGATIVE.read_text())

    assert data["schema"] == "citizen_blockchain_reverse_replay_ledger.v0_1"
    assert data["ledger_id"] == "CITIZEN_BLOCKCHAIN_REVERSE_REPLAY_LEDGER_V0_1"
    assert data["lane"] == "AMERICAN_CITIZEN_PUBLIC_RECORD"
    assert data["round_06_executive_state"] == "READY_NOT_ROLLED"

    b = data["boundaries"]
    assert b["american_citizen_not_american_family"] is True
    assert b["joy_family_privacy_sealed"] is True
    assert b["citizen_research_public_record_only"] is True
    assert b["tx_hash_not_fact"] is True
    assert b["hash_not_semantic_truth"] is True
    assert b["token_transfer_not_invoice"] is True
    assert b["onchain_event_not_legal_authority"] is True
    assert b["wallet_address_not_natural_person_identity"] is True
    assert b["missing_link_is_hold"] is True
    assert b["dice_select_question"] is True
    assert b["dice_decide_truth"] is False
    assert b["authority_created"] is False

    assert negative["source_origin"] == "USER_SUPPLIED_RPC_OUTPUT"
    assert negative["classification"]["repository_anchor_claim"] == "CONFLICT"
    assert negative["classification"]["transaction_edge"] == "CONFLICT"
    assert negative["classification"]["independent_chain_replay"] == "CONFLICT"
    assert negative["classification"]["reject_threshold_met"] is False
    assert negative["boundaries"]["round_06_executive_advanced"] is False
    assert negative["boundaries"]["authority_created"] is False

    assert len(data["entries"]) >= 1
    seed = data["entries"][0]
    assert seed["entry_id"] == "CITIZEN_LEDGER_ITEM_001"
    assert "base-sepolia" in seed["network"]["value"]
    assert "0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35" in seed["transaction"]["value"]
    assert seed["transaction"]["status"] == "CONFLICT"
    assert seed["receipt_and_event_log"]["status"] == "CONFLICT"
    assert seed["reverse_replay"]["terminal"] in TERMINALS
    assert seed["reverse_replay"]["terminal"] == "CONFLICT"
    assert seed["reverse_replay"]["independent_chain_replay"] == "CONFLICT"
    assert seed["entry_boundaries"]["natural_person_identity_bound"] is False
    assert seed["entry_boundaries"]["invoice_bound"] is False
    assert seed["entry_boundaries"]["legal_authority_bound"] is False
    assert seed["entry_boundaries"]["causation_bound"] is False

    print("CITIZEN_BLOCKCHAIN_LEDGER_SCHEMA=PASS_STRUCTURE")
    print("NEGATIVE_RPC_REPLAY=BOUND_USER_SUPPLIED")
    print("CITIZEN_LEDGER_ITEM_001=CONFLICT")
    print("REJECT_THRESHOLD=NOT_MET_WITHOUT_INDEPENDENT_ASSISTANT_REPLAY")
    print("ROUND_06_EXECUTIVE=READY_NOT_ROLLED")
    print("JOY_FAMILY_PRIVACY=SEALED")
    print("AUTHORITY_CREATED=FALSE")


if __name__ == "__main__":
    main()
