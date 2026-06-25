import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD_MAP = ROOT / 'world-map' / 'world-map-v0.1.json'

REQUIRED_SURFACES = {
    'graphiti_memory_audit',
    'replay_instructions',
    'blocked_continuity_receipt',
    'business_recovery_log',
    'graphiti_ingest_ro',
    'minnesota_receipt_arcade',
    'family_continuity_protection',
    'replay_transform_registry',
    'public_replay_verifier',
}


def load_map():
    return json.loads(WORLD_MAP.read_text(encoding='utf-8'))


def test_world_map_global_boundary():
    data = load_map()
    assert data['authority'] == 'NONE'
    assert data['runtime'] == 'NOT_PERMITTED'
    assert data['map_is_not_authority'] is True
    assert data['memory_is_not_authority'] is True
    assert data['mcp_runtime_enabled'] is False
    assert data['network_access'] is False
    assert data['write_access'] is False
    assert data['witness_only'] is True
    assert data['closing_rule'] == 'Map is not authority. Memory is not authority. Receipts beat narrative.'


def test_world_map_required_surfaces_present():
    data = load_map()
    ids = {surface['id'] for surface in data['surfaces']}
    assert REQUIRED_SURFACES.issubset(ids)


def test_world_map_surface_boundaries():
    data = load_map()
    for surface in data['surfaces']:
        assert surface['authority'] == 'NONE'
        assert surface['runtime'] == 'NOT_PERMITTED'
        assert surface['path']
        assert surface['git_blob_sha']
        assert 'pending' not in surface['git_blob_sha']
        assert surface['type']


def test_world_map_allowed_types_only():
    data = load_map()
    allowed = {
        'memory-index',
        'replay-navigation',
        'receipt-index',
        'navigation-map',
        'replay-builder',
        'playable-map',
        'continuity-map',
        'replay-transform-registry',
        'replay-verifier',
    }
    for surface in data['surfaces']:
        assert surface['type'] in allowed


def test_world_map_does_not_enable_runtime_authority():
    text = WORLD_MAP.read_text(encoding='utf-8').lower()
    forbidden = [
        '"authority": "true"',
        '"runtime": "permitted"',
        '"mcp_runtime_enabled": true',
        '"network_access": true',
        '"write_access": true',
        'wallet_authority": true',
        'signing_authority": true',
        'execution_authority": true',
        'merge_authority": true',
        'eas_attestation_authority": true',
    ]
    for phrase in forbidden:
        assert phrase not in text
