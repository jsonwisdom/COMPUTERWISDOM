#!/usr/bin/env python3
"""JASON-denominator HOLD registry: read-only scoped evidence tally.

Original source_gate, current workflow_gate, and evidence_verdict are distinct.
This program validates a declared sample and its arithmetic; it does not
re-read sources, run the whole GitHub estate, or grant authority.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

VERDICTS = frozenset(("PASS", "FAIL", "UNKNOWN"))
GATES = frozenset(("HOLD", "OPEN"))
PROOF = frozenset(("DIRECT", "DATED_RECORD", "OPERATOR_OUTPUT", "SECONDARY"))
SOURCE_GATES = frozenset(("HOLD", "BLOCKED", "NOT_CLAIMED", "NOT_LISTED", "PRECONDITION_FAILED", "INCOMPLETE", "UNRESOLVED", "NOT_IMPLEMENTED"))
CLASSES = frozenset(("SOURCE_COVERAGE", "ENVIRONMENT_ACCESS", "IDENTITY_PROOF", "DELIVERY_CONTINUITY", "GOVERNANCE_PROCESS", "REPLAY_VALIDATION"))


def audit(manifest):
    d = manifest.get("denominator", {})
    if d.get("person") != "JASON" or d.get("coverage") != "BOUNDED_EVIDENCE_SAMPLE":
        raise ValueError("Define JASON and bounded scope; no invented estate-wide population")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Nonempty source-bound cases required")
    seen = set()
    reasons = collections.Counter()
    verdicts = collections.Counter()
    gates = collections.Counter()
    source_gates = collections.Counter()
    protective = collections.Counter()
    for i, c in enumerate(cases):
        key = c.get("id")
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError(f"Missing or duplicate case ID at {i}")
        seen.add(key)
        for field in ("source_locator", "source_observation", "next_test"):
            if not isinstance(c.get(field), str) or not c[field].strip():
                raise ValueError(f"{key}: missing {field}")
        if c.get("reason_class") not in CLASSES:
            raise ValueError(f"{key}: invalid reason class")
        if c.get("evidence_verdict") not in VERDICTS:
            raise ValueError(f"{key}: HOLD cannot be an evidence verdict")
        if c.get("workflow_gate") not in GATES:
            raise ValueError(f"{key}: invalid workflow gate")
        if c.get("source_gate") not in SOURCE_GATES:
            raise ValueError(f"{key}: missing/invalid original source status")
        if c.get("provenance_class") not in PROOF:
            raise ValueError(f"{key}: missing provenance classification")
        if type(c.get("protective_gate")) is not bool:
            raise ValueError(f"{key}: protective_gate must be boolean")
        reasons[c["reason_class"]] += 1
        verdicts[c["evidence_verdict"]] += 1
        gates[c["workflow_gate"]] += 1
        source_gates[c["source_gate"]] += 1
        protective["PROTECTIVE" if c["protective_gate"] else "REPAIR_CANDIDATE"] += 1
    return {
        "schema": "JASON_HOLD_TALLY_V0_1",
        "denominator": {"person": "JASON", "unit": "unique source-linked cases",
                        "observed_cases": len(cases), "coverage": "BOUNDED_EVIDENCE_SAMPLE",
                        "total_estate_cases": "UNKNOWN"},
        "reason_counts": dict(sorted(reasons.items())),
        "declared_evidence_verdict_counts": {k: verdicts[k] for k in ("PASS", "FAIL", "UNKNOWN")},
        "source_readback_verification": "NOT_PERFORMED_BY_THIS_TALLY",
        "workflow_gate_counts": {k: gates[k] for k in ("HOLD", "OPEN")},
        "observed_source_gate_counts": dict(sorted(source_gates.items())),
        "protection_counts": dict(protective),
        "unfixed": [c["id"] for c in cases if c["workflow_gate"] == "HOLD" and not c["protective_gate"]],
        "invariants": [
            "HOLD_NEVER_A_VERDICT", "UNKNOWN_NEVER_PROMOTED",
            "NO_HUMAN_AUDIT_VERDICT_GATE", "ORIGINALS_NOT_OVERWRITTEN",
            "HUMAN_APPROVAL_ONLY_FOR_CONSEQUENTIAL_ACTIONS",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Existing local JSON case registry")
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.manifest.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"UNKNOWN - input/denominator invalid: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
