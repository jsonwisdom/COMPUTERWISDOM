#!/usr/bin/env python3
import fnmatch
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'schemas' / 'admission-policy.v2.json'
REQUIRED_KEYS = {'PURPOSE','MAY_CONTAIN','MUST_NOT_CONTAIN','ENTRY_PRECONDITIONS','AUTHORITY_NOT_CREATED'}
SEMVER = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')

def governed_directories():
    yield ROOT
    for path in sorted(ROOT.rglob('*')):
        if path.is_dir() and '__pycache__' not in path.parts:
            yield path

def governed_files():
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            yield path

def main():
    errors = []
    try:
        policy = json.loads(POLICY.read_text(encoding='utf-8'))['directories']
    except Exception as exc:
        print(f'FAIL: admission policy unavailable: {exc}', file=sys.stderr)
        return 1
    for directory in governed_directories():
        rel = '.' if directory == ROOT else directory.relative_to(ROOT).as_posix()
        contract = directory / 'DIRECTORY_CONTRACT.json'
        if not contract.is_file():
            errors.append(f'missing directory contract: {rel}')
        else:
            try:
                data = json.loads(contract.read_text(encoding='utf-8'))
                missing = sorted(REQUIRED_KEYS - set(data))
                if missing: errors.append(f'{rel}/DIRECTORY_CONTRACT.json missing {missing}')
                if data.get('AUTHORITY_NOT_CREATED') is not True:
                    errors.append(f'{rel}/DIRECTORY_CONTRACT.json AUTHORITY_NOT_CREATED must be true')
            except Exception as exc:
                errors.append(f'invalid contract JSON {rel}: {exc}')
        if rel not in policy:
            errors.append(f'no admission policy for directory: {rel}')
    json_count = 0
    for path in governed_files():
        rel_dir = '.' if path.parent == ROOT else path.parent.relative_to(ROOT).as_posix()
        patterns = policy.get(rel_dir, [])
        if not any(fnmatch.fnmatch(path.name, pattern) for pattern in patterns):
            errors.append(f'artifact not admitted: {path.relative_to(ROOT).as_posix()}')
        if path.suffix == '.json':
            json_count += 1
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except Exception as exc:
                errors.append(f'invalid JSON {path.relative_to(ROOT)}: {exc}')
                continue
            if isinstance(data, dict):
                if data.get('authority_created') is True or data.get('AUTHORITY_CREATED') is True:
                    errors.append(f'authority laundering flag true: {path.relative_to(ROOT)}')
                if 'object_id' in data:
                    for key in ('object_id','object_type','version'):
                        if not data.get(key): errors.append(f'{path.relative_to(ROOT)} missing {key}')
                    if data.get('version') and not SEMVER.match(str(data['version'])):
                        errors.append(f'{path.relative_to(ROOT)} invalid semantic version')
    if errors:
        for error in errors: print(f'FAIL: {error}', file=sys.stderr)
        print(f'VALIDATION=FAIL ERRORS={len(errors)} AUTHORITY_CREATED=false', file=sys.stderr)
        return 1
    print(f'VALIDATION=PASS DIRECTORIES={sum(1 for _ in governed_directories())} JSON={json_count} AUTHORITY_CREATED=false')
    return 0

if __name__ == '__main__': raise SystemExit(main())
