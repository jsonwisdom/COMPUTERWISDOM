from __future__ import annotations

import re
from typing import Any, Dict, List

from replay.validators.base import Validator

_RING_RE = re.compile(r"^R[0-5]-[A-Z0-9]+$")
_HEX64_RE = re.compile(r"^[a-f0-9]{64}$")

_ALLOWED_OBSERVATION_KEYS = (
    "where",
    "when",
    "what",
    "baseline",
    "delta",
    "corroboration",
    "confidence",
    "severity",
    "sources",
)
_ALLOWED_REPORT_KEYS = (
    "source",
    "engine_version",
    "locality",
    "time_window",
    "snapshot_digest",
    "baseline_digest",
)


class LocalityAnomalyValidator(Validator):
    name = "locality_anomaly"
    version = "v0.1"

    def validate(
        self,
        work_order: Dict[str, Any],
        observed_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        locality = work_order.get("locality")
        if not locality:
            return self.result("PASS", 1.0, "No locality specified.")

        report = next(
            (
                output
                for output in observed_outputs
                if isinstance(output, dict) and output.get("source") == "locality_anomaly"
            ),
            None,
        )
        if report is None:
            return self.result(
                "INDETERMINATE",
                0.5,
                "No frozen locality anomaly report is present in observed outputs.",
            )

        safe_report = self._sanitize_report(report)
        if not self._is_structured_report(safe_report, work_order):
            return self.result(
                "INDETERMINATE",
                0.5,
                "Locality anomaly report is present but malformed or mismatched.",
            )

        severe = [
            observation
            for observation in safe_report["observations"]
            if float(observation.get("confidence", 0.0)) > 0.8
            and int(observation.get("corroboration", 0)) >= 2
            and observation.get("severity") == "HIGH"
        ]
        status = "FAIL" if severe else "PASS"
        result = self.result(
            status,
            0.0 if severe else 1.0,
            f"{len(severe)} severe locality anomalies detected."
            if severe
            else "No severe locality anomalies detected.",
        )
        result["details"] = safe_report
        return result

    @staticmethod
    def _is_structured_report(report: Dict[str, Any], work_order: Dict[str, Any]) -> bool:
        locality = report.get("locality")
        if not isinstance(locality, str) or not _RING_RE.fullmatch(locality):
            return False
        if locality != work_order.get("locality"):
            return False
        if report.get("time_window") != work_order.get("time_window"):
            return False
        if report.get("engine_version") != "v0.1":
            return False
        if not isinstance(report.get("snapshot_digest"), str) or not _HEX64_RE.fullmatch(report["snapshot_digest"]):
            return False
        if not isinstance(report.get("baseline_digest"), str) or not _HEX64_RE.fullmatch(report["baseline_digest"]):
            return False
        observations = report.get("observations")
        if not isinstance(observations, list):
            return False
        required = {"where", "when", "what", "baseline", "delta", "corroboration", "confidence", "severity"}
        for observation in observations:
            if not isinstance(observation, dict) or not required.issubset(observation):
                return False
            if observation.get("where") != locality:
                return False
        return True

    @staticmethod
    def _sanitize_report(report: Dict[str, Any]) -> Dict[str, Any]:
        safe = {key: report.get(key) for key in _ALLOWED_REPORT_KEYS}
        safe["source"] = "locality_anomaly"
        safe_observations = []
        for observation in report.get("observations", []):
            if not isinstance(observation, dict):
                continue
            safe_observations.append(
                {
                    key: observation[key]
                    for key in _ALLOWED_OBSERVATION_KEYS
                    if key in observation
                }
            )
        safe["observations"] = safe_observations
        return safe
