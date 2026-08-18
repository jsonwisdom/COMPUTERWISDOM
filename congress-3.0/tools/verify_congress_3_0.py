from __future__ import annotations

import json
import sys
from pathlib import Path

TERMINAL_ORDER = {"PASS": 0, "HOLD": 1, "CONFLICT": 2, "REJECT": 3}

REQUIRED_PATHS = [
    ("authority", "source_ref"),
    ("authority", "actor"),
    ("authority", "role"),
    ("authority", "jurisdiction"),
    ("authority", "delegation_ref"),
    ("implementation", "rule_ref"),
    ("implementation", "machine_rule_id"),
    ("implementation", "version"),
    ("execution", "actor_type"),
    ("execution", "actor_id"),
    ("execution", "permission_ref"),
    ("execution", "authorization_ref"),
    ("execution", "action"),
    ("execution", "timestamp"),
    ("execution", "input_ref"),
    ("execution", "output_ref"),
    ("record_delta", "before_ref"),
    ("record_delta", "after_ref"),
    ("record_delta", "write_receipt_ref"),
    ("citizen_effect", "effect_type"),
    ("citizen_effect", "notice_ref"),
    ("citizen_effect", "explanation_ref"),
    ("review", "review_ref"),
    ("review", "reviewer_authority_ref"),
    ("replay", "receipt_ref"),
]

PROMOTION_FLAGS = {
    "capability_as_authority": "CAPABILITY_PROMOTED_TO_AUTHORITY",
    "permission_as_authorization": "PERMISSION_PROMOTED_TO_AUTHORIZATION",
    "database_state_as_legal_state": "DATABASE_STATE_PROMOTED_TO_LEGAL_STATE",
    "green_check_as_correct_action": "GREEN_CHECK_PROMOTED_TO_CORRECT_ACTION",
    "model_output_as_government_decision": "MODEL_OUTPUT_PROMOTED_TO_GOVERNMENT_DECISION",
}


def get_path(obj: dict, path: tuple[str, ...]):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def combine(current: str, candidate: str) -> str:
    return candidate if TERMINAL_ORDER[candidate] > TERMINAL_ORDER[current] else current


def verify(case: dict) -> dict:
    disposition = "PASS"
    reasons: list[str] = []
    signals: list[str] = []

    promotions = case.get("attempted_promotions", {})
    for flag, reason in PROMOTION_FLAGS.items():
        if promotions.get(flag) is True:
            disposition = combine(disposition, "REJECT")
            reasons.append(reason)

    missing = [".".join(path) for path in REQUIRED_PATHS if not get_path(case, path)]
    if missing:
        disposition = combine(disposition, "HOLD")
        reasons.append("MISSING_REQUIRED_PROVENANCE:" + ",".join(sorted(missing)))

    scope_relation = get_path(case, ("implementation", "scope_relation"))
    if scope_relation == "conflicts_with_authority":
        disposition = combine(disposition, "CONFLICT")
        reasons.append("MACHINE_RULE_SCOPE_CONFLICT")
    elif scope_relation in (None, "unknown"):
        disposition = combine(disposition, "HOLD")
        reasons.append("MACHINE_RULE_SCOPE_NOT_RECONCILED")

    if case.get("government_records_conflict") is True:
        disposition = combine(disposition, "CONFLICT")
        reasons.append("BOUND_GOVERNMENT_RECORDS_CONFLICT")

    if get_path(case, ("record_delta", "canonical")) is True and not get_path(case, ("record_delta", "promotion_authority_ref")):
        disposition = combine(disposition, "HOLD")
        reasons.append("CANONICAL_MUTATION_PROMOTION_AUTHORITY_MISSING")

    effect_type = get_path(case, ("citizen_effect", "effect_type"))
    if effect_type not in (None, "none", "informational"):
        if not get_path(case, ("review", "review_available")):
            disposition = combine(disposition, "HOLD")
            reasons.append("CONSEQUENTIAL_EFFECT_WITHOUT_REVIEW_PATH")
        if not get_path(case, ("review", "correction_ref")):
            disposition = combine(disposition, "HOLD")
            reasons.append("CORRECTION_RECEIPT_MISSING")

    burden = case.get("burden", {})
    if burden.get("proof_requested_from") == "citizen" and int(burden.get("repeat_count", 0) or 0) > 1:
        signals.append("RECURSIVE_CITIZEN_REPROOF")
        if burden.get("government_record_conflict") is True and not burden.get("government_reconciliation_ref"):
            disposition = combine(disposition, "HOLD")
            reasons.append("GOVERNMENT_RECORD_NOT_RECONCILED_BEFORE_REPROOF")

    forward = get_path(case, ("replay", "forward"))
    reverse = get_path(case, ("replay", "reverse"))
    if isinstance(forward, list) and isinstance(reverse, list):
        if list(reversed(forward)) != reverse:
            disposition = combine(disposition, "CONFLICT")
            reasons.append("FORWARD_REVERSE_REPLAY_MISMATCH")
    else:
        disposition = combine(disposition, "HOLD")
        reasons.append("REPLAY_SEQUENCE_MISSING")

    model = case.get("model", {})
    if model.get("used") is True and effect_type not in (None, "none", "informational"):
        if not model.get("human_or_institutional_decision_ref"):
            disposition = combine(disposition, "HOLD")
            reasons.append("MODEL_USED_WITHOUT_SEPARATE_DECISION_RECEIPT")

    return {
        "case_id": case.get("case_id"),
        "disposition": disposition,
        "reasons": sorted(set(reasons)),
        "signals": sorted(set(signals)),
        "authority_created": False,
        "legal_violation_proven": False,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_congress_3_0.py <vectors.json>")

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = []
    results = []

    for case in payload["cases"]:
        result = verify(case)
        results.append(result)
        if result["disposition"] != case["expected_disposition"]:
            failures.append(
                {
                    "case_id": case["case_id"],
                    "expected": case["expected_disposition"],
                    "actual": result["disposition"],
                    "reasons": result["reasons"],
                }
            )

    print(json.dumps({"results": results, "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
