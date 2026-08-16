import hashlib
import json
from pathlib import Path


FIXTURE = (
    Path(__file__).parent
    / "receiptos_history_vectors_v0_1"
    / "AUNT_RANN_SAME_ENDPOINT_DIFFERENT_HISTORY_V0_1.json"
)


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_commitment(value):
    payload = canonical_json(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_fixture_hashes_recompute_exactly():
    fixture = load_fixture()
    assert fixture["initial_state_hash"] == sha256_commitment(fixture["initial_state"])

    for path in fixture["paths"].values():
        assert path["event_count"] == len(path["event_history"])
        assert path["state_hash"] == sha256_commitment(path["final_state"])
        expected_history_hash = sha256_commitment(path["event_history"])
        assert path["path_hash"] == expected_history_hash
        assert path["event_history_hash"] == expected_history_hash


def test_same_endpoint_does_not_collapse_history():
    fixture = load_fixture()
    path_a = fixture["paths"]["PATH_A"]
    path_b = fixture["paths"]["PATH_B"]

    assert path_a["final_state"] == path_b["final_state"]
    assert path_a["state_hash"] == path_b["state_hash"]
    assert path_a["path_hash"] != path_b["path_hash"]
    assert fixture["comparison"]["state_hash_equal"] is True
    assert fixture["comparison"]["path_hash_equal"] is False
    assert fixture["comparison"]["event_history_hash_equal"] is False
    assert fixture["comparison"]["replay_result"] == "MULTIPLE_PATHS_DISTINGUISHED"


def test_path_a_is_canonical_empty_history():
    fixture = load_fixture()
    path_a = fixture["paths"]["PATH_A"]

    assert path_a["event_count"] == 0
    assert path_a["event_history"] == []
    assert path_a["path_hash"] == (
        "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
    )


def test_path_b_preserves_three_distinct_events():
    fixture = load_fixture()
    path_b = fixture["paths"]["PATH_B"]

    assert path_b["event_count"] == 3
    assert path_b["event_history"] == [
        "ROUTE_REQUESTED",
        "CONSENT_CHECKED",
        "ROUTE_BLOCKED",
    ]


def test_gatekeeper_blocks_unsupported_causal_promotion():
    fixture = load_fixture()
    gatekeeper = fixture["three_wisdom_girls"]["GATEKEEPER"]

    assert gatekeeper["blocked_promotion"] == "DELIVERED_FALSE -> NOBODY_TRIED"
    assert "OBSERVED_RESULT != PROVEN_CAUSE" in fixture["laws"]


def test_authority_remains_false():
    fixture = load_fixture()

    assert fixture["authority_created"] is False
    assert fixture["replay_objects"]["PATH_A"]["authority_created"] is False
    assert fixture["replay_objects"]["PATH_B"]["authority_created"] is False
