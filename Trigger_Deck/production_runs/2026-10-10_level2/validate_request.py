#!/usr/bin/env python3
"""Read-only TriggerDeck v0.1 request/manifest gate; never publishes artwork."""
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import zipfile

HERE = Path(__file__).resolve().parent
request_path = Path(os.environ.get('TRIGGERDECK_REQUEST_PATH', HERE / 'production_request_exported_20261010.json'))
manifest_path = Path(os.environ.get('TRIGGERDECK_MANIFEST_PATH', HERE / 'proof_manifest.json'))
request = json.loads(request_path.read_text(encoding='utf-8'))
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
errors = []
def gate(predicate, name):
    if not predicate:
        errors.append(name)
    return bool(predicate)

cards = request.get('cards', [])
proof = manifest.get('cards', [])
ids = [x.get('id') for x in cards]
proof_by_id = {c.get('id'): c for c in proof}
expected = [f'TD-{x}' for x in range(199,206)]
gate(len(cards) == 7, 'count_7')
gate(ids == expected and len(set(ids)) == len(ids), 'ids_sequential_unique')
gate(request.get('canvas') == {'width':900,'height':1200,'aspect':'3:4 portrait'}, 'canvas_3_4')
gate(request.get('kind') == 'triggerdeck-production-request-v0.1', 'request_kind')
gate(request.get('executed') is False, 'request_nonexecuted')
gate(request.get('canon') is False and request.get('authority') is False, 'authority_false')
gate(request.get('render_backend') == 'UNBOUND' and request.get('github_automation') == 'UNBOUND', 'runtime_unbound_honestly_recorded')
gate(all(c.get('local_decision') == 'UNREVIEWED' for c in cards), 'all_decisions_unreviewed')
gate(set(proof_by_id) == set(ids), 'manifest_id_set')
for c in cards:
    p = proof_by_id.get(c['id'], {})
    gate(all(c.get(left) == p.get(right) for left,right in (
        ('title','title'),('source_url','source_url'),
        ('evidence_status','evidence_status'),('expected_sha256','sha256'))), f"manifest_fields_{c['id']}")

archive = os.environ.get('TRIGGERDECK_ARCHIVE_PATH')
archive_checked = bool(archive)
if archive:
    p = Path(archive)
    gate(p.is_file(), 'archive_exists')
    if p.is_file():
        raw_sha = hashlib.sha256(p.read_bytes()).hexdigest()
        gate(raw_sha == (manifest.get('sha256_zip') or os.environ.get('TRIGGERDECK_EXPECTED_ZIP_SHA256')), 'archive_sha256')
        with zipfile.ZipFile(p) as z:
            gate(z.testzip() is None, 'zip_integrity')
            for c in cards:
                name = f"{c['id']}.png"
                gate(name in z.namelist(), f'zip_contains_{name}')
                if name in z.namelist():
                    data = z.read(name)
                    gate(hashlib.sha256(data).hexdigest() == c['expected_sha256'], f'png_sha256_{name}')
                    dims = struct.unpack('>II',data[16:24]) if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24 else None
                    gate(dims == (900,1200), f'png_dimensions_{name}')

result = {'schema':'TD_LEVEL2_VALIDATION_V0_1', 'state':'PASS' if not errors else 'FAIL',
 'cards':len(cards),'archive_checked':archive_checked,'errors':errors,
 'request_executed':False,'render_backend':'UNBOUND', 'canon':False,
 'scope':'metadata_gate_and_optional_binary_integrity_only_not_visual_approval'}
Path('validation_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if errors:
    sys.exit(1)
