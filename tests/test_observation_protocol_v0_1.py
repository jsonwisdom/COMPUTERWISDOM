import json
from pathlib import Path

import jsonschema

from src.observation_protocol_v0_1 import attach_observation, validate_observation

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.load(open(ROOT / 'schemas' / 'observation.v0_1.schema.json', encoding='utf-8'))


def load_example():
    return json.load(open(ROOT / 'examples' / 'observation_example_v0_1.json', encoding='utf-8'))


def test_example_validates_against_schema():
    observation = load_example()
    jsonschema.Draft202012Validator(SCHEMA).validate(observation)


def test_boundary_fields_enforced():
    observation = load_example()
    validate_observation(observation, SCHEMA)
    assert observation['schema_version'] == 'OBSERVATION_V0_1'
    assert observation['authority'] is False
    assert observation['authority_boundary'] == 'NONE'


def test_attachment_is_additive_and_non_mutating():
    target = {'artifact_id': 'ers-event-example-v0-1'}
    observation = load_example()
    original = dict(target)

    envelope = attach_observation(target, observation, SCHEMA)

    assert target == original
    assert envelope['attachment_type'] == 'additive_witness_record'
    assert envelope['observation']['observation_id'] == observation['observation_id']


def test_witness_reference_exists_as_string():
    observation = load_example()
    assert isinstance(observation['observed_artifact_id'], str)
