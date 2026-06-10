#!/usr/bin/env python3
import json, sys
from pathlib import Path

REQ = {
  "OBSERVER_IS_NOT_OFFICE",
  "MEDIA_REPORT_IS_NOT_BINDING_LAW",
  "ADVISORY_APPOINTMENT_IS_NOT_EXECUTIVE_ORDER",
  "CORROBORATION_IS_NOT_AUTHORITY"
}

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

p = Path(sys.argv[1]) if len(sys.argv) == 2 else fail("usage: verify_federal_observer_child.py <child.json>")
d = json.loads(p.read_text())

if d.get("authority") != "NONE": fail("authority must be NONE")
if d.get("boundary") != "OBSERVER_IS_NOT_OFFICE": fail("boundary must be OBSERVER_IS_NOT_OFFICE")
if d.get("writes") != "APPEND_ONLY_RECEIPTS": fail("writes must be APPEND_ONLY_RECEIPTS")
if d.get("mutates_existing_records") is not False: fail("mutates_existing_records must be false")
if d.get("is_federal_authority") is not False: fail("is_federal_authority must be false")

missing = REQ - set(d.get("invariants", []))
if missing: fail(f"missing invariants: {sorted(missing)}")

print("PASS")
