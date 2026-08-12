#!/usr/bin/env python3
"""Read-only COMPUTERWISDOM asset inventory v0.3.

Separates artifact class from capability role so a runnable validator is one
executable artifact with an instrument role, not a multi-home conflict.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

CANONICAL_ROOTS = {"executables":"executables","fixtures":"fixtures","proofs":"proofs","whitepapers":"whitepapers"}
SKIP_PARTS = {".git","node_modules",".venv","venv","__pycache__"}
EXEC_SUFFIXES = {".sh",".ps1",".bat",".cmd",".py"}
TEXT_PROOF_SUFFIXES = {".json",".jsonl",".md",".markdown",".txt",".csv",".yaml",".yml"}
EXEC_PATH_HINTS = {"scripts","tools","bin","cli"}
INSTRUMENT_HINTS = ("auditor","audit","validator","validate","verifier","verify","evaluator","scanner","router","meter")
PROOF_HINTS = ("proof","verifier_chain","verification_result")
WHITEPAPER_HINTS = ("whitepaper","white_paper","white-paper")
WHITEPAPER_CONTENT_HINTS = ("abstract","methodology","methods","findings","conclusion","references","research","architecture")
NATIVE_HOME_RULES = ((("tests",),"executables"),)

def _first_line(path: Path) -> str:
    try:
        with path.open("r",encoding="utf-8",errors="ignore") as handle:
            return handle.readline(256)
    except OSError:
        return ""

def _sample_text(path: Path, limit: int = 32768) -> str:
    try:
        return path.read_text(encoding="utf-8",errors="ignore")[:limit].lower()
    except OSError:
        return ""

def _is_runnable(path: Path, rel: Path) -> bool:
    if path.suffix.lower() not in EXEC_SUFFIXES:
        return False
    name=path.name.lower(); parts={p.lower() for p in rel.parts}
    return (_first_line(path).startswith("#!") or bool(parts & EXEC_PATH_HINTS) or any(t in name for t in ("run","cli","verify","validate","audit","replay")) or (rel.parts and rel.parts[0].lower()=="executables"))

def classify(path: Path, root: Path):
    rel=path.relative_to(root); posix=rel.as_posix().lower(); name=path.name.lower(); parts={p.lower() for p in rel.parts}
    classes=set(); roles=set(); basis={"artifact_classes":{},"capability_roles":{}}
    def add_class(c,r): classes.add(c); basis["artifact_classes"].setdefault(c,[]).append(r)
    def add_role(c,r): roles.add(c); basis["capability_roles"].setdefault(c,[]).append(r)
    runnable=_is_runnable(path,rel)
    if "fixture" in posix or "fixtures" in parts:
        add_class("fixtures","path_or_name_fixture_hint")
    elif runnable:
        add_class("executables","runnable_or_command_hint")
    else:
        if path.suffix.lower() in TEXT_PROOF_SUFFIXES and (any(h in posix for h in PROOF_HINTS) or "proofs" in parts):
            add_class("proofs","explicit_proof_hint")
        if any(h in posix for h in WHITEPAPER_HINTS) or "whitepapers" in parts:
            add_class("whitepapers","explicit_whitepaper_hint")
        elif path.suffix.lower() in {".md",".markdown"} and "proofs" not in classes:
            text=_sample_text(path); score=sum(1 for h in WHITEPAPER_CONTENT_HINTS if h in text)
            if score>=3: add_class("whitepapers",f"content_whitepaper_score:{score}")
    if runnable and any(h in name for h in INSTRUMENT_HINTS):
        add_role("instrument","runnable_instrument_name_hint")
    elif rel.parts and rel.parts[0].lower()=="instruments":
        add_role("instrument","canonical_instrument_spec")
    return sorted(classes),sorted(roles),basis

def _native_home(rel: Path, asset_class: str) -> bool:
    parts=tuple(p.lower() for p in rel.parts)
    return any(native_class==asset_class and parts[:len(prefix)]==prefix for prefix,native_class in NATIVE_HOME_RULES)

def inventory(root: Path) -> dict:
    records=[]
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel=path.relative_to(root)
        if any(part in SKIP_PARTS for part in rel.parts): continue
        classes,roles,basis=classify(path,root)
        if not classes and not roles: continue
        statuses={}
        for c in classes:
            if rel.parts and rel.parts[0].lower()==CANONICAL_ROOTS[c]: status="CANONICAL"
            elif _native_home(rel,c): status="NATIVE_HOME"
            else: status="BURIED_CANDIDATE"
            statuses[c]=status
        records.append({"path":rel.as_posix(),"artifact_classes":classes,"capability_roles":roles,"classification_candidates":classes,"classification_basis":basis,"status_by_class":statuses})
    buried=sum(1 for r in records if "BURIED_CANDIDATE" in r["status_by_class"].values())
    multi=sum(1 for r in records if sum(1 for s in r["status_by_class"].values() if s=="BURIED_CANDIDATE")>1)
    return {"schema":"computerwisdom.asset_inventory.v0.3","classification_model":"ORTHOGONAL_ARTIFACT_CLASS_AND_CAPABILITY_ROLE","root":str(root),"records":records,"summary":{"candidate_files":len(records),"buried_candidate_files":buried,"multi_artifact_class_candidates":multi},"classification_requires_review":True,"moves_performed":False,"authority_created":False}

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--root",default="."); args=parser.parse_args()
    print(json.dumps(inventory(Path(args.root).resolve()),indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
