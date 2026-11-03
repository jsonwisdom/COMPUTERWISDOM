#!/usr/bin/env python3
"""JASON candidate-only CEO -> GRAPH -> FOLD -> QUERY provenance bridge.

Private, deterministic, read-only evidence processing. Never authenticates
voice identity, speaker, original exports, factual truth, or historic coverage.
Do not publish this report: excerpt text, source IDs, and digests are PRIVATE.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import copy
import datetime
import hashlib
import json
import re
from pathlib import Path

from person_first_sources_v0_1 import ManifestError, _confined, _validate, evaluate

SCHEMA = "JASON_CEO_GRAPH_FOLD_QUERY_CANDIDATE_V0_1"
PARSER = "EXACT_UTF8_SPAN_BRIDGE_V0_1"
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _utc_or_none(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ManifestError("reported_event_time_utc must be string or null")
    try:
        parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ManifestError("invalid reported_event_time_utc") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != datetime.timedelta(0):
        raise ManifestError("reported_event_time_utc requires UTC offset")
    return parsed.isoformat().replace("+00:00", "Z")


def compile_pipeline(manifest: dict, root: str | Path | None,
                     proposed_claims: list, previous: dict | None = None) -> dict:
    """All claimed words and source digests require exact local byte readback."""
    expected, index = _validate(manifest)
    if not isinstance(proposed_claims, list):
        raise ManifestError("proposed_claims must be array")
    if previous is not None and (not isinstance(previous, dict)
                                or previous.get("schema") != SCHEMA):
        raise ManifestError("previous private candidate report schema mismatch")

    recovery = evaluate(manifest, root)
    expected_by_id = {e["id"]: e for e in expected}
    source_by_id = {e["id"]: e for e in recovery["records"]}
    prior = copy.deepcopy(previous.get("observations", [])) if previous else []
    if not isinstance(prior, list) or any(not isinstance(o, dict) for o in prior):
        raise ManifestError("previous observation history malformed")

    observations = {}
    for obs in prior:
        if not isinstance(obs.get("observation_id"), str) or not obs["observation_id"]:
            raise ManifestError("previous observation lacks stable ID")
        if obs["observation_id"] in observations and observations[obs["observation_id"]] != obs:
            raise ManifestError("previous event ID collision")
        observations[obs["observation_id"]] = obs

    scoped_holds = []
    accepted = 0
    for proposal in proposed_claims:
        if not isinstance(proposal, dict):
            raise ManifestError("claim proposal must be object")
        sid = proposal.get("source_id")
        if sid not in expected_by_id:
            raise ManifestError("claim references unregistered source")
        kind = expected_by_id[sid]["kind"]
        state = source_by_id[sid]
        topic = proposal.get("topic")
        interpretation = proposal.get("interpretation")
        if not isinstance(topic, str) or not topic.strip():
            raise ManifestError("topic required")
        if not isinstance(interpretation, str) or not interpretation.strip():
            raise ManifestError("interpretation required")
        if state["source_state"] != "PRESENT_PARSED":
            scoped_holds.append({
                "source_id": sid, "topic": topic,
                "reason": state["source_state"],
                "recovery_action": state["recovery_action"],
            })
            continue
        candidate = index[sid]["candidates"][0]
        location = _confined(Path(root), candidate["path"])
        try:
            raw = location.read_bytes()
        except OSError:
            scoped_holds.append({
                "source_id": sid, "topic": topic, "reason": "SOURCE_DISAPPEARED_DURING_READ",
                "recovery_action": "RECHECK_AND_RESTORE_" + kind.upper(),
            })
            continue
        actual_sha = _digest(raw)
        original_expected = candidate.get("expected_sha256")
        if original_expected is not None:
            if not isinstance(original_expected, str) or not HEX64.fullmatch(original_expected):
                raise ManifestError("expected_sha256 must be 64 hex digits")
            if original_expected.lower() != actual_sha:
                scoped_holds.append({
                    "source_id": sid, "topic": topic, "reason": "SOURCE_DIGEST_MISMATCH",
                    "recovery_action": "REVERIFY_ORIGINAL_SOURCE_BYTES",
                })
                continue
        start, end = proposal.get("byte_start"), proposal.get("byte_end")
        if (type(start) is not int or type(end) is not int
                or start < 0 or end <= start or end > len(raw)):
            scoped_holds.append({
                "source_id": sid, "topic": topic, "reason": "INVALID_BYTE_SPAN",
                "recovery_action": "RECHECK_SOURCE_OFFSETS",
            })
            continue
        try:
            excerpt = raw[start:end].decode("utf-8", errors="strict")
        except UnicodeError:
            scoped_holds.append({
                "source_id": sid, "topic": topic, "reason": "SPAN_DECODE_ERROR",
                "recovery_action": "RECHECK_SOURCE_OFFSETS",
            })
            continue
        if not excerpt or excerpt != proposal.get("expected_excerpt"):
            scoped_holds.append({
                "source_id": sid, "topic": topic, "reason": "SPAN_BYTES_DISAGREE",
                "recovery_action": "RECOMPUTE_EXCERPT_FROM_ORIGINAL",
            })
            continue
        when = _utc_or_none(proposal.get("reported_event_time_utc"))
        identity = {
            "source_id": sid, "source_sha256": actual_sha,
            "byte_start": start, "byte_end": end,
            "topic": topic, "interpretation": interpretation,
            "reported_event_time_utc": when,
        }
        obs_id = _digest(_canonical(identity).encode("utf-8"))
        observation = {
            "observation_id": obs_id, **identity,
            "source_kind": kind, "source_excerpt": excerpt,
            "source_span_sha256": _digest(raw[start:end]),
            "parser_version": PARSER,
            "source_authenticity": "NOT_ESTABLISHED",
            "reported_time_authority": "DECLARED_UNVERIFIED",
            "claim_verdict": "UNKNOWN",
            "object_class": "CANDIDATE_OBSERVATION_NOT_VALIDATED_CEO",
            "voice_timecode_proof": "NOT_ESTABLISHED",
        }
        if obs_id in observations and observations[obs_id] != observation:
            raise ManifestError("immutable observation ID collision")
        if obs_id not in observations:
            observations[obs_id] = observation
            accepted += 1

    # Source loss/changes invalidate current replay, never erase historical observations.
    source_warning = defaultdict(list)
    for sid in expected_by_id:
        current = source_by_id[sid]
        prior_hashes = {o.get("source_sha256") for o in observations.values()
                        if o.get("source_id") == sid}
        if prior_hashes and current["source_state"] != "PRESENT_PARSED":
            source_warning[sid].append("SOURCE_UNAVAILABLE_PRIOR_OBSERVATION_RETAINED")
        if prior_hashes and current["source_state"] == "PRESENT_PARSED":
            candidate = index[sid]["candidates"][0]
            try:
                digest_now = _digest(_confined(Path(root), candidate["path"]).read_bytes())
                if digest_now not in prior_hashes:
                    source_warning[sid].append("SOURCE_CONTENT_CHANGED_PRIOR_VERSIONS_RETAINED")
            except OSError:
                source_warning[sid].append("SOURCE_UNAVAILABLE_PRIOR_OBSERVATION_RETAINED")

    # FOLD is an append-only, view-only projection; all contradictory candidates stay.
    by_topic = defaultdict(list)
    for observation in observations.values():
        by_topic[observation["topic"]].append(observation)
    declared_topic_inputs = defaultdict(list)
    for e in expected:
        for topic in e.get("topics", []):
            if not isinstance(topic, str) or not topic.strip():
                raise ManifestError("invalid expected topic")
            declared_topic_inputs[topic].append(e["id"])

    queries = {}
    for topic in sorted(set(by_topic) | set(declared_topic_inputs)):
        obs = sorted(by_topic[topic], key=lambda o: o["observation_id"])
        candidate_values = sorted({o["interpretation"] for o in obs})
        related_sources = sorted({o["source_id"] for o in obs}
                                 | set(declared_topic_inputs[topic]))
        warnings = []
        for sid in related_sources:
            current = source_by_id.get(sid)
            if current is None:
                warnings.append({"source_id": sid, "warning": "FORMER_SOURCE_NO_LONGER_INDEXED"})
                continue
            if current["source_state"] != "PRESENT_PARSED":
                warnings.append({
                    "source_id": sid, "warning": current["source_state"],
                    "recovery_action": current["recovery_action"],
                })
            for warning in sorted(set(source_warning[sid])):
                warnings.append({"source_id": sid, "warning": warning})
        if len(candidate_values) > 1:
            warnings.append({"warning": "CONFLICTING_INTERPRETATIONS_PRESERVED"})
        queries[topic] = {
            "claim_verdict": "UNKNOWN",
            "observation_ids": [o["observation_id"] for o in obs],
            "candidate_interpretations": candidate_values,
            "conflict_candidate": len(candidate_values) > 1,
            "warnings": warnings,
            "historical_completeness": "UNKNOWN",
            "scope": "CANDIDATE_EVIDENCE_ONLY",
        }

    ordered = [observations[key] for key in sorted(observations)]
    # Graph edges are typed and source-bound; no identity/family inference.
    edges = [
        {"from_observation": o["observation_id"], "to_source": o["source_id"],
         "relation": "EXACT_BYTE_SPAN_OF", "sha256": o["source_sha256"]}
        for o in ordered
    ]
    return {
        "schema": SCHEMA, "denominator": "JASON",
        "source_recovery": recovery, "observations": ordered,
        "graph_edges": edges, "fold_query": queries, "scoped_holds": scoped_holds,
        "new_unique_observations": accepted,
        "historical_completeness": "UNKNOWN", "authority_created": False,
        "independent_supported_work_continues": True,
        "private_only": True,
        "progress_reason": "PRESERVE_ORIGINAL_CONTEXT_AND_MAKE_EACH_ERROR_RECOVERABLE",
    }


def safe_public_summary(private_report: dict) -> dict:
    count = Counter(c["reason"] for c in private_report["scoped_holds"])
    return {
        "denominator": "JASON",
        "schema": SCHEMA,
        "candidate_observation_count": len(private_report["observations"]),
        "new_unique_observation_count": private_report["new_unique_observations"],
        "scoped_hold_reason_counts": dict(sorted(count.items())),
        "topic_count": len(private_report["fold_query"]),
        "historical_completeness": "UNKNOWN",
        "private_source_bytes_included": False,
        "authority_created": False,
        "scope": "SYNTHETIC_OR_LOCAL_PRIVATE_CANDIDATE_ONLY",
    }
