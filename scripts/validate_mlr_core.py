#!/usr/bin/env python3
import hashlib, json, sys

EXPECTED_SHA256 = "3864e9148683a3c6cb7e951c154af46fcd10ed88da7b3c72618aab5460b8e910"
REQUIRED_LINEAGE_IDS = {
    "triggerdeck-canon-v1",
    "mirrorstorm-genesis-v0",
    "mirrorstorm-monastery-quarantine",
}

path = sys.argv[1] if len(sys.argv) > 1 else "MLR_CORE_001.json"
raw = open(path, "rb").read()
actual = hashlib.sha256(raw).hexdigest()

if path == "MLR_CORE_001.json" and actual != EXPECTED_SHA256:
    print(f"FAILED: SHA256 mismatch expected={EXPECTED_SHA256} actual={actual}")
    sys.exit(1)

data = json.loads(raw)
lineage_ids = {entry.get("lineage_id") for entry in data.get("entries", [])}
missing = REQUIRED_LINEAGE_IDS - lineage_ids

if missing:
    print(f"FAILED: missing lineage IDs: {sorted(missing)}")
    sys.exit(1)

print("SUCCESS: MLR registry validated.")
