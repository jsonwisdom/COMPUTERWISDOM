import hashlib
import json
from pathlib import Path


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def h(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def canonicalize_graph(path):
    graph = load_json(path)
    if graph.get('authority') != 'NONE':
        raise ValueError('claim graph authority must be NONE')
    claims = graph.get('claims', [])
    graph['claims'] = sorted(claims, key=lambda c: c.get('claim_id', json.dumps(c, sort_keys=True)))
    for claim in graph['claims']:
        if isinstance(claim.get('dependencies'), list):
            claim['dependencies'] = sorted(claim['dependencies'])
    return graph


def seal(artifact_path, graph_path):
    graph = canonicalize_graph(graph_path)
    core = {
        'artifact_hash': h(Path(artifact_path).read_bytes()),
        'claim_graph_hash': h(canonical_bytes(graph)),
        'claims_count': len(graph.get('claims', [])),
        'confidence': {'authority': 'NONE'},
    }
    core['receipt_core_hash'] = h(canonical_bytes(core))
    rid_core = dict(core)
    rid_core['receipt_id'] = ''
    core['receipt_id'] = 'vr:' + h(canonical_bytes(rid_core))
    return core
