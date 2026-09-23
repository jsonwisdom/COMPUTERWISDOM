#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'08-replay'/'story-mode.manifest.v3.json'
ROOT_NOTE=ROOT/'08-replay'/'merkle-root.v1.json'
REPLAY_RESULT=ROOT/'08-replay'/'replay-result.v3.json'
EXCLUDED={MANIFEST,ROOT_NOTE,REPLAY_RESULT}
LEAF_DOMAIN=b'JSONWISDOM_STORY_MODE_LEAF_V1\x00'
NODE_DOMAIN=b'JSONWISDOM_STORY_MODE_NODE_V1\x00'

def safe(value):
    p=PurePosixPath(value)
    return bool(value) and not p.is_absolute() and '..' not in p.parts and '\\' not in value

def root_hash(nodes):
    if not nodes: return hashlib.sha256(b'JSONWISDOM_STORY_MODE_EMPTY_V1').digest()
    level=list(nodes)
    while len(level)>1:
        if len(level)%2: level.append(level[-1])
        level=[hashlib.sha256(NODE_DOMAIN+level[i]+level[i+1]).digest() for i in range(0,len(level),2)]
    return level[0]

def main():
    check=subprocess.run([sys.executable,str(ROOT/'tools'/'validate.v2.py')])
    if check.returncode: return check.returncode
    if not MANIFEST.is_file() or not ROOT_NOTE.is_file():
        print('REPLAY=HOLD REASON=MERKLE_OUTPUT_MISSING AUTHORITY_CREATED=false',file=sys.stderr); return 1
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8')); note=json.loads(ROOT_NOTE.read_text(encoding='utf-8'))
    entries=manifest.get('entries',[]); paths=[e.get('path') for e in entries]; failures=[]
    if paths!=sorted(paths): failures.append('ORDER')
    if len(paths)!=len(set(paths)): failures.append('DUPLICATE_PATH')
    if any(not isinstance(p,str) or not safe(p) for p in paths): failures.append('UNSAFE_PATH')
    actual={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p not in EXCLUDED}
    if set(paths)!=set(actual):
        for p in sorted(set(paths)-set(actual)): failures.append(f'MISSING:{p}')
        for p in sorted(set(actual)-set(paths)): failures.append(f'UNMANIFESTED:{p}')
    leaves=[]
    for entry in entries:
        rel=entry.get('path')
        if rel not in actual: continue
        raw=actual[rel].read_bytes(); sha=hashlib.sha256(raw).hexdigest()
        if len(raw)!=entry.get('bytes'): failures.append(f'BYTES:{rel}')
        if sha!=entry.get('sha256'): failures.append(f'DIGEST:{rel}')
        leaves.append(hashlib.sha256(LEAF_DOMAIN+rel.encode()+b'\x00'+bytes.fromhex(sha)).digest())
    root=root_hash(leaves).hex()
    if root!=note.get('merkle_root'): failures.append('MERKLE_ROOT')
    if note.get('leaf_count')!=len(leaves): failures.append('LEAF_COUNT')
    result={'object_id':'replay:jsonwisdom-story-mode:v3','object_type':'REPLAY_RESULT','version':'3.0.0','files':len(entries),'exact_set':not any(x.startswith(('MISSING','UNMANIFESTED')) for x in failures),'merkle_root':root,'result':'PASS' if not failures else 'FAIL_CLOSED','failures':failures,'authority_created':False}
    REPLAY_RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    if failures:
        for item in failures: print(f'FAIL:{item}',file=sys.stderr)
        print(f'REPLAY=FAIL_CLOSED FAILURES={len(failures)} AUTHORITY_CREATED=false',file=sys.stderr); return 1
    print(f'REPLAY=PASS FILES={len(entries)} EXACT_SET=true MERKLE_ROOT={root} AUTHORITY_CREATED=false')
    return 0

if __name__=='__main__': raise SystemExit(main())
