import hashlib
import json
from typing import Any, Dict


SPINE_VERSION = "v0.1"


def compute_exchange_digest(
    prompt: str,
    model_response: Dict[str, Any],
    spine_version: str = SPINE_VERSION,
) -> str:
    """Bind spine version and canonical exchange fields with SHA-256."""
    canonical = json.dumps(
        {
            "spine_version": spine_version,
            "prompt": prompt,
            "model_answer": model_response["answer"],
            "evidence_summary": model_response["evidence_summary"],
            "confidence": model_response["confidence"],
            "model_identity": model_response["model_id"],
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
