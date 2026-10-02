"""Deterministic JaySpace Replay SDK v0.1 core.

No network, model, external database, or authority dependency.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, Iterable, List

DISPOSITION_RANK = {"PASS": 0, "HOLD": 1, "CONFLICT": 2, "REJECT": 3}
SYNTHETIC_KINDS = {
    "CONTEXT_SPECIFIC_DERIVATION",
    "GENERAL_SYNTHETIC_EXPLAINER",
    "GENERATED_VARIANT",
}
REAL_RECORD_KINDS = {
    "HISTORICAL_IDENTITY",
    "ALTERNATE_IDENTITY_RECORD",
    "PUBLIC_PERSON_RECORD",
}

LAWS = [
    "REAL_PERSON_RECORD != FICTIONAL_DERIVATION",
    "FICTIONAL_DERIVATION != AUTHORITY",
    "RELATIONSHIP_ROLE != IDENTITY_EQUIVALENCE",
    "PUBLIC_RECORD != COMPLETE_BIOGRAPHY",
    "SOURCE_FACT != SYNTHETIC_AUTHORITY",
    "NARRATIVE_SIMILARITY != IDENTITY_MATCH",
    "MODEL_OUTPUT != RECEIPT",
    "REPLAY_RESULT != LEGAL_FINDING",
    "AUTHORITY_CREATED = FALSE",
]


def _max_disposition(values: Iterable[str]) -> str:
    return max(values, key=lambda value: DISPOSITION_RANK[value], default="PASS")


def evaluate(case: Dict[str, Any]) -> Dict[str, Any]:
    signals: List[str] = []
    dispositions: List[str] = ["PASS"]

    if case.get("authority_created") is not False:
        signals.append("AUTHORITY_CREATION_FORBIDDEN")
        dispositions.append("REJECT")

    nodes = {node.get("id"): node for node in case.get("nodes", []) if node.get("id")}

    if len(nodes) != len(case.get("nodes", [])):
        signals.append("NODE_ID_MISSING_OR_DUPLICATE")
        dispositions.append("REJECT")

    for node_id, node in nodes.items():
        if node.get("authority") not in (None, False):
            signals.append(f"NODE_AUTHORITY_FORBIDDEN:{node_id}")
            dispositions.append("REJECT")
        source_status = node.get("source_status")
        if source_status == "UNBOUND":
            signals.append(f"UNBOUND_NODE:{node_id}")
            dispositions.append("HOLD")
        elif source_status == "CONFLICT":
            signals.append(f"CONFLICT_NODE:{node_id}")
            dispositions.append("CONFLICT")
        elif source_status == "REJECTED":
            signals.append(f"REJECTED_NODE:{node_id}")
            dispositions.append("REJECT")

    for index, edge in enumerate(case.get("edges", [])):
        src = nodes.get(edge.get("from"))
        dst = nodes.get(edge.get("to"))
        if src is None or dst is None:
            signals.append(f"BROKEN_EDGE_REFERENCE:{index}")
            dispositions.append("REJECT")
            continue

        status = edge.get("status")
        if status == "UNBOUND":
            signals.append(f"UNBOUND_EDGE:{index}")
            dispositions.append("HOLD")
        elif status == "CONFLICT":
            signals.append(f"CONFLICT_EDGE:{index}")
            dispositions.append("CONFLICT")
        elif status == "REJECTED":
            signals.append(f"REJECTED_EDGE:{index}")
            dispositions.append("REJECT")

        if edge.get("relation") == "IDENTITY_EQUIVALENCE":
            src_kind = src.get("kind")
            dst_kind = dst.get("kind")
            crosses_real_synthetic = (
                src_kind in SYNTHETIC_KINDS and dst_kind in REAL_RECORD_KINDS
            ) or (
                dst_kind in SYNTHETIC_KINDS and src_kind in REAL_RECORD_KINDS
            )
            if crosses_real_synthetic:
                signals.append(f"REAL_SYNTHETIC_IDENTITY_COLLAPSE_BLOCKED:{index}")
                dispositions.append("REJECT")

        if src.get("kind") == "RELATIONSHIP_ROLE" and edge.get("relation") == "IDENTITY_EQUIVALENCE":
            signals.append(f"RELATIONSHIP_IDENTITY_COLLAPSE_BLOCKED:{index}")
            dispositions.append("REJECT")

    return {
        "case_id": case.get("case_id", "UNSPECIFIED"),
        "disposition": _max_disposition(dispositions),
        "signals": sorted(set(signals)),
        "laws_applied": LAWS,
        "authority_created": False,
    }


def main() -> int:
    case = json.load(sys.stdin)
    receipt = evaluate(case)
    json.dump(receipt, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
