#!/usr/bin/env python3
"""Change-only receipt gate (stdlib only). Decides APPEND vs SKIP for one probe receipt.

Each route is keyed independently: (role, http, status, body_sha256). Route A being
healthy never implies route B is healthy. Receipts are appended when ANY route key
changed, or when the heartbeat interval has elapsed. Nothing is ever deleted.
Usage: ooda_receipt_gate.py RECEIPT.json STATE.json HEARTBEAT_HOURS
Prints one JSON line {decision, reason, changed_routes}; updates STATE.json only on APPEND.
"""
import datetime as dt, json, sys
from pathlib import Path

def route_keys(receipt):
    return {r["role"]: [r.get("http"), r.get("status"), r.get("body_sha256")] for r in receipt["routes"]}

def decide(receipt, state, heartbeat_hours, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    keys = route_keys(receipt)
    if not state:
        return "APPEND", "first_observation", sorted(keys), keys
    changed = sorted(k for k in keys if state.get("routes", {}).get(k) != keys[k])
    if changed:
        return "APPEND", "route_state_changed", changed, keys
    last = dt.datetime.fromisoformat(state["last_append_utc"].replace("Z", "+00:00"))
    if now - last >= dt.timedelta(hours=heartbeat_hours):
        return "APPEND", "heartbeat", [], keys
    return "SKIP", "unchanged_within_heartbeat", [], keys

def main(argv):
    receipt = json.loads(Path(argv[1]).read_text())
    sp = Path(argv[2]); hb = float(argv[3])
    state = json.loads(sp.read_text()) if sp.exists() else None
    decision, reason, changed, keys = decide(receipt, state, hb)
    if decision == "APPEND":
        sp.parent.mkdir(parents=True, exist_ok=True)
        sp.write_text(json.dumps({"routes": keys, "last_append_utc": receipt["time_utc"],
                                  "last_receipt_sha256": receipt["canonical_sha256"]}, sort_keys=True) + "\n")
    print(json.dumps({"decision": decision, "reason": reason, "changed_routes": changed}))

if __name__ == "__main__":
    main(sys.argv)
