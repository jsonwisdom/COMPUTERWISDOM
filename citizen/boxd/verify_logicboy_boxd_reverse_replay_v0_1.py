#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
KERNEL = HERE / "LOGICBOY_BOXD_REVERSE_REPLAY_KERNEL_V0_1.json"


def main():
    d = json.loads(KERNEL.read_text())

    assert d["schema"] == "logicboy_boxd_reverse_replay_kernel.v0_1"
    assert d["kernel_id"] == "LOGICBOY_BOXD_REVERSE_REPLAY_V0_1"
    assert d["container"] == "BOXD"
    assert d["operator"] == "ReverseReplay"
    assert d["executor"] == "logicBoy"
    assert d["semantic_type"] == "DETERMINISTIC_INTERNAL_BOXD_OPERATOR"

    p = d["placement"]
    assert p["boxd_is_container"] is True
    assert p["reverse_replay_is_internal_operator"] is True
    assert p["reverse_replay_is_sibling_system"] is False
    assert p["logicboy_is_truth_source"] is False
    assert p["logicboy_is_authority"] is False
    assert p["model_required"] is False

    assert d["boxd_cycle"] == [
        "BIND_ORIGINAL",
        "OBSERVE_CURRENT_STATE",
        "FREEZE_EVIDENCE_GRAPH",
        "REVERSE_REPLAY",
        "CLASSIFY_EACH_EDGE",
        "FORWARD_REPLAY",
        "EMIT_SCOPED_DISPOSITION",
        "APPEND_RECEIPT",
        "LOCK_HISTORY",
    ]

    rr = d["reverse_replay"]
    assert rr["start"] == "CURRENT_CLAIM"
    assert rr["direction"] == "BACKWARD_THROUGH_BOUND_EDGES"
    assert rr["preserve_encountered_states"] is True
    assert rr["stop_on_first_problem"] is False
    assert rr["rules"]["missing_required_edge"] == "HOLD"
    assert rr["rules"]["valid_records_disagree"] == "CONFLICT"
    assert rr["rules"]["bound_record_contradicts_scoped_claim"] == "REJECT"
    assert rr["rules"]["all_required_edges_reconcile"] == "PASS"

    fr = d["forward_replay"]
    assert fr["required_after_reverse_replay"] is True

    r = d["receipt_semantics"]
    assert r["parent_history_append_only"] is True
    assert r["child_recovery_may_reach_new_terminal"] is True
    assert r["child_terminal_does_not_rewrite_parent"] is True
    assert r["scope_must_be_explicit"] is True

    fixture = d["teaching_fixture"]
    assert fixture["fixture_id"] == "CITIZEN_LEDGER_ITEM_001"
    assert fixture["parent_state"] == "CONFLICT_PRESERVED"
    assert fixture["child_state"] == "REJECT_DECLARED_BASE_SEPOLIA_ANCHOR_OBJECTS"

    assert d["round_06_executive"] == "READY_NOT_ROLLED"
    assert d["family_lane_imported"] is False
    assert d["authority_created"] is False

    print("BOXD=PASS_CONTAINER")
    print("REVERSE_REPLAY=PASS_INTERNAL_OPERATOR")
    print("LOGICBOY=PASS_DETERMINISTIC_EXECUTOR")
    print("FORWARD_REPLAY=REQUIRED")
    print("PARENT_HISTORY=APPEND_ONLY")
    print("ROUND_06_EXECUTIVE=READY_NOT_ROLLED")
    print("MODEL_REQUIRED=FALSE")
    print("AUTHORITY_CREATED=FALSE")


if __name__ == "__main__":
    main()
