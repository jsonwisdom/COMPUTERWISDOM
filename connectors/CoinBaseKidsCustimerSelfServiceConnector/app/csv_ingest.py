from __future__ import annotations
import csv
from pathlib import Path
from .normalizer import normalize_row


def ingest_csv(path: str) -> list:
    out = []
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            out.append(normalize_row(row, rail="COINBASE_MANUAL_EXPORT", object_type="CSV_ROW"))
    return out
