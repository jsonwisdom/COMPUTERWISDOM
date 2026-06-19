import json
from pathlib import Path

import jsonschema

from src.dispute_protocol_v0_1 import attach_dispute, validate_dispute

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.load(open(ROOT / 'schemas' / 'dispute.v0_1.schema.json', encoding='utf-8'))


def load_example():
    return json.load(open(ROOT / 'examples' / 'dispute_example_v0_1.json', encoding='utf-8'))


def test_example_validates_against_schema():
    dispute = load_example()
    jsonschema.Draft202012Validator(SCHEMA).validate(dispute)


def test_boundary_fields_enforced():
    dispute = load_example()
    validate_dispute(dispute, SCHEMA)
    assert dispute['schema_version'] == 'DISPUTE_V0_1'
    assert dispute['authority'] is False
    assert dispute['authority_boundary'] == 'NONE'


def test_attachment_is_additive_and_non_mutating():
    target = {'artifact_id': 'ers-event-example-v0-1'}
    dispute = load_example()
    original = dict(target)

    envelope = attach_dispute(target, dispute, SCHEMA)

    assert target == original
    assert envelope['attachment_type'] == 'additive_reference'
    assert envelope['dispute']['dispute_id'] == dispute['dispute_id']


def test_target_reference_exists_as_string():
    dispute = load_example()
    assert isinstance(dispute['target_artifact_id'], str)
