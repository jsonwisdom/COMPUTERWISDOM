#!/usr/bin/env python3
"""Receipt-of-Receipts v0.3 chain verifier.

Bundle format:
{
  "version": "v0.3",
  "authority": "NONE",
  "receipts": [
    {"id": "A", "path": "a.json", "dependencies": []},
    {"id": "B", "path": "b.json", "dependencies": ["A"]}
  ]
}

Exit map bubbles from receipts verify:
0 = pass
1 = policy fail
2 = receipt/schema validation fail
3 = system/input/orchestration error
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli.receipts import verify_receipt


class ChainError(ValueError):
    pass


def load_bundle(path):
    bundle = json.loads(Path(path).read_text(encoding='utf-8'))
    if bundle.get('authority') != 'NONE':
        raise ChainError('bundle authority must be NONE')
    receipts = bundle.get('receipts')
    if not isinstance(receipts, list) or not receipts:
        raise ChainError('bundle receipts must be a non-empty list')
    by_id = {}
    for item in receipts:
        rid = item.get('id')
        if not rid:
            raise ChainError('receipt item missing id')
        if rid in by_id:
            raise ChainError(f'duplicate receipt id: {rid}')
        deps = item.get('dependencies', [])
        if not isinstance(deps, list):
            raise ChainError(f'dependencies must be a list for {rid}')
        by_id[rid] = item
    for rid, item in by_id.items():
        for dep in item.get('dependencies', []):
            if dep not in by_id:
                raise ChainError(f'unknown dependency for {rid}: {dep}')
    return bundle, by_id


def topo_sort(by_id):
    visiting = set()
    visited = set()
    order = []

    def visit(rid):
        if rid in visited:
            return
        if rid in visiting:
            raise ChainError(f'cycle detected at {rid}')
        visiting.add(rid)
        for dep in by_id[rid].get('dependencies', []):
            visit(dep)
        visiting.remove(rid)
        visited.add(rid)
        order.append(rid)

    for rid in by_id:
        visit(rid)
    return order


def verify_chain(bundle_path, policy_path=None):
    try:
        base = Path(bundle_path).resolve().parent
        _, by_id = load_bundle(bundle_path)
        order = topo_sort(by_id)
        for rid in order:
            receipt_path = Path(by_id[rid]['path'])
            if not receipt_path.is_absolute():
                receipt_path = base / receipt_path
            code = verify_receipt(str(receipt_path), policy_path=policy_path)
            if code != 0:
                print(f'FAIL chain receipt={rid} exit={code}', file=sys.stderr)
                return code
        print('PASS Receipt chain verified')
        return 0
    except ChainError as exc:
        print(f'FAIL receipt chain: {exc}', file=sys.stderr)
        return 3
    except Exception as exc:
        print(f'FAIL receipt chain error: {exc}', file=sys.stderr)
        return 3


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print('Usage: verify_chain.py <receipt_bundle.json> [policy.rql]', file=sys.stderr)
        return 3
    policy = argv[1] if len(argv) > 1 else None
    return verify_chain(argv[0], policy)


if __name__ == '__main__':
    raise SystemExit(main())
