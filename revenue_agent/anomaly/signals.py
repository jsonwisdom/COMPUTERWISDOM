from __future__ import annotations

import hashlib
import json
from typing import Any, Callable, Dict, Mapping
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from anomaly.ring import resolve_ring

NWS_ALERTS_ENDPOINT = "https://api.weather.gov/alerts/active"
DEFAULT_USER_AGENT = (
    "COMPUTERWISDOM-locality-anomaly/0.1 "
    "(https://github.com/jsonwisdom/COMPUTERWISDOM)"
)


class SignalConfigurationError(RuntimeError):
    pass


def _severity(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"extreme", "severe"}:
        return "HIGH"
    if normalized == "moderate":
        return "MEDIUM"
    return "LOW"


def _confidence(value: Any) -> float:
    normalized = str(value or "").strip().lower()
    return {
        "observed": 1.0,
        "likely": 0.9,
        "possible": 0.6,
        "unlikely": 0.3,
        "unknown": 0.5,
    }.get(normalized, 0.5)


def _source_ref(value: str) -> str:
    return "nws:sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


class NWSWeatherAlertsSignal:
    """Capture privacy-reduced public NWS alerts for configured ring localities.

    Locality controls map ring IDs to public NWS county/forecast-zone identifiers.
    Raw descriptions, area names, addresses, and person-level data are never retained.
    """

    def __init__(
        self,
        locality_controls: Mapping[str, Mapping[str, str]],
        *,
        user_agent: str = DEFAULT_USER_AGENT,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        self.locality_controls = {
            resolve_ring(locality).locality_id: dict(control)
            for locality, control in locality_controls.items()
        }
        self.user_agent = user_agent
        self.opener = opener or urlopen

    def fetch_all(self, locality: str, time_window: str) -> list[Dict[str, Any]]:
        del time_window  # v0.1 captures the active-alert set; scope is frozen by snapshot.
        locality_id = resolve_ring(locality).locality_id
        control = self.locality_controls.get(locality_id)
        if not control:
            raise SignalConfigurationError(f"no public signal control configured for {locality_id}")
        zone = control.get("nws_zone")
        if not isinstance(zone, str) or not zone.strip():
            raise SignalConfigurationError("locality control must define nws_zone")

        url = f"{NWS_ALERTS_ENDPOINT}?{urlencode({'zone': zone.strip().upper()})}"
        request = Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/geo+json",
            },
        )
        with self.opener(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

        features = payload.get("features", []) if isinstance(payload, dict) else []
        safe_signals: list[Dict[str, Any]] = []
        for feature in features:
            if not isinstance(feature, dict):
                continue
            properties = feature.get("properties")
            if not isinstance(properties, dict):
                continue
            when = (
                properties.get("sent")
                or properties.get("effective")
                or properties.get("onset")
            )
            if not isinstance(when, str) or not when:
                continue
            raw_id = feature.get("id") or properties.get("id") or properties.get("@id")
            if not isinstance(raw_id, str) or not raw_id:
                raw_id = json.dumps(
                    {
                        "when": when,
                        "severity": properties.get("severity"),
                        "certainty": properties.get("certainty"),
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                )
            safe_signals.append(
                {
                    "what": "weather_alert",
                    "when": when,
                    "value": 1.0,
                    "confidence": _confidence(properties.get("certainty")),
                    "severity": _severity(properties.get("severity")),
                    "sources": [_source_ref(raw_id)],
                }
            )

        return sorted(
            safe_signals,
            key=lambda item: (item["when"], item["severity"], item["sources"]),
        )
