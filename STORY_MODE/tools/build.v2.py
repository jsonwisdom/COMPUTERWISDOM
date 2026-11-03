#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '08-replay' / 'story-mode.manifest.v2.json'

def governed_files():
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or path == OUTPUT:
            continue
        yield path

def main():
    check = subprocess.run([sys.executable, str(ROOT/'tools'/'validate.v2.py')])
    if check.returncode: return check.returncode
    entries=[]
    for path in governed_files():
        raw=path.read_bytes()
        entries.append({'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    manifest={
      'manifest_id':'JSONWISDOM-STORY-MODE-MANIFEST-v2',
      'version':'2.0.0',
      'algorithm':'sha256',
      'deterministic_order':'path_ascending',
      'excludes':['08-replay/story-mode.manifest.v2.json','**/__pycache__/**'],
      'proposal_issue':459,
      'entries':entries,
      'authority_created':False
    }
    OUTPUT.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f'MANIFEST_BUILD=PASS FILES={len(entries)} OUTPUT={OUTPUT.relative_to(ROOT)} AUTHORITY_CREATED=false')
    return 0

if __name__ == '__main__': raise SystemExit(main())
