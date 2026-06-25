from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli.receipts import verify_receipt
from core import seal


def test_receipts_verify_pass(tmp_path):
    artifact = tmp_path / 'artifact.txt'
    artifact.write_text('hello', encoding='utf-8')
    graph = tmp_path / 'graph.json'
    graph.write_text(json.dumps({'authority':'NONE','claims':[{'claim_id':'a','dependencies':[]}]}), encoding='utf-8')
    receipt = seal(str(artifact), str(graph))
    receipt_path = tmp_path / 'sealed_receipt.json'
    receipt_path.write_text(json.dumps(receipt), encoding='utf-8')
    assert verify_receipt(str(receipt_path)) == 0


def test_receipts_verify_rejects_verdict(tmp_path):
    receipt = {
        'receipt_id': 'vr:sha256:' + 'a' * 64,
        'artifact_hash': 'sha256:' + 'b' * 64,
        'claim_graph_hash': 'sha256:' + 'c' * 64,
        'claims_count': 1,
        'receipt_core_hash': 'sha256:' + 'd' * 64,
        'confidence': {'authority': 'NONE'},
        'verdict': 'TRUE'
    }
    receipt_path = tmp_path / 'bad_receipt.json'
    receipt_path.write_text(json.dumps(receipt), encoding='utf-8')
    assert verify_receipt(str(receipt_path)) == 1
