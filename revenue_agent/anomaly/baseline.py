from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Dict, Tuple

from anomaly.ring import resolve_ring

SNAPSHOT_VERSION = "LOCALITY_SIGNAL_SNAPSHOT_V0_1"
BASELINE_VERSION = "LOCALITY_BASELINE_V0_1"
_ALLOWED_SIGNAL_TYPES = {
    "weather_alert",
    "infrastructure_outage",
    "emergency_broadcast",
    "traffic_disruption",
}


class ImmutableStoreConflict(RuntimeError):
    pass


class SnapshotMissing(FileNotFoundError):
    pass


class BaselineMissing(FileNotFoundError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _validate_baseline_anchor(baseline_anchor: str) -> None:
    if (
        not isinstance(baseline_anchor, str)
        or len(baseline_anchor) != 40
        or any(ch not in "0123456789abcdef" for ch in baseline_anchor)
    ):
        raise ValueError("baseline_anchor must be a full lowercase 40-character git SHA")


def _validate_time_window(time_window: str) -> str:
    if not isinstance(time_window, str) or not time_window:
        raise ValueError("time_window must be a non-empty string")
    value = time_window.strip()
    if len(value) > 32:
        raise ValueError("time_window is too long")
    return value


class _ImmutableJsonStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _key_digest(kind: str, locality: str, time_window: str, baseline_anchor: str) -> str:
        key = {
            "kind": kind,
            "locality": locality,
            "time_window": time_window,
            "baseline_anchor": baseline_anchor,
        }
        return sha256_bytes(canonical_json_bytes(key))

    def _path(self, kind: str, locality: str, time_window: str, baseline_anchor: str) -> Path:
        return self.root / f"{self._key_digest(kind, locality, time_window, baseline_anchor)}.json"

    def _put_once(
        self,
        kind: str,
        locality: str,
        time_window: str,
        baseline_anchor: str,
        payload: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], str]:
        path = self._path(kind, locality, time_window, baseline_anchor)
        data = canonical_json_bytes(payload)
        digest = sha256_bytes(data)
        if path.exists():
            existing = path.read_bytes()
            if existing != data:
                raise ImmutableStoreConflict(f"immutable {kind} already exists with different bytes")
            return json.loads(existing), sha256_bytes(existing)

        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(path, flags, 0o600)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            path.unlink(missing_ok=True)
            raise
        return payload, digest

    def _get(
        self,
        kind: str,
        locality: str,
        time_window: str,
        baseline_anchor: str,
        missing_exc: type[FileNotFoundError],
    ) -> Tuple[Dict[str, Any], str]:
        path = self._path(kind, locality, time_window, baseline_anchor)
        if not path.exists():
            raise missing_exc(f"{kind} is not frozen for this locality/time/baseline")
        data = path.read_bytes()
        return json.loads(data), sha256_bytes(data)


class SnapshotStore(_ImmutableJsonStore):
    def put(
        self,
        locality: str,
        time_window: str,
        baseline_anchor: str,
        signals: list[Dict[str, Any]],
    ) -> Tuple[Dict[str, Any], str]:
        locality_id = resolve_ring(locality).locality_id
        window = _validate_time_window(time_window)
        _validate_baseline_anchor(baseline_anchor)
        payload = {
            "snapshot_version": SNAPSHOT_VERSION,
            "locality": locality_id,
            "time_window": window,
            "baseline_anchor": baseline_anchor,
            "signals": signals,
        }
        return self._put_once("snapshot", locality_id, window, baseline_anchor, payload)

    def get(
        self,
        locality: str,
        time_window: str,
        baseline_anchor: str,
    ) -> Tuple[Dict[str, Any], str]:
        locality_id = resolve_ring(locality).locality_id
        window = _validate_time_window(time_window)
        _validate_baseline_anchor(baseline_anchor)
        return self._get("snapshot", locality_id, window, baseline_anchor, SnapshotMissing)


class BaselineStore(_ImmutableJsonStore):
    def put(
        self,
        locality: str,
        time_window: str,
        baseline_anchor: str,
        metrics: Dict[str, float],
    ) -> Tuple[Dict[str, Any], str]:
        locality_id = resolve_ring(locality).locality_id
        window = _validate_time_window(time_window)
        _validate_baseline_anchor(baseline_anchor)
        if not isinstance(metrics, dict):
            raise TypeError("metrics must be an object")
        normalized: Dict[str, float] = {}
        for key, value in sorted(metrics.items()):
            if key not in _ALLOWED_SIGNAL_TYPES:
                raise ValueError(f"unsupported baseline metric: {key}")
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError(f"baseline metric {key} must be numeric")
            if not math.isfinite(float(value)) or float(value) < 0:
                raise ValueError(f"baseline metric {key} must be finite and non-negative")
            normalized[key] = float(value)
        payload = {
            "baseline_version": BASELINE_VERSION,
            "locality": locality_id,
            "time_window": window,
            "baseline_anchor": baseline_anchor,
            "metrics": normalized,
        }
        return self._put_once("baseline", locality_id, window, baseline_anchor, payload)

    def get(
        self,
        locality: str,
        time_window: str,
        baseline_anchor: str,
    ) -> Tuple[Dict[str, Any], str]:
        locality_id = resolve_ring(locality).locality_id
        window = _validate_time_window(time_window)
        _validate_baseline_anchor(baseline_anchor)
        return self._get("baseline", locality_id, window, baseline_anchor, BaselineMissing)
