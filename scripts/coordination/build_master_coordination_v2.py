# build_master_coordination_v2.py
# Pure-function state compilation utility using the AL Compact Serialization standard

import json
import os
import hashlib


def get_canonical_bytes(obj: dict) -> bytes:
    """AL Pattern: Strict canonical serialization standard."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def build_coordination_frame(instructions_path: str, payload_path: str) -> dict:
    if not os.path.exists(instructions_path) or not os.path.exists(payload_path):
        raise FileNotFoundError("MISSING_ARTIFACT")

    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = json.load(f)
    with open(payload_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    calculated_hash = hashlib.sha256(get_canonical_bytes(instructions)).hexdigest()

    master_frame = {
        "schema_version": "v2.0.0",
        "calculated_instructions_hash": calculated_hash,
        "payload_manifest": payload,
        "system_integrity_lock": True,
    }
    return master_frame


if __name__ == "__main__":
    try:
        frame = build_coordination_frame(
            "replay/instructions/replay_instructions_v1.json",
            "public_coordination/eas_anchor_payload.json",
        )
        print("Master Coordination Frame Compiled via AL-Pattern.")
    except Exception as e:
        print(f"Compilation Blocked: {str(e)}")
