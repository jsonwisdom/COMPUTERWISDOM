#!/usr/bin/env python3
"""RePlay Genesis court adapter v0.1.

Scope:
- Public RECAP/CourtListener fetches.
- Deterministic court provenance receipts.
- RFC 8785-compatible canonicalization for the v0.1 no-float profile.
- EAS mapping dry-run only.

Non-goals:
- No PACER credential handling in this module.
- No EAS transaction signing or broadcasting.
- No legal/factual authority creation.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

ADAPTER_VERSION = "0.1"
CHAIN_ID = 8453
NETWORK = "base"
EAS_SCHEMA_UID = "0xc90097ca9f787edcc5fa2ce0920032abe4c4417cc8356198fa12d397c46a453c"
EAS_SCHEMA_STRING = (
    "bytes32 receiptHash,bytes32 lineageHash,bytes32 previousReceiptHash,"
    "bytes32 subjectHash,bytes32 sourceRefHash,uint64 createdAt,"
    "uint8 evidenceState,uint8 retrievalState"
)

EVIDENCE_STATE = {
    "UNRESOLVED": 0,
    "PARTIAL": 1,
    "MATCH": 2,
    "NOT_APPLICABLE": 3,
}
RETRIEVAL_STATE = {
    "COMPLETE": 0,
    "FAILED": 1,
    "AUTH_BLOCKED": 2,
    "BUDGET_EXHAUSTED": 3,
    "NOT_ATTEMPTED": 4,
}
ZERO_HASH = "0x" + ("0" * 64)
ZERO_SHA256 = "sha256:" + ("0" * 64)
MAX_SAFE_INTEGER = (1 << 53) - 1


class CanonicalizationError(ValueError):
    pass


def _validate_jcs_profile(value: Any) -> None:
    """Fail closed on values outside the v0.1 JCS profile.

    v0.1 intentionally prohibits floating-point numbers. Integers must fit
    I-JSON's exact IEEE-754 integer range. Lone UTF-16 surrogates are rejected.
    """
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, float):
        raise CanonicalizationError("floating-point values are prohibited")
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise CanonicalizationError("integer outside exact I-JSON range")
        return
    if isinstance(value, str):
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise CanonicalizationError("lone surrogate code point prohibited")
        return
    if isinstance(value, list):
        for item in value:
            _validate_jcs_profile(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("object keys must be strings")
            _validate_jcs_profile(key)
            _validate_jcs_profile(item)
        return
    raise CanonicalizationError(f"unsupported JSON value: {type(value).__name__}")


def _utf16_sort_key(value: str) -> bytes:
    return value.encode("utf-16-be")


def _jcs_render(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(_jcs_render(item) for item in value) + "]"
    if isinstance(value, dict):
        parts = []
        for key in sorted(value.keys(), key=_utf16_sort_key):
            parts.append(
                json.dumps(key, ensure_ascii=False, separators=(",", ":"))
                + ":"
                + _jcs_render(value[key])
            )
        return "{" + ",".join(parts) + "}"
    raise CanonicalizationError(f"unsupported JSON value: {type(value).__name__}")


def jcs_canonical_bytes(value: Any) -> bytes:
    _validate_jcs_profile(value)
    return _jcs_render(value).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jcs_sha256(value: Any) -> str:
    return sha256_hex(jcs_canonical_bytes(value))


def _parse_utc_seconds(value: str) -> int:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")
    return int(dt.timestamp())


@dataclass(frozen=True)
class FetchObservation:
    url: str
    body: bytes
    status_code: int
    content_type: str
    retrieved_at: str
    cost_billed_microusd: int = 0
    pacer_pages: Optional[int] = None


class RecapTransport:
    """Public RECAP/CourtListener transport. No authentication."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def fetch(self, url: str) -> FetchObservation:
        now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={"User-Agent": "RePlay-Genesis-Court-Adapter/0.1"},
            )
            body = response.content
            content_type = response.headers.get("Content-Type", "application/octet-stream")
            return FetchObservation(
                url=url,
                body=body,
                status_code=response.status_code,
                content_type=content_type,
                retrieved_at=now,
            )
        except requests.RequestException as exc:
            body = f"{type(exc).__name__}: {exc}\n".encode("utf-8")
            return FetchObservation(
                url=url,
                body=body,
                status_code=0,
                content_type="text/plain",
                retrieved_at=now,
            )


