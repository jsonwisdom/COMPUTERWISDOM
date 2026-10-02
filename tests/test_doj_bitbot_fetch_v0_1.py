from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
import requests

MODULE_PATH = Path(__file__).resolve().parents[1] / "executables" / "doj_bitbot_fetch_v0_1.py"
spec = importlib.util.spec_from_file_location("doj_bitbot_fetch_v0_1", MODULE_PATH)
bitbot = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bitbot)


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
    observations.mkdir(parents=True)
    objects.mkdir(parents=True)
    monkeypatch.setattr(bitbot, "OBSERVATIONS_DIR", observations)
    monkeypatch.setattr(bitbot, "OBJECTS_DIR", objects)
    FakeSession.response = None
    FakeSession.exc = None
    monkeypatch.setattr(bitbot.requests, "Session", FakeSession)
    return tmp_path


def test_authority_true_rejected_at_construction():
    with pytest.raises(AssertionError, match="may never create authority"):
        bitbot.Observation(
            observation_id="DOJ-OBS-BAD",
            requested_url="https://www.justice.gov/",
            resolved_url=None,
            observed_at=datetime.now(timezone.utc),
            http_status=None,
            authority_created=True,
        )


def test_200_html_captures_exact_bytes_and_marks_candidate():
    payload = b"<html>official</html>"
    FakeSession.response = FakeResponse(
        200,
        "https://www.justice.gov/olc/example",
        payload,
        {"content-type": "text/html; charset=utf-8"},
    )
    obs = bitbot.fetch("https://www.justice.gov/olc/example")
    assert obs.state == "OBSERVED_BYTES"
    assert obs.primary_source_candidate is True
    assert obs.primary_source_verified is False
    assert obs.sha256 == hashlib.sha256(payload).hexdigest()
    assert Path(obs.object_path).read_bytes() == payload
    assert obs.authority_created is False


def test_all_2xx_are_captured():
    FakeSession.response = FakeResponse(
        206,
        "https://www.justice.gov/partial",
        b"partial",
        {"content-type": "application/pdf"},
    )
    obs = bitbot.fetch("https://www.justice.gov/partial")
    assert obs.http_status == 206
    assert obs.state == "OBSERVED_BYTES"
    assert obs.sha256 is not None


def test_redirect_chain_is_metadata_and_final_bytes_are_observed():
    FakeSession.response = FakeResponse(
        200,
        "https://www.justice.gov/final",
        b"abc",
        {"content-type": "application/pdf"},
        history=[
            FakeResponse(301, "https://justice.gov/olc"),
            FakeResponse(302, "https://www.justice.gov/olc"),
        ],
    )
    obs = bitbot.fetch("https://justice.gov/olc")
    assert obs.state == "OBSERVED_BYTES"
    assert obs.redirect_chain == (
        "https://justice.gov/olc",
        "https://www.justice.gov/olc",
    )
    assert obs.resolved_url == "https://www.justice.gov/final"


@pytest.mark.parametrize(
    "status,expected",
    [
        (401, "HOLD_HTTP_FAILURE"),
        (403, "HOLD_HTTP_FAILURE"),
        (404, "HOLD_NOT_FOUND"),
        (500, "HOLD_UNKNOWN"),
    ],
)
def test_non_2xx_never_enters_primary_object_store(status, expected):
    FakeSession.response = FakeResponse(
        status,
        "https://www.justice.gov/problem",
        b"error-body-must-not-be-promoted",
        {"content-type": "text/html"},
    )
    obs = bitbot.fetch("https://www.justice.gov/problem")
    assert obs.state == expected
    assert obs.sha256 is None
    assert obs.object_path is None
    assert obs.primary_source_candidate is False


@pytest.mark.parametrize(
    "exc",
    [
        requests.exceptions.Timeout("timeout"),
        requests.exceptions.ConnectionError("dns/connection"),
        requests.exceptions.SSLError("tls"),
    ],
)
def test_network_transport_failures_become_observations(exc):
    FakeSession.exc = exc
    obs = bitbot.fetch("https://www.justice.gov/olc")
    assert obs.state == "HOLD_NETWORK"
    assert obs.http_status is None
    assert obs.sha256 is None


