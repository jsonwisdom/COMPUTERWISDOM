import json
from pathlib import Path

import jsonschema

from src.replay_kernel_v0_1 import replay

ROOT = Path(__file__).resolve().parents[1]
ERS_SCHEMA = json.load(open(ROOT / "schemas" / "ers.v0_1.schema.json", encoding="utf-8"))
TRACE_SCHEMA = json.load(open(ROOT / "schemas" / "replay_trace.v0_1.schema.json", encoding="utf-8"))

CONSTITUTIONAL_ROOT = "808f2b1c6c339eb46e68a2161da3cca22f7b0eeb"


def load_example(name):
    return json.load(open(ROOT / "examples" / name, encoding="utf-8"))


def test_replay_is_deterministic_for_same_inputs():
    artifacts = [
        load_example("observation_example.json"),
        load_example("event_example.json"),
    ]
    first = replay(artifacts, ERS_SCHEMA)
    second = replay(list(reversed(artifacts)), ERS_SCHEMA)
    assert first == second


def test_replay_trace_validates_against_schema():
    artifacts = [
        load_example("event_example.json"),
        load_example("observation_example.json"),
    ]
    trace = replay(artifacts, ERS_SCHEMA)
    jsonschema.Draft202012Validator(TRACE_SCHEMA).validate(trace)


def test_replay_preserves_lineage_and_boundary():
    artifacts = [load_example("event_example.json")]
    trace = replay(artifacts, ERS_SCHEMA)

    assert trace["constitutional_root"] == CONSTITUTIONAL_ROOT
    assert trace["authority"] is False
    assert trace["authority_boundary"] == "NONE"
    assert trace["artifact_count"] == 1
    assert trace["ordered_artifact_ids"] == ["ers-event-example-v0-1"]
    assert trace["lineage_edges"] == [
        {
            "artifact_id": "ers-event-example-v0-1",
            "lineage_root": "f5c98f688296d1cece1cb8ac6635421384756f00",
        }
    ]


def test_replay_rejects_authority_escalation():
    artifact = load_example("event_example.json")
    artifact["authority"] = True
    try:
        replay([artifact], ERS_SCHEMA)
    except Exception as exc:
        assert "authority" in str(exc)
    else:
        raise AssertionError("authority escalation was not rejected")
