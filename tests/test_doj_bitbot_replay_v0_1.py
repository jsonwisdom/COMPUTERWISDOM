from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
FETCH_PATH = ROOT / "executables" / "doj_bitbot_fetch_v0_1.py"
REPLAY_PATH = ROOT / "executables" / "doj_bitbot_replay_v0_1.py"

fetch_spec = importlib.util.spec_from_file_location("doj_bitbot_fetch_v0_1", FETCH_PATH)
fetch_stage = importlib.util.module_from_spec(fetch_spec)
assert fetch_spec.loader is not None
sys.modules["doj_bitbot_fetch_v0_1"] = fetch_stage
fetch_spec.loader.exec_module(fetch_stage)

replay_spec = importlib.util.spec_from_file_location("doj_bitbot_replay_v0_1", REPLAY_PATH)
replay_stage = importlib.util.module_from_spec(replay_spec)
assert replay_spec.loader is not None
sys.modules["doj_bitbot_replay_v0_1"] = replay_stage
replay_spec.loader.exec_module(replay_stage)


class FakeResponse:
    def __init__(self, status, url, content=b"", headers=None, history=None):
        self.status_code = status
        self.url = url
        self.content = content
        self.headers = headers or {}
        self.history = history or []


class FakeSession:
    response = None
    exc = None

    def __init__(self):
        self.max_redirects = 10

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get(self, *args, **kwargs):
        if self.exc is not None:
            raise self.exc
        return self.response


@pytest.fixture(autouse=True)
def isolated_store(tmp_path, monkeypatch):
    observations = tmp_path / "observations"
    objects = tmp_path / "objects" / "sha256"
    replays = tmp_path / "replay"
    observations.mkdir(parents=True)
    objects.mkdir(parents=True)
    replays.mkdir(parents=True)

    monkeypatch.setattr(fetch_stage, "OBSERVATIONS_DIR", observations)
    monkeypatch.setattr(fetch_stage, "OBJECTS_DIR", objects)
    monkeypatch.setattr(replay_stage, "REPLAYS_DIR", replays)
    monkeypatch.setattr(fetch_stage.requests, "Session", FakeSession)

    FakeSession.response = None
    FakeSession.exc = None
    return tmp_path


def _stored_prior(
    observation_id,
    state,
    *,
    payload=None,
    requested_url="https://www.justice.gov/x",
    resolved_url="https://www.justice.gov/x",
    redirects=(),
):
    status = 200
    if state == "HOLD_NOT_FOUND":
        status = 404
    elif state == "HOLD_HTTP_FAILURE":
        status = 403
    elif state == "HOLD_NETWORK":
        status = None
        resolved_url = None
    elif state == "FAIL_PROVENANCE":
        status = 200

    sha256 = None
    object_path = None
    byte_length = None
    if state == "OBSERVED_BYTES":
        assert payload is not None
        sha256 = hashlib.sha256(payload).hexdigest()
        path = fetch_stage.OBJECTS_DIR / sha256[:2] / sha256
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        object_path = str(path)
        byte_length = len(payload)

    obs = fetch_stage.Observation(
        observation_id=observation_id,
        requested_url=requested_url,
        resolved_url=resolved_url,
        observed_at=datetime.now(timezone.utc),
        http_status=status,
        redirect_chain=tuple(redirects),
        byte_length=byte_length,
        sha256=sha256,
        object_path=object_path,
        state=state,
        authority_created=False,
    )
    fetch_stage._write_observation_atomic(obs)
    return obs


def _response(status, *, payload=b"", resolved="https://www.justice.gov/x", redirects=()):
    history = [FakeResponse(302, url) for url in redirects]
    FakeSession.response = FakeResponse(
        status,
        resolved,
        payload,
        {"content-type": "application/pdf"},
        history,
    )


