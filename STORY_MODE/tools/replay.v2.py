#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'08-replay'/'story-mode.manifest.v2.json'

def actual_files():
    return {p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p != MANIFEST}

def safe_path(value):
    p=PurePosixPath(value)
    return bool(value) and not p.is_absolute() and '..' not in p.parts and '\\' not in value

def main():
    check=subprocess.run([sys.executable,str(ROOT/'tools'/'validate.v2.py')])
    if check.returncode: return check.returncode
    if not MANIFEST.is_file():
        print('REPLAY=HOLD REASON=MANIFEST_MISSING AUTHORITY_CREATED=false',file=sys.stderr); return 1
    try: data=json.loads(MANIFEST.read_text(encoding='utf-8'))
    except Exception as exc:
        print(f'REPLAY=FAIL REASON=INVALID_MANIFEST DETAIL={exc} AUTHORITY_CREATED=false',file=sys.stderr); return 1
    failures=[]; entries=data.get('entries',[]); paths=[e.get('path') for e in entries]
    if data.get('manifest_id')!='JSONWISDOM-STORY-MODE-MANIFEST-v2': failures.append('MANIFEST_ID')
    if data.get('algorithm')!='sha256': failures.append('ALGORITHM')
    if data.get('authority_created') is not False: failures.append('AUTHORITY_FLAG')
    if paths != sorted(paths): failures.append('ORDER')
    if len(paths)!=len(set(paths)): failures.append('DUPLICATE_PATH')
    if any(not isinstance(p,str) or not safe_path(p) for p in paths): failures.append('UNSAFE_PATH')
    actual=actual_files(); expected=set(p for p in paths if isinstance(p,str))
    for missing in sorted(expected-set(actual)): failures.append(f'MISSING:{missing}')
    for extra in sorted(set(actual)-expected): failures.append(f'UNMANIFESTED:{extra}')
    for entry in entries:
        rel=entry.get('path')
        if rel not in actual: continue
        raw=actual[rel].read_bytes()
        if len(raw)!=entry.get('bytes'): failures.append(f'BYTE_COUNT:{rel}')
        if hashlib.sha256(raw).hexdigest()!=entry.get('sha256'): failures.append(f'DIGEST:{rel}')
    if failures:
        for item in failures: print(f'FAIL:{item}',file=sys.stderr)
        print(f'REPLAY=FAIL_CLOSED FAILURES={len(failures)} AUTHORITY_CREATED=false',file=sys.stderr); return 1
    print(f'REPLAY=PASS FILES={len(entries)} EXACT_SET=true AUTHORITY_CREATED=false')
    return 0

if __name__ == '__main__': raise SystemExit(main())
