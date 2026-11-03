#!/usr/bin/env python3
"""Read-only JASON_OS canonical schema byte-pin gate.

Historical SHA-256 commitments were reported in the 2026-09-21 ingestion status
record. This module does NOT contain their original schema bytes.
Missing/mismatched bytes cannot be repaired by constructing substitute schemas.

A matching SHA-256 AND successful instance validation proves a narrow schema
compatibility claim only. It cannot authenticate original voice/chat, validate
historical events, or grant identity/financial/decision authority.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

# Historical documented SHA-256 pins: a distinct hash per layer.
HISTORICAL_PINS = {
    "ceo": "9b43f71d7dd261cf3d7854f36e9c4a86896710d68576b787fc7a80a03746823c",
    "graph": "d05f637f92b04ae2c57cac5308bc9f55a5c4e8f1d80012e48930f1f2c6672e8c",
    "fold": "96db1f57b6413bc9fad4f3c20d46236d1cae0a4d868ee9e20c218cabed10ed6c",
    "query": "093c5601d23805ab9e73e36d201c8181170aabb47f7919a730f9c3091419a0e4",
}
LAYER_FILENAMES = {k: k + ".schema.json" for k in HISTORICAL_PINS}
PARSER_VERSION = "JASON_OS_CANDIDATE_BRIDGE_V0_1"


def _unique_pairs(pairs):
    values = {}
    for key, value in pairs:
        if key in values:
            raise ValueError("JSON_DUPLICATE_KEY")
        values[key] = value
    return values


def _local_refs_only(schema):
    """External schema references could perform network I/O: reject them."""
    if isinstance(schema, list):
        return all(_local_refs_only(x) for x in schema)
    if not isinstance(schema, dict):
        return True
    for k, v in schema.items():
        if k in ("$ref", "$dynamicRef", "$recursiveRef"):
            if not isinstance(v, str) or not v.startswith("#"):
                return False
        if not _local_refs_only(v):
            return False
    return True


def _status(gates: list[str]):
    return "FAIL" if "FAIL" in gates else "UNKNOWN" if "UNKNOWN" in gates else "PASS"


def verify_canonical_schema_bundle(pipeline: dict, schema_root: str | Path | None,
                                   *, expected_pins=None, test_profile=False) -> dict:
    """Conservative schema compatibility; never a truth/ownership finding.

    Supplying expected_pins is ONLY permitted in synthetic test profile. An
    injected synthetic profile returns FIXTURE_PASS, never canonical PASS.
    """
    if expected_pins is not None and not test_profile:
        raise ValueError("CANONICAL_PINS_CANNOT_BE_OVERRIDDEN")
    pins = dict(expected_pins) if expected_pins is not None else HISTORICAL_PINS
    if set(pins) != set(HISTORICAL_PINS):
        raise ValueError("FOUR_SCHEMA_PINS_REQUIRED")
    if not isinstance(pipeline, dict) or any(k not in pipeline for k in HISTORICAL_PINS):
        raise ValueError("FOUR_CANDIDATE_STAGES_REQUIRED")

    root = Path(schema_root) if schema_root is not None else None
    stages = {}
    for layer in HISTORICAL_PINS:
        result = {"digest_verdict": "UNKNOWN", "validation_verdict": "UNKNOWN",
                  "schema_gate": "UNKNOWN", "recovery_action": "LOCATE_ORIGINAL_CANONICAL_SCHEMA"}
        if root is None or not root.is_dir():
            stages[layer] = result
            continue
        path = (root / LAYER_FILENAMES[layer]).resolve()
        if root.resolve() not in path.parents:
            raise ValueError("INVALID_CANONICAL_SCHEMA_LOCATION")
        if not path.is_file():
            stages[layer] = result
            continue
        try:
            source = path.read_bytes()
            digest = hashlib.sha256(source).hexdigest()
        except OSError:
            result["recovery_action"] = "RESTORE_READABLE_CANONICAL_SCHEMA"
            stages[layer] = result
            continue
        if digest != pins[layer]:
            result.update(digest_verdict="FAIL", schema_gate="FAIL",
                          recovery_action="RECOVER_SCHEMA_MATCHING_HISTORICAL_SHA256")
            stages[layer] = result
            continue
        result["digest_verdict"] = "PASS"
        try:
            schema = json.loads(source.decode("utf-8-sig"), object_pairs_hook=_unique_pairs)
            if not isinstance(schema, dict):
                raise ValueError("SCHEMA_NOT_OBJECT")
            if not _local_refs_only(schema):
                result["recovery_action"] = "RESOLVE_EXTERNAL_SCHEMA_REFERENCES_OFFLINE"
                stages[layer] = result
                continue
        except (UnicodeError, json.JSONDecodeError, ValueError):
            result.update(validation_verdict="FAIL", schema_gate="FAIL",
                          recovery_action="REPAIR_PINNED_SCHEMA_PARSE_OR_RETRIEVE")
            stages[layer] = result
            continue
        try:
            from jsonschema.validators import validator_for
            from jsonschema import FormatChecker
        except ImportError:
            result["recovery_action"] = "INSTALL_PINNED_OFFLINE_SCHEMA_VALIDATOR"
            stages[layer] = result
            continue
        try:
            cls = validator_for(schema)
            cls.check_schema(schema)
            cls(schema, format_checker=FormatChecker()).validate(pipeline[layer])
            result.update(validation_verdict="PASS", schema_gate="PASS", recovery_action=None)
        except Exception as exc:
            # Never return schema content/instance text or exception messages.
            result.update(validation_verdict="FAIL", schema_gate="FAIL",
                          recovery_action="RECONCILE_CANDIDATE_WITH_PINNED_SCHEMA",
                          error_class=type(exc).__name__)
        stages[layer] = result
    aggregate = _status([x["schema_gate"] for x in stages.values()])
    if test_profile and aggregate == "PASS":
        aggregate = "FIXTURE_PASS_ONLY"
    return {
        "denominator": "JASON",
        "schema": "JASON_OS_CANONICAL_SCHEMA_GATE_V0_1",
        "profile": "SYNTHETIC_TEST_ONLY" if test_profile else "HISTORICAL_HASH_COMMITMENTS",
        "canonical_compatibility": aggregate,
        "truth_verdict": "UNKNOWN",
        "history_complete": "UNKNOWN",
        "authority_created": False,
        "stages": stages,
    }


def private_ingestion_receipt(manifest: dict, candidate_pipeline: dict,
                              *, observed_at_utc: str | None = None) -> dict:
    """Private-only candidate receipt; caller must not publish this result."""
    stamp = observed_at_utc or dt.datetime.now(dt.timezone.utc).isoformat()
    parsed_stamp = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if parsed_stamp.tzinfo is None:
        raise ValueError("INGESTION_TIME_MUST_HAVE_OFFSET")
    if manifest.get("denominator") != "JASON" or candidate_pipeline.get("denominator") != "JASON":
        raise ValueError("DENOMINATOR_MISMATCH")
    index = {row["id"]: row for row in manifest.get("index", [])}
    original = {row["id"]: row for row in manifest.get("expected", [])}
    items = []
    for obs in candidate_pipeline["ceo"]["observations"]:
        source_id = obs["source_id"]
        if source_id not in original:
            raise ValueError("SOURCE_MISSING_FROM_EXPECTED_MANIFEST")
        entry = index.get(source_id, {})
        candidates = entry.get("candidates", [])
        # A path is a pointer only. It is not a custody or authenticity proof.
        pointer = candidates[0]["path"] if len(candidates) == 1 else None
        items.append({
            "source_id": source_id, "source_kind": obs["source_kind"],
            "private_local_pointer": pointer,
            "source_sha256": obs["source_sha256"],
            "ingested_at_utc": stamp,
            "parser_version": PARSER_VERSION,
            "transcriber_version_declared": original[source_id].get("transcriber_version"),
            "transcriber_version_verified": False,
            "source_authenticity": "UNKNOWN",
            "claim_verdict": "UNKNOWN",
            "schema_conformance": "UNKNOWN",
            "event_time_declared": obs.get("declared_event_time"),
            "event_time_verified": False,
            "delivery_time": None,
            "acknowledgment_time": None,
        })
    return {
        "schema": "JASON_OS_LOCAL_INGESTION_CANDIDATE_RECEIPT_V0_1",
        "denominator": "JASON", "privacy": "PRIVATE_ONLY_DO_NOT_UPLOAD",
        "history_complete": "UNKNOWN", "authority_created": False,
        "rows": items,
    }


def public_gate_summary(result: dict) -> dict:
    """Never include source text, local pointers, IDs, hashes, or validation errors."""
    return {
        "denominator": "JASON",
        "canonical_compatibility": result["canonical_compatibility"],
        "layer_states": {k: {"digest_verdict": v["digest_verdict"],
                             "validation_verdict": v["validation_verdict"],
                             "schema_gate": v["schema_gate"],
                             "recovery_action": v["recovery_action"]}
                         for k, v in result["stages"].items()},
        "history_complete": "UNKNOWN", "authority_created": False,
        "original_source_authenticity": "UNKNOWN",
    }
