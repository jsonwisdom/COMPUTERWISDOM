#!/usr/bin/env python3
"""Validate Seymour Supreme story/entity invariants.

This validator checks the local build contract only.
It does not create authority, seat purpose, or validate external court facts.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OBJ = json.loads((HERE / "SEYMOUR_SUPREME_ENTITY_V0_1.json").read_text())

required_roles = {
    "SS_ROLE_001": "PROCEDURAL_REPLAY_SPECIALIST",
    "SS_ROLE_002": "SUPREME_EDITION_CHARACTER",
    "SS_ROLE_003": "GPKMONSTER_CHARACTER_MEMBER",
}

errors = []

if OBJ.get("authority_created") is not False:
    errors.append("authority_created must be false")

if OBJ.get("canon") is not False:
    errors.append("canon must be false")

roles = {r.get("role_instance_id"): r for r in OBJ.get("role_instances", [])}
for rid, rtype in required_roles.items():
    if rid not in roles:
        errors.append(f"missing role instance {rid}")
    elif roles[rid].get("role_type") != rtype:
        errors.append(f"{rid} role_type mismatch")

research = roles.get("SS_ROLE_001", {})
cannot = set(research.get("authority_ceiling", {}).get("cannot", []))
for hard_stop in {
    "ISSUE_RULING",
    "CREATE_PRECEDENT",
    "PROMOTE_AUTHORITY",
    "PROMOTE_ROLE",
    "SEAT_REPO_PURPOSE",
}:
    if hard_stop not in cannot:
        errors.append(f"research ceiling missing {hard_stop}")

contract = OBJ.get("replay_contract", {})
if contract.get("precedent") is not False:
    errors.append("replay precedent must be false")

for clock in ("EFFECTIVE_AT", "OBSERVED_AT", "RECEIVED_AT"):
    if clock not in contract.get("clocks", []):
        errors.append(f"missing clock {clock}")

container = roles.get("SS_ROLE_003", {}).get("relation", {})
if container.get("purpose_from_relation") != "NOT_PERMITTED":
    errors.append("GPK relation must not infer purpose")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)

print("PASS: Seymour Supreme story/entity membrane intact")
print("AUTHORITY_CREATED=false")
print("CANON=false")
