import importlib.util
import subprocess
import tempfile
from pathlib import Path

def load(repo: Path):
    p=repo/"executables"/"asset_migration_plan_v0_2.py"; s=importlib.util.spec_from_file_location("planner",p); m=importlib.util.module_from_spec(s); assert s.loader; s.loader.exec_module(m); return m

def test_instrument_role_does_not_create_multi_home_hold():
    repo=Path(__file__).resolve().parents[1]; m=load(repo)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); subprocess.run(["git","init","-q",str(root)],check=True)
        p=root/"angie-act"/"scripts"/"validate_scorecard.py"; p.parent.mkdir(parents=True); p.write_text("#!/usr/bin/env python3\n"); subprocess.run(["git","-C",str(root),"add","."],check=True)
        inv={"schema":"computerwisdom.asset_inventory.v0.3","classification_model":"ORTHOGONAL_ARTIFACT_CLASS_AND_CAPABILITY_ROLE","records":[{"path":"angie-act/scripts/validate_scorecard.py","artifact_classes":["executables"],"capability_roles":["instrument"],"status_by_class":{"executables":"BURIED_CANDIDATE"}}]}
        out=m.build_plan(inv,root); item=out["plan"][0]
        assert item["state"]=="REVIEW_REQUIRED"
        assert item["target_class"]=="executables"
        assert item["suggested_target_path"]=="executables/angie-act/validate_scorecard.py"
        assert item["suggested_companion_contract"]=="instruments/validate_scorecard.md"
        assert item["move_authorized"] is False
        assert out["moves_performed"] is False and out["authority_created"] is False

def test_true_multi_artifact_class_still_holds():
    repo=Path(__file__).resolve().parents[1]; m=load(repo)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); subprocess.run(["git","init","-q",str(root)],check=True)
        p=root/"docs"/"ambiguous.md"; p.parent.mkdir(parents=True); p.write_text("x\n"); subprocess.run(["git","-C",str(root),"add","."],check=True)
        inv={"schema":"computerwisdom.asset_inventory.v0.3","records":[{"path":"docs/ambiguous.md","artifact_classes":["proofs","whitepapers"],"capability_roles":[],"status_by_class":{"proofs":"BURIED_CANDIDATE","whitepapers":"BURIED_CANDIDATE"}}]}
        assert m.build_plan(inv,root)["plan"][0]["state"]=="HOLD_MULTI_ARTIFACT_CLASS"
