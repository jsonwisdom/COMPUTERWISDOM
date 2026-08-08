from __future__ import annotations

import hashlib
import math
from typing import Dict, List

DECOMPOSITION_VERSION = "DECOMPOSITION_V0_1"


def _work_order_id(claim_text: str, parent_id: str | None) -> str:
    material = f"{parent_id or ''}\0{claim_text}".encode("utf-8")
    return f"wo_{hashlib.sha256(material).hexdigest()[:16]}"


def decompose_claim(
    claim_text: str,
    parent_id: str | None = None,
    token_weight: float = 0.0,
) -> List[Dict]:
    """
    v0.1: Returns a single atomic, unverified work order.
    Future: LLM + rules decomposition with quadratic weight propagation.

    The token signal may route or prioritize work. It cannot alter verification
    status, acceptance criteria, evidence, or authority.
    """
    normalized_claim = claim_text.strip()
    if not normalized_claim:
        raise ValueError("claim_text must be non-empty")

    if not isinstance(token_weight, (int, float)) or isinstance(token_weight, bool):
        raise TypeError("token_weight must be a finite non-negative number")
    if not math.isfinite(float(token_weight)) or token_weight < 0:
        raise ValueError("token_weight must be a finite non-negative number")

    normalized_parent = parent_id.strip() if parent_id else None
    if parent_id is not None and not normalized_parent:
        raise ValueError("parent_id must be non-empty when provided")

    return [
        {
            "work_order_id": _work_order_id(normalized_claim, normalized_parent),
            "parent_id": normalized_parent,
            "claim_text": normalized_claim,
            "decomposition_version": DECOMPOSITION_VERSION,
            "verification_status": "UNVERIFIED",
            "assumptions": [],
            "evidence_requirements": [],
            "method": "PENDING",
            "acceptance_test": "PENDING",
            "hazards": [],
            "output_schema": "PENDING",
            "replay_requirement": "REQUIRED",
            "quadratic_weight": float(token_weight),
            "authority_created": False,
        }
    ]
