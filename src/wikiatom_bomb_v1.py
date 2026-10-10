from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set

BRANCHES = (
    "RECORD",
    "PROVENANCE",
    "AUTHORITY",
    "CUSTODY",
    "CLOCK",
    "IDENTITY",
    "METRIC",
    "CONTRADICTION",
    "CHALLENGE",
    "MIGRATION",
    "UNKNOWN",
    "NEXT_RECEIPT",
)

REQUIRED_FIELDS = (
    "atom_id",
    "claim_or_object",
    "source_pointer",
    "observed_clock",
    "version",
    "state",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _normalize_values(value: Any) -> List[Any]:
    if isinstance(value, list):
        return sorted((deepcopy(v) for v in value), key=canonical_json)
    return [deepcopy(value)]


def _child_atom(parent: Dict[str, Any], branch: str, payload: Any, index: int = 0) -> Dict[str, Any]:
    suffix = branch if index == 0 else f"{branch}:{index}"
    state = "HOLD" if payload is None else "OBSERVED"
    return {
        "atom_id": f"{parent['atom_id']}::{suffix}",
        "claim_or_object": payload,
        "source_pointer": parent["source_pointer"],
        "observed_clock": parent["observed_clock"],
        "version": parent["version"],
        "state": state,
        "branch": branch,
        "parent_atom_id": parent["atom_id"],
    }


def run_wikiatom_bomb_v1(
    atom: Dict[str, Any],
    *,
    branch_payloads: Optional[Dict[str, Any]] = None,
    related_atoms: Optional[Dict[str, Dict[str, Any]]] = None,
    max_depth: int = 1,
    promotion_requested: bool = False,
    promotion_receipt: Optional[str] = None,
) -> Dict[str, Any]:
    """Pure deterministic WIKIATOM_BOMB_V1 candidate.

    No network, filesystem, clock, randomness, or repository mutation occurs here.
    """
    branch_payloads = branch_payloads or {}
    related_atoms = related_atoms or {}
    visited: Set[str] = set()
    events: List[Dict[str, Any]] = []

    missing = [name for name in REQUIRED_FIELDS if name not in atom or atom[name] in (None, "")]
    if missing:
        result = {
            "engine": "WIKIATOM_BOMB_V1_CANDIDATE",
            "disposition": "HOLD",
            "reason": "MISSING_EDGE",
            "missing_fields": sorted(missing),
            "children": [],
            "events": [{"type": "MISSING_EDGE", "fields": sorted(missing)}],
            "promotion": "NOT_REQUESTED" if not promotion_requested else "BLOCKED",
            "side_effects": False,
        }
        result["output_hash"] = sha256_json(result)
        return result

    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    def expand(current: Dict[str, Any], depth: int) -> List[Dict[str, Any]]:
        atom_id = str(current["atom_id"])
        if atom_id in visited:
            events.append({"type": "CYCLE", "atom_id": atom_id, "action": "RECORD_AND_STOP_BRANCH"})
            return []
        visited.add(atom_id)

        if depth >= max_depth:
            events.append({"type": "MAX_DEPTH", "atom_id": atom_id, "depth": depth})
            return []

        children: List[Dict[str, Any]] = []
        for branch_name in BRANCHES:
            payload = branch_payloads.get(branch_name)
            if isinstance(payload, dict) and payload.get("conflict") is True and "values" in payload:
                values = _normalize_values(payload["values"])
                events.append({"type": "CONFLICT", "branch": branch_name, "count": len(values), "action": "PRESERVE_BOTH"})
                for i, value in enumerate(values, start=1):
                    children.append(_child_atom(current, branch_name, value, i))
            else:
                children.append(_child_atom(current, branch_name, payload))

        linked_ids = current.get("related_atom_ids", []) or []
        for linked_id in sorted(set(str(x) for x in linked_ids)):
            if linked_id in visited:
                events.append({"type": "CYCLE", "atom_id": linked_id, "action": "RECORD_AND_STOP_BRANCH"})
                continue
            linked = related_atoms.get(linked_id)
            if linked is None:
                events.append({"type": "MISSING_EDGE", "related_atom_id": linked_id, "action": "HOLD"})
                continue
            children.extend(expand(linked, depth + 1))
        return children

    children = expand(deepcopy(atom), 0)

    promotion = "NOT_REQUESTED"
    if promotion_requested:
        if promotion_receipt:
            promotion = "ELIGIBLE_FOR_HUMAN_REVIEW"
        else:
            promotion = "BLOCKED"
            events.append({"type": "PROMOTION_BLOCKED", "reason": "RECEIPT_REQUIRED"})

    disposition = "HOLD" if any(e["type"] in {"MISSING_EDGE", "PROMOTION_BLOCKED"} for e in events) else "PASS"
    result = {
        "engine": "WIKIATOM_BOMB_V1_CANDIDATE",
        "disposition": disposition,
        "root_atom_id": atom["atom_id"],
        "children": children,
        "events": sorted(events, key=canonical_json),
        "visited_atom_ids": sorted(visited),
        "promotion": promotion,
        "side_effects": False,
        "max_depth": max_depth,
    }
    result["output_hash"] = sha256_json(result)
    return result
