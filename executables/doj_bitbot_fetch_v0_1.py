#!/usr/bin/env python3
"""DOJ BitBot v0.1 fetch stage.

Evidence navigator only. Fetch records observations and exact bytes when a
request resolves to a successful 2xx response. Expected HTTP and network
failures are represented as observation states. This module never creates
legal or policy authority and does not mutate Internal Rules Schism specimens.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests

BITBOT_ROOT = Path("doj-bitbot")
OBSERVATIONS_DIR = BITBOT_ROOT / "observations"
OBJECTS_DIR = BITBOT_ROOT / "objects" / "sha256"
PRIMARY_SOURCE_DOMAINS = {"justice.gov"}


@dataclass(frozen=True)
class Observation:
    observation_id: str
    requested_url: str
    resolved_url: Optional[str]
    observed_at: datetime
    http_status: Optional[int]
    redirect_chain: tuple[str, ...] = field(default_factory=tuple)
    media_type: Optional[str] = None
    byte_length: Optional[int] = None
    sha256: Optional[str] = None
    object_path: Optional[str] = None
    state: str = "HOLD_UNKNOWN"
    primary_source_candidate: bool = False
    primary_source_verified: bool = False
    authority_created: bool = False

    def __post_init__(self) -> None:
        if self.authority_created:
            raise AssertionError("DOJ BitBot v0.1 may never create authority")


def _compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _publish_temp_exclusive(tmp_path: Path, final_path: Path) -> None:
    """Atomically publish tmp_path without overwriting final_path."""
    try:
        os.link(tmp_path, final_path)
    finally:
        tmp_path.unlink(missing_ok=True)


def _write_object_immutable(sha256: str, data: bytes) -> Path:
    """Write/reuse one content-addressed object without overwriting bytes."""
    path = OBJECTS_DIR / sha256[:2] / sha256
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        existing_hash = _compute_sha256(path.read_bytes())
        if existing_hash != sha256:
            raise RuntimeError(
                f"Content-addressed object corruption: expected {sha256}, got {existing_hash}"
            )
        return path

    with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, delete=False) as tmp:
        tmp.write(data)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)

    written_hash = _compute_sha256(tmp_path.read_bytes())
    if written_hash != sha256:
        tmp_path.unlink(missing_ok=True)
        raise RuntimeError(
            f"Hash mismatch on staged write: expected {sha256}, got {written_hash}"
        )

    try:
        _publish_temp_exclusive(tmp_path, path)
    except FileExistsError:
        # Another writer won the race. Reuse only if the published object is exact.
        existing_hash = _compute_sha256(path.read_bytes())
        if existing_hash != sha256:
            raise RuntimeError(
                f"Concurrent publication conflict: expected {sha256}, got {existing_hash}"
            )

    return path


def _write_observation_atomic(obs: Observation) -> Path:
    """Publish immutable observation JSON without overwriting an existing ID."""
    OBSERVATIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = OBSERVATIONS_DIR / f"{obs.observation_id}.json"
    data = asdict(obs)
    data["observed_at"] = obs.observed_at.isoformat()
    data["redirect_chain"] = list(obs.redirect_chain)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=OBSERVATIONS_DIR,
        delete=False,
        suffix=".json",
    ) as tmp:
        json.dump(data, tmp, indent=2, sort_keys=True)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)

    try:
        _publish_temp_exclusive(tmp_path, path)
    except FileExistsError as exc:
        raise RuntimeError(f"Observation ID collision: {obs.observation_id}") from exc

    return path


def _is_primary_source_domain(url: str) -> bool:
    """Return true only for justice.gov or a justice.gov subdomain."""
    hostname = (urlparse(url).hostname or "").lower()
    return hostname == "justice.gov" or hostname.endswith(".justice.gov")


def _network_observation(obs_id: str, url: str, observed_at: datetime, state: str) -> Observation:
    return Observation(
        observation_id=obs_id,
        requested_url=url,
        resolved_url=None,
        observed_at=observed_at,
        http_status=None,
        state=state,
        primary_source_candidate=False,
        primary_source_verified=False,
        authority_created=False,
    )


def fetch(url: str, timeout: int = 30) -> Observation:
    """Fetch one URL and return a completed immutable observation.

    HTTP status failures, redirects, timeouts, DNS/connection/transport failures,
    and redirect loops are represented in Observation.state. Invalid arguments or
    malformed request configuration raise because a trustworthy fetch observation
    cannot be constructed from them.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("url must be a non-empty string")
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError("timeout must be a positive number")

    obs_id = f"DOJ-OBS-{uuid.uuid4().hex[:12].upper()}"
    observed_at = datetime.now(timezone.utc)

    try:
        with requests.Session() as session:
            session.max_redirects = 10
            response = session.get(url, timeout=timeout, allow_redirects=True)

        resolved_url = response.url
        redirect_chain = tuple(r.url for r in response.history)
        status = response.status_code

        state = "HOLD_UNKNOWN"
        sha256 = None
        byte_length = None
        media_type = None
        object_path = None
        primary_source_candidate = False

        if 200 <= status < 300:
            data = response.content
            sha256 = _compute_sha256(data)
            byte_length = len(data)
            media_type = (
                response.headers.get("content-type", "application/octet-stream")
                .split(";", 1)[0]
                .strip()
            )
            try:
                object_path = str(_write_object_immutable(sha256, data))
                state = "OBSERVED_BYTES"
                primary_source_candidate = _is_primary_source_domain(resolved_url)
            except RuntimeError:
                state = "FAIL_PROVENANCE"
                object_path = str(OBJECTS_DIR / sha256[:2] / sha256)

        elif status in (401, 403):
            state = "HOLD_HTTP_FAILURE"
        elif status == 404:
            state = "HOLD_NOT_FOUND"

        obs = Observation(
            observation_id=obs_id,
            requested_url=url,
            resolved_url=resolved_url,
            observed_at=observed_at,
            http_status=status,
            redirect_chain=redirect_chain,
            media_type=media_type,
            byte_length=byte_length,
            sha256=sha256,
            object_path=object_path,
            state=state,
            primary_source_candidate=primary_source_candidate,
            primary_source_verified=False,
            authority_created=False,
        )

    except requests.exceptions.TooManyRedirects:
        obs = _network_observation(obs_id, url, observed_at, "HOLD_REDIRECT_LOOP")
    except (
        requests.exceptions.InvalidURL,
        requests.exceptions.InvalidSchema,
        requests.exceptions.MissingSchema,
    ) as exc:
        raise ValueError(f"invalid request URL/configuration: {exc}") from exc
    except requests.exceptions.RequestException:
        obs = _network_observation(obs_id, url, observed_at, "HOLD_NETWORK")

    # Redundant defense: Observation.__post_init__ enforces the same invariant.
    if obs.authority_created:
        raise AssertionError("DOJ BitBot v0.1 may never create authority")

    _write_observation_atomic(obs)
    return obs


def main() -> int:
    import sys

    if len(sys.argv) != 2:
        print("Usage: doj_bitbot_fetch_v0_1.py <URL>")
        return 1
    obs = fetch(sys.argv[1])
    print(
        json.dumps(
            {
                "observation_id": obs.observation_id,
                "state": obs.state,
                "authority_created": obs.authority_created,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