def test_redirect_loop_becomes_observation():
    FakeSession.exc = requests.exceptions.TooManyRedirects("loop")
    obs = bitbot.fetch("https://www.justice.gov/loop")
    assert obs.state == "HOLD_REDIRECT_LOOP"
    assert obs.authority_created is False


def test_invalid_url_is_programmer_configuration_error():
    FakeSession.exc = requests.exceptions.MissingSchema("missing schema")
    with pytest.raises(ValueError, match="invalid request URL/configuration"):
        bitbot.fetch("justice.gov/no-scheme")


def test_existing_identical_content_addressed_object_is_reused():
    payload = b"same"
    digest = hashlib.sha256(payload).hexdigest()
    path = bitbot.OBJECTS_DIR / digest[:2] / digest
    path.parent.mkdir(parents=True)
    path.write_bytes(payload)

    FakeSession.response = FakeResponse(200, "https://www.justice.gov/x", payload)
    obs = bitbot.fetch("https://www.justice.gov/x")
    assert obs.state == "OBSERVED_BYTES"
    assert Path(obs.object_path) == path
    assert path.read_bytes() == payload


def test_corrupt_existing_content_addressed_object_fails_provenance_without_overwrite():
    payload = b"good"
    digest = hashlib.sha256(payload).hexdigest()
    path = bitbot.OBJECTS_DIR / digest[:2] / digest
    path.parent.mkdir(parents=True)
    path.write_bytes(b"evil")

    FakeSession.response = FakeResponse(200, "https://www.justice.gov/x", payload)
    obs = bitbot.fetch("https://www.justice.gov/x")
    assert obs.state == "FAIL_PROVENANCE"
    assert path.read_bytes() == b"evil"


def test_exclusive_publication_never_overwrites_existing_destination(tmp_path):
    final = tmp_path / "final"
    staged = tmp_path / "staged"
    final.write_bytes(b"existing")
    staged.write_bytes(b"new")

    with pytest.raises(FileExistsError):
        bitbot._publish_temp_exclusive(staged, final)

    assert final.read_bytes() == b"existing"
    assert staged.exists() is False


def test_observation_id_collision_never_overwrites_existing_receipt(monkeypatch):
    fixed_id = "DOJ-OBS-FIXED"
    monkeypatch.setattr(bitbot.uuid, "uuid4", lambda: type("U", (), {"hex": "fixed00000000abcdef"})())
    existing = bitbot.OBSERVATIONS_DIR / "DOJ-OBS-FIXED0000000.json"

    # Direct writer collision is deterministic and avoids relying on UUID slicing details.
    obs = bitbot.Observation(
        observation_id=fixed_id,
        requested_url="https://www.justice.gov/",
        resolved_url=None,
        observed_at=datetime.now(timezone.utc),
        http_status=None,
    )
    existing = bitbot.OBSERVATIONS_DIR / f"{fixed_id}.json"
    existing.write_text('{"old": true}\n', encoding="utf-8")

    with pytest.raises(RuntimeError, match="Observation ID collision"):
        bitbot._write_observation_atomic(obs)

    assert json.loads(existing.read_text(encoding="utf-8")) == {"old": True}


def test_non_doj_success_is_not_primary_source_candidate():
    FakeSession.response = FakeResponse(200, "https://example.com/document", b"bytes")
    obs = bitbot.fetch("https://example.com/document")
    assert obs.state == "OBSERVED_BYTES"
    assert obs.primary_source_candidate is False


def test_domain_suffix_does_not_accept_lookalike():
    assert bitbot._is_primary_source_domain("https://justice.gov/x") is True
    assert bitbot._is_primary_source_domain("https://www.justice.gov/x") is True
    assert bitbot._is_primary_source_domain("https://eviljustice.gov/x") is False
    assert bitbot._is_primary_source_domain("https://justice.gov.evil.example/x") is False


def test_observation_receipt_is_complete_and_authority_false():
    FakeSession.response = FakeResponse(404, "https://www.justice.gov/missing", b"404")
    obs = bitbot.fetch("https://www.justice.gov/missing")
    path = bitbot.OBSERVATIONS_DIR / f"{obs.observation_id}.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["requested_url"] == "https://www.justice.gov/missing"
    assert receipt["http_status"] == 404
    assert receipt["state"] == "HOLD_NOT_FOUND"
    assert receipt["authority_created"] is False
    assert receipt["observed_at"].endswith("+00:00")
