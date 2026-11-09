"""Synthetic, read-only scoped inheritance conformance model.

Not an authority engine. An actual evidence verifier must validate documents and
witness signatures outside this module before setting the trusted test fields.
No family or military personal records are embedded here.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

STATES = frozenset({"OBSERVED", "HOLD", "CONFLICT", "VERIFIED_SCOPED", "APPROVED"})
ENLISTED_GRADES = frozenset(f"E-{n}" for n in range(1, 10))


def canonical_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(data.encode("utf-8")).hexdigest()


def witness_valid(witness: dict | None, *, target_kind: str, target_id: str, scope: str) -> bool:
    """Consume a verifier-provided witness result; never authenticate it here."""
    return bool(
        isinstance(witness, dict)
        and witness.get("verified") is True
        and witness.get("authorized") is True
        and witness.get("target_kind") == target_kind
        and witness.get("target_id") == target_id
        and witness.get("scope") == scope
    )


def derive_child_state(child: dict) -> str:
    """Claimed statuses are deliberately ignored; synthetic verification inputs rule."""
    source = child.get("evidence", "missing")
    if source == "conflict":
        return "CONFLICT"
    if source != "verified":
        return "OBSERVED" if source == "observed" else "HOLD"
    verification = child.get("verification") or {}
    needed = set(child.get("required_checks", ("input_hash", "method")))
    performed = set(verification.get("checks", ()))
    if not (verification.get("verified") is True
            and verification.get("scope") == child.get("type")
            and needed.issubset(performed)):
        return "HOLD"
    if witness_valid(child.get("approval_witness"), target_kind="child",
                     target_id=child.get("id"), scope=child.get("type")):
        return "APPROVED"
    return "VERIFIED_SCOPED"


def evaluate(parent: dict, children: list[dict], profile: dict, *,
             reducer: bool = False, parent_witness: dict | None = None,
             current_profile_revision: str | None = None,
             conflicts: list[tuple[str, str]] | None = None,
             supersessions: dict[str, str] | None = None,
             parent_exists: bool = True,
             attempt_parent_mutation: bool = False) -> dict:
    """Return a new derived result and never mutate parent, children or profile.

    This is test-fixture semantics only; evidence assertions and witness validation
    must come from independently trusted upstream processes in production.
    """
    original = copy.deepcopy(parent)
    result = {"aggregate": "HOLD", "parent_state": original.get("state"),
              "new_parent_receipt": None, "child_states": {}, "error": None,
              "retained_child_ids": sorted(c.get("id", "") for c in children)}
    if attempt_parent_mutation:
        result["error"] = "REJECT_MUTATION"
        return result
    if not parent_exists or not original.get("id") or not original.get("digest"):
        result["error"] = "UNRESOLVED_PARENT"
        return result
    if current_profile_revision is not None and current_profile_revision != profile.get("revision"):
        result["error"] = "PROFILE_CHANGED"
        return result
    if not profile.get("required_types"):
        result["error"] = "MISSING_REQUIRED_PROFILE"
        return result
    child_ids = [c.get("id") for c in children]
    source_ids = [c.get("source_digest") for c in children if c.get("source_digest")]
    if len(child_ids) != len(set(child_ids)) or len(source_ids) != len(set(source_ids)):
        result["error"] = "DUPLICATE_LINEAGE"
        return result
    if original["id"] in child_ids or any(c.get("ancestor_id") in child_ids
                                             for c in children if c.get("ancestor_id")):
        result["error"] = "LINEAGE_CYCLE"
        return result
    if any(c.get("parent_id") != original["id"] or
           c.get("parent_digest") != original["digest"] for c in children):
        result["error"] = "WRONG_PARENT_BINDING"
        return result

    states = {c["id"]: derive_child_state(c) for c in children}
    result["child_states"] = dict(sorted(states.items()))
    supersessions = supersessions or {}
    for old, new in supersessions.items():
        if old not in states or new not in states or old == new:
            result["error"] = "INVALID_SUPERSESSION"
            return result
        # Explicitly supersede only a previous HOLD with scoped verified evidence.
        if states[old] != "HOLD" or states[new] not in ("VERIFIED_SCOPED", "APPROVED"):
            result["error"] = "INVALID_SUPERSESSION"
            return result
    required = [c for c in children if c.get("requirement") == "REQUIRED"
                and c["id"] not in supersessions]
    required_types = set(profile["required_types"])
    if not required_types.issubset({c.get("type") for c in required}):
        return result
    required_states = [states[c["id"]] for c in required if c.get("type") in required_types]
    if "CONFLICT" in required_states:
        result["aggregate"] = "CONFLICT"
    elif all(s in ("VERIFIED_SCOPED", "APPROVED") for s in required_states):
        result["aggregate"] = "VERIFIED_SCOPED"
    # An affirmative contradiction between independent relevant children
    # must survive, even if each was individually verified within its scope.
    for left, right in conflicts or []:
        if left in states and right in states and left != right and all(
                states[k] in ("VERIFIED_SCOPED", "APPROVED") for k in (left, right)):
            result["aggregate"] = "CONFLICT"
    if (reducer and result["aggregate"] == "VERIFIED_SCOPED" and
            witness_valid(parent_witness, target_kind="parent", target_id=original["id"],
                          scope=profile.get("parent_scope", "CitizenRoot"))):
        result["new_parent_receipt"] = {
            "parent_id": original["id"], "old_parent_digest": original["digest"],
            "new_state": "APPROVED", "authority_from_witness": True,
            "new_receipt_digest": canonical_hash({"parent": original["digest"],
                                                  "verified_children": sorted(states.items()),
                                                  "profile": profile.get("revision")})}
    return result


def reconcile_documented_pay(periods: list[dict]) -> dict:
    """No E-0 rate, no inferred entitlement, and no missing months as $0."""
    total = 0
    unknown = []
    for row in periods:
        label = row.get("period_id", "unknown")
        grade = row.get("actual_grade")
        if grade not in ENLISTED_GRADES or not row.get("verified_due") or not row.get("verified_paid"):
            unknown.append(label)
            continue
        due, paid = row.get("documented_gross_due"), row.get("recorded_gross_paid")
        if not isinstance(due, (int, float)) or not isinstance(paid, (int, float)):
            unknown.append(label)
            continue
        total += due - paid
    return {"fully_reconciled_shortfall": total if not unknown else None,
            "known_period_difference": total, "unresolved_periods": unknown,
            "not_an_entitlement_decision": True}
