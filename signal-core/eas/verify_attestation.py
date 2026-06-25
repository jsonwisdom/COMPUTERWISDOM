#!/usr/bin/env python3
"""Optional EAS attestation verification rail for Receipt Core.

This module keeps EAS lookup optional. Local verification remains the source of
execution semantics. EAS is used only as a public schema and attestation lookup.

Exit map:
0 = pass
1 = policy fail
2 = schema / attestation / receipt mismatch
3 = system / missing dependency / input error
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / 'eas' / 'receipt-core-v0.4.eas.json'


def load_manifest(path=MANIFEST_PATH):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def load_local_receipt(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require_optional_sdk():
    try:
        from EAS import EAS  # type: ignore
    except Exception as exc:
        raise RuntimeError('optional EAS SDK missing; install eas-sdk/web3 before live lookup') from exc
    return EAS


def normalize_decoded_data(decoded):
    if decoded is None:
        return {}
    if isinstance(decoded, dict):
        return decoded
    if isinstance(decoded, list):
        out = {}
        for item in decoded:
            if isinstance(item, dict) and 'name' in item and 'value' in item:
                out[item['name']] = item['value']
        return out
    return {}


def verify_attestation_data(attestation, local_receipt_path=None, manifest_path=MANIFEST_PATH):
    manifest = load_manifest(manifest_path)
    expected_schema = manifest['schema_uid']
    att_schema = getattr(attestation, 'schema', None)
    if att_schema != expected_schema:
        print('FAIL EAS schema mismatch', file=sys.stderr)
        return 2

    data = normalize_decoded_data(getattr(attestation, 'decoded_data', None))
    if data.get('authorityNone') is not True:
        print('FAIL EAS authorityNone missing or false', file=sys.stderr)
        return 2

    if local_receipt_path:
        receipt = load_local_receipt(local_receipt_path)
        if data.get('receiptCoreHash') != receipt.get('receipt_core_hash'):
            print('FAIL EAS receiptCoreHash mismatch', file=sys.stderr)
            return 2
        if data.get('receiptId') != receipt.get('receipt_id'):
            print('FAIL EAS receiptId mismatch', file=sys.stderr)
            return 2

    print('PASS EAS attestation verified')
    return 0


def verify_onchain_attestation(attestation_uid, local_receipt_path=None):
    try:
        EAS = require_optional_sdk()
        eas = EAS.from_chain(chain='base')
        attestation = eas.get_attestation(attestation_uid)
        return verify_attestation_data(attestation, local_receipt_path)
    except RuntimeError as exc:
        print(f'FAIL EAS dependency: {exc}', file=sys.stderr)
        return 3
    except Exception as exc:
        print(f'FAIL EAS lookup: {exc}', file=sys.stderr)
        return 3


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print('Usage: verify_attestation.py <attestation_uid> [local_receipt.json]', file=sys.stderr)
        return 3
    uid = argv[0]
    local = argv[1] if len(argv) > 1 else None
    return verify_onchain_attestation(uid, local)


if __name__ == '__main__':
    raise SystemExit(main())
