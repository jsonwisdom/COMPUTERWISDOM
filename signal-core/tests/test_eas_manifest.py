from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_eas_manifest_authority_none():
    manifest = json.loads((ROOT / 'eas' / 'receipt-core-v0.4.eas.json').read_text(encoding='utf-8'))
    assert manifest['authority'] == 'NONE'
    assert manifest['revocable'] is False
    assert manifest['resolver'] == 'none'


def test_eas_schema_contains_locked_fields():
    manifest = json.loads((ROOT / 'eas' / 'receipt-core-v0.4.eas.json').read_text(encoding='utf-8'))
    schema = manifest['schema']
    for field in ['receiptId', 'artifactHash', 'claimGraphHash', 'claimsCount', 'receiptCoreHash', 'authorityNone', 'policyHash', 'bundleRoot', 'version']:
        assert field in schema
