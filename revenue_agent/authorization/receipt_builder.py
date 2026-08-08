from __future__ import annotations

import hashlib
import hmac
import json
import re
from typing import Any, Dict

from authorization.policy import AUTH_POLICY_DIGEST
from authorization.signature import VerificationResult

_ISO8601_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}([.][0-9]+)?Z$"
)
_DIGEST_RE = re.compile(r"^[a-f0-9]{64}$")
_TASK_ID_RE = re.compile(r"^TASK-[A-F0-9]{32}$")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def build_authorization_receipt(
    task_id: str,
    signer_ens: str,
    signer_role: str,
    routing_receipt_digest: str,
    sig_result: VerificationResult,
    action_implementation_digest: str,
    canonical_timestamp: str,
) -> Dict[str, Any]:
    if not _TASK_ID_RE.fullmatch(task_id):
        raise ValueError("invalid task_id")
    if not _DIGEST_RE.fullmatch(routing_receipt_digest):
        raise ValueError("invalid routing receipt digest")
    if not _DIGEST_RE.fullmatch(action_implementation_digest):
        raise ValueError("invalid action implementation digest")
    if not _ISO8601_RE.fullmatch(canonical_timestamp):
        raise ValueError("canonical_timestamp must be ISO8601 UTC")
    receipt = {
        "task_id": task_id,
        "signer_ens": signer_ens,
        "signer_role": signer_role,
        "routing_receipt_digest": routing_receipt_digest,
        "authorization_policy_digest": AUTH_POLICY_DIGEST,
        "signature_verification_status": sig_result.status,
        "signature_verification_reason": sig_result.reason,
        "action_implementation_digest": action_implementation_digest,
        "canonical_timestamp": canonical_timestamp,
        "action_authorized": False,
        "authority_created": False,
    }
    receipt["receipt_digest"] = hashlib.sha256(_canonical_bytes(receipt)).hexdigest()
    return receipt


def verify_authorization_receipt(receipt: Dict[str, Any]) -> bool:
    if not isinstance(receipt, dict) or not _DIGEST_RE.fullmatch(
        str(receipt.get("receipt_digest", ""))
    ):
        return False
    payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
    recomputed = hashlib.sha256(_canonical_bytes(payload)).hexdigest()
    return hmac.compare_digest(receipt["receipt_digest"], recomputed)
