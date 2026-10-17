import copy
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wikiatom_bomb_v1 import BRANCHES, canonical_json, run_wikiatom_bomb_v1

BASE = {
    "atom_id": "ATOM-001",
    "claim_or_object": "example",
    "source_pointer": "fixture://atom-001",
    "observed_clock": "2026-10-04T21:30:00Z",
    "version": "1",
    "state": "OBSERVED",
}


def test_01_simple_fanout():
    out = run_wikiatom_bomb_v1(BASE, max_depth=1)
    assert len(out["children"]) == len(BRANCHES)
    assert [c["branch"] for c in out["children"]] == list(BRANCHES)


def test_02_cycle():
    root = {**BASE, "related_atom_ids": ["ATOM-001"]}
    out = run_wikiatom_bomb_v1(root, related_atoms={"ATOM-001": root}, max_depth=3)
    assert any(e["type"] == "CYCLE" for e in out["events"])


def test_03_missing_edge():
    bad = copy.deepcopy(BASE)
    del bad["source_pointer"]
    out = run_wikiatom_bomb_v1(bad)
    assert out["disposition"] == "HOLD"
    assert out["reason"] == "MISSING_EDGE"


def test_04_conflict_preserved():
    out = run_wikiatom_bomb_v1(
        BASE,
        branch_payloads={"CONTRADICTION": {"conflict": True, "values": ["A", "B"]}},
    )
    vals = [c["claim_or_object"] for c in out["children"] if c["branch"] == "CONTRADICTION"]
    assert vals == ["A", "B"]
    assert any(e["type"] == "CONFLICT" for e in out["events"])


def test_05_promotion_without_receipt():
    out = run_wikiatom_bomb_v1(BASE, promotion_requested=True)
    assert out["promotion"] == "BLOCKED"
    assert out["disposition"] == "HOLD"


def test_06_depth_limit():
    child = {**BASE, "atom_id": "ATOM-002"}
    root = {**BASE, "related_atom_ids": ["ATOM-002"]}
    out = run_wikiatom_bomb_v1(root, related_atoms={"ATOM-002": child}, max_depth=1)
    assert any(e["type"] == "MAX_DEPTH" and e["atom_id"] == "ATOM-002" for e in out["events"])


def test_07_determinism():
    a = run_wikiatom_bomb_v1(BASE, branch_payloads={"RECORD": {"b": 2, "a": 1}})
    b = run_wikiatom_bomb_v1(BASE, branch_payloads={"RECORD": {"a": 1, "b": 2}})
    assert canonical_json(a) == canonical_json(b)


def test_08_side_effects_false():
    out = run_wikiatom_bomb_v1(BASE)
    assert out["side_effects"] is False
