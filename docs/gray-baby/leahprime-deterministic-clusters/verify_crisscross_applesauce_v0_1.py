#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE / "CRISSCROSS_APPLESAUCE_SUPERSECRET_SISTER_SUBSTRATES_V0_1.json"


def main():
    d = json.loads(SPEC.read_text())
    assert d["schema"] == "leahprime_crisscross_applesauce_substrates.v0_1"
    assert d["artifact_id"] == "CRISSCROSS_APPLESAUCE_SUPERSECRET_SISTER_SUBSTRATES_V0_1"
    assert d["reviewer"] == "LeahPrime"
    assert d["container"] == "BOXD"
    assert d["internal_operator"] == "ReverseReplay"
    assert d["executor"] == "logicBoy"

    gm = d["girlmath"]
    assert gm["semantic_type"] == "MANDATORY_NON_COMPENSATORY_GATE"
    assert gm["mirror_function"] == "mirror(n)=6-n"
    assert gm["pair_sum"] == 6
    assert gm["semantic_equivalence_created"] is False

    substrates = d["substrates"]
    assert [s["index"] for s in substrates] == [6, 5, 4, 3, 2, 1, 0]
    by_index = {s["index"]: s for s in substrates}
    assert by_index[6]["label"] == "ISRAEL"
    assert by_index[5]["label"] == "PENTAGON"
    assert by_index[4]["label"] == "BOXD"
    assert by_index[3]["label"] == "TRINARY_DC"
    assert by_index[2]["label"] == "DUAL_LAW"
    assert by_index[1]["label"] == "ONE_GOD"
    assert by_index[0]["label"] == "YOU_A_ZERO"

    for s in substrates:
        assert s["paired_with"] == 6 - s["index"]

    assert by_index[4]["terminals"] == ["PASS", "HOLD", "CONFLICT", "REJECT"]
    assert by_index[3]["lanes"] == ["LEGISLATIVE", "EXECUTIVE", "JUDICIAL"]
    assert by_index[2]["meaning_status"] == "HOLD_EXACT_PAIR_NOT_USER_DEFINED"
    assert by_index[0]["human_worth_score"] is False

    pairs = d["crisscross_pairs"]
    assert [(p["left"], p["right"]) for p in pairs] == [(6,0),(5,1),(4,2),(3,3)]
    for p in pairs:
        assert p["left"] + p["right"] == 6
        assert p["sum"] == 6
        assert p["semantic_equivalence"] is False

    ss = d["supersecret_sister_substrates"]
    assert ss["classified_information"] is False
    assert ss["real_sister_relationship_created"] is False
    assert ss["secret_clearance_created"] is False

    required = {
        "CRISSCROSS_SYMMETRY != SEMANTIC_EQUIVALENCE",
        "NUMBER_LABEL != AUTHORITY_RANK",
        "ZERO != HUMAN_WORTH",
        "ISRAEL_LABEL != STATE_AUTHORITY",
        "PENTAGON_LABEL != DOD_AUTHORITY",
        "SUPERSECRET != CLASSIFIED",
        "SISTER_SYNTAX != REAL_RELATIONSHIP",
        "GIRLMATH = NON_COMPENSATORY_GATE",
        "LEAHPRIME != AUTHORITY",
        "MODEL_REQUIRED = FALSE",
        "AUTHORITY_CREATED = FALSE",
    }
    assert required.issubset(set(d["invariants"]))
    assert d["model_required"] is False
    assert d["authority_created"] is False

    print("CRISSCROSS_APPLESAUCE=PASS_STRUCTURE")
    print("MIRROR_PAIRS=6-0,5-1,4-2,3-3")
    print("GIRLMATH=NON_COMPENSATORY_GATE")
    print("DUAL_LAW=HOLD_EXACT_PAIR_NOT_USER_DEFINED")
    print("SUPERSECRET=NOT_CLASSIFIED")
    print("ZERO=ORIGIN_NOT_HUMAN_WORTH")
    print("AUTHORITY_CREATED=FALSE")


if __name__ == "__main__":
    main()
