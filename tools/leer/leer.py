#!/usr/bin/env python3
"""Read-only LEAR pilot: 'children' are curriculum nodes, never people."""
import hashlib
import json
import sys

BUDGET = 100
LESSONS = {
    "MN-13": {
        "title": "Gopher Math: evidence and denominators",
        "jurisdiction": "Minnesota",
        "source": "https://www.revisor.mn.gov/statutes/cite/13",
        "source_verified_at": None,
        "parent": "CLASSES-WITH-GLASSES",
        "synthetic": True,
    },
    "AL-01": {
        "title": "ALISON: legal sources and public records",
        "jurisdiction": "Alabama",
        "source": "https://alison.legislature.state.al.us/",
        "source_verified_at": None,
        "parent": "CLASSES-WITH-GLASSES",
        "synthetic": True,
    },
}
POLICY = {
    "schema": "computerwisdom/leer/v0.1",
    "authority": False,
    "legal_effect": False,
    "external_writes": False,
    "real_voting": False,
    "human_child_records": False,
}

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def run(args):
    if args == ["get", "children"]:
        return {"status": "SYNTHETIC_ONLY", "children": sorted(LESSONS)}
    if len(args) == 3 and args[:2] == ["get", "child"]:
        node = LESSONS.get(args[2])
        return {"status": "READ_ONLY", "node": args[2], "lesson": node} if node else {"status": "UNKNOWN", "error": "No permitted synthetic lesson"}
    if len(args) == 2 and args[0] == "learn":
        node = LESSONS.get(args[1])
        if not node:
            return {"status": "UNKNOWN", "error": "No permitted synthetic lesson"}
        return {"status": "EDUCATIONAL_ONLY", "node": args[1], "source": node["source"], "source_verified_at": None, "questions": ["Who alleges?", "What law and effective date?", "Who carries the burden?", "Which authenticated records?", "What remains UNKNOWN?"]}
    if len(args) == 2 and args[0] == "vote":
        try:
            votes = int(args[1])
        except ValueError:
            return {"status": "REJECT", "reason": "Integer vote count required"}
        if votes < 0 or votes > 100:
            return {"status": "REJECT", "reason": "Out of classroom range"}
        cost = votes ** 2
        return {"status": "SIMULATION_ONLY" if cost <= BUDGET else "REJECT", "votes": votes, "credits_required": cost, "credits_remaining": BUDGET - cost if cost <= BUDGET else None, "real_election_action": False}
    if args == ["replay"]:
        payload = {"policy": POLICY, "lessons": LESSONS}
        return {"status": "LOCAL_BYTES_ONLY", "sha256": hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest(), "authority": False, "proves": "local synthetic serialization integrity only", "external_source_authentication": "NOT_PERFORMED"}
    return {"status": "REJECT", "help": "get children | get child ID | learn ID | vote N | replay"}

def main(argv=None):
    result = run(sys.argv[1:] if argv is None else argv)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 2 if result["status"] in ("UNKNOWN", "REJECT") else 0

if __name__ == "__main__":
    raise SystemExit(main())
