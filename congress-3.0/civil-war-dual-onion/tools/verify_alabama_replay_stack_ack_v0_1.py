#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "alabama-live-constitution/schema/ALABAMA_REPLAY_STACK_ACK_SCHEMA_V0_1.json"
RECEIPT = ROOT / "alabama-live-constitution/receipts/ALABAMA_REPLAY_STACK_ACK_2026_08_18.json"

schema = json.loads(SCHEMA.read_text())
wrapper = json.loads(RECEIPT.read_text())
receipt = wrapper["declared_receipt"]
stack = receipt["alabama_replay_stack"]

assert schema["$id"] == "ALABAMA_REPLAY_STACK_ACK_SCHEMA_V0_1"
assert set(receipt) == {"timestamp", "alabama_replay_stack"}
for key in schema["required"]:
    assert key in receipt
for key in schema["properties"]["alabama_replay_stack"]["required"]:
    assert key in stack

assert stack["pr"]["number"] == 496
assert len(stack["pr"]["head"]) == 40
int(stack["pr"]["head"], 16)
assert len(stack["components"]) >= 5
assert stack["current_gates"]["FACT_PROMOTION"] == 0
assert stack["current_gates"]["AUTHORITY_CREATED"] is False
assert stack["current_gates"]["MERGE"] == "NO"
assert stack["api_key_status"]["created"] is False
assert stack["api_key_status"]["model_required"] is False

observed = datetime.fromisoformat(wrapper["observation_time"].replace("Z", "+00:00"))
declared = datetime.fromisoformat(receipt["timestamp"].replace("Z", "+00:00"))
assert declared > observed
assert wrapper["validation"]["schema_compliance"] == "PASS_AFTER_SCHEMA_BINDING"
assert wrapper["validation"]["timestamp_relation"] == "HOLD_FUTURE_RELATIVE_TO_OBSERVATION"

print("ALABAMA_REPLAY_ACK_SCHEMA_COMPLIANCE=PASS")
print("ALABAMA_REPLAY_ACK_TIMESTAMP_RELATION=HOLD_FUTURE_RELATIVE_TO_OBSERVATION")
print("FACT_PROMOTION=0")
print("AUTHORITY_CREATED=FALSE")
print("MERGE_AUTHORIZED=FALSE")
