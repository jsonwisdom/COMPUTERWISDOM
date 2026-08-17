#!/usr/bin/env python3
"""Fail-closed DOJ/OIG evidence-classification observer.

The observer classifies mechanical evidence gates only. It does not create a DOJ
decision, legal conclusion/finding, White House misconduct finding, authorization,
policy, or authority.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "fixtures/jaywisdom/fraud_ledger/OIG_OVERSIGHT_CERTIFICATE_TEST_VECTORS_V0_1.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

GATE_ORDER = ("identity", "provenance", "temporal", "delta", "dependency", "scope", "authority")
RESULT_PRECEDENCE = ("REJECTED", "DIVERGENCE", "HOLD", "PROVEN")


@dataclass(frozen=True)
class SourceObject:
    source_id: str
    url: str
    sha256: str
    byte_length: int | None = None
    observed_at: str | None = None

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SourceObject":
        return cls(
            source_id=value.get("source_id", ""),
            url=value.get("url", ""),
            sha256=value.get("sha256", ""),
            byte_length=value.get("byte_length"),
            observed_at=value.get("observed_at"),
        )


@dataclass(frozen=True)
class Edge:
    edge_id: str
    source_objects: tuple[SourceObject, ...]
    delta_claimed: bool = False
    delta_evidence_source_ids: tuple[str, ...] = ()
    dependency_required: bool = False
    dependency_source_ids: tuple[str, ...] = ()
    scope_claimed: bool = False
    scope_evidence_source_ids: tuple[str, ...] = ()
    authority_claimed: bool = False
    authorization_claimed: bool = False
    legal_conclusion_claimed: bool = False
    policy_claimed: bool = False
    authority_evidence_source_ids: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, edge_id: str, value: dict[str, Any]) -> "Edge":
        # The caller may never submit the terminal observer state.
        if "observer_result" in value:
            raise ValueError("CALLER_SUPPLIED_OBSERVER_RESULT_FORBIDDEN")
        return cls(
            edge_id=edge_id,
            source_objects=tuple(SourceObject.from_mapping(item) for item in value.get("source_objects", [])),
            delta_claimed=bool(value.get("delta_claimed", False)),
            delta_evidence_source_ids=tuple(value.get("delta_evidence_source_ids", [])),
            dependency_required=bool(value.get("dependency_required", False)),
            dependency_source_ids=tuple(value.get("dependency_source_ids", [])),
            scope_claimed=bool(value.get("scope_claimed", False)),
            scope_evidence_source_ids=tuple(value.get("scope_evidence_source_ids", [])),
            authority_claimed=bool(value.get("authority_claimed", False)),
            authorization_claimed=bool(value.get("authorization_claimed", False)),
            legal_conclusion_claimed=bool(value.get("legal_conclusion_claimed", False)),
            policy_claimed=bool(value.get("policy_claimed", False)),
            authority_evidence_source_ids=tuple(value.get("authority_evidence_source_ids", [])),
        )


@dataclass
class OIGOversightCertificate:
    edge: Edge
    gate_outcomes: dict[str, str] = field(init=False)
    observer_result: str = field(init=False)
    doj_decision_created: bool = field(init=False, default=False)
    legal_conclusion_created: bool = field(init=False, default=False)
    legal_finding_created: bool = field(init=False, default=False)
    white_house_misconduct_finding_created: bool = field(init=False, default=False)
    authorization_created: bool = field(init=False, default=False)
    policy_created: bool = field(init=False, default=False)
    authority_created: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        self.gate_outcomes = evaluate_gates(self.edge)
        self.observer_result = derive_observer_result(self.gate_outcomes)

    def as_dict(self) -> dict[str, Any]:
        return {
            "format": "OIG_OVERSIGHT_CERTIFICATE_V0.1",
            "classification": "EVIDENCE_CLASSIFICATION_ONLY",
            "edge_id": self.edge.edge_id,
            "source_objects": [
                {
                    "source_id": item.source_id,
                    "url": item.url,
                    "sha256": item.sha256,
                    **({"byte_length": item.byte_length} if item.byte_length is not None else {}),
                    **({"observed_at": item.observed_at} if item.observed_at is not None else {}),
                }
                for item in self.edge.source_objects
            ],
            "gate_outcomes": self.gate_outcomes,
            "observer_result": self.observer_result,
            "doj_decision_created": False,
            "legal_conclusion_created": False,
            "legal_finding_created": False,
            "white_house_misconduct_finding_created": False,
            "authorization_created": False,
            "policy_created": False,
            "authority_created": False,
        }


def _valid_refs(refs: tuple[str, ...], source_ids: set[str]) -> bool:
    return bool(refs) and all(ref in source_ids for ref in refs)


def _identity_gate(edge: Edge) -> str:
    if not edge.source_objects:
        return "HOLD"
    bindings: dict[str, str] = {}
    for item in edge.source_objects:
        if not item.source_id or not item.url:
            return "HOLD"
        prior = bindings.get(item.source_id)
        if prior is not None and prior != item.url:
            return "DIVERGENCE"
        bindings[item.source_id] = item.url
    return "PROVEN"


def _provenance_gate(edge: Edge) -> str:
    if not edge.source_objects:
        return "HOLD"
    for item in edge.source_objects:
        if SHA256_RE.fullmatch(item.sha256) is None:
            return "REJECTED"
        if item.byte_length is not None and (not isinstance(item.byte_length, int) or item.byte_length < 0):
            return "REJECTED"
    return "PROVEN"


def _temporal_gate(edge: Edge) -> str:
    if not edge.source_objects:
        return "HOLD"
    for item in edge.source_objects:
        if item.observed_at is None:
            return "HOLD"
        try:
            datetime.fromisoformat(item.observed_at.replace("Z", "+00:00"))
        except ValueError:
            return "REJECTED"
    return "PROVEN"


def _delta_gate(edge: Edge, source_ids: set[str]) -> str:
    if not edge.delta_claimed:
        return "PROVEN"
    if len(set(edge.delta_evidence_source_ids)) < 2:
        return "HOLD_DELTA"
    if not _valid_refs(edge.delta_evidence_source_ids, source_ids):
        return "HOLD_DELTA"
    return "PROVEN"


def _dependency_gate(edge: Edge, source_ids: set[str]) -> str:
    if not edge.dependency_required:
        return "DEPENDENCY_NOT_REQUIRED"
    return "PROVEN" if _valid_refs(edge.dependency_source_ids, source_ids) else "HOLD"


def _scope_gate(edge: Edge, source_ids: set[str]) -> str:
    if not edge.scope_claimed:
        return "PROVEN"
    return "PROVEN" if _valid_refs(edge.scope_evidence_source_ids, source_ids) else "HOLD"


def _authority_gate(edge: Edge, source_ids: set[str]) -> str:
    semantic_claimed = any((
        edge.authority_claimed,
        edge.authorization_claimed,
        edge.legal_conclusion_claimed,
        edge.policy_claimed,
    ))
    if not semantic_claimed:
        return "PROVEN"
    # URL wording never counts. Only explicit source-object references can satisfy this gate.
    return "PROVEN" if _valid_refs(edge.authority_evidence_source_ids, source_ids) else "HOLD"


def evaluate_gates(edge: Edge) -> dict[str, str]:
    source_ids = {item.source_id for item in edge.source_objects}
    return {
        "identity": _identity_gate(edge),
        "provenance": _provenance_gate(edge),
        "temporal": _temporal_gate(edge),
        "delta": _delta_gate(edge, source_ids),
        "dependency": _dependency_gate(edge, source_ids),
        "scope": _scope_gate(edge, source_ids),
        "authority": _authority_gate(edge, source_ids),
    }


def derive_observer_result(gates: dict[str, str]) -> str:
    values = set(gates.values())
    if "REJECTED" in values:
        return "REJECTED"
    if "DIVERGENCE" in values:
        return "DIVERGENCE"
    if "HOLD" in values or "HOLD_DELTA" in values:
        return "HOLD"
    return "PROVEN"


def run_self_test() -> int:
    suite = json.loads(VECTORS.read_text(encoding="utf-8"))
    failures: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []

    # Prove the caller cannot inject the terminal state.
    caller_result_rejected = False
    try:
        Edge.from_mapping("FORBIDDEN_RESULT_TEST", {
            "source_objects": [],
            "observer_result": "PROVEN",
        })
    except ValueError as exc:
        caller_result_rejected = str(exc) == "CALLER_SUPPLIED_OBSERVER_RESULT_FORBIDDEN"

    for vector in suite["vectors"]:
        edge = Edge.from_mapping(vector["id"], vector["edge"])
        certificate = OIGOversightCertificate(edge)
        output = certificate.as_dict()
        ok = output["observer_result"] == vector["expected_result"]

        for gate, expected in vector.get("expected_gates", {}).items():
            ok = ok and output["gate_outcomes"].get(gate) == expected
        for name in vector.get("expected_false_fields", []):
            ok = ok and output.get(name) is False
        if "expected_source_count" in vector:
            ok = ok and len(output["source_objects"]) == vector["expected_source_count"]

        # Constitutional membrane is global, not vector-specific.
        boundary_fields = (
            "doj_decision_created",
            "legal_conclusion_created",
            "legal_finding_created",
            "white_house_misconduct_finding_created",
            "authorization_created",
            "policy_created",
            "authority_created",
        )
        ok = ok and all(output[name] is False for name in boundary_fields)

        result = {
            "id": vector["id"],
            "expected_result": vector["expected_result"],
            "observed_result": output["observer_result"],
            "gate_outcomes": output["gate_outcomes"],
            "pass": ok,
        }
        results.append(result)
        if not ok:
            failures.append(result)

    summary = {
        "observer": "OIG_OVERSIGHT_CERTIFICATE_V0.1",
        "test_vector_count": len(results),
        "test_vectors_passed": len(results) - len(failures),
        "test_vectors_failed": len(failures),
        "caller_observer_result_rejected": caller_result_rejected,
        "observer_result_init_false": True,
        "byte_length_optional": True,
        "result_precedence": list(RESULT_PRECEDENCE),
        "doj_decision_created": False,
        "legal_conclusion_created": False,
        "legal_finding_created": False,
        "white_house_misconduct_finding_created": False,
        "authorization_created": False,
        "policy_created": False,
        "authority_created": False,
        "roll_002_live": False,
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not failures and caller_result_rejected else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    parser.error("Only --self-test is implemented in v0.1")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
