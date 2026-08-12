import importlib.util
import tempfile
from pathlib import Path


def load_module(repo_root: Path):
    tool = repo_root / "tools" / "asset_inventory_v0_1.py"
    spec = importlib.util.spec_from_file_location("asset_inventory_v0_1", tool)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_asset_inventory_classifies_without_moving():
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "receipts" / "coinbase-agent").mkdir(parents=True)
        buried_exec = root / "receipts" / "coinbase-agent" / "run_live.sh"
        buried_exec.write_text("#!/usr/bin/env bash\necho test\n", encoding="utf-8")

        (root / "data").mkdir()
        (root / "data" / "router-fixture.json").write_text("{}\n", encoding="utf-8")

        (root / "docs" / "runbooks").mkdir(parents=True)
        (root / "docs" / "runbooks" / "FINAL_CONNECTOR_PROOF.md").write_text("proof\n", encoding="utf-8")

        (root / "projects" / "alpha").mkdir(parents=True)
        (root / "projects" / "alpha" / "network_auditor.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")

        (root / "whitepapers").mkdir()
        (root / "whitepapers" / "architecture_whitepaper.md").write_text("paper\n", encoding="utf-8")

        report = module.inventory(root)
        by_path = {record["path"]: record for record in report["records"]}

        assert by_path["receipts/coinbase-agent/run_live.sh"]["status_by_class"]["executables"] == "BURIED_CANDIDATE"
        assert by_path["data/router-fixture.json"]["status_by_class"]["fixtures"] == "BURIED_CANDIDATE"
        assert by_path["docs/runbooks/FINAL_CONNECTOR_PROOF.md"]["status_by_class"]["proofs"] == "BURIED_CANDIDATE"
        assert by_path["projects/alpha/network_auditor.py"]["status_by_class"]["instruments"] == "BURIED_CANDIDATE"
        assert by_path["whitepapers/architecture_whitepaper.md"]["status_by_class"]["whitepapers"] == "CANONICAL"
        assert report["moves_performed"] is False
        assert report["authority_created"] is False
