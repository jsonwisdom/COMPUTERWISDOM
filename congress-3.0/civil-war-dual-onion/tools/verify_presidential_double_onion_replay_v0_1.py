#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "alabama-live-constitution" / "alison-legislative-teacher-civil-war" / "presidential-replay"

TERMINALS = {"PASS", "HOLD", "CONFLICT", "REJECT"}


def load(name):
    return json.loads((P / name).read_text())


def main():
    schema = load("PRESIDENTIAL_DOUBLE_ONION_REPLAY_SCHEMA_V0_1.json")
    template = load("PRESIDENTIAL_DOUBLE_ONION_REPLAY_TEMPLATE_V0_1.json")

    assert schema["$id"] == "alison_presidential_double_onion_replay.v0_1"
    assert template["schema"] == "alison_presidential_double_onion_replay.v0_1"
    assert template["replay_id"] == "PRESIDENTIAL_REPLAY_TEMPLATE"

    b = template["boundaries"]
    for key in [
        "president_identity_not_authority",
        "election_win_not_blank_check",
        "presidential_statement_not_law",
        "court_nonreview_not_validation",
        "historical_reputation_not_authority",
        "formal_right_not_practical_access",
        "source_bound_not_authority_validated",
    ]:
        assert b[key] is True, key
    assert b["model_required"] is False
    assert b["authority_created"] is False

    cross = template["cross_onion_receipt"]
    assert cross["power_status"] in TERMINALS
    assert cross["challenge_capacity_status"] in TERMINALS
    assert cross["terminal"] in TERMINALS
    assert cross["terminal"] == "HOLD"
    assert cross["power_status"] == "HOLD"
    assert cross["challenge_capacity_status"] == "HOLD"

    power = template["power_onion"]
    people = template["people_onion"]
    assert power["boxd"]["source_bound"] is False
    assert people["boxd"]["source_bound"] is False
    assert power["boxd"]["raw_bytes_frozen"] is False
    assert people["boxd"]["raw_bytes_frozen"] is False
    assert power["boxd"]["sha256_computed"] is False
    assert people["boxd"]["sha256_computed"] is False

    assert set(power["legal_authority_jaw"]) == {
        "action", "basis", "agency_or_executor", "deadline_or_duration", "funding", "limits"
    }
    assert set(power["execution_evidence_jaw"]) == {
        "guidance", "contracts_or_orders", "deployment", "testing_or_review", "results", "missing_or_conflicting_records"
    }

    required_people = {
        "right_to_object",
        "right_to_vote",
        "right_to_petition",
        "access_to_court",
        "access_to_counsel_or_profession",
        "institutional_barriers",
        "retaliation_or_burden",
        "actual_remedy",
        "challenge_evidence",
        "boxd",
    }
    assert set(people) == required_people

    print("PRESIDENTIAL_DOUBLE_ONION_SCHEMA=PASS")
    print("PRESIDENTIAL_DOUBLE_ONION_TEMPLATE=HOLD_TEMPLATE_ONLY")
    print("POWER_ONION=PASS_STRUCTURE")
    print("PEOPLE_ONION=PASS_STRUCTURE")
    print("CROSS_ONION=HOLD_NO_EVENT_BOUND")
    print("MODEL_REQUIRED=FALSE")
    print("AUTHORITY_CREATED=FALSE")


if __name__ == "__main__":
    main()
