"""Hash-linked append-only receipt ledger for ResumeReplay v0.1."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ReceiptError(ValueError):
    """Raised when a receipt cannot be appended without breaking the membrane."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    if isinstance(value, bytes):
        payload = value
    elif isinstance(value, str):
        payload = value.encode("utf-8")
    else:
        payload = canonical_json_bytes(value)
    return hashlib.sha256(payload).hexdigest()


def _last_receipt_hash(ledger_path: Path) -> str | None:
    if not ledger_path.exists():
        return None

    last_line: bytes | None = None
    with ledger_path.open("rb") as handle:
        for line in handle:
            if line.strip():
                last_line = line.rstrip(b"\n")

    if last_line is None:
        return None

    try:
        parsed = json.loads(last_line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReceiptError("ledger tail is not valid UTF-8 JSON") from exc

    return sha256_hex(parsed)


def _observer_reason(observer_result: dict[str, Any]) -> str:
    reason = observer_result.get("reason")
    if reason is None:
        reasons = observer_result.get("reasons")
        if isinstance(reasons, list) and reasons:
            return "; ".join(str(item) for item in reasons)
        return "PASS"
    return str(reason)


def append_receipt(
    *,
    raw_input: dict[str, Any],
    normalized: dict[str, Any],
    observer_result: dict[str, Any],
    resume_language: dict[str, Any] | str,
    ledger_path: str | os.PathLike[str],
    timestamp: str | None = None,
    receipt_id: str | None = None,
) -> dict[str, Any]:
    """Append one immutable receipt to a JSONL hash chain.

    This function records finalized upstream outputs. It MUST NOT:
    - change evidence_state
    - upgrade observer verdicts
    - create authority/employment/production claims
    - rewrite or delete prior ledger rows
    """
    if not isinstance(raw_input, dict) or not isinstance(normalized, dict):
        raise ReceiptError("raw_input and normalized must be objects")
    if not isinstance(observer_result, dict):
        raise ReceiptError("observer_result must be an object")

    evidence_state = observer_result.get("observer_result")
    verdict = observer_result.get("verdict")
    if not isinstance(evidence_state, str) or not evidence_state:
        raise ReceiptError("observer_result.observer_result is required")
    if not isinstance(verdict, str) or not verdict:
        raise ReceiptError("observer_result.verdict is required")

    # Read-only membrane outputs from Gray Baby.
    authority_claim = bool(observer_result.get("authority_created", False))
    employment_claim = bool(observer_result.get("employment_created", False))
    production_claim = bool(
        observer_result.get("production_proof_created", False)
    )
    if authority_claim:
        raise ReceiptError("authority claim cannot be appended")
    if employment_claim:
        raise ReceiptError("employment claim cannot be appended")

    if timestamp is None:
        timestamp = (
            datetime.now(timezone.utc)
            .isoformat(timespec="microseconds")
            .replace("+00:00", "Z")
        )

    ledger = Path(ledger_path)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    prior_receipt_hash = _last_receipt_hash(ledger)

    if receipt_id is None:
        identity_material = {
            "source_hash": sha256_hex(raw_input),
            "normalized_object_hash": sha256_hex(normalized),
            "observer_result": evidence_state,
            "observer_verdict": verdict,
            "timestamp": timestamp,
            "prior_receipt_hash": prior_receipt_hash,
        }
        receipt_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                sha256_hex(identity_material),
            )
        )

    receipt = {
        "receipt_id": receipt_id,
        "source_hash": sha256_hex(raw_input),
        "source_type": normalized.get("source_type"),
        "normalized_object_hash": sha256_hex(normalized),
        "evidence_state": evidence_state,
        "observer_verdict": verdict,
        "observer_reason": _observer_reason(observer_result),
        "rendered_language_hash": sha256_hex(resume_language),
        "timestamp": timestamp,
        "prior_receipt_hash": prior_receipt_hash,
        "authority_claim": False,
        "employment_claim": False,
        "production_proof_claim": production_claim,
    }

    encoded = canonical_json_bytes(receipt) + b"\n"

    # O_APPEND ensures this function never seeks backward to replace prior rows.
    fd = os.open(
        ledger,
        os.O_WRONLY | os.O_CREAT | os.O_APPEND,
        0o600,
    )
    try:
        with os.fdopen(fd, "ab", closefd=True) as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise

    return receipt
