from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core import seal


def test_seal_pass(tmp_path):
    artifact = tmp_path / 'artifact.txt'
    artifact.write_text('hello', encoding='utf-8')
    graph = tmp_path / 'graph.json'
    graph.write_text(json.dumps({'authority':'NONE','claims':[{'claim_id':'b','dependencies':['a']},{'claim_id':'a','dependencies':[]}]}), encoding='utf-8')
    receipt = seal(str(artifact), str(graph))
    assert receipt['confidence']['authority'] == 'NONE'
    assert receipt['receipt_id'].startswith('vr:sha256:')
