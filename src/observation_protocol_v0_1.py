import copy
import json
from pathlib import Path
from typing import Any, Dict

import jsonschema

SCHEMA_VERSION = "OBSERVATION_V0_1"
CONSTITUTIONAL_ROOT = "808f2b1c6c339eb46e68a2161da3cca22f7b0eeb"
AUTHORITY = False
AUTHORITY_BOUNDARY = "NONE"


def load_json(path: str | Path) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_observation(observation: Dict[str, Any], schema: Dict[str, Any]) -> None:
    jsonschema.Draft202012Validator(schema).validate(observation)
    if observation["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if observation["constitutional_root"] != CONSTITUTIONAL_ROOT:
        raise ValueError("constitutional_root mismatch")
    if observation["authority"] is not AUTHORITY:
        raise ValueError("authority must be false")
    if observation["authority_boundary"] != AUTHORITY_BOUNDARY:
        raise ValueError("authority_boundary must be NONE")
    if not (observation.get("observed_artifact_id") or observation.get("observed_trace_id") or observation.get("source_ref")):
        raise ValueError("observation requires observed_artifact_id, observed_trace_id, or source_ref")


def attach_observation(target: Dict[str, Any], observation: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    original_target = copy.deepcopy(target)
    validate_observation(observation, schema)
    envelope = {
        "target": copy.deepcopy(target),
        "observation": copy.deepcopy(observation),
        "attachment_type": "additive_witness_record",
        "authority": AUTHORITY,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    if target != original_target:
        raise ValueError("target mutation detected")
    return envelope
