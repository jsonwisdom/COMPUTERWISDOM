import importlib.util
import tempfile
from pathlib import Path

def load_module(repo_root: Path):
    p=repo_root/"executables"/"asset_inventory_v0_3.py"
    spec=importlib.util.spec_from_file_location("asset_inventory_v0_3",p); m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m

def test_orthogonal_artifact_class_and_role():
    repo=Path(__file__).resolve().parents[1]; m=load_module(repo)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        samples={
            "scripts/validate_scorecard.py":"#!/usr/bin/env python3\n",
            "tests/fixtures/invalid_missing_audit.json":"{}\n",
            "receipts/portal_public_proof_audit.json":"{}\n",
            "docs/research_note.md":"# Paper\nAbstract\nMethodology\nResearch\nArchitecture\nConclusion\n",
        }
        for rel,text in samples.items():
            p=root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding="utf-8")
        report=m.inventory(root); by={r["path"]:r for r in report["records"]}
        assert by["scripts/validate_scorecard.py"]["artifact_classes"]==["executables"]
        assert by["scripts/validate_scorecard.py"]["capability_roles"]==["instrument"]
        assert by["tests/fixtures/invalid_missing_audit.json"]["artifact_classes"]==["fixtures"]
        assert by["tests/fixtures/invalid_missing_audit.json"]["capability_roles"]==[]
        assert by["receipts/portal_public_proof_audit.json"]["artifact_classes"]==["proofs"]
        assert by["receipts/portal_public_proof_audit.json"]["capability_roles"]==[]
        assert by["docs/research_note.md"]["artifact_classes"]==["whitepapers"]
        assert report["summary"]["multi_artifact_class_candidates"]==0
        assert report["classification_requires_review"] is True
        assert report["moves_performed"] is False
        assert report["authority_created"] is False