def build_receipt_core(
    observation: FetchObservation,
    *,
    receipt_id: str,
    lineage_id: str,
    cell: str,
    jurisdiction: str,
    case_ref: str,
    official_ref: str,
    prev_receipt_hash: str = ZERO_SHA256,
    docket_entry: Optional[int] = None,
    genesis_key: Optional[str] = None,
) -> Dict[str, Any]:
    complete = 200 <= observation.status_code < 300
    retrieval_state = "COMPLETE" if complete else "FAILED"
    evidence_state = "UNRESOLVED"

    content_scope = "RETRIEVED_SOURCE_BYTES" if complete else "RETRIEVAL_ARTIFACT_NOT_COURT_DOCUMENT"

    core: Dict[str, Any] = {
        "receipt_version": "0.1",
        "receipt_id": receipt_id,
        "schema": "replay.court.provenance.v0.1",
        "created_at": observation.retrieved_at,
        "created_by": "replay.court.adapter.recap",
        "lineage_id": lineage_id,
        "subject": {
            "cell": cell,
            "jurisdiction": jurisdiction,
            "genesis_key": genesis_key,
            "case_ref": case_ref,
            "docket_entry": docket_entry,
        },
        "evidence_state": evidence_state,
        "retrieval_state": retrieval_state,
        "authority_chain": {
            "primary": "PACER_CMECF",
            "index_used": "RECAP_COURTLISTENER",
            "enrichment_used": None,
            "secondary_summary": False,
        },
        "provenance": {
            "official_ref": official_ref,
            "source_url": observation.url,
            "content_hash": "sha256:" + sha256_hex(observation.body),
            "content_hash_scope": content_scope,
            "content_length": len(observation.body),
            "mime_type": observation.content_type,
            "retrieval_timestamp": observation.retrieved_at,
            "cost_billed_microusd": observation.cost_billed_microusd,
            "currency": "USD",
            "pacer_pages": observation.pacer_pages,
        },
        "auth_context": {
            "credential_event_receipt": None,
            "account_type": "public_recap",
            "mfa_used": False,
            "environment": "public",
        },
        "integrity": {
            "prev_receipt_hash": prev_receipt_hash,
            "self_hash": None,
        },
        "authority": False,
    }

    if not complete:
        core["failure"] = {
            "http_status": observation.status_code,
            "category": "SOURCE_FETCH_FAILED" if observation.status_code == 0 else "SOURCE_FETCH_NON_SUCCESS",
            "retryable": observation.status_code in {0, 408, 425, 429, 500, 502, 503, 504},
        }

    hash_payload = copy.deepcopy(core)
    del hash_payload["integrity"]["self_hash"]
    core["integrity"]["self_hash"] = "sha256:" + jcs_sha256(hash_payload)
    return core


def validate_receipt_core(core: Dict[str, Any]) -> None:
    if core.get("authority") is not False:
        raise ValueError("authority must be false")
    if core.get("evidence_state") not in EVIDENCE_STATE:
        raise ValueError("unknown evidence_state")
    if core.get("retrieval_state") not in RETRIEVAL_STATE:
        raise ValueError("unknown retrieval_state")

    integrity = core.get("integrity") or {}
    self_hash = integrity.get("self_hash")
    if not isinstance(self_hash, str) or not self_hash.startswith("sha256:"):
        raise ValueError("self_hash missing or malformed")

    payload = copy.deepcopy(core)
    del payload["integrity"]["self_hash"]
    expected = "sha256:" + jcs_sha256(payload)
    if self_hash != expected:
        raise ValueError("self_hash mismatch")

    forbidden_fragments = ("password", "secret", "token", "otp")
    for key in _walk_keys(core):
        low = key.lower()
        if any(fragment in low for fragment in forbidden_fragments):
            if key != "credential_event_receipt":
                raise ValueError(f"secret-like field name prohibited: {key}")


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item)


def build_eas_dry_run(core: Dict[str, Any]) -> Dict[str, Any]:
    validate_receipt_core(core)

    receipt_hash = core["integrity"]["self_hash"].removeprefix("sha256:")
    prev_hash = core["integrity"]["prev_receipt_hash"].removeprefix("sha256:")

    mapping = {
        "receiptHash": "0x" + receipt_hash,
        "lineageHash": "0x" + jcs_sha256({"lineage_id": core["lineage_id"]}),
        "previousReceiptHash": "0x" + prev_hash,
        "subjectHash": "0x" + jcs_sha256(core["subject"]),
        "sourceRefHash": "0x" + jcs_sha256(
            {
                "authority_chain": core["authority_chain"],
                "official_ref": core["provenance"]["official_ref"],
            }
        ),
        "createdAt": _parse_utc_seconds(core["created_at"]),
        "evidenceState": EVIDENCE_STATE[core["evidence_state"]],
        "retrievalState": RETRIEVAL_STATE[core["retrieval_state"]],
    }

    for name in (
        "receiptHash",
        "lineageHash",
        "previousReceiptHash",
        "subjectHash",
        "sourceRefHash",
    ):
        if not isinstance(mapping[name], str) or not mapping[name].startswith("0x") or len(mapping[name]) != 66:
            raise ValueError(f"{name} must be bytes32")

    return {
        "dry_run_version": "0.1",
        "network": NETWORK,
        "chain_id": CHAIN_ID,
        "schema_uid": EAS_SCHEMA_UID,
        "schema_string": EAS_SCHEMA_STRING,
        "mapping": mapping,
        "validation": {
            "jcs_profile_valid": True,
            "self_hash_valid": True,
            "lineage_valid": True,
            "state_enum_valid": True,
            "secret_fields_present": False,
            "pii_onchain": False,
            "authority": False,
        },
        "transaction_submitted": False,
        "attestation_uid": None,
        "status": "DRY_RUN_VALIDATED",
    }


def build_pending_seal_envelope(core: Dict[str, Any], dry_run: Dict[str, Any]) -> Dict[str, Any]:
    if dry_run.get("status") != "DRY_RUN_VALIDATED":
        raise ValueError("dry run must validate before creating pending envelope")
    return {
        "seal_version": "0.1",
        "receipt_hash": core["integrity"]["self_hash"],
        "method": "EAS",
        "network": NETWORK,
        "chain_id": CHAIN_ID,
        "schema_uid": EAS_SCHEMA_UID,
        "attestation_uid": None,
        "attester": None,
        "transaction_hash": None,
        "block_number": None,
        "sealed_at": None,
        "status": "PENDING",
        "dry_run_validated": True,
        "authority": False,
    }
