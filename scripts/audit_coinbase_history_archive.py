#!/usr/bin/env python3
"""Read-only audit of a local materialization of the private Drive archive.

This script never calls Coinbase and never places or previews trades.
It emits metadata only and must not print raw private identifiers.
"""

from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path
from datetime import datetime

STABLE_ID_FIELD = {"orders": "order_id", "fills": "trade_id"}
TIME_FIELDS = {"orders": ("created_time", "last_fill_time"), "fills": ("trade_time",)}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_time(v: str):
    if not v:
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except Exception:
        return None

def audit_csv(path: Path, surface: str):
    stable = STABLE_ID_FIELD[surface]
    ids, times, rows = set(), [], 0
    duplicates = 0
    fields = None
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = tuple(reader.fieldnames or ())
        for row in reader:
            rows += 1
            sid = (row.get(stable) or "").strip()
            if sid:
                if sid in ids:
                    duplicates += 1
                ids.add(sid)
            for tf in TIME_FIELDS[surface]:
                t = parse_time((row.get(tf) or "").strip())
                if t:
                    times.append(t)
                    break
    return {
        "file": path.name,
        "sha256": sha256(path),
        "rows": rows,
        "distinct_stable_ids": len(ids),
        "duplicate_stable_ids": duplicates,
        "newest_timestamp": max(times).isoformat() if times else None,
        "oldest_timestamp": min(times).isoformat() if times else None,
        "columns": list(fields or ()),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive", type=Path)
    ap.add_argument("--out", type=Path, default=Path("coinbase_history_audit.json"))
    args = ap.parse_args()

    result = {"mode": "READ_ONLY", "execution_performed": False, "authority_created": False, "surfaces": {}}
    for surface in ("orders", "fills"):
        folder = args.archive / surface
        chunks = []
        if folder.exists():
            for p in sorted(folder.glob("*.csv")):
                chunks.append(audit_csv(p, surface))
        schemas = {tuple(c["columns"]) for c in chunks}
        result["surfaces"][surface] = {
            "chunks": len(chunks),
            "rows": sum(c["rows"] for c in chunks),
            "duplicate_stable_ids_within_chunks": sum(c["duplicate_stable_ids"] for c in chunks),
            "schema_variants": len(schemas),
            "chunks_meta": chunks,
        }

    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "orders_chunks": result["surfaces"]["orders"]["chunks"],
        "fills_chunks": result["surfaces"]["fills"]["chunks"],
        "execution_performed": False,
        "authority_created": False,
    }))

if __name__ == "__main__":
    main()
