"""CI-FIRST forensic event validation. Public code only; private evidence stays off GitHub."""
from __future__ import annotations

import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

EVENT_TYPES = {"purchase", "deposit", "withdrawal", "transfer", "balance_snapshot", "claim", "dispute"}
STATES = {"reported", "requested", "approved", "confirmed", "unknown"}
SHA256 = re.compile(r"^[a-f0-9]{64}$")
HEX = re.compile(r"^[a-f0-9]+$")
REQUIRED = ("event_id", "date_utc", "provider", "asset", "event_type", "state", "amount", "source_ref")


def validate(event: dict) -> list[str]:
    errors = []
    if not isinstance(event, dict):
        return ["event must be an object"]
    for key in REQUIRED:
        if not isinstance(event.get(key), str) or not event[key].strip():
            errors.append(f"missing or invalid {key}")
    if errors:
        return errors
    if event["event_type"] not in EVENT_TYPES:
        errors.append("unrecognized event_type")
    if event["state"] not in STATES:
        errors.append("unrecognized state")
    try:
        number = Decimal(event["amount"])
        if not number.is_finite() or number < 0:
            errors.append("amount must be nonnegative finite decimal")
    except (InvalidOperation, TypeError, ValueError):
        errors.append("amount must be a decimal string")
    # Retain provider identifiers only in access-controlled evidence storage.
    for key in ("source_sha256",):
        value = event.get(key)
        if value is not None and (not isinstance(value, str) or not SHA256.fullmatch(value)):
            errors.append(f"{key} must be SHA-256 hex")
    for key in ("destination", "seed", "mnemonic", "private_key", "secret", "password", "recovery_url"):
        if key in event:
            errors.append(f"sensitive field prohibited: {key}")
    if event.get("asserted_current_balance") is not None:
        errors.append("current balance must have separate independently verified record")
    return errors


def audit(records: list[dict]) -> dict:
    issues = []
    seen_ids = set()
    identity = {}
    for i, event in enumerate(records):
        errs = validate(event)
        issues.extend(f"row {i}: {e}" for e in errs)
        if errs:
            continue
        eid = event["event_id"]
        if eid in seen_ids:
            issues.append(f"row {i}: repeated event_id")
        seen_ids.add(eid)
        # Identical provider+order+event+asset records are duplicate evidence, not extra assets.
        order = event.get("provider_order_ref")
        if order:
            key = (event["provider"], order, event["event_type"], event["asset"])
            if key in identity:
                issues.append(f"row {i}: duplicate order-event; review with row {identity[key]}")
            else:
                identity[key] = i
    return {
        "status": "PASS" if not issues else "HOLD",
        "records_examined": len(records),
        "findings": issues,
        "portfolio_total": None,
        "asset_recovered": None,
        "loss_inferred": False,
        "signing_authority": False,
        "reconciliation_complete": False,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python forensic-ledger/validator.py synthetic-events.json", file=sys.stderr)
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("input must be an event array", file=sys.stderr)
        return 2
    report = audit(data)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
