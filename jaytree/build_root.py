#!/usr/bin/env python3
"""Build a deterministic Jaytree root from identity-vector-v0.1.json."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDENTITY = ROOT / 'identity-vector-v0.1.json'
OUTPUT = ROOT / 'identity-vector-v0.1.root.json'


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def main():
    identity = json.loads(IDENTITY.read_text(encoding='utf-8'))
    root = {
        'version': 'jaytree-root-v0.1',
        'authority': 'NONE',
        'identity_manifest': str(IDENTITY.name),
        'identity_manifest_hash': digest(canonical_bytes(identity))
    }
    OUTPUT.write_text(json.dumps(root, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(root, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
