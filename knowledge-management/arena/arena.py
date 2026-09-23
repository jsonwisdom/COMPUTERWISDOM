#!/usr/bin/env python3
"""Deterministic Sentinel Arena evaluator.

The Arena adjudicates competing instrument hypotheses against referenced evidence.
It never grants authority and never applies remediation. Output is a replayable
State of Reality record suitable for Orchestrator review.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


class ArenaError(ValueError):
    """Raised when an Arena round violates runtime invariants."""


@dataclass(frozen=True)
class InstrumentScore:
    instrument_id: str
    hypothesis: str
    declared_confidence: float
    calibrated_confidence: float
    support_weight: float
    contradiction_weight: float
    evidence_count: int
    missing_evidence_refs: tuple[str, ...]


def _bounded_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ArenaError(f"{name} must be a number between 0 and 1")
    value = float(value)
    if math.isnan(value) or value < 0.0 or value > 1.0:
        raise ArenaError(f"{name} must be a number between 0 and 1")
    return value


def _require_round_invariants(round_data: dict[str, Any]) -> None:
    if round_data.get("authority") is not False:
        raise ArenaError("Arena rounds must set authority=false")
    if round_data.get("remediation_applied") not in (None, False):
        raise ArenaError("Arena cannot silently remediate; remediation_applied must be false")

    instruments = round_data.get("instruments")
    if not isinstance(instruments, list) or len(instruments) < 2:
        raise ArenaError("Arena requires at least two competing instruments")

    evidence = round_data.get("evidence")
    if not isinstance(evidence, list):
        raise ArenaError("evidence must be an array")

    instrument_ids = [item.get("id") for item in instruments if isinstance(item, dict)]
    if len(instrument_ids) != len(instruments) or any(not item for item in instrument_ids):
        raise ArenaError("every instrument requires a non-empty id")
    if len(set(instrument_ids)) != len(instrument_ids):
        raise ArenaError("instrument ids must be unique")

    evidence_ids = [item.get("id") for item in evidence if isinstance(item, dict)]
    if len(evidence_ids) != len(evidence) or any(not item for item in evidence_ids):
        raise ArenaError("every evidence item requires a non-empty id")
    if len(set(evidence_ids)) != len(evidence_ids):
        raise ArenaError("evidence ids must be unique")

    known_instruments = set(instrument_ids)
    for item in evidence:
        for field in ("supports", "contradicts"):
            refs = item.get(field, [])
            if not isinstance(refs, list):
                raise ArenaError(f"evidence.{field} must be an array")
            unknown = sorted(set(refs) - known_instruments)
            if unknown:
                raise ArenaError(
                    f"evidence {item['id']} references unknown instruments in {field}: {unknown}"
                )


def _score_instrument(
    instrument: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    minimum_evidence_items: int,
) -> InstrumentScore:
    instrument_id = instrument["id"]
    declared = _bounded_number(instrument.get("confidence", 0.0), f"{instrument_id}.confidence")
    requested_refs = instrument.get("evidence_refs", [])
    if not isinstance(requested_refs, list):
        raise ArenaError(f"{instrument_id}.evidence_refs must be an array")

    missing = tuple(sorted(ref for ref in requested_refs if ref not in evidence_by_id))
    usable = [evidence_by_id[ref] for ref in requested_refs if ref in evidence_by_id]

    support_weight = 0.0
    contradiction_weight = 0.0
    relevant_count = 0
    for item in usable:
        reliability = _bounded_number(item.get("reliability", 0.5), f"{item['id']}.reliability")
        supports = instrument_id in item.get("supports", [])
        contradicts = instrument_id in item.get("contradicts", [])
        if supports:
            support_weight += reliability
        if contradicts:
            contradiction_weight += reliability
        if supports or contradicts:
            relevant_count += 1

    total_weight = support_weight + contradiction_weight
    if total_weight == 0:
        evidence_ratio = 0.0
    else:
        evidence_ratio = support_weight / total_weight

    coverage = min(1.0, relevant_count / max(1, minimum_evidence_items))
    calibrated = round(evidence_ratio * coverage, 6)

    return InstrumentScore(
        instrument_id=instrument_id,
        hypothesis=str(instrument.get("hypothesis", "")),
        declared_confidence=declared,
        calibrated_confidence=calibrated,
        support_weight=round(support_weight, 6),
        contradiction_weight=round(contradiction_weight, 6),
        evidence_count=relevant_count,
        missing_evidence_refs=missing,
    )


def evaluate_round(round_data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one Arena round and return a non-authoritative report."""
    _require_round_invariants(round_data)

    policy = round_data.get("decision_policy", {})
    minimum_evidence_items = int(policy.get("minimum_evidence_items", 2))
    if minimum_evidence_items < 1:
        raise ArenaError("decision_policy.minimum_evidence_items must be at least 1")
    disagreement_threshold = _bounded_number(
        policy.get("disagreement_threshold", 0.15), "decision_policy.disagreement_threshold"
    )
    escalation_severity = str(policy.get("escalation_severity", "critical"))
    if escalation_severity not in SEVERITY_RANK:
        raise ArenaError(f"unknown escalation severity: {escalation_severity}")
    escalation_threshold = SEVERITY_RANK[escalation_severity]

    evidence_by_id = {item["id"]: item for item in round_data["evidence"]}
    scores = [
        _score_instrument(instrument, evidence_by_id, minimum_evidence_items)
        for instrument in round_data["instruments"]
    ]
    scores.sort(key=lambda item: (-item.calibrated_confidence, item.instrument_id))

    top = scores[0]
    runner_up = scores[1]
    margin = round(top.calibrated_confidence - runner_up.calibrated_confidence, 6)
    max_relevant_evidence = max((score.evidence_count for score in scores), default=0)

    critical_evidence = [
        item["id"]
        for item in round_data["evidence"]
        if SEVERITY_RANK.get(str(item.get("severity", "info")), 0) >= escalation_threshold
    ]

    missing_refs = sorted({ref for score in scores for ref in score.missing_evidence_refs})
    if max_relevant_evidence < minimum_evidence_items:
        status = "insufficient_evidence"
    elif margin <= disagreement_threshold:
        status = "contested"
    else:
        status = "resolved"

    escalate = bool(critical_evidence)
    if escalate:
        status = "escalate"

    if status == "insufficient_evidence":
        state = "Available evidence is insufficient to prefer a hypothesis. Unknown remains valid."
    elif status == "contested":
        state = (
            f"Evidence remains contested: {top.instrument_id} leads {runner_up.instrument_id} "
            f"by {margin:.3f}, within the disagreement threshold."
        )
    elif status == "escalate":
        state = (
            f"Critical evidence requires Orchestrator review. Current evidence leader: "
            f"{top.instrument_id} at calibrated confidence {top.calibrated_confidence:.3f}."
        )
    else:
        state = (
            f"Current evidence favors {top.instrument_id} at calibrated confidence "
            f"{top.calibrated_confidence:.3f}; this is a finding, not authority."
        )

    recommended_actions: list[str] = []
    if missing_refs:
        recommended_actions.append("Acquire or repair missing evidence references before promotion.")
    if status in {"insufficient_evidence", "contested"}:
        recommended_actions.append("Run another falsification round with evidence targeted at the leading hypotheses.")
    if escalate:
        recommended_actions.append("Route critical evidence to the Orchestrator; do not auto-remediate.")
    if not recommended_actions:
        recommended_actions.append("Preserve the report and seek independent replay before acting on it.")

    return {
        "contract_version": "v0.1",
        "arena_id": round_data.get("arena_id"),
        "round_id": round_data.get("round_id"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "COMPUTERWISDOM Sentinel Arena v0.1",
        "authority": False,
        "remediation_applied": False,
        "question": round_data.get("question"),
        "status": status,
        "state_of_reality": state,
        "winning_instrument": top.instrument_id if status in {"resolved", "escalate"} else None,
        "confidence": top.calibrated_confidence,
        "confidence_margin": margin,
        "critical_evidence": critical_evidence,
        "missing_evidence_refs": missing_refs,
        "scores": [
            {
                "instrument_id": score.instrument_id,
                "hypothesis": score.hypothesis,
                "declared_confidence": score.declared_confidence,
                "calibrated_confidence": score.calibrated_confidence,
                "support_weight": score.support_weight,
                "contradiction_weight": score.contradiction_weight,
                "evidence_count": score.evidence_count,
                "missing_evidence_refs": list(score.missing_evidence_refs),
            }
            for score in scores
        ],
        "dissent": [
            {
                "instrument_id": score.instrument_id,
                "hypothesis": score.hypothesis,
                "calibrated_confidence": score.calibrated_confidence,
            }
            for score in scores[1:]
        ],
        "recommended_actions": recommended_actions,
        "escalate": escalate,
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a COMPUTERWISDOM Sentinel Arena round")
    parser.add_argument("input", type=Path, help="Arena round JSON file")
    parser.add_argument("--output", "-o", type=Path, help="Write report JSON to this path")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    try:
        round_data = json.loads(args.input.read_text(encoding="utf-8"))
        report = evaluate_round(round_data)
    except (OSError, json.JSONDecodeError, ArenaError, TypeError, ValueError) as exc:
        print(f"arena: {exc}", file=sys.stderr)
        return 2

    if args.compact:
        payload = json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n"
    else:
        payload = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
