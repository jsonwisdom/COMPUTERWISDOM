import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from policy.rql_lite import PolicyError, evaluate_policy_file
from validator.schema_validate import ReceiptSchemaError, validate_receipt


DEFAULT_SCHEMA = ROOT / 'schema' / 'verification-receipt-v0.1.schema.json'


def verify_receipt(receipt_path: str, schema_path: str = None, policy_path: str = None) -> int:
    """Verify a sealed receipt with the v0.1 structural contract and optional policy gate."""
    try:
        path = Path(receipt_path)
        receipt = json.loads(path.read_text(encoding='utf-8'))

        schema = Path(schema_path) if schema_path else DEFAULT_SCHEMA
        if schema.exists():
            print(f'Schema check: {schema}')

        validate_receipt(receipt)

        if policy_path:
            evaluate_policy_file(receipt, policy_path)
            print(f'Policy check: {policy_path}')

        print('PASS Receipt verified')
        return 0
    except FileNotFoundError as exc:
        print(f'FAIL missing file: {exc}', file=sys.stderr)
        return 3
    except json.JSONDecodeError as exc:
        print(f'FAIL invalid json: {exc}', file=sys.stderr)
        return 3
    except ReceiptSchemaError as exc:
        print(f'FAIL receipt schema: {exc}', file=sys.stderr)
        return 2
    except PolicyError as exc:
        print(f'FAIL receipt policy: {exc}', file=sys.stderr)
        return 1
    except Exception as exc:
        print(f'FAIL error: {exc}', file=sys.stderr)
        return 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='receipts')
    sub = parser.add_subparsers(dest='command', required=True)
    verify = sub.add_parser('verify', help='verify a sealed receipt')
    verify.add_argument('receipt_path')
    verify.add_argument('--schema', default=None)
    verify.add_argument('--policy', default=None)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == 'verify':
        return verify_receipt(args.receipt_path, args.schema, args.policy)
    return 3


if __name__ == '__main__':
    raise SystemExit(main())
