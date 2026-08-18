"""Enterprise Receipt API v0.2 authorized-attestation verifier.

This module verifies deterministic receipt identity, Ed25519 signature validity,
and tenant/key authorization at the historical signing time.

It deliberately does not create replay dispositions or institutional authority.
"""

from __future__ import annotations

import base64
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Set

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ALGORITHM = "Ed25519"
HASH_PREFIX = "sha256:"
ALLOWED_RECEIPT_PAYLOAD_FIELDS: Set[str] = {
    "case_id",
    "request_hash",
    "replay_graph_hash",
    "evidence_hash",
    "ruleset_hash",
    "ruleset_version",
    "disposition",
}
ALLOWED_DISPOSITIONS = {"PASS", "HOLD", "CONFLICT", "REJECT"}
ALLOWED_SIGNER_ROLES = {
    "REPLAY_SERVICE",
    "TENANT_SERVICE",
    "AUDIT_SERVICE",
    "ROTATION_SERVICE",
}


def jcs(value: Any) -> bytes:
    return rfc8785.dumps(value)


def sha256_id(payload: bytes) -> str:
    return HASH_PREFIX + hashlib.sha256(payload).hexdigest()


def raw_digest_from_sha256_id(value: str) -> bytes:
    if not isinstance(value, str) or not value.startswith(HASH_PREFIX):
        raise ValueError("not a sha256 identifier")
    hex_part = value[len(HASH_PREFIX):]
    if len(hex_part) != 64:
        raise ValueError("sha256 identifier must contain 32 bytes")
    return bytes.fromhex(hex_part)


def compute_receipt_id(receipt_payload: Dict[str, Any]) -> str:
    return sha256_id(jcs(receipt_payload))


def compute_public_key_fingerprint(public_key_raw: bytes) -> str:
    return sha256_id(public_key_raw)


def compute_key_event_id(event: Dict[str, Any]) -> str:
    payload = {key: value for key, value in event.items() if key != "key_event_id"}
    return sha256_id(jcs(payload))


def compute_signing_event_id(
    receipt_id: str,
    key_id: str,
    signed_at: str,
    signature_b64: str,
) -> str:
    event_payload = {
        "receipt_id": receipt_id,
        "key_id": key_id,
        "signed_at": signed_at,
        "signature": signature_b64,
    }
    return sha256_id(jcs(event_payload))


def parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def key_state_at(key_record: Dict[str, Any], signed_at: str) -> Dict[str, Any]:
    target = parse_time(signed_at)
    registered = False
    tenant_id = None
    roles: Set[str] = set()
    active = False
    revoked = False
    expired = False
    suspended = False
    rotated = False

    events = sorted(key_record.get("events", []), key=lambda event: parse_time(event["at"]))
    for event in events:
        if parse_time(event["at"]) > target:
            break
        event_type = event.get("type")
        if event_type == "KEY_REGISTERED":
            registered = True
        elif event_type == "TENANT_BOUND":
            tenant_id = event.get("tenant_id")
        elif event_type == "ROLE_GRANTED":
            role = event.get("role")
            if role:
                roles.add(role)
        elif event_type == "ROLE_REVOKED":
            role = event.get("role")
            if role:
                roles.discard(role)
        elif event_type == "ACTIVE":
            active = True
            suspended = False
        elif event_type == "SUSPENDED":
            active = False
            suspended = True
        elif event_type == "REVOKED":
            active = False
            revoked = True
        elif event_type == "EXPIRED":
            active = False
            expired = True
        elif event_type == "ROTATED":
            active = False
            rotated = True

    return {
        "registered": registered,
        "tenant_id": tenant_id,
        "roles": roles,
        "active": active,
        "revoked": revoked,
        "expired": expired,
        "suspended": suspended,
        "rotated": rotated,
    }


def _append(signals: List[str], signal: str) -> None:
    if signal not in signals:
        signals.append(signal)


