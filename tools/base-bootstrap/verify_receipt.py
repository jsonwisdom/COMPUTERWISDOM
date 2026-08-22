#!/usr/bin/env python3
import hashlib
import json
import pathlib
import re
import sys

REQUIRED_FALSE = (
    "transaction_sent",
    "payment",
    "automatic_signing",
    "merge",
    "push",
    "authority_created",
)
CHAIN_IDS = {"base": 8453, "base-sepolia": 84532}
SCHEMA = "computerwisdom.base-bootstrap-receipt.v1"
WALLET_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")


def fail(message: str) -> None:
    print(f"VALIDATION_ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_receipt(data: object) -> dict:
    if not isinstance(data, dict):
        fail("receipt must be a JSON object")

    if data.get("schema") != SCHEMA:
        fail("invalid or missing schema")

    chain = data.get("chain")
    if chain not in CHAIN_IDS:
        fail("invalid or missing chain")

    if data.get("chain_id") != CHAIN_IDS[chain]:
        fail("chain_id does not match chain")

    for key in REQUIRED_FALSE:
        if key not in data or data[key] is not False:
            fail(f"{key} must be explicitly false")

    wallet = data.get("wallet_address")
    if not isinstance(wallet, str) or WALLET_RE.fullmatch(wallet) is None:
        fail("wallet_address must be a 20-byte 0x-prefixed EVM address")

    return data


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: verify_receipt.py RECEIPT.json")

    path = pathlib.Path(sys.argv[1])
    try:
        raw = path.read_bytes()
    except OSError as exc:
        fail(f"cannot read receipt: {exc}")

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(f"invalid JSON payload: {exc}")

    validate_receipt(data)
    print(
        json.dumps(
            {
                "receipt": str(path),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "verified": True,
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
