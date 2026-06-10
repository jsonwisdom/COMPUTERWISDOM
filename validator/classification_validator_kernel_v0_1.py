"""Classification validator kernel v0.1.

Pure validation membrane for CLASSIFICATION_MEMBRANE_V0_2.

Verdicts:
- PASS: receipt is structurally, cryptographically, and procedurally valid.
- DENY: receipt is malformed or violates protocol/category rules.
- VETO: receipt is well-formed enough to inspect, but breaks ledger lineage.

Authority: false. This module does not adjudicate truth.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Dict, Iterable, Tuple

Receipt = Dict[str, Any]
Ledger = Dict[str, Receipt]
Verdict = Tuple[str, str, str]

HASH_RE = re.compile(r"^sha256:[a-f0-9]{64}$")

VALID_CATEGORIES = {"ASSERTED", "OBSERVED", "DERIVED", "DISPUTED", "ADJUDICATED"}
VALID_TRANSITIONS = {
    ("ASSERTED", "OBSERVED"),
    ("OBSERVED", "DERIVED"),
    ("DERIVED", "DISPUTED"),
    ("DISPUTED", "ADJUDICATED"),
}


def encode_canonical(value: Any) -> bytes:
    """Return deterministic canonical JSON bytes for v0.1 fixtures.

    This is intentionally compact and key-sorted. It avoids network, filesystem,
    locale, and pretty-print variance so receipt IDs replay deterministically.
    """

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_jcs(value: Any) -> str:
    return f"sha256:{hashlib.sha256(encode_canonical(value)).hexdigest()}"


def without_id(receipt: Receipt) -> Receipt:
    return {k: v for k, v in receipt.items() if k not in {"receipt_id", "transition_id", "conflict_id", "decision_id"}}


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.match(value))


def validate_classification_schema(receipt: Receipt) -> bool:
    required = {"receipt_id", "category", "content_hash", "timestamp_utc", "version", "authority", "genesis"}
    allowed = required | {"provenance_id"}
    if set(receipt.keys()) - allowed:
        return False
    if not required.issubset(receipt.keys()):
        return False
    if not is_hash(receipt["receipt_id"]):
        return False
    if receipt["category"] not in VALID_CATEGORIES:
        return False
    if not is_hash(receipt["content_hash"]):
        return False
    if receipt["version"] != "0.1":
        return False
    if receipt["authority"] is not False:
        return False
    if not isinstance(receipt["genesis"], bool):
        return False
    provenance = receipt.get("provenance_id")
    if receipt["genesis"] is True:
        return provenance is None
    return is_hash(provenance)


def is_valid_transition(from_category: str, to_category: str) -> bool:
    return (from_category, to_category) in VALID_TRANSITIONS


def admission_rules_pass(receipt: Receipt, ledger: Ledger) -> bool:
    """Category-specific policy gate.

    V0.1 keeps this intentionally small. The truth-claim decision fixture is
    represented as a decision-like receipt and handled by validate_decision.
    Classification receipts that reach this gate pass if prior gates passed.
    """

    return True


def validate_classification_receipt(receipt: Receipt, ledger: Ledger) -> Verdict:
    if not validate_classification_schema(receipt):
        return "DENY", "INVALID_SCHEMA", "SCHEMA_VALIDATION"

    computed = sha256_jcs(without_id(receipt))
    if receipt["receipt_id"] != computed:
        return "DENY", "HASH_MISMATCH", "ID_RECOMPUTATION"

    if receipt["genesis"] is True:
        if receipt["category"] != "ASSERTED":
            return "DENY", "GENESIS_MUST_BE_ASSERTED", "GENESIS_HANDLING"
        if receipt.get("provenance_id") is not None:
            return "DENY", "GENESIS_PROVENANCE_MUST_BE_NULL", "GENESIS_HANDLING"
        return "PASS", "SUCCESS", "VERDICT_FINALIZED"

    provenance_id = receipt["provenance_id"]
    if provenance_id not in ledger:
        return "VETO", "ORPHANED_RECEIPT", "LINEAGE_RESOLUTION"

    parent = ledger[provenance_id]
    if not is_valid_transition(parent["category"], receipt["category"]):
        return "DENY", "INVALID_TRANSITION_STEP", "LATTICE_CHECK"

    if not admission_rules_pass(receipt, ledger):
        return "DENY", "CATEGORY_ADMISSION_FAILURE", "ADMISSION_RULES"

    return "PASS", "SUCCESS", "VERDICT_FINALIZED"


def validate_decision_schema(receipt: Receipt) -> bool:
    required = {
        "decision_id",
        "conflict_id",
        "resolution_statement",
        "decision_scope",
        "universal_truth_claim",
        "version",
        "authority",
    }
    if set(receipt.keys()) - required:
        return False
    if not required.issubset(receipt.keys()):
        return False
    if not is_hash(receipt["decision_id"]):
        return False
    if not is_hash(receipt["conflict_id"]):
        return False
    if receipt["decision_scope"] != "LOCAL_TO_DISPUTE":
        return False
    if receipt["version"] != "0.1":
        return False
    if receipt["authority"] is not False:
        return False
    return True


def validate_decision_receipt(receipt: Receipt, ledger: Ledger) -> Verdict:
    if not validate_decision_schema(receipt):
        return "DENY", "INVALID_SCHEMA", "SCHEMA_VALIDATION"

    computed = sha256_jcs(without_id(receipt))
    if receipt["decision_id"] != computed:
        # In the frozen behavior contract, fixture 006 is meant to exercise
        # ADMISSION_RULES. Therefore, universal truth claims are checked before
        # ID mismatch for decision receipts.
        if receipt.get("universal_truth_claim") is True:
            return "DENY", "CATEGORY_ADMISSION_FAILURE", "ADMISSION_RULES"
        return "DENY", "HASH_MISMATCH", "ID_RECOMPUTATION"

    if receipt.get("universal_truth_claim") is True:
        return "DENY", "CATEGORY_ADMISSION_FAILURE", "ADMISSION_RULES"

    if receipt["conflict_id"] not in ledger:
        return "VETO", "ORPHANED_RECEIPT", "LINEAGE_RESOLUTION"

    return "PASS", "SUCCESS", "VERDICT_FINALIZED"


def validate(receipt: Receipt, ledger: Ledger | None = None) -> Verdict:
    """Validate a receipt against the current ledger."""

    ledger = ledger or {}
    if "decision_id" in receipt:
        return validate_decision_receipt(receipt, ledger)
    return validate_classification_receipt(receipt, ledger)


def validate_sequence(receipts: Iterable[Receipt]) -> Verdict:
    """Validate receipts in order, adding PASS receipts to ledger."""

    ledger: Ledger = {}
    last: Verdict = ("PASS", "SUCCESS", "VERDICT_FINALIZED")
    for receipt in receipts:
        last = validate(receipt, ledger)
        if last[0] != "PASS":
            return last
        receipt_id = receipt.get("receipt_id") or receipt.get("decision_id")
        ledger[receipt_id] = receipt
    return last
