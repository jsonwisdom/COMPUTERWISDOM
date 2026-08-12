#!/usr/bin/env python3
"""Fail-closed migration planner for orthogonal COMPUTERWISDOM inventory."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
from typing import Any
CANONICAL_ROOTS={"executables":"executables","fixtures":"fixtures","proofs":"proofs","whitepapers":"whitepapers"}
GENERIC_CONTAINERS={"scripts","tools","bin","cli","tests","fixtures"}

def git_blob_sha(repo_root: Path, rel_path: str):
    p=subprocess.run(["git","-C",str(repo_root),"ls-files","-s","--",rel_path],text=True,capture_output=True,check=False)
    if p.returncode!=0 or not p.stdout.strip(): return None
    f=p.stdout.splitlines()[0].split(); return f[1] if len(f)>=2 else None

def suggested_target(asset_class: str, source_path: str) -> str:
    parts=list(Path(source_path).parts); kept=[p for p in parts[:-1] if p.lower() not in GENERIC_CONTAINERS]
    return Path(CANONICAL_ROOTS[asset_class],*(kept+[parts[-1]])).as_posix()

def build_plan(inventory: dict[str,Any], repo_root: Path) -> dict[str,Any]:
    plan=[]
    for r in inventory.get("records",[]):
        classes=r.get("artifact_classes",r.get("classification_candidates",[])); roles=sorted(r.get("capability_roles",[]))
        buried=sorted(c for c in classes if r.get("status_by_class",{}).get(c)=="BURIED_CANDIDATE")
        if not buried: continue
        src=r["path"]; blob=git_blob_sha(repo_root,src)
        if len(buried)!=1: target_class=target=None; state="HOLD_MULTI_ARTIFACT_CLASS"
        else:
            target_class=buried[0]; target=suggested_target(target_class,src)
            if blob is None: state="HOLD_SOURCE_BLOB_UNKNOWN"
            elif (repo_root/target).exists() and target!=src: state="HOLD_TARGET_COLLISION"
            else: state="REVIEW_REQUIRED"
        companion=f"instruments/{Path(src).stem}.md" if target_class=="executables" and "instrument" in roles else None
        plan.append({"source_path":src,"source_blob_sha":blob,"artifact_classes":sorted(classes),"capability_roles":roles,"buried_artifact_classes":buried,"target_class":target_class,"suggested_target_path":target,"suggested_companion_contract":companion,"target_namespace_strategy":"PRESERVE_SOURCE_CONTEXT","state":state,"dependencies_updated":False,"semantic_review_passed":False,"tests_passed":False,"move_authorized":False})
    counts={}
    for i in plan: counts[i["state"]]=counts.get(i["state"],0)+1
    return {"schema":"computerwisdom.asset_migration_plan.v0.2","classification_model":inventory.get("classification_model"),"source_inventory_schema":inventory.get("schema"),"plan":plan,"summary":{"candidate_count":len(plan),"state_counts":counts},"moves_performed":False,"authority_created":False}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("inventory",type=Path); p.add_argument("--repo-root",type=Path,default=Path(".")); a=p.parse_args()
    inv=json.loads(a.inventory.read_text(encoding="utf-8")); print(json.dumps(build_plan(inv,a.repo_root.resolve()),indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