def test_same_bytes_exact_and_available():
    prior = _stored_prior("DOJ-OBS-1", "OBSERVED_BYTES", payload=b"same")
    _response(200, payload=b"same")
    receipt = replay_stage.replay(prior.observation_id)
    assert receipt.content_result == "EXACT"
    assert receipt.availability_transition == "AVAILABLE_TO_AVAILABLE"


def test_different_bytes_changed():
    prior = _stored_prior("DOJ-OBS-2", "OBSERVED_BYTES", payload=b"a")
    _response(200, payload=b"b")
    assert replay_stage.replay(prior.observation_id).content_result == "CHANGED"


def test_missing_to_available():
    prior = _stored_prior("DOJ-OBS-3", "HOLD_NOT_FOUND")
    _response(200, payload=b"new")
    assert replay_stage.replay(prior.observation_id).availability_transition == "MISSING_TO_AVAILABLE"


def test_available_to_missing():
    prior = _stored_prior("DOJ-OBS-4", "OBSERVED_BYTES", payload=b"x")
    _response(404, payload=b"ignored")
    assert replay_stage.replay(prior.observation_id).availability_transition == "AVAILABLE_TO_MISSING"


def test_available_to_blocked():
    prior = _stored_prior("DOJ-OBS-5", "OBSERVED_BYTES", payload=b"x")
    _response(403, payload=b"ignored")
    assert replay_stage.replay(prior.observation_id).availability_transition == "AVAILABLE_TO_BLOCKED"


def test_blocked_to_available():
    prior = _stored_prior("DOJ-OBS-6", "HOLD_HTTP_FAILURE")
    _response(200, payload=b"x")
    assert replay_stage.replay(prior.observation_id).availability_transition == "BLOCKED_TO_AVAILABLE"


def test_network_failure_is_distinct_and_not_resolution_comparable():
    prior = _stored_prior(
        "DOJ-OBS-7",
        "OBSERVED_BYTES",
        payload=b"x",
        resolved_url="https://www.justice.gov/final",
        redirects=("https://justice.gov/start",),
    )
    FakeSession.exc = requests.exceptions.ConnectionError("network")
    receipt = replay_stage.replay(prior.observation_id)
    assert receipt.availability_transition == "NETWORK_FAILURE"
    assert receipt.content_result == "NOT_COMPARABLE"
    assert receipt.resolved_url_comparable is False
    assert receipt.resolved_url_changed is None
    assert receipt.redirect_chain_comparable is False
    assert receipt.redirect_chain_changed is None


def test_network_failure_from_missing_is_still_network_failure():
    prior = _stored_prior("DOJ-OBS-8", "HOLD_NOT_FOUND")
    FakeSession.exc = requests.exceptions.Timeout("timeout")
    assert replay_stage.replay(prior.observation_id).availability_transition == "NETWORK_FAILURE"


def test_same_bytes_redirect_change_keeps_content_exact():
    prior = _stored_prior(
        "DOJ-OBS-9",
        "OBSERVED_BYTES",
        payload=b"x",
        resolved_url="https://www.justice.gov/a",
        redirects=("https://justice.gov/old",),
    )
    _response(
        200,
        payload=b"x",
        resolved="https://www.justice.gov/b",
        redirects=("https://justice.gov/new",),
    )
    receipt = replay_stage.replay(prior.observation_id)
    assert receipt.content_result == "EXACT"
    assert receipt.resolved_url_comparable is True
    assert receipt.resolved_url_changed is True
    assert receipt.redirect_chain_comparable is True
    assert receipt.redirect_chain_changed is True


def test_prior_not_in_storage():
    with pytest.raises(FileNotFoundError):
        replay_stage.replay("DOJ-OBS-NOT-THERE")


def test_prior_record_identity_mismatch_is_rejected():
    path = fetch_stage.OBSERVATIONS_DIR / "DOJ-OBS-FILENAME.json"
    data = {
        "observation_id": "DOJ-OBS-DIFFERENT",
        "requested_url": "https://www.justice.gov/x",
        "resolved_url": None,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "http_status": 404,
        "redirect_chain": [],
        "media_type": None,
        "byte_length": None,
        "sha256": None,
        "object_path": None,
        "state": "HOLD_NOT_FOUND",
        "primary_source_candidate": False,
        "primary_source_verified": False,
        "authority_created": False,
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="identity mismatch"):
        replay_stage.replay("DOJ-OBS-FILENAME")


