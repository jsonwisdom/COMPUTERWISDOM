"""Generate public-safe synthetic RGBA8 PNGs + a manifest, offline and local-only."""
from __future__ import annotations
import hashlib
import json
import pathlib
import sys
import zlib


def chunk(kind, payload):
    return (len(payload).to_bytes(4,'big') + kind + payload
            + (zlib.crc32(kind+payload)&0xffffffff).to_bytes(4,'big'))


def png(w, h):
    head = w.to_bytes(4,'big') + h.to_bytes(4,'big') + bytes([8,6,0,0,0])
    row = b'\x00' + (b'\xff\xff\xff\xff'*w)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR',head)
            + chunk(b'IDAT',zlib.compress(row*h)) + chunk(b'IEND',b''))


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python3 tests/make_synthetic_fixture.py NEW_EMPTY_DIRECTORY')
    root = pathlib.Path(sys.argv[1])
    root.mkdir(mode=0o700,parents=True,exist_ok=False)
    asset = png(3,4)
    (root/'synthetic.png').write_bytes(asset)
    digest = hashlib.sha256(asset).hexdigest()
    manifest = {
        'schema':'CW_TRIGGERED_DECKS_BATCH_V0_1',
        'purpose':'ADULT_FICTION_SATIRE_CANDIDATE',
        'operator':'JAY',
        'mode':'DESIGN_CANDIDATE_ONLY',
        'family_data':False,
        'canon_policy':'SEPARATE_LINEAGE_NO_CANON_WRITE',
        'cards':[{'card_id':f'CWTD-SYN-{i:03d}',
                  'asset_path':'synthetic.png','asset_sha256':digest,
                  'fiction_label':'FICTION / SATIRE — NOT PREDICTIONS OR FACTS',
                  'source_class':'FICTION_SATIRE','instances':3,
                  'caption':f'Synthetic placeholder {i} — not a real card',
                  'master_status':'CANDIDATE_NOT_APPROVED'} for i in range(1,4)]
    }
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'created_synthetic_fixture':str(root),'cards':3,'instances':9,
                      'production_status':'HOLD'}))

if __name__=='__main__':
    main()
