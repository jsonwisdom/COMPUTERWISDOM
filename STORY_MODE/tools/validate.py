#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = {
    'PURPOSE', 'MAY_CONTAIN', 'MUST_NOT_CONTAIN',
    'ENTRY_PRECONDITIONS', 'AUTHORITY_NOT_CREATED'
}
REQUIRED_DIRS = [
    '00-identity','01-worlds','02-characters','03-projects','04-scenes',
    '05-claims','06-evidence','07-receipts','08-replay','09-publication',
    'schemas','tools'
]

def fail(message):
    print(f'FAIL: {message}', file=sys.stderr)
    return 1

def main():
    errors = []
    for name in ['.'] + REQUIRED_DIRS:
        directory = ROOT if name == '.' else ROOT / name
        contract = directory / 'DIRECTORY_CONTRACT.json'
        if not contract.is_file():
            errors.append(f'missing directory contract: {contract.relative_to(ROOT)}')
            continue
        try:
            data = json.loads(contract.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid JSON {contract.relative_to(ROOT)}: {exc}')
            continue
        missing = sorted(REQUIRED_KEYS - set(data))
        if missing:
            errors.append(f'{contract.relative_to(ROOT)} missing {missing}')
        if data.get('AUTHORITY_NOT_CREATED') is not True:
            errors.append(f'{contract.relative_to(ROOT)} must set AUTHORITY_NOT_CREATED=true')
    for path in ROOT.rglob('*.json'):
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid JSON {path.relative_to(ROOT)}: {exc}')
    if errors:
        for error in errors:
            fail(error)
        return 1
    print(f'PASS: {len(REQUIRED_DIRS) + 1} contracts; all JSON parsed; AUTHORITY_CREATED=false')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
