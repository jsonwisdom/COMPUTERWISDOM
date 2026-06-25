import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'memory' / 'graphiti-memory-v0.1.json'


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


def test_graphiti_memory_is_not_authority():
    manifest = load_manifest()
    assert manifest['authority'] == 'NONE'
    assert manifest['runtime'] == 'NOT_PERMITTED'
    assert manifest['required_invariant'] == 'memory is not authority'
    assert manifest['verdict'] == 'GO for read-only prototype; NO-GO for authority role'


def test_graphiti_closed_surfaces():
    manifest = load_manifest()
    closed = manifest['closed_surfaces']
    assert closed['wallet_authority'] is False
    assert closed['signing_authority'] is False
    assert closed['execution_authority'] is False
    assert closed['merge_authority'] is False
    assert closed['eas_attestation_authority'] is False
    assert closed['evm_write_rpc'] is False
    assert closed['github_write_token'] is False
    assert closed['x402_enabled'] is False
    assert closed['runtime_enabled'] is False


def test_graphiti_anchors_locked():
    manifest = load_manifest()
    anchors = manifest['anchors']
    assert anchors['root_tag'] == 'v0.1-al-base-mcp-root'
    assert anchors['root_commit'] == '261f7588a3955ec0f26b08eb609c888b7f12cbcc'
    assert anchors['eas_receipt_tag'] == 'v0.1-al-base-mcp-eas-receipt'
    assert anchors['eas_receipt_commit'] == '035802353e2ee622de0690aae4bfd6dd773b7bea'
    assert anchors['eas_uid'] == '0x0718576a2cdb3eaabaf6bb338a8a4d1bfb09678b05357e7d8c15e237f92a8abb'
    assert anchors['eas_tx'] == '0x081e969eb9afd5dbef5e604cd903f9666271ef63eceb10af2457e4d1ea04ce3c'
    assert anchors['receipt_id'] == 'vr:sha256:cc438cbc26e0139d0b581f0ca3ae4434e0ee82cf5d3740e446ca0ad45d9b2166'
