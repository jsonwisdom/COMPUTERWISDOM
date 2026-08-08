from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any, Dict

import jsonschema

from authorization.policy import (
    AUTH_POLICY_DIGEST,
    KNOWN_ROUTER_POLICY_DIGESTS,
    get_allowed_roles,
)
from authorization.signature import SignatureVerifier, VerificationResult

_ROOT = Path(__file__).resolve().parent
_ROUTING_SCHEMA = json.loads(
    (_ROOT / "schemas" / "routing_receipt_v439.schema.json").read_text(encoding="utf-8")
)
_ROUTING_VALIDATOR = jsonschema.Draft7Validator(_ROUTING_SCHEMA)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def verify_routing_receipt(receipt: Dict[str, Any]) -> bool:
    if not isinstance(receipt, dict) or not _ROUTING_VALIDATOR.is_valid(receipt):
        return False
    payload = {key: value for key, value in receipt.items() if key != "routing_digest"}
    recomputed = hashlib.sha256(_canonical_bytes(payload)).hexdigest()
    return hmac.compare_digest(receipt["routing_digest"], recomputed)


def verify_policy_agreement(receipt: Dict[str, Any], signer_role: str) -> bool:
    return (
        receipt.get("human_authorization_required") is True
        and signer_role in receipt.get("eligible_response_roles", [])
        and signer_role in get_allowed_roles(receipt.get("locality_scope", ""))
        and receipt.get("policy_digest") in KNOWN_ROUTER_POLICY_DIGESTS
    )


def generate_task_id(routing_receipt: Dict[str, Any]) -> str:
    if not verify_routing_receipt(routing_receipt):
        raise ValueError("cannot generate task ID from invalid routing receipt")
    return f"TASK-{routing_receipt['routing_digest'][:32].upper()}"


def authorization_intent_hash(
    routing_digest: str,
    signer_ens: str,
    signer_role: str,
    action_implementation_digest: str,
) -> bytes:
    intent = {
        "action_implementation_digest": action_implementation_digest,
        "authorization_policy_digest": AUTH_POLICY_DIGEST,
        "routing_receipt_digest": routing_digest,
        "signer_ens": signer_ens,
        "signer_role": signer_role,
    }
    return hashlib.sha256(_canonical_bytes(intent)).digest()


def verify_authorization(
    routing_receipt: Dict[str, Any],
    signer_ens: str,
    signer_role: str,
    action_implementation_digest: str,
    signature: bytes,
    sig_verifier: SignatureVerifier,
) -> VerificationResult:
    if not verify_routing_receipt(routing_receipt):
        return VerificationResult("INVALID", "ROUTING_RECEIPT_INVALID", False)
    if not verify_policy_agreement(routing_receipt, signer_role):
        return VerificationResult("INVALID", "POLICY_AGREEMENT_FAILED", False)
    if not isinstance(signer_ens, str) or not signer_ens or signer_ens != signer_ens.lower():
        return VerificationResult("INVALID", "SIGNER_ENS_INVALID", False)
    if (
        not isinstance(action_implementation_digest, str)
        or len(action_implementation_digest) != 64
        or any(ch not in "0123456789abcdef" for ch in action_implementation_digest)
    ):
        return VerificationResult("INVALID", "ACTION_IMPLEMENTATION_DIGEST_INVALID", False)
    message_hash = authorization_intent_hash(
        routing_receipt["routing_digest"],
        signer_ens,
        signer_role,
        action_implementation_digest,
    )
    return sig_verifier.verify(signer_ens, message_hash, signature)
