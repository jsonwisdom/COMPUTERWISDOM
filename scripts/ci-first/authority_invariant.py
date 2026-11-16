#!/usr/bin/env python3
"""CI-FIRST v2 source-only invariant verification. Not an authority mechanism."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

STATES = ("PASS", "FAIL", "UNKNOWN", "HOLD")
EXPECTED_CONFIGS = 1024


def valid(evidence: object, human_approved: object, signed_authorization: object) -> bool:
    """Reject anything but precisely four known states and literal booleans."""
    return (
        type(evidence) in (tuple, list)
        and len(evidence) == 4
        and all(type(s) is str and s in STATES for s in evidence)
        and type(human_approved) is bool
        and type(signed_authorization) is bool
    )


def eligible(evidence: object, human_approved: object, signed_authorization: object) -> bool:
    """Eligibility, not authority. Malformed input is ineligible."""
    if not valid(evidence, human_approved, signed_authorization):
        return False
    return all(s == "PASS" for s in evidence) and human_approved and signed_authorization


def classify(evidence: object, human_approved: object, signed_authorization: object) -> str:
    """Report observed FAIL ahead of UNKNOWN; unfinished authorization is HOLD."""
    if not valid(evidence, human_approved, signed_authorization):
        return "FAIL"  # schema violation, irrespective of apparent evidence
    if "FAIL" in evidence:
        return "FAIL"
    if "UNKNOWN" in evidence:
        return "UNKNOWN"
    if "HOLD" in evidence or not human_approved or not signed_authorization:
        return "HOLD"
    return "PASS"  # model evaluation ONLY, never grants deployment/financial authority


def broken_unsigned_model(evidence: object, human_approved: object, signed_authorization: object) -> bool:
    """Negative control deliberately ignores signed authorization."""
    if not valid(evidence, human_approved, signed_authorization):
        return False
    return all(s == "PASS" for s in evidence) and human_approved


def broken_schema_model(evidence: object, human_approved: object, signed_authorization: object) -> bool:
    """Negative control deliberately omits strict schema validation."""
    try:
        return all(s == "PASS" for s in evidence) and bool(human_approved) and bool(signed_authorization)
    except TypeError:
        return False


def cases():
    for evidence in itertools.product(STATES, repeat=4):
        for h, signed in itertools.product((False, True), repeat=2):
            yield evidence, h, signed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="authority-model-receipt-v2.json")
    args = parser.parse_args()
    configs = list(cases())
    eligible_count = unauthorized = classification_errors = 0
    signed_negative_leaks = 0
    for e, h, s in configs:
        value = eligible(e, h, s)
        eligible_count += int(value)
        unauthorized += int(value and (not h or not s or any(x != "PASS" for x in e)))
        classification_errors += int((classify(e, h, s) == "PASS") != value)
        signed_negative_leaks += int(broken_unsigned_model(e, h, s) and not s)

    # Test malformed evidence and authorization types, including truthy "False".
    malformed = [
        ((), True, True),
        ([], True, True),
        (("PASS",) * 3, True, True),
        (("PASS",) * 5, True, True),
        (("PASS", "PASS", "PASS", "BOGUS"), True, True),
        ("PASS", True, True),
        (None, True, True),
        (("PASS",) * 4, "False", True),
        (("PASS",) * 4, True, "False"),
        (("PASS",) * 4, 1, True),
        (("PASS",) * 4, True, 1),
        (("PASS",) * 4, None, True),
        (("PASS",) * 4, True, None),
        (("PASS",) * 4, [], True),
        (("PASS",) * 4, True, {}),
        (("PASS", "PASS", "PASS", None), True, True),
        (("PASS",) * 4, "True", "True"),
    ]
    malformed_blocked = sum(not eligible(*x) and classify(*x) == "FAIL" for x in malformed)
    schema_negative_leaks = sum(broken_schema_model(*x) for x in malformed)
    fixtures = {
        "pr752_live_unknown": classify(("PASS", "PASS", "PASS", "UNKNOWN"), False, False),
        "issue760_original_bytes_unknown": classify(("PASS", "PASS", "UNKNOWN", "UNKNOWN"), False, False),
        "citizen_root_preflight_fail": classify(("PASS", "FAIL", "UNKNOWN", "UNKNOWN"), False, False),
        "human_gate_closed": classify(("PASS",) * 4, False, True),
        "signing_gate_closed": classify(("PASS",) * 4, True, False),
        "all_model_gates_pass": classify(("PASS",) * 4, True, True),
    }
    success = (
        len(configs) == EXPECTED_CONFIGS
        and eligible_count == 1
        and unauthorized == 0
        and classification_errors == 0
        and signed_negative_leaks == 1
        and malformed_blocked == len(malformed)
        and schema_negative_leaks >= 1
        and fixtures == {
            "pr752_live_unknown": "UNKNOWN",
            "issue760_original_bytes_unknown": "UNKNOWN",
            "citizen_root_preflight_fail": "FAIL",
            "human_gate_closed": "HOLD",
            "signing_gate_closed": "HOLD",
            "all_model_gates_pass": "PASS",
        }
    )
    receipt = {
        "schema": "computerwisdom.ci-first.authority-model.v2",
        "result": "PASS" if success else "FAIL",
        "scope": "synthetic-source-only",
        "configurations": len(configs),
        "eligible_configurations": eligible_count,
        "unauthorized_eligibility": unauthorized,
        "classification_errors": classification_errors,
        "strict_input_validation": {
            "malformed_cases": len(malformed),
            "blocked": malformed_blocked,
            "result": "PASS" if malformed_blocked == len(malformed) else "FAIL",
        },
        "negative_controls": {
            "missing_signature_leaks": signed_negative_leaks,
            "missing_schema_leaks": schema_negative_leaks,
            "detected": signed_negative_leaks == 1 and schema_negative_leaks >= 1,
        },
        "fixture_classifications": fixtures,
        "authority_created": False,
        "github_actions_run": "NOT_PERFORMED",
        "required_branch_check": "NOT_CONFIGURED_BY_PACKAGE",
        "production_enforcement": "UNKNOWN",
        "wallet_signing_authority": "UNKNOWN",
        "production_checkout": "NOT_ESTABLISHED",
        "independent_wolfram": "SEPARATE_VERIFICATION_REQUIRED",
        "ci_only": True,
    }
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
