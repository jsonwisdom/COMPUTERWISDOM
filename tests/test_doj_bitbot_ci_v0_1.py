from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

fetch_stage = load("doj_bitbot_fetch_v0_1", ROOT/"executables"/"doj_bitbot_fetch_v0_1.py")
replay_stage = load("doj_bitbot_replay_v0_1", ROOT/"executables"/"doj_bitbot_replay_v0_1.py")
ci_stage = load("doj_bitbot_ci_v0_1", ROOT/"executables"/"doj_bitbot_ci_v0_1.py")


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    obs = tmp_path/"observations"
    obj = tmp_path/"objects"/"sha256"
    rep = tmp_path/"replay"
    poc = tmp_path/"poc"
    obs.mkdir(parents=True)
    obj.mkdir(parents=True)
    rep.mkdir(parents=True)
    poc.mkdir(parents=True)

    monkeypatch.setattr(fetch_stage, "OBSERVATIONS_DIR", obs)
    monkeypatch.setattr(fetch_stage, "OBJECTS_DIR", obj)
    monkeypatch.setattr(replay_stage, "REPLAYS_DIR", rep)
    monkeypatch.setattr(ci_stage, "SPECIMEN_ROOT", poc)

    # Prove CI never calls the network-bearing operations.
    monkeypatch.setattr(fetch_stage, "fetch", lambda *a, **k: (_ for _ in ()).throw(AssertionError("CI called fetch")))
    monkeypatch.setattr(replay_stage, "replay", lambda *a, **k: (_ for _ in ()).throw(AssertionError("CI called replay")))
    return tmp_path


def make_obs(obs_id, state, *, url="https://www.justice.gov/x", payload=None,
             at=None, resolved="https://www.justice.gov/x"):
    if at is None:
        at = datetime.now(timezone.utc)
    status = 200
    if state == "HOLD_NOT_FOUND":
        status = 404
    elif state == "HOLD_HTTP_FAILURE":
        status = 403
    elif state == "HOLD_NETWORK":
        status = None
        resolved = None

    sha = path = length = None
    if state == "OBSERVED_BYTES":
        assert payload is not None
        sha = hashlib.sha256(payload).hexdigest()
        p = fetch_stage.OBJECTS_DIR/sha[:2]/sha
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(payload)
        path = str(p)
        length = len(payload)

    o = fetch_stage.Observation(
        observation_id=obs_id, requested_url=url, resolved_url=resolved,
        observed_at=at, http_status=status, byte_length=length, sha256=sha,
        object_path=path, state=state, authority_created=False,
    )
    fetch_stage._write_observation_atomic(o)
    return o


def make_replay(replay_id, first, second):
    f1, h1, _ = replay_stage._load_stored_observation(first.observation_id)
    f2, h2, _ = replay_stage._load_stored_observation(second.observation_id)
    fv = replay_stage._verify_observed_object(f1)
    sv = replay_stage._verify_observed_object(f2)
    rc, rch = replay_stage._resolution_comparison(f1, f2)
    cc, cch = replay_stage._redirect_comparison(f1, f2)
    receipt = replay_stage.ReplayReceipt(
        replay_id=replay_id,
        first_observation_id=f1.observation_id,
        first_observation_sha256=h1,
        second_observation_id=f2.observation_id,
        second_observation_sha256=h2,
        requested_url=f1.requested_url,
        first_state=f1.state,
        second_state=f2.state,
        first_source_sha256=f1.sha256,
        second_source_sha256=f2.sha256,
        content_result=replay_stage._content_result(f1, f2, fv, sv),
        availability_transition=replay_stage._availability_transition(f1, f2),
        resolved_url_comparable=rc,
        resolved_url_changed=rch,
        redirect_chain_comparable=cc,
        redirect_chain_changed=cch,
        authority_created=False,
    )
    replay_stage._write_replay_receipt_immutable(receipt)
    return receipt


def test_no_observation_pending_first_fetch():
    c=ci_stage.ci_evaluate("https://www.justice.gov/x")
    assert c.verdict=="PENDING_FIRST_FETCH"


def test_observed_without_replay_requires_replay():
    make_obs("DOJ-OBS-A","OBSERVED_BYTES",payload=b"x")
    assert ci_stage.ci_evaluate("https://www.justice.gov/x").verdict=="REPLAY_REQUIRED"