def test_prior_object_corruption_fails_before_refetch():
    prior = _stored_prior("DOJ-OBS-10", "OBSERVED_BYTES", payload=b"good")
    Path(prior.object_path).write_bytes(b"evil")
    _response(200, payload=b"current")
    with pytest.raises(RuntimeError, match="Prior observation object integrity failed"):
        replay_stage.replay(prior.observation_id)


def test_fail_provenance_cannot_masquerade_as_exact():
    first = fetch_stage.Observation(
        observation_id="A",
        requested_url="u",
        resolved_url="u",
        observed_at=datetime.now(timezone.utc),
        http_status=200,
        sha256="a" * 64,
        state="FAIL_PROVENANCE",
    )
    second = fetch_stage.Observation(
        observation_id="B",
        requested_url="u",
        resolved_url="u",
        observed_at=datetime.now(timezone.utc),
        http_status=200,
        sha256="a" * 64,
        state="FAIL_PROVENANCE",
    )
    assert replay_stage._content_result(first, second, False, False) == "NOT_COMPARABLE"


def test_record_hash_binds_exact_stored_json_bytes():
    prior = _stored_prior("DOJ-OBS-11", "HOLD_NOT_FOUND")
    path = fetch_stage.OBSERVATIONS_DIR / f"{prior.observation_id}.json"
    _, record_hash, file_bytes = replay_stage._load_stored_observation(prior.observation_id)
    assert record_hash == hashlib.sha256(path.read_bytes()).hexdigest()
    assert record_hash == hashlib.sha256(file_bytes).hexdigest()


def test_prior_record_never_mutated():
    prior = _stored_prior("DOJ-OBS-12", "OBSERVED_BYTES", payload=b"x")
    path = fetch_stage.OBSERVATIONS_DIR / f"{prior.observation_id}.json"
    before = path.read_bytes()
    _response(200, payload=b"x")
    replay_stage.replay(prior.observation_id)
    assert path.read_bytes() == before


def test_replay_receipt_collision_never_overwrites(monkeypatch):
    prior = _stored_prior("DOJ-OBS-13", "OBSERVED_BYTES", payload=b"x")
    _response(200, payload=b"x")

    class FixedUUID:
        hex = "FIXED00000000ABCDEF"

    monkeypatch.setattr(replay_stage.uuid, "uuid4", lambda: FixedUUID())
    target = replay_stage.REPLAYS_DIR / f"DOJ-REPLAY-{FixedUUID.hex[:12]}.json"
    target.write_text('{"old": true}\n', encoding="utf-8")

    with pytest.raises(FileExistsError):
        replay_stage.replay(prior.observation_id)

    assert json.loads(target.read_text(encoding="utf-8")) == {"old": True}


def test_authority_true_rejected_at_replay_receipt_construction():
    with pytest.raises(AssertionError, match="may never create authority"):
        replay_stage.ReplayReceipt(
            replay_id="R",
            first_observation_id="A",
            first_observation_sha256="h",
            second_observation_id="B",
            second_observation_sha256="h",
            requested_url="u",
            first_state="x",
            second_state="x",
            first_source_sha256=None,
            second_source_sha256=None,
            content_result="NOT_COMPARABLE",
            availability_transition="OTHER",
            resolved_url_comparable=False,
            resolved_url_changed=None,
            redirect_chain_comparable=False,
            redirect_chain_changed=None,
            authority_created=True,
        )


def test_replay_has_no_url_override_parameter():
    assert list(inspect.signature(replay_stage.replay).parameters) == ["prior_observation_id"]


def test_invalid_prior_id_is_programmer_error():
    with pytest.raises(ValueError):
        replay_stage.replay("")
