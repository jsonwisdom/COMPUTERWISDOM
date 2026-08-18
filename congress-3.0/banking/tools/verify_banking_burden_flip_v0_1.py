from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

TERMINAL_ORDER = {"PASS": 0, "HOLD": 1, "CONFLICT": 2, "REJECT": 3}

TRIGGER_RULES = {
    "CIP_ACCOUNT_OPENING": {
        "actor": "bank",
        "duty": "verify_identity_and_record",
        "burden_state": "SHARED_SEQUENTIAL",
        "signal": "CIP_CUSTOMER_INFORMATION_PLUS_BANK_VERIFICATION_DUTY",
    },
    "ECOA_ADVERSE_ACTION": {
        "actor": "creditor",
        "duty": "adverse_action_notice_and_reasons_path",
        "burden_state": "INSTITUTION_DUTY_ACTIVE",
        "signal": "ECOA_EXPLANATION_DUTY",
    },
    "FCRA_CRA_DISPUTE": {
        "actor": "consumer_reporting_agency",
        "duty": "cra_reinvestigate_and_correct",
        "burden_state": "INSTITUTION_DUTY_ACTIVE",
        "signal": "FCRA_CRA_REINVESTIGATION_DUTY",
    },
    "FCRA_FURNISHER_DIRECT_DISPUTE": {
        "actor": "furnisher",
        "duty": "furnisher_investigate_and_correct",
        "burden_state": "INSTITUTION_DUTY_ACTIVE",
        "signal": "FCRA_FURNISHER_INVESTIGATION_DUTY",
    },
    "FDCPA_WRITTEN_DISPUTE_30D": {
        "actor": "debt_collector",
        "duty": "pause_collect_verify_mail",
        "burden_state": "INSTITUTION_DUTY_ACTIVE",
        "signal": "FDCPA_VALIDATION_AND_COLLECTION_PAUSE_DUTY",
    },
}

PROMOTION_FLAGS = {
    "private_action_as_government_action": "PRIVATE_ACTION_PROMOTED_TO_GOVERNMENT_ACTION",
    "general_bank_action_as_ecoa": "GENERAL_BANK_ACTION_PROMOTED_TO_ECOA_ADVERSE_ACTION",
    "any_dispute_as_fcra": "ANY_DISPUTE_PROMOTED_TO_FCRA_TRIGGER",
    "any_collector_as_fdcpa": "ANY_COLLECTOR_PROMOTED_TO_FDCPA_DEBT_COLLECTOR",
    "missing_receipt_as_legal_violation": "MISSING_RECEIPT_PROMOTED_TO_LEGAL_VIOLATION",
}


def combine(current: str, candidate: str) -> str:
    return candidate if TERMINAL_ORDER[candidate] > TERMINAL_ORDER[current] else current


