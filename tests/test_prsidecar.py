import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prsidecar.render import canonical, receipt, render, sha256

ROOT = Path(__file__).resolve().parents[1]
SRC = json.loads((ROOT / "prsidecar/fixtures/pr_576.source.json").read_text())

def test_stable_serialization():
    a = canonical(render(SRC))
    b = canonical(render(SRC))
    assert a == b
    assert a.endswith("\n")

def test_replay_matches_fixture():
    sidecar = render(SRC)
    stored = json.loads((ROOT / "prsidecar/fixtures/pr_576.sidecar.json").read_text())
    assert sidecar["renderer"]["sidecar_sha256"] == stored["renderer"]["sidecar_sha256"]
    assert canonical(sidecar) == canonical(stored)

def test_receipt_binds_source_not_renderer_claim():
    sidecar = render(SRC)
    rec = receipt(SRC, sidecar)
    stored = json.loads((ROOT / "prsidecar/fixtures/pr_576.receipt.json").read_text())
    assert rec["head_sha"] == "ca87a7e9aec5d67c8694585d221df9a2a59a5296"
    assert rec["base_sha"] == "33ca735424f3092c6c4c1b240a3ba5ebf8be61b7"
    assert rec["sidecar_sha256"] == sidecar["renderer"]["sidecar_sha256"]
    assert rec["renderer_is_not_source"] is True
    assert rec["authority_created"] is False
    assert rec["identity_binding"] == "HOLD"
    assert rec["eth_limo_readback"] == "NOT_CHECKED"
    assert canonical(rec) == canonical(stored)

def test_conflict_and_hold_preserved():
    sidecar = render(SRC)
    assert "LIST_MERGED_FALSE vs GET_MERGED_TRUE on PR 576" in sidecar["unresolved_conflicts"]
    assert sidecar["identity_binding"] == "HOLD"
    assert sidecar["authority_created"] is False
    assert sidecar["changed_paths"] == [
        "jaywisdom/projects/gray-baby.html",
        "jaywisdom/projects/index.html",
    ]

def test_hash_is_of_canonical_bytes():
    sidecar = render(SRC)
    frozen = json.loads(canonical(sidecar))
    frozen["renderer"].pop("sidecar_sha256")
    assert sha256(canonical(frozen)) == sidecar["renderer"]["sidecar_sha256"]

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in tests:
        try:
            fn()
            print("PASS", fn.__name__)
        except Exception as exc:
            failed += 1
            print("FAIL", fn.__name__, exc)
    print("failed", failed)
    raise SystemExit(failed)
