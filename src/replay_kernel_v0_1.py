import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import jsonschema

KERNEL_VERSION = "REPLAY_KERNEL_V0_1"
TRACE_SCHEMA_VERSION = "REPLAY_TRACE_V0_1"
ERS_SCHEMA_VERSION = "ERS_V0_1"
CONSTITUTIONAL_ROOT = "808f2b1c6c339eb46e68a2161da3cca22f7b0eeb"
AUTHORITY = False
AUTHORITY_BOUNDARY = "NONE"

REPLAY_FIELDS = (
    "artifact_id",
    "artifact_type",
    "timestamp",
    "lineage_root",
    "constitutional_root",
    "schema_version",
    "hash",
    "authority",
    "authority_boundary",
)


def load_json(path: str | Path) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_ers_artifact(artifact: Dict[str, Any], schema: Dict[str, Any]) -> None:
    jsonschema.Draft202012Validator(schema).validate(artifact)
    if artifact["schema_version"] != ERS_SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if artifact["constitutional_root"] != CONSTITUTIONAL_ROOT:
        raise ValueError("constitutional_root mismatch")
    if artifact["authority"] is not AUTHORITY:
        raise ValueError("authority must be false")
    if artifact["authority_boundary"] != AUTHORITY_BOUNDARY:
        raise ValueError("authority_boundary must be NONE")


def replay(artifacts: Iterable[Dict[str, Any]], ers_schema: Dict[str, Any]) -> Dict[str, Any]:
    valid: List[Dict[str, Any]] = []
    for artifact in artifacts:
        validate_ers_artifact(artifact, ers_schema)
        valid.append({field: artifact[field] for field in REPLAY_FIELDS})

    ordered = sorted(valid, key=lambda item: (item["timestamp"], item["artifact_id"], item["hash"]))
    ordered_ids = [item["artifact_id"] for item in ordered]
    lineage_edges = [
        {"artifact_id": item["artifact_id"], "lineage_root": item["lineage_root"]}
        for item in ordered
    ]

    lineage_root = ordered[0]["lineage_root"] if ordered else "EMPTY"
    replay_core = {
        "kernel_version": KERNEL_VERSION,
        "constitutional_root": CONSTITUTIONAL_ROOT,
        "lineage_root": lineage_root,
        "artifact_count": len(ordered),
        "ordered_artifact_ids": ordered_ids,
        "lineage_edges": lineage_edges,
    }

    replay_hash = sha256_text(canonical_json(replay_core))
    trace_id = sha256_text(canonical_json({"replay_hash": replay_hash, "kernel_version": KERNEL_VERSION}))

    return {
        "trace_id": trace_id,
        "schema_version": TRACE_SCHEMA_VERSION,
        "kernel_version": KERNEL_VERSION,
        "constitutional_root": CONSTITUTIONAL_ROOT,
        "lineage_root": lineage_root,
        "artifact_count": len(ordered),
        "ordered_artifact_ids": ordered_ids,
        "lineage_edges": lineage_edges,
        "replay_hash": replay_hash,
        "authority": AUTHORITY,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