def test_exact_replay_stable_available():
    t=datetime.now(timezone.utc)
    a=make_obs("DOJ-OBS-A","OBSERVED_BYTES",payload=b"x",at=t)
    b=make_obs("DOJ-OBS-B","OBSERVED_BYTES",payload=b"x",at=t+timedelta(seconds=1))
    make_replay("DOJ-REPLAY-1",a,b)
    c=ci_stage.ci_evaluate(a.requested_url)
    assert c.verdict=="STABLE_AVAILABLE" and c.latest_replay_id=="DOJ-REPLAY-1"


def test_changed_replay_source_changed():
    t=datetime.now(timezone.utc)
    a=make_obs("DOJ-OBS-A","OBSERVED_BYTES",payload=b"a",at=t)
    b=make_obs("DOJ-OBS-B","OBSERVED_BYTES",payload=b"b",at=t+timedelta(seconds=1))
    make_replay("DOJ-REPLAY-2",a,b)
    assert ci_stage.ci_evaluate(a.requested_url).verdict=="SOURCE_CHANGED"


@pytest.mark.parametrize("first_state,second_state,expected",[
    ("OBSERVED_BYTES","HOLD_NOT_FOUND","SOURCE_DISAPPEARED"),
    ("HOLD_NOT_FOUND","OBSERVED_BYTES","SOURCE_APPEARED"),
    ("OBSERVED_BYTES","HOLD_HTTP_FAILURE","SOURCE_BLOCKED"),
    ("HOLD_HTTP_FAILURE","OBSERVED_BYTES","SOURCE_BECAME_AVAILABLE"),
    ("OBSERVED_BYTES","HOLD_NETWORK","FETCH_FAILURE"),
])
def test_transition_verdicts(first_state,second_state,expected):
    t=datetime.now(timezone.utc)
    p1=b"x" if first_state=="OBSERVED_BYTES" else None
    p2=b"x" if second_state=="OBSERVED_BYTES" else None
    a=make_obs("DOJ-OBS-A-"+first_state,first_state,payload=p1,at=t)
    b=make_obs("DOJ-OBS-B-"+second_state,second_state,payload=p2,at=t+timedelta(seconds=1))
    make_replay("DOJ-REPLAY-"+expected,a,b)
    assert ci_stage.ci_evaluate(a.requested_url).verdict==expected


def test_failure_without_replay_is_fetch_failure():
    make_obs("DOJ-OBS-404","HOLD_NOT_FOUND")
    assert ci_stage.ci_evaluate("https://www.justice.gov/x").verdict=="FETCH_FAILURE"


def test_valid_unmapped_replay_is_observation_anomaly():
    t=datetime.now(timezone.utc)
    a=make_obs("DOJ-OBS-X","HOLD_NOT_FOUND",at=t)
    b=make_obs("DOJ-OBS-Y","HOLD_NOT_FOUND",at=t+timedelta(seconds=1))
    make_replay("DOJ-REPLAY-OTHER",a,b)
    assert ci_stage.ci_evaluate(a.requested_url).verdict=="OBSERVATION_ANOMALY"


def test_stale_replay_does_not_satisfy_latest_observation():
    t=datetime.now(timezone.utc)
    a=make_obs("DOJ-OBS-A","OBSERVED_BYTES",payload=b"x",at=t)
    b=make_obs("DOJ-OBS-B","OBSERVED_BYTES",payload=b"x",at=t+timedelta(seconds=1))
    make_replay("DOJ-REPLAY-OLD",a,b)
    make_obs("DOJ-OBS-C","OBSERVED_BYTES",payload=b"x",at=t+timedelta(seconds=2))
    c=ci_stage.ci_evaluate(a.requested_url)
    assert c.verdict=="REPLAY_REQUIRED" and c.latest_observation_id=="DOJ-OBS-C"


