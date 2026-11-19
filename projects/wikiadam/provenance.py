#!/usr/bin/env python3
"""WikiAdam v0.1 — evidence-qualified provenance navigation.

"JASON = DENOMINATOR" is the person-first anchor, not a claim that all paths
lead to JASON. Mathematical coverage uses enumerated candidate IDs and is
undefined on an empty population.

Source hash replay verifies file bytes, not the truth or authorship of a
historical assertion. REVIEWED is an explicitly *declared* review status.
Output is POLICY_QUALIFIED, never unqualified proof of real-world authorship.
No network, browser, filesystem mutation or human audit signoff.
"""
from __future__ import annotations

from collections import Counter, deque
from pathlib import Path
import hashlib
import json
import re

SCHEMA = "WIKIADAM_PROVENANCE_V0_1"
POLICY = "WIKIADAM_POLICY_V0_1"

# This is a closed grammar: derivation from someone's work does NOT
# imply authorship of the new derivative.
RELATION_GRAMMAR = {
    "AUTHORED_BY": (("authored_by",),),
    "PROPOSED_BY": (("proposed_by",),),
    "IMPLEMENTED_BY": (("implemented_by",),),
    "DISCUSSED_BY": (("discussed_by",),),
    "DERIVED_FROM_PERSON_WORK": (
        ("derived_from", "authored_by"),
        ("derived_from", "proposed_by"),
    ),
}
EDGE_TYPES = {
    "authored_by", "proposed_by", "implemented_by", "discussed_by",
    "derived_from", "attributed_by",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class AuditInputError(ValueError):
    pass


def _validate(report: dict) -> tuple[dict, list, dict, list]:
    if not isinstance(report, dict) or report.get("schema") != SCHEMA:
        raise AuditInputError("Wrong WikiAdam schema")
    if report.get("denominator") != "JASON":
        raise AuditInputError("Missing person-first JASON anchor")
    scope = report.get("scope")
    if not isinstance(scope, dict) or scope.get("policy") != POLICY:
        raise AuditInputError("Missing versioned verification policy")
    if not all(isinstance(scope.get(x), str) and scope[x] for x in ("id", "snapshot")):
        raise AuditInputError("Scope and snapshot required")
    for item in ("candidates", "edges", "evidence"):
        if not isinstance(report.get(item), list):
            raise AuditInputError(f"{item} must be a list")
    candidates = scope.get("candidate_ids")
    if not isinstance(candidates, list) or any(not isinstance(x, str) or not x for x in candidates):
        raise AuditInputError("Scope candidate_ids must be stable nonblank strings")
    if scope.get("population_completeness") not in ("UNKNOWN", "BOUNDED"):
        raise AuditInputError("Do not assert full corpus completeness")
    seen_edges = set()
    edges = report["edges"]
    for edge in edges:
        if not isinstance(edge, dict):
            raise AuditInputError("Malformed edge")
        key = edge.get("id")
        if not isinstance(key, str) or not key or key in seen_edges:
            raise AuditInputError("Duplicate or missing edge ID")
        seen_edges.add(key)
        if edge.get("type") not in EDGE_TYPES:
            raise AuditInputError(f"Invalid edge type {key}")
        if any(not isinstance(edge.get(k), str) or not edge[k] for k in ("from", "to")):
            raise AuditInputError("Edge requires exact subject and object")
        if not isinstance(edge.get("evidence_ids"), list) or not isinstance(edge.get("contradictions"), list):
            raise AuditInputError("Edge must declare evidence and contradictions arrays")
    evidences = {}
    for ev in report["evidence"]:
        if not isinstance(ev, dict) or not isinstance(ev.get("id"), str) or not ev["id"]:
            raise AuditInputError("Invalid evidence record")
        if ev["id"] in evidences:
            raise AuditInputError("Duplicate evidence ID")
        evidences[ev["id"]] = ev
    return scope, list(dict.fromkeys(candidates)), evidences, edges


def _evidence_status(ref: str, evidences: dict, evidence_root: Path | None) -> str:
    ev = evidences.get(ref)
    if ev is None:
        return "MISSING_INDEX_REFERENCE"
    if ev.get("review_state") == "DISPUTED":
        return "CONFLICT"
    if ev.get("review_state") != "REVIEWED":
        return "UNREVIEWED"
    if not isinstance(ev.get("source_locator"), str) or not ev["source_locator"].strip():
        return "MISSING_SOURCE_LOCATOR"
    digest = ev.get("sha256")
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        return "MISSING_OR_INVALID_HASH"
    rel = ev.get("relative_path")
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        return "INVALID_RELATIVE_PATH"
    if evidence_root is None or not evidence_root.is_dir():
        return "SOURCE_ROOT_UNAVAILABLE"
    target = (evidence_root.resolve() / rel).resolve()
    if target == evidence_root.resolve() or evidence_root.resolve() not in target.parents:
        return "PATH_ESCAPE"
    if not target.is_file():
        return "MISSING_SOURCE_FILE"
    try:
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
    except OSError:
        return "UNREADABLE_SOURCE_FILE"
    return "BYTES_MATCH_REVIEW_DECLARED" if actual == digest else "HASH_CONFLICT"


def audit(document: dict, evidence_root: str | Path | None, relationship: str = "AUTHORED_BY") -> dict:
    scope, candidates, evidences, edges = _validate(document)
    if relationship not in RELATION_GRAMMAR:
        raise AuditInputError("Requested relationship is not in policy grammar")
    root = Path(evidence_root) if evidence_root is not None else None
    status = {key: _evidence_status(key, evidences, root) for key in evidences}
    outgoing = {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge)
    for key in outgoing:
        outgoing[key].sort(key=lambda e: e["id"])

    def qualified(e: dict) -> bool:
        refs = e["evidence_ids"]
        return (
            e.get("verification_state") == "REVIEWED"
            and not e["contradictions"]
            and bool(refs)
            and all(status.get(ref, "MISSING_INDEX_REFERENCE") == "BYTES_MATCH_REVIEW_DECLARED" for ref in refs)
        )

    def search(candidate: str):
        # Graph traversal is bounded and deterministic; cycles never imply authorship.
        queue = deque([(candidate, (), (), (candidate,))])
        while queue:
            current, types, links, visited = queue.popleft()
            if current == "JASON" and types in RELATION_GRAMMAR[relationship]:
                return list(links)
            if len(types) >= 3:
                continue
            for edge in outgoing.get(current, []):
                if not qualified(edge) or edge["to"] in visited:
                    continue
                next_types = types + (edge["type"],)
                if not any(grammar[:len(next_types)] == next_types for grammar in RELATION_GRAMMAR[relationship]):
                    continue
                queue.append((edge["to"], next_types, links + (edge["id"],), visited + (edge["to"],)))
        return []

    rows = []
    qualified_count = 0
    for candidate in candidates:
        path = search(candidate)
        has_conflict = any(e["from"] == candidate and (
            e["contradictions"] or e.get("verification_state") == "CONFLICTED" or
            any(status.get(r) in ("CONFLICT", "HASH_CONFLICT") for r in e["evidence_ids"])
        ) for e in outgoing.get(candidate, []))
        verdict = ("DISPUTED" if has_conflict else
                   "POLICY_QUALIFIED" if path else "UNKNOWN")
        if verdict == "DISPUTED":
            path = []  # conflicting evidence cannot be silently promoted
        if verdict == "POLICY_QUALIFIED":
            qualified_count += 1
        needed = sorted({r for e in outgoing.get(candidate, []) for r in e["evidence_ids"]
                         if status.get(r, "MISSING_INDEX_REFERENCE") != "BYTES_MATCH_REVIEW_DECLARED"})
        rows.append({
            "candidate": candidate,
            "requested_relationship": relationship,
            "verdict": verdict,
            "evidence_path_edge_ids": path,
            "unresolved_evidence_ids": needed,
            "recovery_action": (
                "RESOLVE_CONTRADICTORY_EVIDENCE" if verdict == "DISPUTED"
                else "REPLAY_MISSING_OR_UNREVIEWED_SOURCE" if needed
                else "DISCOVER_OR_REVIEW_TYPED_RELATIONSHIP" if not path
                else None
            ),
        })

    denominator = len(candidates)
    return {
        "schema": "WIKIADAM_AUDIT_RESULT_V0_1",
        "person_first_denominator": "JASON",
        "policy": POLICY,
        "scope_id": scope["id"],
        "snapshot": scope["snapshot"],
        "population_completeness": scope["population_completeness"],
        "requested_relationship": relationship,
        "candidate_count": denominator,
        "policy_qualified_count": qualified_count,
        "coverage": None if denominator == 0 else {"numerator": qualified_count, "denominator": denominator},
        "coverage_undefined": denominator == 0,
        "historical_completeness": "UNKNOWN",
        "evidence_byte_states": dict(sorted(Counter(status.values()).items())),
        "rows": rows,
        "source_authorship_authenticated_by_hash_alone": False,
        "authority_created": False,
        "no_human_audit_verdict_gate": True,
    }


def public_summary(private_report: dict) -> dict:
    """Share only aggregate results; never publish IDs, source paths, or hashes."""
    return {
        "schema": "WIKIADAM_PUBLIC_SUMMARY_V0_1",
        "scope_id": private_report["scope_id"],
        "policy": private_report["policy"],
        "candidate_count": private_report["candidate_count"],
        "policy_qualified_count": private_report["policy_qualified_count"],
        "coverage": private_report["coverage"],
        "historical_completeness": "UNKNOWN",
        "verdict_counts": dict(sorted(Counter(r["verdict"] for r in private_report["rows"]).items())),
        "authority_created": False,
    }


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", help="Private JSON index with source references")
    p.add_argument("--source-root", help="Local private evidence directory (required for qualification)")
    p.add_argument("--relationship", choices=sorted(RELATION_GRAMMAR), default="AUTHORED_BY")
    p.add_argument("--public-summary", action="store_true", help="Suppress source identities/paths")
    args = p.parse_args()
    document = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    result = audit(document, args.source_root, args.relationship)
    print(json.dumps(public_summary(result) if args.public_summary else result, indent=2))


if __name__ == "__main__":
    main()
