#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DICE = {
    "RECORD_DIE": ["PRIMARY_SOURCE", "CONSTITUTION", "STATUTE", "COURT_OPINION", "ARCHIVE", "FAMILY_STORY"],
    "AUTHORITY_DIE": ["CONGRESS", "PRESIDENT", "STATE", "COURT", "MILITARY", "PRIVATE_ACTOR"],
    "PHASE_DIE": ["SECESSION", "WAR", "EMANCIPATION", "RECONSTRUCTION", "AMENDMENTS", "MEMORY"],
    "PERSPECTIVE_DIE": ["NORTH", "SOUTH", "BORDER", "ENSLAVED_PERSON", "FREEDPERSON", "CIVILIAN"],
    "QUESTION_DIE": ["WHO", "WHAT", "WHEN", "WHERE", "WHY", "HOW"],
    "REPLAY_DIE": ["SOURCE_CHECK", "TIME_CHECK", "AUTHORITY_CHECK", "CONSEQUENCE_CHECK", "CONTRADICTION_CHECK", "CLERK"],
}


def classify(v):
    if v["modern_enemy_label"] or v["claim_contradicted"]:
        return "REJECT"
    if v["valid_records_conflict"]:
        return "CONFLICT"
    if not v["official_authority_bound"]:
        return "HOLD"
    return "PASS"


def deterministic_roll(seed):
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return {
        name: faces[digest[i] % len(faces)]
        for i, (name, faces) in enumerate(DICE.items())
    }


def main():
    kernel = json.loads((ROOT / "kernel/KERNEL_JAY_V0_1.json").read_text())
    receipt = json.loads((ROOT / "receipts/ROUND_0001.json").read_text())
    suite = json.loads((ROOT / "fixtures/TEST_VECTORS_V0_1.json").read_text())
    source_map = json.loads((ROOT / "sources/SOURCE_MAP_V0_1.json").read_text())

    assert kernel["operator_identity"] == "jaywisdom.eth"
    assert kernel["base_identity_anchor"] == "jaywisdom.base.eth"
    assert kernel["authority_created"] is False
    assert kernel["cryptographic_control_verified"] is False
    assert "HISTORY_REPLAY != MODERN_CIVIL_WAR" in kernel["rules"]
    assert "GAME_SCORE != HUMAN_WORTH" in kernel["rules"]

    expected_hash = hashlib.sha256(receipt["seed"].encode("utf-8")).hexdigest()
    assert expected_hash == receipt["seed_sha256"]
    assert deterministic_roll(receipt["seed"]) == receipt["roll"]
    assert receipt["disposition"] == "HOLD"
    assert receipt["boundaries"]["authority_created"] is False
    assert receipt["boundaries"]["family_fact_created"] is False

    assert len(source_map["sources"]) >= 3
    assert source_map["operator_identity"] == "jaywisdom.eth"

    passed = 0
    for vector in suite["vectors"]:
        actual = classify(vector)
        assert actual == vector["expected"], f"{vector['id']}: {actual} != {vector['expected']}"
        passed += 1

    print(json.dumps({
        "result": "PASS",
        "vectors": f"{passed}/{len(suite['vectors'])} PASS",
        "round_0001": receipt["disposition"],
        "seed_sha256": receipt["seed_sha256"],
        "operator_identity": kernel["operator_identity"],
        "authority_created": False,
        "modern_enemy_list_created": False,
        "family_fact_created": False
    }, indent=2))


if __name__ == "__main__":
    main()
