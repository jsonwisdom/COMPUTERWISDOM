import json
from pathlib import Path
from decimal import Decimal

WALLET = "0x6076815543ee881fdc486b84c3c99435eca729cc"

summary = {
    "schema": "BOSS_BRE_TREASURY_SUMMARY_V1",
    "wallet": WALLET,
    "pending_count": 0,
    "settled_count": 0,
    "pending_totals": {},
    "settled_totals": {},
    "rewards": [],
}

def add_total(bucket, asset, amount):
    current = Decimal(bucket.get(asset, "0"))
    bucket[asset] = str(current + amount)

for path in Path("rewards").rglob("*.json"):
    if "fixtures" in path.parts:
        continue

    data = json.loads(path.read_text())
    asset = data["asset"]
    amount = Decimal(str(data["amount"]))
    status = data["settlement_status"]

    lane = "settled" if status == "SETTLED" else "pending"

    if lane == "settled":
        summary["settled_count"] += 1
        add_total(summary["settled_totals"], asset, amount)
    else:
        summary["pending_count"] += 1
        add_total(summary["pending_totals"], asset, amount)

    summary["rewards"].append({
        "reward_id": data["reward_id"],
        "asset": asset,
        "amount": str(amount),
        "settlement_status": status,
        "lane": lane,
    })

Path("dashboard").mkdir(exist_ok=True)
Path("dashboard/treasury_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
