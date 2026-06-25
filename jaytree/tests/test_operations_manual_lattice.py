import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / 'operations-manual' / 'receipt-log-v0.1.json'
SNAPSHOT = ROOT / 'operations-manual' / 'lattice-snapshot-v0.1.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_receipt_log_tag_pair_locked():
    log = load(LOG)
    entries = {entry['entry_id']: entry for entry in log['entries']}
    assert entries['al-base-mcp-root-v0.1']['tag'] == 'v0.1-al-base-mcp-root'
    assert entries['al-base-mcp-root-v0.1']['target_commit'] == '261f7588a3955ec0f26b08eb609c888b7f12cbcc'
    assert entries['al-base-mcp-eas-receipt-v0.1']['tag'] == 'v0.1-al-base-mcp-eas-receipt'
    assert entries['al-base-mcp-eas-receipt-v0.1']['target_commit'] == '035802353e2ee622de0690aae4bfd6dd773b7bea'


def test_receipt_log_eas_receipt_locked():
    log = load(LOG)
    receipt = {entry['entry_id']: entry for entry in log['entries']}['al-base-mcp-eas-receipt-v0.1']
    assert receipt['eas_attestation_uid'] == '0x0718576a2cdb3eaabaf6bb338a8a4d1bfb09678b05357e7d8c15e237f92a8abb'
    assert receipt['eas_transaction_hash'] == '0x081e969eb9afd5dbef5e604cd903f9666271ef63eceb10af2457e4d1ea04ce3c'
    assert receipt['receipt_id'] == 'vr:sha256:cc438cbc26e0139d0b581f0ca3ae4434e0ee82cf5d3740e446ca0ad45d9b2166'


def test_lattice_closed_surfaces():
    snapshot = load(SNAPSHOT)
    closed = snapshot['closed_surfaces']
    assert closed['wallet_authority'] is False
    assert closed['execution_authority'] is False
    assert closed['signing_authority'] is False
    assert closed['merge_authority'] is False
    assert closed['x402_enabled'] is False
    assert closed['runtime_enabled'] is False


def test_l0_and_boss_bre_boundary():
    snapshot = load(SNAPSHOT)
    assert snapshot['l0_human_authority']['name'] == 'Jay Wisdom'
    assert snapshot['l0_human_authority']['ens'] == 'jaywisdom.eth'
    assert snapshot['l0_human_authority']['basename'] == 'jaywisdom.base.eth'
    assert snapshot['manual_layer']['maintainer'] == 'Boss Bre'
    assert snapshot['manual_layer']['wallet_authority'] is False
    assert snapshot['manual_layer']['signing_authority'] is False
    assert snapshot['manual_layer']['execution_authority'] is False
