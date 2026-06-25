import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'memory' / 'receipts' / 'graphiti-memory-v0.1.eas-receipt.json'


def load_receipt():
    return json.loads(RECEIPT.read_text(encoding='utf-8'))


def test_graphiti_memory_eas_receipt_boundary():
    receipt = load_receipt()
    assert receipt['authority'] == 'NONE'
    assert receipt['runtime'] == 'NOT_PERMITTED'
    assert receipt['authority_none'] is True
    assert receipt['required_invariant'] == 'memory is not authority'


def test_graphiti_memory_eas_receipt_locked_ids():
    receipt = load_receipt()
    assert receipt['source_artifact'] == 'jaytree/memory/graphiti-memory-v0.1.json'
    assert receipt['source_merge_commit'] == '804f4d61716b199173078cd94bbed8d2b235bd2c'
    assert receipt['schema_uid'] == '0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11'
    assert receipt['attestation_uid'] == '0x22b32e59336970d44ad03cb32064e8d8e17fbdde9fe5f079a9ea94fa2a4aa46b'
    assert receipt['transaction_hash'] == '0x40b05628f634f7ab9f427234e00a8edf14f79bf72407ddf8558dc03d2d81208c'
    assert receipt['receipt_id'] == 'vr:sha256:c027a4129b426c47a2d373936bc005c1eacc00f3f10b0d7a5c0deea498fcbc1e'


def test_graphiti_memory_eas_receipt_hashes():
    receipt = load_receipt()
    assert receipt['artifact_hash'] == 'sha256:88ac6e76beff169dc9d5f4242f51e48b48fbf520aa8bc02edeb3121b6a2bcda7'
    assert receipt['claim_graph_hash'] == 'sha256:03bf3b6a5b734925d0e00bb4c51461c7e2451a9092ebbc105c7e2a1c1f93d79d'
    assert receipt['receipt_core_hash'] == 'sha256:c7cfd3670dde9aaea44e949b82ebc2196bb4132aa18f646c41f1a2896f67ebdf'
    assert receipt['bundle_root'] == 'sha256:d12a0cffd1fcbc1214808df49c2e219d7144858896a482f096090846fb430f5a'