def test_forged_replay_hash_holds_integrity():
    t=datetime.now(timezone.utc)
    a=make_obs("DOJ-OBS-A","OBSERVED_BYTES",payload=b"x",at=t)
    b=make_obs("DOJ-OBS-B","OBSERVED_BYTES",payload=b"x",at=t+timedelta(seconds=1))
    r=make_replay("DOJ-REPLAY-FORGE",a,b)
    p=replay_stage.REPLAYS_DIR/f"{r.replay_id}.json"
    d=json.loads(p.read_text())
    d["second_observation_sha256"]="0"*64
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    assert ci_stage.ci_evaluate(a.requested_url).verdict=="EVIDENCE_INTEGRITY_HOLD"


def test_corrupt_latest_object_holds_integrity():
    o=make_obs("DOJ-OBS-CORRUPT","OBSERVED_BYTES",payload=b"good")
    Path(o.object_path).write_bytes(b"evil")
    assert ci_stage.ci_evaluate(o.requested_url).verdict=="EVIDENCE_INTEGRITY_HOLD"


def test_duplicate_replay_ending_latest_holds_ambiguity():
    t=datetime.now(timezone.utc)
    a=make_obs("DOJ-OBS-A","OBSERVED_BYTES",payload=b"x",at=t)
    b=make_obs("DOJ-OBS-B","OBSERVED_BYTES",payload=b"x",at=t+timedelta(seconds=1))
    make_replay("DOJ-REPLAY-1",a,b)
    make_replay("DOJ-REPLAY-2",a,b)
    assert ci_stage.ci_evaluate(a.requested_url).verdict=="EVIDENCE_AMBIGUITY_HOLD"


def test_poc_pending_without_url_holds_primary_bytes():
    d=ci_stage.SPECIMEN_ROOT/"0001"
    d.mkdir()
    (d/"rule.json").write_text(json.dumps({
        "poc_id":"INTERNAL_RULES_SCHISM_POC_0001",
        "source_attestation":{"canonical_url":None}
    }))
    c=ci_stage.ci_evaluate("INTERNAL_RULES_SCHISM_POC_0001")
    assert c.verdict=="HOLD_PRIMARY_BYTES"
    assert c.primary_source_verified is False


def test_missing_specimen_is_explicit():
    assert ci_stage.ci_evaluate("NO_SUCH_SPECIMEN").verdict=="RULE_SPECIMEN_NOT_FOUND"


def test_specimen_with_url_delegates_to_url_evidence():
    d=ci_stage.SPECIMEN_ROOT/"0002"
    d.mkdir()
    url="https://www.justice.gov/y"
    (d/"rule.json").write_text(json.dumps({
        "poc_id":"POC_2","source_attestation":{"canonical_url":url}
    }))
    c=ci_stage.ci_evaluate("POC_2")
    assert c.verdict=="PENDING_FIRST_FETCH"
    assert c.target==url and c.rule_specimen_id=="POC_2"


def test_ci_certificate_rejects_authority_true():
    with pytest.raises(AssertionError,match="may never create authority"):
        ci_stage.CiCertificate(
            ci_id="x",target="u",rule_specimen_id=None,
            latest_observation_id=None,latest_observation_state=None,
            latest_replay_id=None,latest_replay_content_result=None,
            latest_replay_availability=None,verdict="X",verdict_reason="X",
            authority_created=True
        )


def test_ci_certificate_rejects_primary_verification_promotion():
    with pytest.raises(AssertionError,match="may never promote"):
        ci_stage.CiCertificate(
            ci_id="x",target="u",rule_specimen_id=None,
            latest_observation_id=None,latest_observation_state=None,
            latest_replay_id=None,latest_replay_content_result=None,
            latest_replay_availability=None,verdict="X",verdict_reason="X",
            primary_source_verified=True
        )


def test_certificate_id_is_deterministic():
    a=ci_stage.ci_evaluate("https://www.justice.gov/x")
    b=ci_stage.ci_evaluate("https://www.justice.gov/x")
    assert a==b and a.ci_id.startswith("DOJ-CI-")


def test_ci_never_calls_fetch_or_replay():
    # Fixture monkeypatches both to raise. Reaching a verdict proves read-only execution.
    assert ci_stage.ci_evaluate("https://www.justice.gov/x").verdict=="PENDING_FIRST_FETCH"


def test_ci_evaluate_has_single_target_argument():
    assert list(inspect.signature(ci_stage.ci_evaluate).parameters)==["target"]


def test_invalid_target_rejected():
    with pytest.raises(ValueError):
        ci_stage.ci_evaluate("")
