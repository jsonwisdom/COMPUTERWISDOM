#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / '08-replay' / 'story-mode.manifest.json'

def main():
    if not MANIFEST.is_file():
        print('HOLD: manifest missing; run build.py first', file=sys.stderr)
        return 1
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    failures = []
    for entry in data.get('entries', []):
        path = ROOT / entry['path']
        if not path.is_file():
            failures.append(f'MISSING {entry["path"]}')
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != entry['sha256']:
            failures.append(f'DIGEST_MISMATCH {entry["path"]}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        print('REPLAY=FAIL_CLOSED AUTHORITY_CREATED=false', file=sys.stderr)
        return 1
    print(f'REPLAY=PASS FILES={len(data.get("entries", []))} AUTHORITY_CREATED=false')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
