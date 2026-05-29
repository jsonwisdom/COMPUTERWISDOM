"""
Caseflow State Machine Engine v0.2
Constitutional Game Stack

Enforces:
- caseflow/state_machine/schema_v0_2.json
- caseflow/state_machine/transition_rules_v0_2.json

Boundary:
- authority remains false
- legal_effect remains false
- no witness output becomes verified truth
- no score becomes authority
- no Base / ENS pointer becomes legal effect
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional


class CaseflowEngine:
    """Bounded caseflow transition engine.

    This engine validates and applies procedural state transitions only.
    It does not adjudicate truth, grant authority, sign transactions,
    write ENS records, anchor on Base, or merge repository changes.
    """

    def __init__(self, rules_path: str = "caseflow/state_machine/transition_rules_v0_2.json") -> None:
        self.rules_path = Path(rules_path)
        with self.rules_path.open("r", encoding="utf-8") as handle:
            self.rules: Dict[str, Any] = json.load(handle)

        self.forbidden_promotions = set(self.rules.get("forbidden_promotions", []))
        self.global_invariants = self.rules.get("global_invariants", {})

    def validate_transition(self, case: Dict[str, Any], to_state: str, actor: str) -> Dict[str, Any]:
        """Validate a requested transition without mutating the case."""
        current = case.get("current_state")
        if not current:
            return self._deny("missing_current_state")

        rule = self._find_rule(current, to_state)
        if rule is None:
            return self._deny(f"transition_not_allowed:{current}->{to_state}")

        if actor not in rule.get("allowed_actors", []):
            return self._deny(f"actor_not_permitted:{actor}")

        invariant_result = self._check_global_invariants(case)
        if not invariant_result["valid"]:
            return invariant_result

        promotion_result = self._check_forbidden_promotions(case)
        if not promotion_result["valid"]:
            return promotion_result

        if rule.get("membrane_hold", False):
            governance_result = self._run_governance_checks(case, rule)
            if not governance_result["valid"]:
                return governance_result

        receipt = self._generate_transition_receipt(case, to_state, actor, rule)
        return {"valid": True, "reason": "transition_allowed", "receipt": receipt, "rule": rule}

    def apply_transition(self, case: Dict[str, Any], to_state: str, actor: str) -> Dict[str, Any]:
        """Apply a transition only after validation succeeds."""
        result = self.validate_transition(case, to_state, actor)
        if not result["valid"]:
            case.setdefault("denials", []).append({
                "timestamp": self._now(),
                "from_state": case.get("current_state"),
                "to_state": to_state,
                "actor": actor,
                "reason": result["reason"],
                "authority": False,
            })
            return case

        receipt = result["receipt"]
        previous_state = case["current_state"]
        case.setdefault("history", []).append({
            "timestamp": receipt["timestamp_utc"],
            "from_state": previous_state,
            "to_state": to_state,
            "trigger": f"Actor:{actor}",
            "actor": actor,
            "witness_hash": receipt["case_hash"],
            "receipt": receipt["receipt_hash"],
        })
        case.setdefault("receipts", []).append(receipt)
        case["current_state"] = to_state
        return case

    def _find_rule(self, from_state: str, to_state: str) -> Optional[Dict[str, Any]]:
        for rule in self.rules.get("rules", []):
            if rule.get("from") == from_state and rule.get("to") == to_state:
                return rule
        return None

    def _check_global_invariants(self, case: Dict[str, Any]) -> Dict[str, Any]:
        metadata = case.get("metadata", {})
        if metadata.get("authority_level", 0) > 0:
            return self._deny("authority_level_must_remain_zero")
        if metadata.get("legal_effect", False):
            return self._deny("legal_effect_must_remain_false")
        if metadata.get("ghost_anchor", False):
            return self._deny("ghost_anchor_blocked")
        return {"valid": True, "reason": "global_invariants_hold"}

    def _check_forbidden_promotions(self, case: Dict[str, Any]) -> Dict[str, Any]:
        promotions = set(case.get("forbidden_promotions_detected", []))
        metadata_promotions = set(case.get("metadata", {}).get("forbidden_promotions_detected", []))
        detected = promotions | metadata_promotions
        blocked = sorted(detected & self.forbidden_promotions)
        if blocked:
            return self._deny("forbidden_promotion_detected:" + ",".join(blocked))
        return {"valid": True, "reason": "no_forbidden_promotions"}

    def _run_governance_checks(self, case: Dict[str, Any], rule: Dict[str, Any]) -> Dict[str, Any]:
        required = set(rule.get("required_checks", []))
        satisfied = set(case.get("satisfied_checks", [])) | set(case.get("metadata", {}).get("satisfied_checks", []))
        missing = sorted(check for check in required if check not in satisfied)
        if missing:
            return self._deny("missing_required_checks:" + ",".join(missing))
        return {"valid": True, "reason": "governance_checks_passed"}

    def _generate_transition_receipt(
        self,
        case: Dict[str, Any],
        to_state: str,
        actor: str,
        rule: Dict[str, Any],
    ) -> Dict[str, Any]:
        case_hash = self._hash_json(case)
        receipt = {
            "artifact": "CASEFLOW_TRANSITION_RECEIPT_V0_2",
            "case_id": case["case_id"],
            "transition": f"{case['current_state']}->{to_state}",
            "actor": actor,
            "timestamp_utc": self._now(),
            "case_hash": case_hash,
            "rule_ref": f"{rule['from']}->{rule['to']}",
            "authority": False,
            "legal_effect": False,
        }
        receipt["receipt_hash"] = self._hash_json(receipt)
        return receipt

    @staticmethod
    def _hash_json(value: Dict[str, Any]) -> str:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return "sha256:" + hashlib.sha256(payload).hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _deny(reason: str) -> Dict[str, Any]:
        return {"valid": False, "reason": reason, "authority": False}


if __name__ == "__main__":
    engine = CaseflowEngine()
    case = {
        "case_id": "CASE-20260529-001",
        "current_state": "UNDER_REVIEW",
        "history": [],
        "metadata": {
            "authority_level": 0,
            "boundary_honest": True,
            "satisfied_checks": [
                "review_context_present",
                "receipt_or_pointer_present",
                "authority_false",
            ],
        },
    }
    updated = engine.apply_transition(case, "GOVERNANCE_CHECK", "GROK_WITNESS")
    print(json.dumps(updated, indent=2, sort_keys=True))
