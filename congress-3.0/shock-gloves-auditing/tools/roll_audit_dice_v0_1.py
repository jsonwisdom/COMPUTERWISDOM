#!/usr/bin/env python3
import hashlib
import json
import sys

FACES = {
    "TIME_SOURCE_DIE": ["COURT_DOCKET", "NEF", "SERVER_LOG", "GIT_COMMIT", "ARCHIVE_CAPTURE", "USER_DECLARED"],
    "TEMPORAL_STATE_DIE": ["ORDERED", "OUT_OF_ORDER", "CLOCK_SKEW", "EDIT_AFTER_EVENT", "MISSING_TIMESTAMP", "CONFLICT"],
    "RECEIPT_DIE": ["HASHED", "SIGNED", "DOCKETED", "EMAILED", "SCREENSHOT_ONLY", "NONE"],
    "CLERK_GATE_DIE": ["FILING_RECEIVED", "DOCKET_ENTRY", "NOTICE_ISSUED", "CORRECTION_ENTRY", "NOT_APPLICABLE", "HOLD"],
    "CONTEMPT_GATE_DIE": ["COURT_ORDER_BOUND", "NOTICE_BOUND", "DISOBEDIENCE_BOUND", "AUTHORITY_BOUND", "ELEMENT_MISSING", "NOT_A_COURT_QUESTION"],
    "SUFFICIENCY_DIE": ["PASS", "HOLD", "CONFLICT", "REJECT", "NEEDS_SOURCE", "NEEDS_AUTHORITY"],
}


def roll(seed_input: str):
    digest = hashlib.sha256(seed_input.encode("utf-8")).hexdigest()
    raw = bytes.fromhex(digest)
    result = {}
    for index, (die, faces) in enumerate(FACES.items()):
        result[die] = faces[raw[index] % len(faces)]
    sufficiency = result["SUFFICIENCY_DIE"]
    terminal = sufficiency if sufficiency in {"PASS", "HOLD", "CONFLICT", "REJECT"} else "HOLD"
    return digest, result, terminal


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: roll_audit_dice_v0_1.py '<seed-input>'")
    digest, result, terminal = roll(sys.argv[1])
    print(json.dumps({
        "seed_input": sys.argv[1],
        "seed_sha256": digest,
        "roll": result,
        "terminal": terminal,
        "boundaries": {
            "dice_roll_is_fact": False,
            "contempt_found": False,
            "physical_enforcement": False,
            "legal_advice": False,
            "authority_created": False,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
