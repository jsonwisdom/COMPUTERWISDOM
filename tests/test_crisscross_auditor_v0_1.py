import importlib.util
import json
from pathlib import Path


def load_module(repo_root: Path):
    tool = repo_root / "executables" / "crisscross_auditor_v0_1.py"
    spec = importlib.util.spec_from_file_location("crisscross_auditor_v0_1", tool)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_identical_evidence_cannot_recover_different_statuses():
    root = Path(__file__).resolve().parents[1]
    module = load_module(root)
    fixture = json.loads(
        (root / "fixtures" / "crisscross_auditor_v0_1" / "http_status_collision.json").read_text(encoding="utf-8")
    )

    result = module.audit(fixture)

    assert result["claim_recoverable"] is False
    assert result["collision_count"] == 1
    assert result["collisions"][0]["distinct_claims"] == [403, 404]
    assert result["label_not_evidence"] is True
    assert result["external_action_performed"] is False
    assert result["authority_created"] is False
