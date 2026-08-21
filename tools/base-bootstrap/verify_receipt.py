#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

REQUIRED_FALSE = ("transaction_sent", "payment", "automatic_signing", "merge", "push", "authority_created")

def main() -> int:
    path = pathlib.Path(sys.argv[1])
    raw = path.read_bytes()
    data = json.loads(raw)
    assert data["schema"] == "computerwisdom.base-bootstrap-receipt.v1"
    assert data["chain"] in {"base", "base-sepolia"}
    assert data["chain_id"] == {"base": 8453, "base-sepolia": 84532}[data["chain"]]
    assert all(data[key] is False for key in REQUIRED_FALSE)
    assert data["wallet_address"].startswith("0x") and len(data["wallet_address"]) == 42
    print(json.dumps({"receipt": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "verified": True}, separators=(",", ":")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


