#!/usr/bin/env python3
import copy
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
VERIFIER = HERE / "verify_receipt.py"

VALID_RECEIPT = {
    "schema": "computerwisdom.base-bootstrap-receipt.v1",
    "receipt_id": "gate2-test-001",
    "observed_at_utc": "2026-08-22T00:00:00Z",
    "chain": "base-sepolia",
    "chain_id": 84532,
    "wallet_address": "0x0000000000000000000000000000000000000001",
    "action": "boundary_check",
    "transaction_sent": False,
    "payment": False,
    "automatic_signing": False,
    "merge": False,
    "push": False,
    "authority_created": False,
}


def die(message: str) -> None:
    print(f"GATE2_TEST_FAILURE: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_verifier(receipt: object, optimize: bool) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = pathlib.Path(tmpdir) / "receipt.json"
        path.write_text(json.dumps(receipt, separators=(",", ":")) + "\n", encoding="utf-8")
        cmd = [sys.executable]
        if optimize:
            cmd.append("-O")
        cmd.extend([str(VERIFIER), str(path)])
        return subprocess.run(cmd, text=True, capture_output=True, check=False)


def require_rejected(name: str, receipt: object, optimize: bool) -> None:
    result = run_verifier(receipt, optimize)
    mode = "python -O" if optimize else "python"
    if result.returncode == 0:
        die(f"{name} was accepted under {mode}")
    if "VALIDATION_ERROR:" not in result.stderr:
        die(f"{name} did not emit deterministic validation error under {mode}: {result.stderr!r}")


def require_accepted(name: str, receipt: object, optimize: bool) -> None:
    result = run_verifier(receipt, optimize)
    mode = "python -O" if optimize else "python"
    if result.returncode != 0:
        die(f"{name} was rejected under {mode}: {result.stderr!r}")
    if '"verified":true' not in result.stdout:
        die(f"{name} did not emit verified=true under {mode}: {result.stdout!r}")


def mutated(**changes: object) -> dict:
    receipt = copy.deepcopy(VALID_RECEIPT)
    receipt.update(changes)
    return receipt


def without(key: str) -> dict:
    receipt = copy.deepcopy(VALID_RECEIPT)
    del receipt[key]
    return receipt


def main() -> int:
    cases = [
        ("wrong schema", mutated(schema="wrong.schema")),
        ("invalid chain", mutated(chain="ethereum", chain_id=1)),
        ("mismatched chain id", mutated(chain_id=8453)),
        ("authority created true", mutated(authority_created=True)),
        ("transaction sent true", mutated(transaction_sent=True)),
        ("missing required false field", without("payment")),
        ("malformed wallet", mutated(wallet_address="0x1234")),
        ("non-object JSON", ["not", "an", "object"]),
    ]

    for optimize in (False, True):
        require_accepted("valid receipt", VALID_RECEIPT, optimize)
        for name, receipt in cases:
            require_rejected(name, receipt, optimize)

    print("GATE2_TEST_SUCCESS: verifier rejects malformed receipts under python and python -O")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
