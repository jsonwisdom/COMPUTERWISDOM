#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
RULES_PATH = ROOT / "tools" / "mission_control" / "classify_rules.json"
INDEX_PATH = ROOT / "missions" / "_MISSION_INDEX.json"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, errors="replace")


def refs():
    raw = git("for-each-ref", "--format=%(refname)\t%(objectname)", "refs/remotes/origin", "refs/heads")
    chosen = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        ref, sha = line.split("\t", 1)
        if ref == "refs/remotes/origin/HEAD":
            continue
        if ref.startswith("refs/remotes/origin/"):
            branch = ref[len("refs/remotes/origin/"):]
            rank = 2
        elif ref.startswith("refs/heads/"):
            branch = ref[len("refs/heads/"):]
            rank = 1
        else:
            continue
        old = chosen.get(branch)
        if old is None or rank > old[0]:
            chosen[branch] = (rank, ref, sha)
    return [(branch, ref, sha) for branch, (_, ref, sha) in sorted(chosen.items())]


def tree_paths(sha):
    try:
        return git("ls-tree", "-r", "--name-only", sha).splitlines()
    except subprocess.CalledProcessError:
        return []


def state_signal(branch):
    b = branch.lower()
    if b.startswith("archive/"):
        return "ARCHIVED_SIGNAL"
    if b.startswith("proposal/") or b.startswith("draft/") or b.startswith("design/"):
        return "PROPOSAL_SIGNAL"
    if b.startswith("post-merge/") or b.startswith("post-anchor/") or b.startswith("receipt/"):
        return "POST_EVENT_SIGNAL"
    if b.startswith("fix/"):
        return "ACTIVE_FIX_SIGNAL"
    if b in ("master", "main"):
        return "DEFAULT_BRANCH_SIGNAL"
    return "UNVERIFIED"


def classify(branch, paths, rules):
    hits = []
    for rule in rules:
        branch_hit = bool(re.search(rule["branch_regex"], branch))
        path_hits = []
        for pattern in rule.get("path_regex", []):
            rx = re.compile(pattern)
            if any(rx.search(p) for p in paths):
                path_hits.append(pattern)
        if branch_hit or path_hits:
            score = int(rule.get("priority", 0)) * 100 + (10 if branch_hit else 0) + len(path_hits)
            hits.append((score, rule, branch_hit, path_hits))
    hits.sort(key=lambda x: (-x[0], x[1]["id"]))
    if not hits:
        return None, []
    selected = hits[0][1]
    detail = [
        {
            "rule_id": h[1]["id"],
            "score": h[0],
            "branch_hit": h[2],
            "path_hits": h[3],
        }
        for h in hits
    ]
    return selected, detail


def discovery_id(branch, sha):
    return hashlib.sha256(f"{branch}\0{sha}".encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Generate provenance-preserving COMPUTERWISDOM mission registry.")
    ap.add_argument("--no-path-scan", action="store_true", help="Classify by branch name only.")
    args = ap.parse_args()

    rules_bytes = RULES_PATH.read_bytes()
    rules_doc = json.loads(rules_bytes)
    rules = rules_doc["rules"]
    entries = []

    for branch, ref, sha in refs():
        paths = [] if args.no_path_scan else tree_paths(sha)
        selected, matches = classify(branch, paths, rules)
        if selected:
            mission_id = selected["mission_id"]
            artifact_class = selected["artifact_class"]
            destination = f"missions/{mission_id}/"
        else:
            mission_id = "UNKNOWN"
            artifact_class = "UNKNOWN"
            destination = None

        entries.append({
            "DISCOVERY_ID": discovery_id(branch, sha),
            "ARTIFACT_ID": "UNSPLIT_BRANCH_TIP",
            "MISSION_ID": mission_id,
            "CURRENT_LOCATION": ref,
            "BRANCH": branch,
            "ARTIFACT_CLASS": artifact_class,
            "CURRENT_STATE": state_signal(branch),
            "CANONICAL_DESTINATION": destination,
            "DESTINATION_SUBDIR": None,
            "SOURCE_SHA": sha,
            "SOURCE_PATHS": [],
            "MIGRATION_STATUS": "PENDING_REVIEW",
            "AUTHORITY_CREATED": False,
            "REVIEW_REQUIRED": True,
            "CLASSIFICATION_MATCHES": matches,
            "CLASSIFICATION_AMBIGUOUS": len(matches) > 1,
            "DISCOVERY_SCOPE": "BRANCH_TIP",
        })

    output = {
        "REGISTRY_VERSION": "0.1",
        "GENERATOR": "tools/mission_control/build_index.py",
        "RULESET_SHA256": hashlib.sha256(rules_bytes).hexdigest(),
        "AUTHORITY_CREATED": False,
        "MIGRATION_AUTHORIZED": False,
        "entries": entries,
    }
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} branch-tip entries to {INDEX_PATH}")
    print("All generated entries require explicit review before migration eligibility.")
    print("SOURCE_PATHS and DESTINATION_SUBDIR are intentionally empty until artifact-level review.")
    print(f"Unclassified: {sum(1 for e in entries if e['MISSION_ID'] == 'UNKNOWN')}")
    print(f"Ambiguous classification: {sum(1 for e in entries if e['CLASSIFICATION_AMBIGUOUS'])}")


if __name__ == "__main__":
    main()
