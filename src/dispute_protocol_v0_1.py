import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict

import jsonschema

SCHEMA_VERSION = "DISPUTE_V0_1"
CONSTITUTIONAL_ROOT = "808f2b1c6c339eb46e68a2161da3cca22f7b0eeb"
AUTHORITY = False
AUTHORITY_BOUNDARY = "NONE"


def load_json(path: str | Path) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_dispute(dispute: Dict[str, Any], schema: Dict[str, Any]) -> None:
    jsonschema.Draft202012Validator(schema).validate(dispute)
    if dispute["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if dispute["constitutional_root"] != CONSTITUTIONAL_ROOT:
        raise ValueError("constitutional_root mismatch")
    if dispute["authority"] is not AUTHORITY:
        raise ValueError("authority must be false")
    if dispute["authority_boundary"] != AUTHORITY_BOUNDARY:
        raise ValueError("authority_boundary must be NONE")
    if not dispute.get("target_artifact_id") and not dispute.get("target_trace_id"):
        raise ValueError("dispute requires target_artifact_id or target_trace_id")


def attach_dispute(target: Dict[str, Any], dispute: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    original_target = copy.deepcopy(target)
    validate_dispute(dispute, schema)
    envelope = {
        "target": copy.deepcopy(target),
        "dispute": copy.deepcopy(dispute),
        "attachment_type": "additive_reference",
        "authority": AUTHORITY,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    if target != original_target:
        raise ValueError("target mutation detected")
    return envelope
