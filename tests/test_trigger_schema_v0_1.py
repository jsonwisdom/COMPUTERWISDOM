import json
from pathlib import Path
import jsonschema

SCHEMA = json.loads(Path('schemas/trigger_v0_1.schema.json').read_text())


def test_valid_trigger():
    obj = {
        'watch_id': 'WATCH_001',
        'trigger_id': 'TRIGGER_001',
        'source_domain': 'example.gov',
        'artifact_type': 'omb_memo',
        'state_transition': {
            'from_level': 2,
            'to_level': 3
        },
        'authority': False
    }
    jsonschema.validate(obj, SCHEMA)


def test_authority_must_be_false():
    obj = {
        'watch_id': 'WATCH_001',
        'trigger_id': 'TRIGGER_001',
        'source_domain': 'example.gov',
        'artifact_type': 'omb_memo',
        'state_transition': {
            'from_level': 2,
            'to_level': 3
        },
        'authority': True
    }
    try:
        jsonschema.validate(obj, SCHEMA)
        assert False
    except jsonschema.ValidationError:
        assert True
