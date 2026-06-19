import json
import sys
from pathlib import Path
from decimal import Decimal, InvalidOperation

WALLET = "0x6076815543ee881fdc486b84c3c99435eca729cc"
REQUIRED = [
    "reward_id",
    "destination",
    "network",
    "asset",
    "amount",
    "replay_status",
    "settlement_status",
    "created",
]

errors = []

for path in Path("rewards").rglob("*.json"):
    if "fixtures" in path.parts:
        continue

    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        continue

    for key in REQUIRED:
        if key not in data:
            errors.append(f"{path}: missing {key}")

    if data.get("destination", "").lower() != WALLET.lower():
        errors.append(f"{path}: destination must be Boss Bre wallet")

    if data.get("replay_status") != "REPLAYED":
        errors.append(f"{path}: replay_status must be REPLAYED")

    if data.get("settlement_status") not in ("PENDING", "SETTLED", "REJECTED"):
        errors.append(f"{path}: invalid settlement_status")

    try:
        if Decimal(str(data.get("amount", "0"))) <= 0:
            errors.append(f"{path}: amount must be positive")
    except InvalidOperation:
        errors.append(f"{path}: amount must be numeric string")

if errors:
    print("VALIDATION FAILED")
    for err in errors:
        print(" -", err)
    sys.exit(1)

print("OK: reward receipts valid")
