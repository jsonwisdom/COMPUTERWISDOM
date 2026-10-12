#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '08-replay' / 'story-mode.manifest.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def governed_files():
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path == OUTPUT or '__pycache__' in path.parts:
            continue
        yield path

def main():
    check = subprocess.run([sys.executable, str(ROOT / 'tools' / 'validate.py')])
    if check.returncode:
        return check.returncode
    entries = [
        {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path), 'bytes': path.stat().st_size}
        for path in governed_files()
    ]
    manifest = {
        'manifest_id': 'JSONWISDOM-STORY-MODE-MANIFEST-v1',
        'algorithm': 'sha256',
        'deterministic_order': 'path_ascending',
        'proposal_issue': 459,
        'entries': entries,
        'authority_created': False
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f'BUILT: {OUTPUT.relative_to(ROOT)} with {len(entries)} entries')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
