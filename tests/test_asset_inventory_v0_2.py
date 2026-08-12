import importlib.util
import tempfile
from pathlib import Path


def load_module(repo_root: Path):
    path = repo_root / "executables" / "asset_inventory_v0_2.py"
    spec = importlib.util.spec_from_file_location("asset_inventory_v0_2", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_v0_2_native_home_and_whitepaper_detection():
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / ".github" / "workflows" / "repo-audit.yml").write_text("name: audit\n", encoding="utf-8")

        (root / "docs").mkdir()
        (root / "docs" / "research_architecture.md").write_text(
            "# Model\n## Abstract\nResearch architecture.\n## Methodology\nX\n## Conclusion\nY\n",
            encoding="utf-8",
        )

        (root / "receipts").mkdir()
        (root / "receipts" / "run_live.sh").write_text("#!/bin/sh\n", encoding="utf-8")

        report = module.inventory(root)
        by_path = {record["path"]: record for record in report["records"]}

        assert by_path[".github/workflows/repo-audit.yml"]["status_by_class"]["instruments"] == "NATIVE_HOME"
        assert by_path["docs/research_architecture.md"]["status_by_class"]["whitepapers"] == "BURIED_CANDIDATE"
        assert by_path["receipts/run_live.sh"]["status_by_class"]["executables"] == "BURIED_CANDIDATE"
        assert report["schema"] == "computerwisdom.asset_inventory.v0.2"
        assert report["classification_requires_review"] is True
        assert report["moves_performed"] is False
        assert report["authority_created"] is False