def verify_signed_receipt(
    signed_receipt: Dict[str, Any],
    key_registry: Dict[str, Any],
    expected_tenant_id: str,
) -> Dict[str, Any]:
    signals: List[str] = []

    payload = signed_receipt.get("receipt_payload")
    if not isinstance(payload, dict):
        return {
            "authorized_attestation": False,
            "disposition": "REJECT",
            "signals": ["RECEIPT_PAYLOAD_MISSING"],
            "authority_created": False,
        }

    if set(payload.keys()) != ALLOWED_RECEIPT_PAYLOAD_FIELDS:
        _append(signals, "RECEIPT_PAYLOAD_FIELDS_INVALID")

    if payload.get("disposition") not in ALLOWED_DISPOSITIONS:
        _append(signals, "RECEIPT_DISPOSITION_INVALID")

    computed_receipt_id = compute_receipt_id(payload)
    receipt_id = signed_receipt.get("receipt_id")
    if receipt_id != computed_receipt_id:
        _append(signals, "RECEIPT_ID_MISMATCH")

    bundle = signed_receipt.get("signature_bundle")
    if not isinstance(bundle, dict):
        _append(signals, "SIGNATURE_BUNDLE_MISSING")
        return {
            "authorized_attestation": False,
            "disposition": "REJECT",
            "signals": signals,
            "computed_receipt_id": computed_receipt_id,
            "authority_created": False,
        }

    if bundle.get("algorithm") != ALGORITHM:
        _append(signals, "ALGORITHM_NOT_ALLOWED")

    if bundle.get("payload_hash") != computed_receipt_id:
        _append(signals, "PAYLOAD_HASH_MISMATCH")

    key_id = bundle.get("key_id")
    key_record = key_registry.get("keys", {}).get(key_id)
    if not key_record:
        _append(signals, "KEY_ID_UNREGISTERED")
        return {
            "authorized_attestation": False,
            "disposition": "REJECT",
            "signals": signals,
            "computed_receipt_id": computed_receipt_id,
            "authority_created": False,
        }

    try:
        signed_at = bundle["signed_at"]
        state = key_state_at(key_record, signed_at)
    except (KeyError, ValueError, TypeError):
        _append(signals, "SIGNED_AT_INVALID")
        return {
            "authorized_attestation": False,
            "disposition": "REJECT",
            "signals": signals,
            "computed_receipt_id": computed_receipt_id,
            "authority_created": False,
        }

    for index, event in enumerate(key_record.get("events", [])):
        if event.get("key_event_id") != compute_key_event_id(event):
            _append(signals, f"KEY_EVENT_ID_MISMATCH:{index}")

    if not state["registered"]:
        _append(signals, "KEY_NOT_REGISTERED_AT_SIGNING_EVENT")

    if state["tenant_id"] != expected_tenant_id:
        _append(signals, "TENANT_MISMATCH")

    signer_role = bundle.get("signer_role")
    if signer_role not in ALLOWED_SIGNER_ROLES or signer_role not in state["roles"]:
        _append(signals, "SIGNER_ROLE_NOT_ALLOWED")

    if not state["active"]:
        _append(signals, "KEY_NOT_ACTIVE_AT_SIGNING_EVENT")
    if state["revoked"]:
        _append(signals, "KEY_REVOKED_FOR_EVENT_SCOPE")
    if state["expired"]:
        _append(signals, "KEY_EXPIRED_FOR_EVENT_SCOPE")
    if state["suspended"]:
        _append(signals, "KEY_SUSPENDED_FOR_EVENT_SCOPE")
    if state["rotated"]:
        _append(signals, "KEY_ROTATED_FOR_EVENT_SCOPE")

    try:
        public_key_raw = base64.b64decode(key_record["public_key_base64"], validate=True)
    except Exception:
        public_key_raw = b""
        _append(signals, "PUBLIC_KEY_ENCODING_INVALID")

    computed_fingerprint = compute_public_key_fingerprint(public_key_raw)
    if key_record.get("public_key_fingerprint") != computed_fingerprint:
        _append(signals, "REGISTRY_FINGERPRINT_MISMATCH")
    if bundle.get("public_key_fingerprint") != computed_fingerprint:
        _append(signals, "PUBLIC_KEY_FINGERPRINT_MISMATCH")

    signature_b64 = bundle.get("signature")
    try:
        signature = base64.b64decode(signature_b64, validate=True)
        digest = raw_digest_from_sha256_id(computed_receipt_id)
        public_key = Ed25519PublicKey.from_public_bytes(public_key_raw)
        public_key.verify(signature, digest)
    except (InvalidSignature, ValueError, TypeError):
        _append(signals, "SIGNATURE_INVALID")

    expected_signing_event_id = compute_signing_event_id(
        computed_receipt_id,
        str(key_id),
        signed_at,
        str(signature_b64),
    )
    if bundle.get("signing_event_id") != expected_signing_event_id:
        _append(signals, "SIGNING_EVENT_ID_MISMATCH")

    authorized = not signals
    return {
        "authorized_attestation": authorized,
        "disposition": "PASS" if authorized else "REJECT",
        "signals": signals,
        "computed_receipt_id": computed_receipt_id,
        "computed_signing_event_id": expected_signing_event_id,
        "authority_created": False,
    }
