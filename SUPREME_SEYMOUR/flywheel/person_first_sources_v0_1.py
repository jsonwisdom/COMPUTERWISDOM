#!/usr/bin/env python3
"""JASON person-first, local-private source discovery for the Seymour flywheel.

This is a candidate intake checker, NOT proof of ownership, truthful transcription,
complete historical coverage, human learning, or authenticated identity.
No network, payment, signing, or public publication of source bytes.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

KINDS = ("voice", "chat")
STATES = (
    "PRESENT_PARSED", "PRESENT_UNREADABLE", "MISSING_SOURCE_FILE",
    "MISSING_INDEX_REFERENCE", "AMBIGUOUS_DUPLICATE_CONFLICT",
    "EVIDENCE_UNAVAILABLE",
)
RECOVERY = {
    "voice": {
        "PRESENT_UNREADABLE": "RETRANSCRIBE_OR_REPARSE_VOICE",
        "MISSING_SOURCE_FILE": "LOCATE_OR_RESTORE_ORIGINAL_VOICE",
        "MISSING_INDEX_REFERENCE": "REPAIR_VOICE_INDEX",
        "AMBIGUOUS_DUPLICATE_CONFLICT": "RESOLVE_VOICE_CONFLICT",
        "EVIDENCE_UNAVAILABLE": "DISCOVER_ORIGINAL_VOICE",
    },
    "chat": {
        "PRESENT_UNREADABLE": "REPARSE_CHAT",
        "MISSING_SOURCE_FILE": "LOCATE_OR_RESTORE_ORIGINAL_CHAT",
        "MISSING_INDEX_REFERENCE": "REPAIR_CHAT_INDEX",
        "AMBIGUOUS_DUPLICATE_CONFLICT": "RESOLVE_CHAT_CONFLICT",
        "EVIDENCE_UNAVAILABLE": "DISCOVER_ORIGINAL_CHAT",
    },
}


class ManifestError(ValueError):
    pass


def _validate(manifest: dict) -> tuple[list, dict]:
    if not isinstance(manifest, dict) or manifest.get("schema") != "JASON_SOURCE_INPUT_MANIFEST_V0_1":
        raise ManifestError("expected JASON_SOURCE_INPUT_MANIFEST_V0_1")
    if manifest.get("denominator") != "JASON":
        raise ManifestError("JASON must be explicit denominator")
    expected, index = manifest.get("expected"), manifest.get("index")
    if not isinstance(expected, list) or not isinstance(index, list):
        raise ManifestError("expected and index must be arrays")
    expected_ids = set()
    for e in expected:
        if not isinstance(e, dict) or e.get("kind") not in KINDS:
            raise ManifestError("expected item needs voice/chat kind")
        key = e.get("id")
        if not isinstance(key, str) or not key.strip() or key in expected_ids:
            raise ManifestError("missing/duplicate expected ID")
        expected_ids.add(key)
    entries = {}
    for i in index:
        if not isinstance(i, dict) or not isinstance(i.get("id"), str):
            raise ManifestError("index entry requires ID")
        key = i["id"]
        if key in entries or key not in expected_ids:
            raise ManifestError("duplicate or unexpected index entry")
        if not isinstance(i.get("candidates"), list):
            raise ManifestError("index candidates must be array")
        for c in i["candidates"]:
            if not isinstance(c, dict) or not isinstance(c.get("path"), str):
                raise ManifestError("candidate path required")
            if c.get("format") not in ("text", "json", "audio"):
                raise ManifestError("unsupported candidate format")
        entries[key] = i
    return expected, entries


def _confined(root: Path, relative: str) -> Path:
    relative_path = Path(relative)
    if not relative or relative_path.is_absolute():
        raise ManifestError("absolute or empty source paths forbidden")
    base = root.resolve()
    dest = (base / relative_path).resolve()
    if dest == base or base not in dest.parents:
        raise ManifestError("source path escapes declared private root")
    return dest


def _parse(kind: str, fmt: str, raw: bytes) -> tuple[bool, str]:
    if fmt == "audio":
        # Audio bytes alone are not a readable/confirmed transcript.
        return False, "TRANSCRIPTION_REQUIRED"
    if kind == "voice" and fmt != "text":
        return False, "VOICE_TRANSCRIPT_FORMAT_UNSUPPORTED"
    if kind == "chat" and fmt != "json":
        return False, "CHAT_EXPORT_FORMAT_UNSUPPORTED"
    try:
        decoded = raw.decode("utf-8-sig", errors="strict")
        if not decoded.strip():
            return False, "EMPTY_OR_UNREADABLE"
        if fmt == "json":
            obj = json.loads(decoded)
            if not isinstance(obj, (list, dict)) or not obj:
                return False, "EMPTY_OR_INVALID_CHAT_JSON"
        return True, "PARSED_CANDIDATE_ONLY"
    except (UnicodeError, json.JSONDecodeError):
        return False, "PARSE_FAILED"


def evaluate(manifest: dict, source_root: str | Path | None) -> dict:
    """Process each declared expected source independently, stable manifest order."""
    expected, index = _validate(manifest)
    root = Path(source_root) if source_root is not None else None
    root_ready = bool(root and root.is_dir())
    records = []
    for e in expected:
        key, kind = e["id"], e["kind"]
        entry = index.get(key)
        state, parser_note, content_hash = None, None, None
        if entry is None:
            state = "MISSING_INDEX_REFERENCE"
        elif not entry["candidates"] or not root_ready:
            state = "EVIDENCE_UNAVAILABLE"
        elif len(entry["candidates"]) > 1:
            state = "AMBIGUOUS_DUPLICATE_CONFLICT"
        else:
            candidate = entry["candidates"][0]
            path = _confined(root, candidate["path"])
            if not path.is_file():
                state = "MISSING_SOURCE_FILE"
            else:
                try:
                    raw = path.read_bytes()
                    content_hash = hashlib.sha256(raw).hexdigest()
                    ok, parser_note = _parse(kind, candidate["format"], raw)
                    state = "PRESENT_PARSED" if ok else "PRESENT_UNREADABLE"
                except OSError:
                    state = "PRESENT_UNREADABLE"
                    parser_note = "READ_FAILED"
        action = None if state == "PRESENT_PARSED" else RECOVERY[kind][state]
        if parser_note == "TRANSCRIPTION_REQUIRED":
            action = "TRANSCRIBE_VOICE_AUDIO"
        records.append({
            "id": key, "kind": kind, "source_state": state,
            "candidate_parse_status": parser_note,
            "private_source_sha256": content_hash,
            "claim_verdict": "UNKNOWN",
            "recovery_action": action,
            "dependent_path_hold": state != "PRESENT_PARSED",
            "original_source_authenticated": False,
        })
    count = Counter(r["source_state"] for r in records)
    return {
        "schema": "JASON_SOURCE_RECOVERY_CANDIDATE_V0_1",
        "denominator": "JASON",
        "scope": "EXPLICIT_EXPECTED_INPUTS_ONLY",
        "original_history_completeness": "UNKNOWN",
        "source_root_checked": root_ready,
        "expected_count": len(records),
        "candidate_parsed_count": count["PRESENT_PARSED"],
        "source_states": {k: count[k] for k in STATES},
        "independent_supported_work_continues": True,
        "authority_created": False,
        "records": records,  # PRIVATE LOCAL ONLY, do not upload
    }


def safe_public_summary(private_result: dict) -> dict:
    """No IDs, paths, raw data, private digests, or voice/chat content."""
    return {
        "denominator": "JASON",
        "scope": "EXPLICIT_EXPECTED_INPUTS_ONLY",
        "source_states": dict(private_result["source_states"]),
        "expected_count": private_result["expected_count"],
        "candidate_parsed_count": private_result["candidate_parsed_count"],
        "original_history_completeness": "UNKNOWN",
        "independent_supported_work_continues": True,
        "authority_created": False,
        "privacy": "COUNTS_ONLY_NO_PRIVATE_IDENTIFIERS",
        "source_authenticity": "NOT_ESTABLISHED",
    }


def not_configured_summary() -> dict:
    return {
        "denominator": "JASON", "scope": "NO_LOCAL_ORIGINALS_CONFIGURED",
        "source_states": {"EVIDENCE_UNAVAILABLE": 2},
        "expected_count": 2, "candidate_parsed_count": 0,
        "original_history_completeness": "UNKNOWN",
        "independent_supported_work_continues": True,
        "recovery_actions": [
            "CONFIGURE_PRIVATE_VOICE_ORIGINAL_MANIFEST",
            "CONFIGURE_PRIVATE_CHAT_ORIGINAL_MANIFEST",
        ],
        "authority_created": False,
        "privacy": "COUNTS_ONLY_NO_PRIVATE_IDENTIFIERS",
        "source_authenticity": "NOT_ESTABLISHED",
    }
