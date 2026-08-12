import importlib.util
import subprocess
import tempfile
from pathlib import Path


def load_module(repo_root: Path):
    path = repo_root / "executables" / "asset_migration_plan_v0_1.py"
    spec = importlib.util.spec_from_file_location("asset_migration_plan_v0_1", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_migration_plan_is_fail_closed():
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)

        (root / "receipts").mkdir()
        (root / "receipts" / "run_live.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "FINAL_PROOF.md").write_text("proof\n", encoding="utf-8")
        (root / "projects").mkdir()
        (root / "projects" / "network_auditor.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)

        inventory = {
            "schema": "computerwisdom.asset_inventory.v0.1",
            "records": [
                {"path": "receipts/run_live.sh", "classification_candidates": ["executables"], "status_by_class": {"executables": "BURIED_CANDIDATE"}},
                {"path": "docs/FINAL_PROOF.md", "classification_candidates": ["proofs"], "status_by_class": {"proofs": "BURIED_CANDIDATE"}},
                {"path": "projects/network_auditor.py", "classification_candidates": ["executables", "instruments"], "status_by_class": {"executables": "BURIED_CANDIDATE", "instruments": "BURIED_CANDIDATE"}},
                {"path": "missing.sh", "classification_candidates": ["executables"], "status_by_class": {"executables": "BURIED_CANDIDATE"}},
            ],
        }

        result = module.build_plan(inventory, root)
        by_path = {item["source_path"]: item for item in result["plan"]}

        assert by_path["receipts/run_live.sh"]["state"] == "REVIEW_REQUIRED"
        assert len(by_path["receipts/run_live.sh"]["source_blob_sha"]) == 40
        assert by_path["receipts/run_live.sh"]["suggested_target_path"] == "executables/run_live.sh"
        assert by_path["docs/FINAL_PROOF.md"]["state"] == "REVIEW_REQUIRED"
        assert by_path["projects/network_auditor.py"]["state"] == "HOLD_MULTI_CLASS"
        assert by_path["missing.sh"]["state"] == "HOLD_SOURCE_BLOB_UNKNOWN"
        assert all(item["move_authorized"] is False for item in result["plan"])
        assert result["moves_performed"] is False
        assert result["authority_created"] is False
