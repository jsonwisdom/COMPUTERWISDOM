from __future__ import annotations

import hashlib
import json
import math
import re
from types import MappingProxyType
from typing import Any, Dict, Mapping

ROUTER_VERSION = "LOCALITY_MATRIX_ROUTER_V0_1"
_LOCALITY_RE = re.compile(r"^R[0-5]-[A-Z0-9]+$")
_DIGEST_RE = re.compile(r"^[a-f0-9]{64}$")
_ROUTING_CLASSES = {
    "INFORMATION",
    "WATCH",
    "REQUEST_FOR_VERIFICATION",
    "RESOURCE_COORDINATION",
    "HUMAN_REVIEW_REQUIRED",
}
_EVENT_TYPES = {
    "weather_alert",
    "infrastructure_outage",
    "emergency_broadcast",
    "traffic_disruption",
}
_SEVERITY_SCORE = MappingProxyType({"LOW": 0.3, "MEDIUM": 0.6, "HIGH": 1.0})
_ROLES = MappingProxyType(
    {
        "INFORMATION": (),
        "WATCH": ("public_observer",),
        "REQUEST_FOR_VERIFICATION": ("public_works", "public_observer"),
        "RESOURCE_COORDINATION": ("emergency_management", "public_works"),
        "HUMAN_REVIEW_REQUIRED": ("designated_human_reviewer",),
    }
)

# Tuple + mapping proxies prevent in-process mutation of the policy consulted by route().
_RULES = (
    MappingProxyType(
        {
            "event_type": "emergency_broadcast",
            "severity_min": 0.7,
            "routing_class": "HUMAN_REVIEW_REQUIRED",
        }
    ),
    MappingProxyType(
        {
            "event_type": "infrastructure_outage",
            "severity_min": 0.7,
            "routing_class": "RESOURCE_COORDINATION",
        }
    ),
    MappingProxyType(
        {
            "event_type": "infrastructure_outage",
            "severity_min": 0.5,
            "routing_class": "REQUEST_FOR_VERIFICATION",
        }
    ),
    MappingProxyType(
        {
            "event_type": "weather_alert",
            "severity_min": 0.3,
            "routing_class": "WATCH",
        }
    ),
    MappingProxyType(
        {
            "event_type": "traffic_disruption",
            "severity_min": 0.5,
            "routing_class": "REQUEST_FOR_VERIFICATION",
        }
    ),
)


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _policy_document() -> Dict[str, Any]:
    return {
        "version": "v0.1",
        "rules": [dict(rule) for rule in _RULES],
        "default_class": "INFORMATION",
    }


POLICY_DIGEST = _sha256_json(_policy_document())


def _validate_observation(observation: Mapping[str, Any]) -> None:
    if not isinstance(observation, Mapping):
        raise TypeError("routing observation must be an object")
    allowed = {"where", "what", "severity_score", "digest"}
    if set(observation) != allowed:
        raise ValueError("routing observation must contain only where, what, severity_score, digest")
    if not isinstance(observation["where"], str) or not _LOCALITY_RE.fullmatch(
        observation["where"]
    ):
        raise ValueError("where must be an R0-R5 ring-locality identifier")
    if observation["what"] not in _EVENT_TYPES:
        raise ValueError("what is not an allowed structured event type")
    score = observation["severity_score"]
    if (
        not isinstance(score, (int, float))
        or isinstance(score, bool)
        or not math.isfinite(float(score))
        or not 0.0 <= float(score) <= 1.0
    ):
        raise ValueError("severity_score must be finite and bounded [0, 1]")
    if not isinstance(observation["digest"], str) or not _DIGEST_RE.fullmatch(
        observation["digest"]
    ):
        raise ValueError("digest must be a lowercase SHA-256 hex digest")


def route(observation: Mapping[str, Any]) -> Dict[str, Any]:
    """Return a deterministic, non-authoritative routing receipt.

    This pure function performs no I/O and consults only the frozen v0.1 policy.
    """
    _validate_observation(observation)
    routing_class = "INFORMATION"
    for rule in _RULES:
        if (
            observation["what"] == rule["event_type"]
            and float(observation["severity_score"]) >= rule["severity_min"]
        ):
            routing_class = str(rule["routing_class"])
            break
    if routing_class not in _ROUTING_CLASSES:
        raise RuntimeError("frozen policy contains an invalid routing class")

    receipt: Dict[str, Any] = {
        "router_version": ROUTER_VERSION,
        "locality_scope": observation["where"],
        "observation_digest": observation["digest"],
        "routing_class": routing_class,
        "eligible_response_roles": list(_ROLES[routing_class]),
        "human_authorization_required": routing_class
        in {"RESOURCE_COORDINATION", "HUMAN_REVIEW_REQUIRED"},
        "expires_after_window": True,
        "policy_digest": POLICY_DIGEST,
        "authority_created": False,
    }
    receipt["routing_digest"] = _sha256_json(receipt)
    return receipt


def project_anomaly_observation(observation: Mapping[str, Any]) -> Dict[str, Any]:
    """Create the closed router input without changing anomaly evidence bytes."""
    if not isinstance(observation, Mapping):
        raise TypeError("anomaly observation must be an object")
    locality = observation.get("where")
    event_type = observation.get("what")
    severity = observation.get("severity")
    if severity not in _SEVERITY_SCORE:
        raise ValueError("anomaly severity cannot be projected into frozen router policy")
    # Bind the full structured observation, including snapshot-derived evidence fields.
    return {
        "where": locality,
        "what": event_type,
        "severity_score": _SEVERITY_SCORE[severity],
        "digest": _sha256_json(dict(observation)),
    }


def route_anomaly_report(report: Mapping[str, Any]) -> list[Dict[str, Any]]:
    """Project and route every frozen observation in canonical digest order."""
    if not isinstance(report, Mapping) or report.get("source") != "locality_anomaly":
        raise ValueError("report must be locality_anomaly evidence")
    observations = report.get("observations")
    if not isinstance(observations, list):
        raise ValueError("locality anomaly report observations must be an array")
    receipts = [route(project_anomaly_observation(item)) for item in observations]
    return sorted(receipts, key=lambda item: item["routing_digest"])
