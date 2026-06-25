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