def deep_merge(base, patch):
    if not isinstance(base, dict) or not isinstance(patch, dict):
        return copy.deepcopy(patch)
    out = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def verify(case: dict) -> dict:
    disposition = "PASS"
    reasons: list[str] = []
    signals: list[str] = []

    for flag, reason in PROMOTION_FLAGS.items():
        if case.get("attempted_promotions", {}).get(flag) is True:
            disposition = combine(disposition, "REJECT")
            reasons.append(reason)

    if case.get("records_conflict") is True:
        disposition = combine(disposition, "CONFLICT")
        reasons.append("BOUND_RECORDS_CONFLICT")

    family = case.get("trigger_family", "UNCLASSIFIED")
    rule = TRIGGER_RULES.get(family)
    burden_state = "TRIGGER_NOT_BOUND"

    if rule is None:
        disposition = combine(disposition, "HOLD")
        reasons.append("TRIGGER_FAMILY_UNCLASSIFIED")
    else:
        if case.get("actor_class") != rule["actor"]:
            disposition = combine(disposition, "HOLD")
            reasons.append(f"ACTOR_SCOPE_NOT_BOUND:{rule['actor']}")

        consumer = case.get("consumer_step", {})
        if consumer.get("performed") is not True or not consumer.get("receipt_ref"):
            disposition = combine(disposition, "HOLD")
            reasons.append("CONSUMER_TRIGGER_STEP_NOT_BOUND")

        trigger = case.get("trigger", {})
        if trigger.get("qualifying") is not True:
            disposition = combine(disposition, "HOLD")
            reasons.append("QUALIFYING_STATUTORY_TRIGGER_NOT_BOUND")
        else:
            burden_state = rule["burden_state"]
            signals.append(rule["signal"])

        if family == "FDCPA_WRITTEN_DISPUTE_30D" and trigger.get("timing_status") != "within_window":
            disposition = combine(disposition, "HOLD")
            reasons.append("FDCPA_1692G_B_30_DAY_WINDOW_NOT_BOUND")

        if family != "FDCPA_WRITTEN_DISPUTE_30D" and trigger.get("timing_status") == "unknown":
            disposition = combine(disposition, "HOLD")
            reasons.append("TRIGGER_TIMING_NOT_BOUND")

        if not trigger.get("condition_refs"):
            disposition = combine(disposition, "HOLD")
            reasons.append("TRIGGER_CONDITION_RECEIPTS_MISSING")

        duty = case.get("institution_duty", {})
        if duty.get("duty_type") != rule["duty"]:
            disposition = combine(disposition, "HOLD")
            reasons.append(f"EXPECTED_INSTITUTION_DUTY_NOT_BOUND:{rule['duty']}")

        if trigger.get("qualifying") is True:
            if duty.get("performed") is not True:
                disposition = combine(disposition, "HOLD")
                reasons.append("INSTITUTION_DUTY_PERFORMANCE_NOT_BOUND")
            if not duty.get("receipt_ref"):
                disposition = combine(disposition, "HOLD")
                reasons.append("INSTITUTION_DUTY_RECEIPT_MISSING")
            if duty.get("duty_quality") != "sufficient":
                disposition = combine(disposition, "HOLD")
                reasons.append(f"INSTITUTION_DUTY_QUALITY_NOT_PROVEN:{duty.get('duty_quality', 'missing')}")

            if (
                case.get("same_proof_requested_again") is True
                and consumer.get("performed") is True
                and (
                    duty.get("performed") is not True
                    or not duty.get("receipt_ref")
                    or duty.get("duty_quality") != "sufficient"
                )
            ):
                signals.append("RECURSIVE_BANKING_BURDEN_SIGNAL")
                disposition = combine(disposition, "HOLD")
                reasons.append("REPROOF_REQUEST_BEFORE_INSTITUTION_DUTY_RECONCILED")

    constitutional = case.get("constitutional", {})
    if constitutional.get("violation_claimed") is True:
        if constitutional.get("government_actor_bound") is not True and not constitutional.get("state_action_theory_ref"):
            disposition = combine(disposition, "HOLD")
            reasons.append("CONSTITUTIONAL_ATTRIBUTION_NOT_BOUND")
        else:
            disposition = combine(disposition, "HOLD")
            reasons.append("CONSTITUTIONAL_MERITS_OUTSIDE_BANKING_TRIGGER_VERIFIER")

    return {
        "case_id": case.get("case_id"),
        "trigger_family": family,
        "burden_state": burden_state,
        "disposition": disposition,
        "reasons": sorted(set(reasons)),
        "signals": sorted(set(signals)),
        "legal_violation_proven": False,
        "constitutional_violation_proven": False,
        "state_action_proven": False,
        "authority_created": False,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_banking_burden_flip_v0_1.py <vectors.json>")

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    base_case = payload.get("base_case", {})
    results = []
    failures = []

    for vector in payload["cases"]:
        case = deep_merge(base_case, vector.get("patch", {}))
        case["case_id"] = vector["case_id"]
        result = verify(case)
        results.append(result)
        if result["disposition"] != vector["expected_disposition"]:
            failures.append({
                "case_id": vector["case_id"],
                "expected": vector["expected_disposition"],
                "actual": result["disposition"],
                "reasons": result["reasons"],
            })

    print(json.dumps({"results": results, "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
