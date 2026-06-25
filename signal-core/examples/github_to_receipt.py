#!/usr/bin/env python3
"""GitHub PR/Issue -> Receipt Core v0.1 example generator.

Usage:
  python signal-core/examples/github_to_receipt.py jsonwisdom/COMPUTERWISDOM 386 sealed_receipt.json
  python signal-core/cli/receipts.py verify sealed_receipt.json
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def h(value):
    return 'sha256:' + hashlib.sha256(value).hexdigest()


def generate_receipt(owner_repo: str, number: int, output: str = None):
    artifact = {
        'type': 'github_pr_or_issue',
        'repo': owner_repo,
        'number': number,
        'title': f'Example GitHub artifact #{number}',
        'source': f'https://github.com/{owner_repo}/pull/{number}',
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }

    claim_graph = {
        'authority': 'NONE',
        'version': 'v0.1',
        'claims': [
            {
                'claim_id': 'github-artifact-observed',
                'statement': 'A GitHub PR or issue artifact was represented as receipt input.',
                'dependencies': [],
                'provenance': {'source': 'github', 'repo': owner_repo, 'number': number},
            }
        ],
    }

    receipt = {
        'artifact_hash': h(canonical_bytes(artifact)),
        'claim_graph_hash': h(canonical_bytes(claim_graph)),
        'claims_count': 1,
        'confidence': {'authority': 'NONE'},
    }
    receipt['receipt_core_hash'] = h(canonical_bytes(receipt))
    receipt_for_id = dict(receipt)
    receipt_for_id['receipt_id'] = ''
    receipt['receipt_id'] = 'vr:' + h(canonical_bytes(receipt_for_id))

    if output:
        Path(output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f'Generated: {output}')
    else:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2:
        print('Usage: github_to_receipt.py <owner/repo> <number> [output.json]', file=sys.stderr)
        return 1
    owner_repo = argv[0]
    number = int(argv[1])
    output = argv[2] if len(argv) > 2 else None
    generate_receipt(owner_repo, number, output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
