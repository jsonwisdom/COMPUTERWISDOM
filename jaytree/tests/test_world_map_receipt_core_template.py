import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'world-map' / 'receipts' / 'world-map-v0.1.receipt-core-template.json'


def load_template():
    return json.loads(TEMPLATE.read_text(encoding='utf-8'))


def test_world_map_receipt_template_boundary():
    data = load_template()
    assert data['authority'] == 'NONE'
    assert data['runtime'] == 'NOT_PERMITTED'
    assert data['invariant'] == 'map is not authority'
    assert data['memory_is_not_authority'] is True
    assert data['map_is_not_authority'] is True
    assert data['receipt_core_fields_to_forge_locally']['authorityNone'] is True
    assert data['closing_rule'] == 'Map is not authority. Memory is not authority. Receipts beat narrative.'


def test_world_map_receipt_template_commit_and_tag():
    data = load_template()
    assert data['source_merge_commit'] == '292503d8936a610e15d00cb5760f83c53132d13f'
    assert data['expected_release_tag'] == 'v0.1-world-map'
    assert data['primary_artifact']['path'] == 'jaytree/world-map/world-map-v0.1.json'
    assert data['primary_artifact']['git_blob_sha'] == '0dcb192545895cdd3658eeb982893f5a22b06399'


def test_world_map_receipt_template_has_no_unresolved_blob_pins():
    data = load_template()
    blob_values = [data['primary_artifact']['git_blob_sha']]
    blob_values.extend(item['git_blob_sha'] for item in data['supporting_artifacts'])
    blob_values.extend(item['git_blob_sha'] for item in data['indexed_witness_surfaces'])
    for value in blob_values:
        assert value
        assert 'pending' not in value.lower()
        assert len(value) == 40


def test_world_map_receipt_template_forbidden_promotions():
    data = load_template()
    forbidden = data['forbidden_promotions']
    assert 'map grants authority' in forbidden
    assert 'memory grants authority' in forbidden
    assert 'MCP runtime is enabled' in forbidden
    assert 'network access is permitted' in forbidden
    assert 'write access is permitted' in forbidden
    assert 'EAS attestation authority is granted' in forbidden
