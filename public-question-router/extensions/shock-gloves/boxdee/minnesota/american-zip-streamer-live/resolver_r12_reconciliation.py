"""R12 reconciliation predicate for AmericanZipStreamerLIVE.

PASS = applicable reconciliation receipt for the named conflict.
PASS does NOT establish external truth of new_state.
"""

PASS = "PASS"
FAIL = "FAIL"
HOLD = "HOLD"

def _shape_only(value):
    if isinstance(value, str):
        return value.startswith("SHAPE_ONLY") or value.startswith("fixture://shape/")
    if isinstance(value, list):
        return any(_shape_only(v) for v in value)
    if isinstance(value, dict):
        if value.get("shape_only") is True:
            return True
        if value.get("semantic_class") == "NON_SEMANTIC":
            return True
        if value.get("binding_class") == "SHAPE_ONLY":
            return True
        return any(_shape_only(v) for v in value.values())
    return False

def _result(status, reason, new_state=None):
    return {
        "status": status,
        "reason": reason,
        "new_state": new_state,
        "conflict_exit_allowed": status == PASS,
        "authority_created": False,
        "verdict_created": False,
        "external_truth_created": False,
        "append_only": True,
        "preserve_prior_states": True,
    }

def check_R12_RECONCILIATION_APPLICABILITY(inputs):
    if not isinstance(inputs, dict):
        return _result(HOLD, "inputs must be an object")

    conflict_id = inputs.get("conflict_id")
    receipt = inputs.get("reconciliation_receipt")
    bound_receipts = inputs.get("receipts")

    if not conflict_id:
        return _result(HOLD, "conflict_id is required")
    if receipt is None:
        return _result(HOLD, "reconciliation receipt absent")
    if _shape_only(receipt):
        return _result(HOLD, "SHAPE_ONLY/NON_SEMANTIC reconciliation cannot close conflict")
    if not isinstance(receipt, dict):
        return _result(HOLD, "reconciliation receipt must be an object")
    if receipt.get("receipt_type") != "general_reconciliation":
        return _result(HOLD, "receipt_type must be general_reconciliation")
    if receipt.get("resolves_conflict_id") != conflict_id:
        return _result(FAIL, "reconciliation receipt targets a different conflict")
    if "new_state" not in receipt:
        return _result(HOLD, "new_state is required")
    evidence = receipt.get("evidence_receipts")
    if not isinstance(evidence, list) or not evidence:
        return _result(HOLD, "evidence_receipts must be non-empty")
    if not receipt.get("issued_at"):
        return _result(HOLD, "issued_at is required")
    if not isinstance(bound_receipts, list) or receipt.get("receipt_id") not in bound_receipts:
        return _result(HOLD, "reconciliation receipt is not bound into resolver receipts")

    return _result(
        PASS,
        "reconciliation receipt is structurally applicable to the named conflict",
        new_state=receipt["new_state"],
    )
