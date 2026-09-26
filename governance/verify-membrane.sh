#!/usr/bin/env bash
set -euo pipefail

SCHEMA_PATH="${SCHEMA_PATH:-governance/schema/triple_receipt_theater.v0.1.json}"
COMPONENT_RECEIPT_DIR="${COMPONENT_RECEIPT_DIR:-}"

python3 - "$SCHEMA_PATH" "$COMPONENT_RECEIPT_DIR" "$@" <<'PY'
import json
import os
import sys
from pathlib import Path

schema_path = Path(sys.argv[1])
component_dir = Path(sys.argv[2]) if sys.argv[2] else None
theater_paths = [Path(p) for p in sys.argv[3:]]

CANONICAL_ORDER = [
    "base",
    "franny_self_audit",
    "stinker_visibility",
    "dual_receipt",
    "corruption_application",
    "cleaning_attempt",
    "singularity_replay",
]
CHECKED_BY = ["404_KID", "HASH_SMASHER", "SAFE_CRACKER", "PAYDAY_PAIL", "BOSS_BRENDA"]
COMPONENT_MAP = [
    ("base", "base_receipt_id"),
    ("franny_self_audit", "franny_receipt_id"),
    ("stinker_visibility", "stinker_receipt_id"),
    ("dual_receipt", "dual_receipt_id"),
    ("corruption_application", "corruption_receipt_id"),
    ("cleaning_attempt", "cleaning_receipt_id"),
    ("singularity_replay", "singularity_receipt_id"),
]


def die(msg, code=1):
    print(f"MEMBRANE_FAIL: {msg}")
    raise SystemExit(code)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        die(f"invalid JSON in {path}: {exc}")


def receipt_window(obj):
    if "timestamp_start" in obj or "timestamp_end" in obj:
        start = obj.get("timestamp_start")
        end = obj.get("timestamp_end")
        if not isinstance(start, int) or not isinstance(end, int) or start > end:
            return None
        return start, end
    ts = obj.get("timestamp")
    if isinstance(ts, int):
        return ts, ts
    return None


schema = load_json(schema_path)
if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
    die("schema dialect must be Draft 2020-12")
if schema.get("title") != "Triple Receipt Theater v0.1":
    die("unexpected schema title")
inv = schema.get("x-constitutional-invariants", {})
if inv.get("SIMULTANEOUS_TRIPLE_FORCE") != "FORBIDDEN":
    die("simultaneous triple-force invariant missing")
if inv.get("SEQUENTIAL_LINKED_RECEIPT_FAMILY") != "ALLOWED":
    die("sequential linkage invariant missing")
if inv.get("AUTHORITY_CREATED") is not False:
    die("authority-created invariant must remain false")
print("SCHEMA_STRUCTURE=PASS")

if not theater_paths:
    print("THEATER_RECEIPTS=0")
    print("TIMESTAMP_RECONCILIATION=HOLD_UNOBSERVED")
    print("AUTHORITY_CREATED=FALSE")
    print("DISPOSITION=HOLD_NO_THEATER_RECEIPTS")
    raise SystemExit(0)

receipt_index = {}
if component_dir:
    if not component_dir.exists():
        die(f"COMPONENT_RECEIPT_DIR does not exist: {component_dir}")
    for p in component_dir.rglob("*.json"):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        rid = obj.get("receipt_id") if isinstance(obj, dict) else None
        if isinstance(rid, str):
            if rid in receipt_index:
                die(f"duplicate component receipt_id {rid}: {receipt_index[rid][0]} and {p}")
            receipt_index[rid] = (p, obj)

hold = False
for theater_path in theater_paths:
    t = load_json(theater_path)
    if t.get("receipt_type") != "triple_receipt_theater_v0.1":
        die(f"{theater_path}: wrong receipt_type")
    rid = t.get("receipt_id")
    if not isinstance(rid, str) or not rid.startswith("triple_"):
        die(f"{theater_path}: receipt_id must start triple_")
    if t.get("order_of_operations") != CANONICAL_ORDER:
        die(f"{theater_path}: order_of_operations drift")
    if t.get("checked_by") != CHECKED_BY:
        die(f"{theater_path}: checked_by drift")
    if not isinstance(t.get("timestamp"), int) or t["timestamp"] < 0:
        die(f"{theater_path}: timestamp must be non-negative integer")

    final_state = t.get("final_state")
    if not isinstance(final_state, dict):
        die(f"{theater_path}: final_state missing")
    if final_state.get("authority_created") is not False:
        die(f"{theater_path}: authority_created must be false")
    if final_state.get("no_fake_green") is not True:
        die(f"{theater_path}: no_fake_green must be true")
    if final_state.get("membrane") != "INTACT":
        die(f"{theater_path}: membrane must be INTACT")
    if final_state.get("asset_state") not in {"idle", "active", "corrupted", "cleaned", "locked", "burned"}:
        die(f"{theater_path}: invalid asset_state")

    c = t.get("theater_components")
    if not isinstance(c, dict) or not isinstance(c.get("base_receipt_id"), str) or not c["base_receipt_id"]:
        die(f"{theater_path}: base_receipt_id required")
    if "dual_receipt_id" in c and not all(isinstance(c.get(k), str) and c.get(k) for k in ("franny_receipt_id", "stinker_receipt_id")):
        die(f"{theater_path}: dual receipt requires Franny and Stinker component receipts")
    if "singularity_receipt_id" in c and not isinstance(c.get("dual_receipt_id"), str):
        die(f"{theater_path}: Singularity replay in triple theater requires a settled dual receipt")

    referenced = [(op, c[key]) for op, key in COMPONENT_MAP if isinstance(c.get(key), str)]
    if not component_dir:
        print(f"{rid}: STRUCTURE=PASS")
        print(f"{rid}: COMPONENT_READBACK=HOLD_NO_COMPONENT_RECEIPT_DIR")
        hold = True
        continue

    unresolved = [ref for _, ref in referenced if ref not in receipt_index]
    if unresolved:
        print(f"{rid}: STRUCTURE=PASS")
        print(f"{rid}: COMPONENT_READBACK=HOLD_MISSING_RECEIPTS:{','.join(unresolved)}")
        hold = True
        continue

    previous_end = None
    previous_op = None
    for op, ref in referenced:
        _, obj = receipt_index[ref]
        window = receipt_window(obj)
        if window is None:
            print(f"{rid}: TIMESTAMP_RECONCILIATION=HOLD_UNREADABLE_WINDOW:{ref}")
            hold = True
            break
        start, end = window
        if previous_end is not None and start <= previous_end:
            die(f"{rid}: overlapping/non-sequential windows: {previous_op} -> {op}")
        previous_end = end
        previous_op = op
    else:
        print(f"{rid}: STRUCTURE=PASS")
        print(f"{rid}: COMPONENT_READBACK=PASS")
        print(f"{rid}: TIMESTAMP_RECONCILIATION=PASS")

print("AUTHORITY_CREATED=FALSE")
print("NO_FAKE_GREEN=TRUE")
print("DISPOSITION=" + ("HOLD" if hold else "PASS"))
raise SystemExit(0 if not hold else 2)
PY
