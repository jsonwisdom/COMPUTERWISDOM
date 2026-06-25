import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / 'operations-manual' / 'receipt-log-v0.1.json'
SNAPSHOT = ROOT / 'operations-manual' / 'lattice-snapshot-v0.1.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def entries_by_id():
    return {entry['entry_id']: entry for entry in load(LOG)['entries']}


def test_receipt_log_tag_pair_locked():
    entries = entries_by_id()
    assert entries['al-base-mcp-root-v0.1']['tag'] == 'v0.1-al-base-mcp-root'
    assert entries['al-base-mcp-root-v0.1']['target_commit'] == '261f7588a3955ec0f26b08eb609c888b7f12cbcc'
    assert entries['al-base-mcp-eas-receipt-v0.1']['tag'] == 'v0.1-al-base-mcp-eas-receipt'
    assert entries['al-base-mcp-eas-receipt-v0.1']['target_commit'] == '035802353e2ee622de0690aae4bfd6dd773b7bea'


def test_receipt_log_eas_receipt_locked():
    receipt = entries_by_id()['al-base-mcp-eas-receipt-v0.1']
    assert receipt['eas_attestation_uid'] == '0x0718576a2cdb3eaabaf6bb338a8a4d1bfb09678b05357e7d8c15e237f92a8abb'
    assert receipt['eas_transaction_hash'] == '0x081e969eb9afd5dbef5e604cd903f9666271ef63eceb10af2457e4d1ea04ce3c'
    assert receipt['receipt_id'] == 'vr:sha256:cc438cbc26e0139d0b581f0ca3ae4434e0ee82cf5d3740e446ca0ad45d9b2166'


def test_graphiti_world_map_chain_locked():
    entries = entries_by_id()
    assert entries['graphiti-memory-audit-v0.1']['target_commit'] == '804f4d61716b199173078cd94bbed8d2b235bd2c'
    assert entries['graphiti-memory-eas-receipt-v0.1']['target_commit'] == 'fee651690e3178dc6401df9b5ac424303d32ea2e'
    assert entries['graphiti-ingest-ro-v0.1']['target_commit'] == '486adec12a3f2bea799b0faf4c925c179a92d81d'
    assert entries['world-map-v0.1']['target_commit'] == '292503d8936a610e15d00cb5760f83c53132d13f'
    assert entries['world-map-receipt-core-v0.1']['target_commit'] == 'fbc2345c163ab9ab6d81520e753b4cb04ff9df8c'


def test_graphiti_world_map_receipts_locked():
    entries = entries_by_id()
    graphiti = entries['graphiti-memory-eas-receipt-v0.1']
    assert graphiti['eas_attestation_uid'] == '0x22b32e59336970d44ad03cb32064e8d8e17fbdde9fe5f079a9ea94fa2a4aa46b'
    assert graphiti['eas_transaction_hash'] == '0x40b05628f634f7ab9f427234e00a8edf14f79bf72407ddf8558dc03d2d81208c'
    assert graphiti['receipt_id'] == 'vr:sha256:c027a4129b426c47a2d373936bc005c1eacc00f3f10b0d7a5c0deea498fcbc1e'
    world = entries['world-map-receipt-core-v0.1']
    assert world['receipt_id'] == 'vr:sha256:dde2912ec03ce19b54dab8552129a113be12a767de0c3e1114116535d1812742'
    assert world['artifact_hash'] == 'sha256:cfe04f781b937e62f6411207313f86bdd551baff3af4b2681fb6b5cfb7acc0de'
    assert world['claim_graph_hash'] == 'sha256:e81e1015e5c94a7fff8fed7a2943b05ca2bec0830b07f681f2a660ca31a51e83'
    assert world['bundle_root'] == 'sha256:0e99948bbdbdd5cc3495a067be94f8b462b57b23851801a3d23b18b4b1975e21'
    assert world['eas_status'] == 'HOLD'


def test_lattice_closed_surfaces():
    snapshot = load(SNAPSHOT)
    closed = snapshot['closed_surfaces']
    assert closed['wallet_authority'] is False
    assert closed['execution_authority'] is False
    assert closed['signing_authority'] is False
    assert closed['merge_authority'] is False
    assert closed['x402_enabled'] is False
    assert closed['runtime_enabled'] is False
    assert closed['mcp_runtime_enabled'] is False
    assert closed['network_access'] is False
    assert closed['write_access'] is False
    assert closed['eas_attestation_authority'] is False


def test_l0_and_boss_bre_boundary():
    snapshot = load(SNAPSHOT)
    assert snapshot['l0_human_authority']['name'] == 'Jay Wisdom'
    assert snapshot['l0_human_authority']['ens'] == 'jaywisdom.eth'
    assert snapshot['l0_human_authority']['basename'] == 'jaywisdom.base.eth'
    assert snapshot['manual_layer']['maintainer'] == 'Boss Bre'
    assert snapshot['manual_layer']['wallet_authority'] is False
    assert snapshot['manual_layer']['signing_authority'] is False
    assert snapshot['manual_layer']['execution_authority'] is False


def test_memory_and_map_not_authority():
    snapshot = load(SNAPSHOT)
    assert snapshot['memory_layer']['graphiti_memory_audit']['required_invariant'] == 'memory is not authority'
    assert snapshot['memory_layer']['graphiti_ingest_ro']['required_invariant'] == 'memory is not authority'
    assert snapshot['world_map_layer']['world_map_v0_1']['required_invariant'] == 'map is not authority'
    assert snapshot['world_map_layer']['world_map_receipt_core_v0_1']['required_invariant'] == 'map is not authority'
    assert snapshot['world_map_layer']['world_map_receipt_core_v0_1']['eas_status'] == 'HOLD'
