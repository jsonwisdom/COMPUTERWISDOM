"""Explicit replay registry v0.2.

Schema version, canonical version, serializer version, and hash algorithm are
separate axes. No replay-critical value is inferred from another axis.

This module grants no authority and makes no truth claim. It only defines a
deterministic canonicalization contract for supported artifact schemas.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Callable, Dict, Mapping

REGISTRY_VERSION = "REPLAY_REGISTRY_V0_2"
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


def canonicalize_ers_v0_1(record: Mapping[str, Any]) -> Dict[str, Any]:
    """Return only the replay-critical ERS_V0_1 fields in fixed field scope."""
    missing = [field for field in REPLAY_FIELDS if field not in record]
    if missing:
        raise ValueError(f"missing replay fields: {','.join(missing)}")
    return {field: record[field] for field in REPLAY_FIELDS}


def serialize_json_sorted_compact_utf8_v1_0(value: Any) -> bytes:
    """Deterministic UTF-8 JSON serializer contract v1.0."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def hash_sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


SERIALIZERS: Dict[str, Callable[[Any], bytes]] = {
    "JSON_SORTED_COMPACT_UTF8_V1_0": serialize_json_sorted_compact_utf8_v1_0,
}

HASHERS: Dict[str, Callable[[bytes], str]] = {
    "sha256": hash_sha256,
}

# Every replay-critical axis is explicit. There are intentionally no defaults.
REGISTRY: Dict[str, Dict[str, Any]] = {
    "ERS_V0_1": {
        "canonical_version": "ERS_CANONICAL_V1_0",
        "serializer_version": "JSON_SORTED_COMPACT_UTF8_V1_0",
        "hash_algorithm": "sha256",
        "canonicalizer": canonicalize_ers_v0_1,
    },
}


def registry_metadata(schema_version: str) -> Dict[str, str]:
    """Return replay metadata without exposing the canonicalizer callable."""
    meta = REGISTRY[schema_version]
    return {
        "registry_version": REGISTRY_VERSION,
        "schema_version": schema_version,
        "canonical_version": meta["canonical_version"],
        "serializer_version": meta["serializer_version"],
        "hash_algorithm": meta["hash_algorithm"],
    }


def canonical_artifact_hash(record: Mapping[str, Any]) -> str:
    """Replay one artifact using only explicitly registered transformations."""
    schema_version = record["schema_version"]
    if schema_version not in REGISTRY:
        raise ValueError(f"unsupported schema_version: {schema_version}")

    meta = REGISTRY[schema_version]
    canonical = meta["canonicalizer"](record)
    serializer = SERIALIZERS[meta["serializer_version"]]
    hasher = HASHERS[meta["hash_algorithm"]]
    serialized = serializer(canonical)
    return hasher(serialized)


def replay_receipt(record: Mapping[str, Any]) -> Dict[str, Any]:
    """Return the deterministic hash plus all version axes used to produce it."""
    schema_version = record["schema_version"]
    receipt: Dict[str, Any] = registry_metadata(schema_version)
    receipt.update(
        {
            "artifact_id": record["artifact_id"],
            "replay_hash": canonical_artifact_hash(record),
            "authority": AUTHORITY,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }
    )
    return receipt
