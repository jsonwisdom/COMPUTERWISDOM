from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Iterable, Mapping, Optional, Sequence
import json


class Status(str, Enum):
    HOLD = "HOLD"
    BOUND = "BOUND"
    PROVEN = "PROVEN"
    CONFLICT = "CONFLICT"
    REJECT = "REJECT"


class ReplayIntegrity(str, Enum):
    HOLD = "HOLD"
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"


class BranchType(str, Enum):
    EXACT_REPLAY = "EXACT_REPLAY"
    PARAMETER_CHALLENGE = "PARAMETER_CHALLENGE"
    AUTHORITY_CHALLENGE = "AUTHORITY_CHALLENGE"
    COUNTER_RECEIPT = "COUNTER_RECEIPT"
    COUNTERFACTUAL_X = "COUNTERFACTUAL_X"
    STOCHASTIC_STRESS = "STOCHASTIC_STRESS"


QUARANTINED_BRANCHES = {
    BranchType.COUNTERFACTUAL_X,
    BranchType.STOCHASTIC_STRESS,
}


@dataclass(frozen=True)
class SourceAnchor:
    source_uri: str
    retrieved_at: str
    content_digest: str
    signature: Optional[str] = None
    signature_scheme: Optional[str] = None
    signature_verified: bool = False


@dataclass(frozen=True)
class ReceiptPayload:
    parent_run_id: str
    replay_id: str
    branch_type: BranchType
    original_inputs: Mapping[str, Any]
    challenged_input: Optional[Mapping[str, Any]]
    new_receipts: Sequence[Mapping[str, Any]]
    score_delta: Mapping[str, float]
    authority_delta: Mapping[str, Any]
    evidence_state_before: Status
    reason: str
    sealed_parent_hash: str
    timestamp: str
    source_anchors: Sequence[SourceAnchor] = field(default_factory=tuple)
    receipt_hash: str = ""


def _normalize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    return value


def canonical_json_bytes(value: Any) -> bytes:
    normalized = _normalize(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return sha256(value).hexdigest()


def receipt_body(receipt: ReceiptPayload) -> dict[str, Any]:
    body = asdict(receipt)
    body.pop("receipt_hash", None)
    return _normalize(body)


def compute_receipt_hash(receipt: ReceiptPayload) -> str:
    return sha256_hex(canonical_json_bytes(receipt_body(receipt)))


def seal_receipt(receipt: ReceiptPayload) -> ReceiptPayload:
    digest = compute_receipt_hash(receipt)
    return ReceiptPayload(**{**asdict(receipt), "receipt_hash": digest})


def verify_receipt_hash(receipt: ReceiptPayload) -> bool:
    return bool(receipt.receipt_hash) and receipt.receipt_hash == compute_receipt_hash(receipt)


def verify_parent_link(receipt: ReceiptPayload, known_parent_hash: str) -> bool:
    return receipt.sealed_parent_hash == known_parent_hash


def source_anchor_is_well_formed(anchor: SourceAnchor) -> bool:
    if not anchor.source_uri or not anchor.retrieved_at or not anchor.content_digest:
        return False
    if anchor.signature_verified:
        return bool(anchor.signature and anchor.signature_scheme)
    return True


def leaf_hash(receipt: ReceiptPayload) -> str:
    if not verify_receipt_hash(receipt):
        raise ValueError("receipt hash verification failed")
    return receipt.receipt_hash


def merkle_root_hex(leaves: Iterable[str]) -> str:
    level = list(leaves)
    if not level:
        return sha256_hex(b"")

    for item in level:
        if len(item) != 64:
            raise ValueError("Merkle leaves must be SHA-256 hex digests")
        bytes.fromhex(item)

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level: list[str] = []
        for index in range(0, len(level), 2):
            left = bytes.fromhex(level[index])
            right = bytes.fromhex(level[index + 1])
            next_level.append(sha256_hex(left + right))
        level = next_level
    return level[0]


def namespace_for(branch_type: BranchType) -> str:
    return "quarantine" if branch_type in QUARANTINED_BRANCHES else "evidence"


def exact_replay_result(
    *,
    current_evidence_state: Status,
    original_serialized: bytes,
    replayed_serialized: bytes,
) -> tuple[ReplayIntegrity, Status, str]:
    """Exact replay can prove reproducibility, never claim truth by itself."""
    if original_serialized == replayed_serialized:
        return (
            ReplayIntegrity.MATCH,
            current_evidence_state,
            "EXACT_REPLAY_MATCH_EVIDENCE_UNCHANGED",
        )
    return (
        ReplayIntegrity.MISMATCH,
        Status.CONFLICT if current_evidence_state != Status.REJECT else Status.REJECT,
        "EXACT_REPLAY_MISMATCH",
    )
