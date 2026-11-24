"""CLI: read-only deterministic navigation receipt to stdout."""
import argparse
import json
import sys
from pathlib import Path
from .router import replay

def main() -> int:
    p = argparse.ArgumentParser(description='Computer Wisdom read-only trigger replay')
    p.add_argument('query', help='Navigation phrase; never authorizes writes')
    p.add_argument('--records', type=Path, help='Read-only JSON metadata list, maximum 500 entries')
    args = p.parse_args()
    try:
        if args.records:
            if args.records.is_symlink() or not args.records.is_file() or args.records.stat().st_size > 200000:
                raise ValueError('records must be a regular JSON file <= 200KB (no symlinks)')
            records = json.loads(args.records.read_text(encoding='utf-8'))
        else:
            records = None
        print(json.dumps(replay(args.query, records), sort_keys=True, separators=(',', ':'), ensure_ascii=False))
        return 0
    except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'FAIL', 'error_type': type(exc).__name__, 'authority_created': False}), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
