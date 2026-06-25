from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def load_manifest():
    return json.loads((ROOT / 'eas' / 'receipt-core-v0.4.eas.json').read_text(encoding='utf-8'))


def test_eas_manifest_authority_none():
    manifest = load_manifest()
    assert manifest['authority'] == 'NONE'
    assert manifest['revocable'] is False
    assert manifest['resolver'] == 'none'


def test_eas_schema_contains_locked_fields():
    manifest = load_manifest()
    schema = manifest['schema']
    for field in ['receiptId', 'artifactHash', 'claimGraphHash', 'claimsCount', 'receiptCoreHash', 'authorityNone', 'policyHash', 'bundleRoot', 'version']:
        assert field in schema


def test_eas_registration_details_locked():
    manifest = load_manifest()
    assert manifest['network'] == 'Base'
    assert manifest['schema_number'] == 1618
    assert manifest['schema_uid'] == '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11'
    assert manifest['creator'] == '0xC345B26094c63C69222Ee775189a3d3eaead5a84'
    assert manifest['transaction_hash'] == '0x60f9ac0a4d23b112743cc902f4d3f8f06f239664f9b9cc0c3c2909ef682ea7bf'


def test_first_attestation_details_locked():
    attestation = load_manifest()['first_attestation']
    assert attestation['attestation_uid'] == '0x84b58fb78cfde7f791b311c07e5982eeffc3f60b550d594dc9407419ed5d5150'
    assert attestation['transaction_hash'] == '0x539c087bb2987bfa3eae4099b0a37765d1ec824e7c6174169745fc440004cab5'
    assert attestation['receiptId'] == 'vr:sha256:fb83118511079eca8bb21adc5b24a7c26971f055c061ddcd4a7d7f532b2b759c'
    assert attestation['receiptCoreHash'] == 'sha256:b2bb199d65e2d4f66cf093fd0d4218341046d892ce3c17cc881c2bda4d66868e'
    assert attestation['authorityNone'] is True
    assert attestation['attestation_version'] == 'v0.4'
