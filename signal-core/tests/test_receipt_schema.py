from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core import seal
from validator.schema_validate import ReceiptSchemaError, validate_receipt


def test_sealed_receipt_matches_schema(tmp_path):
    artifact = tmp_path / 'artifact.txt'
    artifact.write_text('hello', encoding='utf-8')
    graph = tmp_path / 'graph.json'
    graph.write_text(json.dumps({'authority':'NONE','claims':[{'claim_id':'a','dependencies':[]}]}), encoding='utf-8')
    receipt = seal(str(artifact), str(graph))
    assert validate_receipt(receipt) is True


def test_rejects_extra_fields():
    receipt = {
        'receipt_id': 'vr:sha256:' + 'a' * 64,
        'artifact_hash': 'sha256:' + 'b' * 64,
        'claim_graph_hash': 'sha256:' + 'c' * 64,
        'claims_count': 1,
        'receipt_core_hash': 'sha256:' + 'd' * 64,
        'confidence': {'authority': 'NONE'},
        'verdict': 'TRUE'
    }
    try:
        validate_receipt(receipt)
        assert False
    except ReceiptSchemaError as exc:
        assert 'unexpected fields' in str(exc)


def test_rejects_authority():
    receipt = {
        'receipt_id': 'vr:sha256:' + 'a' * 64,
        'artifact_hash': 'sha256:' + 'b' * 64,
        'claim_graph_hash': 'sha256:' + 'c' * 64,
        'claims_count': 1,
        'receipt_core_hash': 'sha256:' + 'd' * 64,
        'confidence': {'authority': 'ROOT'}
    }
    try:
        validate_receipt(receipt)
        assert False
    except ReceiptSchemaError as exc:
        assert 'authority must be NONE' in str(exc)
