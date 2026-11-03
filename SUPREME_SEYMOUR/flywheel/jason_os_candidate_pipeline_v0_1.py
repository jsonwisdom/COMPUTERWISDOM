#!/usr/bin/env python3
"""Private, candidate-only JASON_OS CEO -> GRAPH -> FOLD -> QUERY projection.

The existing JASON_OS kernel remains unchanged. This adapter emits candidate
observations from locally discovered original-source files. Parsing is not
verification, hashing is not authorship, and no identity is inferred from voice.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

from person_first_sources_v0_1 import _confined, evaluate


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _messages_from_json(obj):
    """Recognize only explicitly bounded synthetic/tested message shapes."""
    if isinstance(obj, dict):
        candidates = obj.get("messages")
        if isinstance(candidates, list):
            return candidates
    if isinstance(obj, list) and len(obj) == 1 and isinstance(obj[0], dict):
        chat = obj[0].get("chat")
        if isinstance(chat, dict) and isinstance(chat.get("messages"), list):
            return chat["messages"]
    return None


def _extract_chat(raw: bytes):
    obj = json.loads(raw.decode("utf-8-sig"))
    messages = _messages_from_json(obj)
    if messages is None:
        return [], "UNSUPPORTED_CHAT_MESSAGE_LAYOUT"
    candidates = []
    for ordinal, message in enumerate(messages):
        if not isinstance(message, dict):
            continue
        body = message.get("text")
        if not isinstance(body, str):
            body = message.get("content")
        if not isinstance(body, str) or not body.strip():
            continue
        candidates.append({
            "ordinal": ordinal,
            "candidate_text": body,
            "candidate_text_sha256": _digest(body.encode("utf-8")),
            "content_class": "UNVERIFIED_EXTRACTED_TEXT",
        })
    return candidates, "EXTRACTED_CANDIDATES_ONLY"


def compile_private_candidates(manifest: dict, source_root: str | Path | None):
    """Never call this output a validated CEO or authenticated history."""
    discovery = evaluate(manifest, source_root)
    root = Path(source_root) if source_root is not None else None
    by_expected = {x["id"]: x for x in manifest["expected"]}
    by_index = {x["id"]: x for x in manifest["index"]}
    ceo, nodes, edges, folds = [], [], [], []
    for observed in discovery["records"]:
        sid = observed["id"]
        item = by_expected[sid]
        kind = observed["kind"]
        status = observed["source_state"]
        source_node = f"source:{sid}"
        nodes.append({"node": source_node, "type": "PRIVATE_SOURCE_REFERENCE",
                      "source_state": status, "verified": False,
                      "evidence_verdict": "UNKNOWN"})
        source = {
            "source_id": sid,
            "source_kind": kind,
            "source_state": status,
            "source_sha256": observed["private_source_sha256"],
            "source_authenticity": "UNKNOWN",
            "evidence_verdict": "UNKNOWN",
            "candidate_stage": "NOT_EXTRACTED",
            "declared_event_time": item.get("declared_event_time"),
            "event_time_verified": False,
            "observation_time": None,
            "generation_time": None,
            "delivery_time": None,
            "operator_acknowledgment_time": None,
            "recovery_action": observed["recovery_action"],
            "audio_original_link": "NOT_APPLICABLE" if kind == "chat" else "UNRESOLVED",
            "audio_original_sha256": None,
            "candidates": [],
        }
        if status == "PRESENT_PARSED":
            index_entry = by_index[sid]["candidates"][0]
            raw = _confined(root, index_entry["path"]).read_bytes()
            if _digest(raw) != observed["private_source_sha256"]:
                source["source_state"] = "CONFLICTED_SOURCE_CHANGED_SINCE_DISCOVERY"
                source["recovery_action"] = "RECAPTURE_SOURCE_BYTES_AND_REPLAY"
            elif kind == "voice":
                transcript = raw.decode("utf-8-sig")
                source["candidates"] = [{
                    "ordinal": 0,
                    "candidate_text": transcript,
                    "candidate_text_sha256": _digest(transcript.encode("utf-8")),
                    "content_class": "UNVERIFIED_TRANSCRIPTION",
                }]
                source["candidate_stage"] = "EXTRACTED_CANDIDATES_ONLY"
                audio_ref = item.get("audio_original_path")
                if isinstance(audio_ref, str) and audio_ref:
                    audio = _confined(root, audio_ref)
                    if audio.is_file():
                        audio_bytes = audio.read_bytes()
                        source["audio_original_sha256"] = _digest(audio_bytes)
                        source["audio_original_link"] = "BYTES_OBSERVED_NOT_AUTHENTICATED"
                        original_node = f"audio:{sid}"
                        nodes.append({"node": original_node, "type": "PRIVATE_AUDIO_ORIGINAL_REFERENCE",
                                      "sha256": source["audio_original_sha256"],
                                      "verified": False, "evidence_verdict": "UNKNOWN"})
                        edges.append({"from": source_node, "to": original_node,
                                      "type": "DECLARED_TRANSCRIPT_OF",
                                      "relation_verdict": "UNKNOWN"})
                    else:
                        source["audio_original_link"] = "AUDIO_SOURCE_FILE_MISSING"
                        source["recovery_action"] = "LOCATE_OR_RESTORE_ORIGINAL_AUDIO"
                else:
                    source["audio_original_link"] = "AUDIO_INDEX_REFERENCE_MISSING"
                    source["recovery_action"] = "REPAIR_AUDIO_REFERENCE"
            elif kind == "chat":
                source["candidates"], source["candidate_stage"] = _extract_chat(raw)
                if source["candidate_stage"] == "UNSUPPORTED_CHAT_MESSAGE_LAYOUT":
                    source["recovery_action"] = "IMPLEMENT_EXPLICIT_CHAT_LAYOUT_EXTRACTOR"
        if source["source_state"] == "PRESENT_PARSED" and source["candidates"]:
            for candidate in source["candidates"]:
                candidate_node = f"candidate:{sid}:{candidate['ordinal']}"
                nodes.append({
                    "node": candidate_node, "type": "UNVERIFIED_CANDIDATE",
                    "candidate_text_sha256": candidate["candidate_text_sha256"],
                    "source_ref": source_node,
                    "verified": False, "evidence_verdict": "UNKNOWN",
                })
                edges.append({
                    "from": candidate_node, "to": source_node,
                    "type": "EXTRACTED_FROM_BYTES", "relation_verdict": "SOURCE_BOUND_ONLY",
                })
        fold_state = "CONFLICT" if "CONFLICT" in source["source_state"] else (
            "UNVERIFIED_CANDIDATE" if source["candidates"] else "SOURCE_NOT_USABLE"
        )
        folds.append({
            "source_id": sid, "source_kind": kind,
            "source_state": source["source_state"],
            "fold_state": fold_state,
            "claim_verdict": "UNKNOWN",
            "candidate_count": len(source["candidates"]),
            "reconstruction_complete": False,
            "recovery_action": source["recovery_action"],
            "provenance_sha256": source["source_sha256"],
            "audio_original_link": source["audio_original_link"],
        })
        ceo.append(source)
    return {
        "schema": "JASON_OS_PRIVATE_CANDIDATE_PIPELINE_V0_1",
        "denominator": "JASON",
        "scope": "EXPLICIT_EXPECTED_INPUTS_ONLY",
        "history_complete": "UNKNOWN",
        "verified_claim_count": 0,
        "authority_created": False,
        "ceo": {"class": "CANDIDATE_ONLY_NOT_VALIDATED_CEO", "observations": ceo},
        "graph": {"class": "EXPLICIT_EDGES_ONLY", "nodes": nodes, "edges": edges},
        "fold": {"class": "UNCERTAINTY_PRESERVING", "rows": folds},
        "query": {"class": "SOURCE_STATUS_VISIBLE", "rows": [
            {"source_id": f["source_id"], "source_state": f["source_state"],
             "candidate_count": f["candidate_count"],
             "claim_verdict": f["claim_verdict"],
             "reconstruction_complete": False,
             "recovery_action": f["recovery_action"],
             "provenance_sha256": f["provenance_sha256"]}
            for f in folds
        ]},
    }


def query_private_pipeline(pipeline, source_id):
    """Return a candidate answer with its provenance, even when not usable."""
    rows = [r for r in pipeline["query"]["rows"] if r["source_id"] == source_id]
    if not rows:
        return {"source_id": source_id, "source_state": "NOT_ENUMERATED",
                "claim_verdict": "UNKNOWN",
                "history_complete": "UNKNOWN",
                "recovery_action": "DISCOVER_EXPECTED_INPUT_OR_MANIFEST_REFERENCE"}
    return {**rows[0], "history_complete": "UNKNOWN"}


def safe_public_pipeline_summary(pipeline):
    """Public output MUST NOT include person/source IDs, text or source hashes."""
    source_counts = Counter(row["source_state"] for row in pipeline["query"]["rows"])
    return {
        "denominator": "JASON",
        "scope": "EXPLICIT_EXPECTED_INPUTS_ONLY",
        "candidate_observation_count": len(pipeline["ceo"]["observations"]),
        "candidate_text_count": sum(len(o["candidates"]) for o in pipeline["ceo"]["observations"]),
        "source_state_counts": dict(sorted(source_counts.items())),
        "history_complete": "UNKNOWN",
        "verified_claim_count": 0,
        "authority_created": False,
        "private_originals_in_public_output": False,
    }
