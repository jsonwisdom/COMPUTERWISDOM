from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eas.verify_attestation import verify_attestation_data


class FakeAttestation:
    def __init__(self, schema, decoded_data):
        self.schema = schema
        self.decoded_data = decoded_data


def test_eas_attestation_accepts_matching_local_receipt(tmp_path):
    receipt = {
        'receipt_id': 'vr:sha256:' + 'a' * 64,
        'receipt_core_hash': 'sha256:' + 'b' * 64
    }
    receipt_path = tmp_path / 'receipt.json'
    receipt_path.write_text(json.dumps(receipt), encoding='utf-8')
    att = FakeAttestation(
        '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11',
        {
            'authorityNone': True,
            'receiptId': receipt['receipt_id'],
            'receiptCoreHash': receipt['receipt_core_hash'],
            'version': 'v0.4'
        }
    )
    assert verify_attestation_data(att, str(receipt_path)) == 0


def test_eas_attestation_rejects_schema_mismatch():
    att = FakeAttestation('0x' + '0' * 64, {'authorityNone': True})
    assert verify_attestation_data(att) == 2


def test_eas_attestation_rejects_authority_escalation():
    att = FakeAttestation(
        '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11',
        {'authorityNone': False}
    )
    assert verify_attestation_data(att) == 2


def test_eas_attestation_rejects_receipt_hash_mismatch(tmp_path):
    receipt = {
        'receipt_id': 'vr:sha256:' + 'a' * 64,
        'receipt_core_hash': 'sha256:' + 'b' * 64
    }
    receipt_path = tmp_path / 'receipt.json'
    receipt_path.write_text(json.dumps(receipt), encoding='utf-8')
    att = FakeAttestation(
        '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11',
        {
            'authorityNone': True,
            'receiptId': receipt['receipt_id'],
            'receiptCoreHash': 'sha256:' + 'c' * 64,
            'version': 'v0.4'
        }
    )
    assert verify_attestation_data(att, str(receipt_path)) == 2
