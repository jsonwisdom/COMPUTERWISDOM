#!/usr/bin/env python3
import csv
import sys
from datetime import datetime
from pathlib import Path

TARGET_ADDRESS = "0xa380552a27b0a5a2874ea7aa52cac09f542002e8"
TARGET_NAME = "jaywisdom.base.eth"
REQUIRED = ["uid", "tx_hash", "block_time", "schema_uid", "from", "recipient", "class", "authority"]
CLASS_BY_SCHEMA_NUMBER = {"1576": "R1", "1526": "R2", "1578": "R3"}


def fail(msg: str) -> None:
    raise ValueError(msg)


def norm(s):
    return (s or "").strip()


def parse_time(value: str):
    value = norm(value)
    if not value:
        fail("missing block_time")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"invalid ISO-8601 block_time: {value}")


def expected_class(schema_uid: str) -> str:
    # The export may provide full schema UIDs. Batch 001 only auto-tags when the
    # primary export itself provides a recognized schema number token.
    raw = norm(schema_uid)
    for number, klass in CLASS_BY_SCHEMA_NUMBER.items():
        if raw == number or raw == f"#{number}":
            return klass
    return "OTHER"


def validate_row(row, line_no):
    for key in REQUIRED:
        if key not in row:
            fail(f"line {line_no}: missing column {key}")
        if key != "recipient" and norm(row[key]) == "":
            fail(f"line {line_no}: empty {key}")

    if norm(row["authority"]).upper() != "FALSE":
        fail(f"line {line_no}: authority must be FALSE")

    klass = norm(row["class"]).upper()
    if klass not in {"R1", "R2", "R3", "OTHER"}:
        fail(f"line {line_no}: invalid class {klass}")

    mechanically_expected = expected_class(row["schema_uid"])
    if mechanically_expected != "OTHER" and klass != mechanically_expected:
        fail(f"line {line_no}: class/schema mismatch: expected {mechanically_expected}")

    # Exact-match gate can only be checked from frozen row fields available here.
    recipient_match = norm(row["recipient"]).lower() == TARGET_ADDRESS
    address_in_fields = TARGET_ADDRESS in " ".join(norm(row[k]).lower() for k in row)
    name_in_fields = TARGET_NAME in " ".join(norm(row[k]).lower() for k in row)
    if not (recipient_match or address_in_fields or name_in_fields):
        fail(f"line {line_no}: row does not satisfy target match rule")

    parse_time(row["block_time"])
    return row


def main(path: str):
    p = Path(path)
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED:
            fail(f"header must equal: {','.join(REQUIRED)}")
        rows = [validate_row(r, i) for i, r in enumerate(reader, start=2)]

    seen = set()
    for i, row in enumerate(rows, start=2):
        key = (norm(row["tx_hash"]).lower(), norm(row["schema_uid"]).lower(), norm(row["uid"]).lower())
        if key in seen:
            fail(f"line {i}: duplicate dedupe key {key}")
        seen.add(key)

    ordered = sorted(rows, key=lambda r: parse_time(r["block_time"]))
    if rows != ordered:
        fail("rows are not ordered by block_time ASC")

    print(f"PASS rows={len(rows)} authority_created=false")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_jaywisdom_base_eth_receipts_rail.py <export.csv>", file=sys.stderr)
        sys.exit(2)
    try:
        main(sys.argv[1])
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
