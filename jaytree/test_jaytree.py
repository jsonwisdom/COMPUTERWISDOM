import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_identity():
    return json.loads((ROOT / 'identity-vector-v0.1.json').read_text(encoding='utf-8'))


def test_authority_none():
    identity = load_identity()
    assert identity['authority'] == 'NONE'


def test_core_surfaces_present():
    identity = load_identity()
    assert identity['basename'] == 'jaywisdom.base.eth'
    assert identity['github']['repository'] == 'jsonwisdom/COMPUTERWISDOM'
    assert identity['eas']['network'] == 'Base'
    assert identity['eas']['schema_uid'] == '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11'
    assert identity['eas']['first_receipt_core_attestation_uid'] == '0x84b58fb78cfde7f791b311c07e5982eeffc3f60b550d594dc9407419ed5d5150'


def test_no_truth_authority_language():
    identity = load_identity()
    joined = json.dumps(identity).lower()
    assert 'truth authority' not in joined.replace('do not create truth authority', '')
