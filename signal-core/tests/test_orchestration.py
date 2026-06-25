from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core import seal
from orchestrator.verify_chain import verify_chain


def write_receipt(tmp_path, name, claims_count=1):
    artifact = tmp_path / f'{name}.txt'
    artifact.write_text(name, encoding='utf-8')
    graph = tmp_path / f'{name}.graph.json'
    claims = [{'claim_id': f'{name}-claim', 'dependencies': []} for _ in range(claims_count)]
    graph.write_text(json.dumps({'authority':'NONE','claims':claims}), encoding='utf-8')
    receipt = seal(str(artifact), str(graph))
    out = tmp_path / f'{name}.json'
    out.write_text(json.dumps(receipt), encoding='utf-8')
    return out


def test_receipt_chain_passes_with_policy(tmp_path):
    a = write_receipt(tmp_path, 'receipt_A')
    b = write_receipt(tmp_path, 'receipt_B')
    bundle = tmp_path / 'receipt_bundle.json'
    bundle.write_text(json.dumps({
        'version': 'v0.3',
        'authority': 'NONE',
        'receipts': [
            {'id': 'A', 'path': str(a), 'dependencies': []},
            {'id': 'B', 'path': str(b), 'dependencies': ['A']}
        ]
    }), encoding='utf-8')
    policy = tmp_path / 'policy.rql'
    policy.write_text('REQUIRE confidence.authority == NONE\nREQUIRE claims_count >= 1\n', encoding='utf-8')
    assert verify_chain(str(bundle), str(policy)) == 0


def test_receipt_chain_bubbles_policy_failure(tmp_path):
    a = write_receipt(tmp_path, 'receipt_A')
    bundle = tmp_path / 'receipt_bundle.json'
    bundle.write_text(json.dumps({
        'version': 'v0.3',
        'authority': 'NONE',
        'receipts': [{'id': 'A', 'path': str(a), 'dependencies': []}]
    }), encoding='utf-8')
    policy = tmp_path / 'policy.rql'
    policy.write_text('REQUIRE claims_count > 1\n', encoding='utf-8')
    assert verify_chain(str(bundle), str(policy)) == 1


def test_receipt_chain_cycle_is_system_error(tmp_path):
    a = write_receipt(tmp_path, 'receipt_A')
    b = write_receipt(tmp_path, 'receipt_B')
    bundle = tmp_path / 'receipt_bundle.json'
    bundle.write_text(json.dumps({
        'version': 'v0.3',
        'authority': 'NONE',
        'receipts': [
            {'id': 'A', 'path': str(a), 'dependencies': ['B']},
            {'id': 'B', 'path': str(b), 'dependencies': ['A']}
        ]
    }), encoding='utf-8')
    assert verify_chain(str(bundle)) == 3


def test_receipt_chain_rejects_authority_escalation(tmp_path):
    a = write_receipt(tmp_path, 'receipt_A')
    bundle = tmp_path / 'receipt_bundle.json'
    bundle.write_text(json.dumps({
        'version': 'v0.3',
        'authority': 'ROOT',
        'receipts': [{'id': 'A', 'path': str(a), 'dependencies': []}]
    }), encoding='utf-8')
    assert verify_chain(str(bundle)) == 3
