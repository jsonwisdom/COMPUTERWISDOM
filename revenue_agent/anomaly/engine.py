from __future__ import annotations

import math
from typing import Any, Dict, Protocol

from anomaly.baseline import BaselineStore, SnapshotMissing, SnapshotStore
from anomaly.ring import resolve_ring

ENGINE_VERSION = "v0.1"
_ALLOWED_WHAT = {
    "weather_alert",
    "infrastructure_outage",
    "emergency_broadcast",
    "traffic_disruption",
}
_ALLOWED_SEVERITY = {"LOW", "MEDIUM", "HIGH"}


class SignalProvider(Protocol):
    def fetch_all(self, locality: str, time_window: str) -> list[Dict[str, Any]]: ...


class BaselineIncomplete(RuntimeError):
    pass


class LocalityAnomalyEngine:
    """Replayable locality-scoped evidence provider.

    Signal acquisition is explicitly separated from analysis: capture_snapshot()
    may touch a public API once, while analyze() only reads immutable frozen bytes.
    """

    def __init__(
        self,
        signals: SignalProvider,
        snapshot_store: SnapshotStore,
        baseline_store: BaselineStore,
    ) -> None:
        self.signals = signals
        self.snapshot_store = snapshot_store
        self.baseline_store = baseline_store

    def capture_snapshot(
        self,
        locality: str,
        time_window: str,
        baseline_anchor: str,
    ) -> Dict[str, Any]:
        locality_id = resolve_ring(locality).locality_id
        try:
            snapshot, digest = self.snapshot_store.get(
                locality_id, time_window, baseline_anchor
            )
            return {"snapshot": snapshot, "snapshot_digest": digest}
        except SnapshotMissing:
            pass

        safe_signals = self.signals.fetch_all(locality_id, time_window)
        normalized = [self._normalize_signal(item) for item in safe_signals]
        snapshot, digest = self.snapshot_store.put(
            locality_id,
            time_window,
            baseline_anchor,
            sorted(
                normalized,
                key=lambda item: (item["when"], item["what"], item["sources"]),
            ),
        )
        return {"snapshot": snapshot, "snapshot_digest": digest}

    def analyze(
        self,
        locality: str,
        time_window: str,
        baseline_anchor: str,
    ) -> Dict[str, Any]:
        locality_id = resolve_ring(locality).locality_id
        snapshot, snapshot_digest = self.snapshot_store.get(
            locality_id, time_window, baseline_anchor
        )
        baseline, baseline_digest = self.baseline_store.get(
            locality_id, time_window, baseline_anchor
        )
        metrics = baseline.get("metrics", {})

        observations: list[Dict[str, Any]] = []
        for signal in snapshot.get("signals", []):
            normalized = self._normalize_signal(signal)
            what = normalized["what"]
            if what not in metrics:
                raise BaselineIncomplete(f"baseline does not contain metric for {what}")
            baseline_value = float(metrics[what])
            delta = float(normalized["value"]) - baseline_value
            observations.append(
                {
                    "where": locality_id,
                    "when": normalized["when"],
                    "what": what,
                    "baseline": baseline_value,
                    "delta": delta,
                    "corroboration": len(normalized["sources"]),
                    "confidence": float(normalized["confidence"]),
                    "severity": normalized["severity"],
                    "sources": normalized["sources"],
                }
            )

        observations.sort(
            key=lambda item: (
                item["when"],
                item["what"],
                item["severity"],
                item["sources"],
            )
        )
        return {
            "source": "locality_anomaly",
            "engine_version": ENGINE_VERSION,
            "locality": locality_id,
            "time_window": time_window,
            "snapshot_digest": snapshot_digest,
            "baseline_digest": baseline_digest,
            "observations": observations,
        }

    @staticmethod
    def _normalize_signal(item: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(item, dict):
            raise TypeError("signal must be an object")
        what = item.get("what")
        when = item.get("when")
        value = item.get("value")
        confidence = item.get("confidence")
        severity = item.get("severity")
        sources = item.get("sources")
        if what not in _ALLOWED_WHAT:
            raise ValueError("signal what is not allowed")
        if not isinstance(when, str) or not when:
            raise ValueError("signal when must be a non-empty date-time string")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("signal value must be numeric")
        if not math.isfinite(float(value)):
            raise ValueError("signal value must be finite")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            raise TypeError("signal confidence must be numeric")
        if not math.isfinite(float(confidence)) or not 0.0 <= float(confidence) <= 1.0:
            raise ValueError("signal confidence must be bounded [0, 1]")
        if severity not in _ALLOWED_SEVERITY:
            raise ValueError("signal severity is not allowed")
        if not isinstance(sources, list) or not sources:
            raise ValueError("signal sources must be a non-empty list")
        safe_sources = sorted({source for source in sources if isinstance(source, str) and source})
        if not safe_sources:
            raise ValueError("signal sources contain no valid references")
        return {
            "what": what,
            "when": when,
            "value": float(value),
            "confidence": float(confidence),
            "severity": severity,
            "sources": safe_sources[:5],
        }
