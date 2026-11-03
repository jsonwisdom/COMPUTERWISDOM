#!/usr/bin/env python3
import copy
import hashlib
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema package required", file=sys.stderr)
    raise SystemExit(2)

SCHEMA_PATH = Path(__file__).parent / "config" / "receipt-schema.json"

def canonical_preimage(receipt):
    data = copy.deepcopy(receipt)
    data.pop("receipt_id", None)
    integrity = data.get("integrity")
    if isinstance(integrity, dict):
        integrity.pop("content_hash", None)
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def computed_hash(receipt):
    return hashlib.sha256(canonical_preimage(receipt)).hexdigest()

def main():
    if len(sys.argv) != 2:
        print("Usage: receipt_validator.py <receipt.json>", file=sys.stderr)
        return 2
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        receipt = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    errors = sorted(validator_cls(schema).iter_errors(receipt), key=lambda e: list(e.absolute_path))
    if errors:
        for error in errors:
            path = ".".join(str(p) for p in error.absolute_path) or "(root)"
            print(f"SCHEMA_VIOLATION: {path}: {error.message}", file=sys.stderr)
        return 1

    digest = computed_hash(receipt)
    if receipt["integrity"]["content_hash"] != digest:
        print("CONTENT_HASH_MISMATCH", file=sys.stderr)
        return 1
    if receipt["receipt_id"] != digest:
        print("RECEIPT_ID_MISMATCH", file=sys.stderr)
        return 1

    print("RECEIPT_VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
