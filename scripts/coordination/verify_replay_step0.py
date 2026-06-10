# verify_replay_step0.py
# Step 0 Replay Baseline ported directly from jsonwisdom/AL verification pattern

import json
import os
import hashlib
import sys


def get_canonical_bytes(obj: dict) -> bytes:
    """AL Pattern: Ensure exact JSON byte mapping across runtimes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def run_replay_verification(instructions_file: str, payload_file: str) -> str:
    """
    Enforces AL-style local-first verification rules.
    Exposes: MATCH_CONFIRMED, FAIL_INVALID, MISSING_ARTIFACT, HASH_MISMATCH
    """
    if not os.path.exists(instructions_file) or not os.path.exists(payload_file):
        return "MISSING_ARTIFACT"

    try:
        with open(instructions_file, "r", encoding="utf-8") as f:
            instructions = json.load(f)
        with open(payload_file, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except (json.JSONDecodeError, IOError):
        return "FAIL_INVALID"

    expected_hash = payload.get("immutable_checksum_lock", {}).get("instructions_sha256", "")
    if not expected_hash:
        return "FAIL_INVALID"

    canon_bytes = get_canonical_bytes(instructions)
    calculated_hash = hashlib.sha256(canon_bytes).hexdigest()

    if calculated_hash != expected_hash:
        return "HASH_MISMATCH"

    return "MATCH_CONFIRMED"


if __name__ == "__main__":
    TARGET_INSTRUCTIONS = "replay/instructions/replay_instructions_v1.json"
    TARGET_PAYLOAD = "public_coordination/eas_anchor_payload.json"

    clean_instructions = {
        "instruction_metadata": {
            "description": "Deterministic instruction parameters for verifying pure-function computation state.",
            "protocol": "Replay-Court-Step0",
            "version": "v1.0.0",
        },
        "invariant_assertions": {
            "allow_state_drift": False,
            "execution_mode": "STRICT_REPLAY",
            "require_exact_match": True,
        },
    }

    clean_payload = {
        "immutable_checksum_lock": {
            "instructions_sha256": "3018e5453c7b1135e51af2e27e0b65e8be2552f93550a168867fbf399ab5e636"
        }
    }

    mutated_instructions = dict(clean_instructions)
    mutated_instructions["invariant_assertions"] = {
        "allow_state_drift": True,
        "execution_mode": "STRICT_REPLAY",
        "require_exact_match": True,
    }

    def mock_verify(inst, pay):
        exp = pay.get("immutable_checksum_lock", {}).get("instructions_sha256", "")
        calc = hashlib.sha256(get_canonical_bytes(inst)).hexdigest()
        return "MATCH_CONFIRMED" if calc == exp else "FAIL_INVALID"

    pass_1_res = mock_verify(clean_instructions, clean_payload)
    pass_2_res = mock_verify(mutated_instructions, clean_payload)

    print(f"PASS_1_CLEAN_ARTIFACT: {pass_1_res}")
    print(f"PASS_2_MUTATED_ARTIFACT: {pass_2_res}")

    result = run_replay_verification(TARGET_INSTRUCTIONS, TARGET_PAYLOAD)

    if result == "MATCH_CONFIRMED":
        sys.exit(0)
    sys.exit(1)
