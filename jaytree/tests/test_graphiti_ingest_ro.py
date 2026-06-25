import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTO = ROOT / 'memory' / 'ingest-ro' / 'prototype.py'
QUERY = ROOT / 'memory' / 'ingest-ro' / 'query.py'


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prototype_has_no_graphiti_runtime_import():
    text = PROTO.read_text(encoding='utf-8')
    assert 'from graphiti_core' not in text
    assert 'import graphiti_core' not in text
    assert 'Graphiti(' not in text
    assert 'add_episode(' not in text


def test_prototype_boundary_constants():
    proto = load_module(PROTO)
    assert proto.AUTHORITY == 'NONE'
    assert proto.RUNTIME == 'NOT_PERMITTED'
    assert proto.REQUIRED_INVARIANT == 'memory is not authority'
    assert proto.GROUP_ID == 'computerwisdom_v0.1'


def test_query_is_read_only_helper():
    text = QUERY.read_text(encoding='utf-8')
    assert 'open("w"' not in text
    assert '.write_text' not in text
    assert 'git ' not in text
    assert 'eas' not in text.lower()
    assert 'wallet' not in text.lower()
