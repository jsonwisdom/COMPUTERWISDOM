import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'external-roots' / 'receipts' / 'al-base-mcp-v0.1.eas-receipt.json'


def load_receipt():
    return json.loads(RECEIPT.read_text(encoding='utf-8'))


def test_al_base_mcp_eas_receipt_authority_none():
    receipt = load_receipt()
    assert receipt['authority'] == 'NONE'
    assert receipt['authority_none'] is True


def test_al_base_mcp_eas_receipt_locked_ids():
    receipt = load_receipt()
    assert receipt['source_root'] == 'jaytree/external-roots/al-base-mcp-v0.1.json'
    assert receipt['schema_uid'] == '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11'
    assert receipt['attestation_uid'] == '0x0718576a2cdb3eaabaf6bb338a8a4d1bfb09678b05357e7d8c15e237f92a8abb'
    assert receipt['transaction_hash'] == '0x081e969eb9afd5dbef5e604cd903f9666271ef63eceb10af2457e4d1ea04ce3c'
    assert receipt['receipt_id'] == 'vr:sha256:cc438cbc26e0139d0b581f0ca3ae4434e0ee82cf5d3740e446ca0ad45d9b2166'
    assert receipt['receipt_core_hash'] == 'sha256:8a71d51008ab2d522202d3cfd0668eb8f33f0f97eb72c71ccf80f1d4b045f914'
