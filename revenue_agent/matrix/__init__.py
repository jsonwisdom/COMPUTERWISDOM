"""Deterministic, non-authoritative locality evidence routing."""

from matrix.router import (
    POLICY_DIGEST,
    ROUTER_VERSION,
    project_anomaly_observation,
    route,
    route_anomaly_report,
)

__all__ = [
    "POLICY_DIGEST",
    "ROUTER_VERSION",
    "project_anomaly_observation",
    "route",
    "route_anomaly_report",
]
