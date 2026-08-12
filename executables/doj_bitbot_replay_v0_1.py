#!/usr/bin/env python3
"""DOJ BitBot v0.1 replay stage.

Loads one immutable prior observation from storage, re-fetches exactly that
observation's requested URL through the certified fetch stage, compares the
two immutable observations, and publishes a separate immutable replay receipt.

Replay is evidentiary only. It never creates legal or policy authority.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import doj_bitbot_fetch_v0_1 as fetch_stage

Observation = fetch_stage.Observation
REPLAYS_DIR = fetch_stage.BITBOT_ROOT / "replay"


@dataclass(frozen=True)
class ReplayReceipt:
    replay_id: str
    first_observation_id: str
    first_observation_sha256: str
    second_observation_id: str
    second_observation_sha256: str
    requested_url: str
    first_state: str
    second_state: str
    first_source_sha256: Optional[str]
    second_source_sha256: Optional[str]
    content_result: str
    availability_transition: str
    resolved_url_comparable: bool
    resolved_url_changed: Optional[bool]
    redirect_chain_comparable: bool
    redirect_chain_changed: Optional[bool]
    authority_created: bool = False
    schema: str = "doj.bitbot.replay.v0.1"

    def __post_init__(self) -> None:
        if self.authority_created:
            raise AssertionError("DOJ BitBot replay may never create authority")
        if self.schema != "doj.bitbot.replay.v0.1":
            raise AssertionError("Unexpected DOJ BitBot replay schema")


def _observation_file_path(observation_id: str) -> Path:
    return fetch_stage.OBSERVATIONS_DIR / f"{observation_id}.json"


def _observation_record_hash_from_bytes(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def _load_stored_observation(observation_id: str) -> tuple[Observation, str, bytes]:
    path = _observation_file_path(observation_id)
    if not path.exists():
        raise FileNotFoundError(f"Observation {observation_id} not found at {path}")

    file_bytes = path.read_bytes()
    record_hash = _observation_record_hash_from_bytes(file_bytes)
    data = json.loads(file_bytes.decode("utf-8"))

    obs = Observation(
        observation_id=data["observation_id"],
        requested_url=data["requested_url"],
        resolved_url=data["resolved_url"],
        observed_at=datetime.fromisoformat(data["observed_at"]),
        http_status=data["http_status"],
        redirect_chain=tuple(data["redirect_chain"]),
        media_type=data["media_type"],
        byte_length=data["byte_length"],
        sha256=data["sha256"],
        object_path=data["object_path"],
        state=data["state"],
        primary_source_candidate=data["primary_source_candidate"],
        primary_source_verified=data["primary_source_verified"],
        authority_created=data["authority_created"],
    )

    if obs.observation_id != observation_id:
        raise RuntimeError(
            f"Observation identity mismatch: requested {observation_id}, "
            f"stored {obs.observation_id}"
        )

    return obs, record_hash, file_bytes


def _verify_observed_object(obs: Observation) -> bool:
    if obs.state != "OBSERVED_BYTES":
        return False
    if not obs.sha256 or not obs.object_path:
        return False

    expected_path = fetch_stage.OBJECTS_DIR / obs.sha256[:2] / obs.sha256
    actual_path = Path(obs.object_path)

    if actual_path != expected_path or not actual_path.is_file():
        return False

    return hashlib.sha256(actual_path.read_bytes()).hexdigest() == obs.sha256


def _availability_transition(first: Observation, second: Observation) -> str:
    if second.state == "HOLD_NETWORK":
        return "NETWORK_FAILURE"

    first_available = first.state == "OBSERVED_BYTES"
    second_available = second.state == "OBSERVED_BYTES"

    if first_available and second_available:
        return "AVAILABLE_TO_AVAILABLE"
    if first_available and second.state == "HOLD_NOT_FOUND":
        return "AVAILABLE_TO_MISSING"
    if first.state == "HOLD_NOT_FOUND" and second_available:
        return "MISSING_TO_AVAILABLE"
    if first_available and second.state == "HOLD_HTTP_FAILURE":
        return "AVAILABLE_TO_BLOCKED"
    if first.state == "HOLD_HTTP_FAILURE" and second_available:
        return "BLOCKED_TO_AVAILABLE"
    return "OTHER"


def _content_result(
    first: Observation,
    second: Observation,
    first_object_verified: bool,
    second_object_verified: bool,
) -> str:
    if (
        first.state == "OBSERVED_BYTES"
        and second.state == "OBSERVED_BYTES"
        and first_object_verified
        and second_object_verified
    ):
        return "EXACT" if first.sha256 == second.sha256 else "CHANGED"
    return "NOT_COMPARABLE"


def _resolution_comparison(
    first: Observation,
    second: Observation,
) -> tuple[bool, Optional[bool]]:
    if first.resolved_url is None or second.resolved_url is None:
        return False, None
    return True, first.resolved_url != second.resolved_url


def _redirect_comparison(
    first: Observation,
    second: Observation,
) -> tuple[bool, Optional[bool]]:
    if first.resolved_url is None or second.resolved_url is None:
        return False, None
    return True, first.redirect_chain != second.redirect_chain


def _write_replay_receipt_immutable(receipt: ReplayReceipt) -> Path:
    REPLAYS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPLAYS_DIR / f"{receipt.replay_id}.json"
    payload = (
        json.dumps(asdict(receipt), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=REPLAYS_DIR,
        delete=False,
    ) as tmp:
        tmp.write(payload)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)

    fetch_stage._publish_temp_exclusive(tmp_path, path)
    return path


def replay(prior_observation_id: str) -> ReplayReceipt:
    if not isinstance(prior_observation_id, str) or not prior_observation_id.strip():
        raise ValueError("prior_observation_id must be a non-empty string")

    prior_obs, prior_record_hash, _ = _load_stored_observation(prior_observation_id)

    if prior_obs.state == "OBSERVED_BYTES" and not _verify_observed_object(prior_obs):
        raise RuntimeError(
            f"Prior observation object integrity failed: {prior_observation_id}"
        )

    current_obs = fetch_stage.fetch(prior_obs.requested_url)

    if current_obs.requested_url != prior_obs.requested_url:
        raise RuntimeError("Replay target substitution detected")

    stored_current, current_record_hash, _ = _load_stored_observation(
        current_obs.observation_id
    )
    if stored_current != current_obs:
        raise RuntimeError("Current observation differs from its stored immutable record")

    if current_obs.state == "OBSERVED_BYTES" and not _verify_observed_object(current_obs):
        raise RuntimeError(
            f"Current observation object integrity failed: {current_obs.observation_id}"
        )

    first_verified = _verify_observed_object(prior_obs)
    second_verified = _verify_observed_object(current_obs)

    resolved_comparable, resolved_changed = _resolution_comparison(
        prior_obs, current_obs
    )
    redirect_comparable, redirect_changed = _redirect_comparison(
        prior_obs, current_obs
    )

    receipt = ReplayReceipt(
        replay_id=f"DOJ-REPLAY-{uuid.uuid4().hex[:12].upper()}",
        first_observation_id=prior_obs.observation_id,
        first_observation_sha256=prior_record_hash,
        second_observation_id=current_obs.observation_id,
        second_observation_sha256=current_record_hash,
        requested_url=prior_obs.requested_url,
        first_state=prior_obs.state,
        second_state=current_obs.state,
        first_source_sha256=prior_obs.sha256,
        second_source_sha256=current_obs.sha256,
        content_result=_content_result(
            prior_obs,
            current_obs,
            first_verified,
            second_verified,
        ),
        availability_transition=_availability_transition(prior_obs, current_obs),
        resolved_url_comparable=resolved_comparable,
        resolved_url_changed=resolved_changed,
        redirect_chain_comparable=redirect_comparable,
        redirect_chain_changed=redirect_changed,
        authority_created=False,
    )

    _write_replay_receipt_immutable(receipt)
    return receipt


def main() -> int:
    import sys

    if len(sys.argv) != 2:
        print("Usage: doj_bitbot_replay_v0_1.py <observation_id>")
        return 1

    try:
        receipt = replay(sys.argv[1])
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps(asdict(receipt), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
