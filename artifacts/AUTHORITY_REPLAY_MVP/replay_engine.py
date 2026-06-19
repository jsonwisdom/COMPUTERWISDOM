#!/usr/bin/env python3
"""Authority Replay MVP.

Validates whether an agent action has a replayable authority chain.
This is intentionally small and dependency-free.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_RECEIPTS = [
    "user_identity_receipt",
    "policy_receipt",
    "delegation_receipt",
    "revocation_status_receipt",
    "agent_action_receipt",
    "tool_execution_receipt",
]


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def evaluate(receipt: dict) -> dict:
    missing = [key for key in REQUIRED_RECEIPTS if key not in receipt]
    if missing:
        return {"status": "UNOBSERVED", "reason": "missing_receipts", "missing": missing}

    policy = receipt["policy_receipt"]
    action = receipt["agent_action_receipt"]
    revocation = receipt["revocation_status_receipt"]
    delegation = receipt["delegation_receipt"]
    tool = receipt["tool_execution_receipt"]

    if not receipt["user_identity_receipt"].get("verified", False):
        return {"status": "UNOBSERVED", "reason": "user_identity_not_verified"}

    if policy.get("revoked", False) or revocation.get("revoked", False):
        return {"status": "UNOBSERVED", "reason": "policy_revoked"}

    if delegation.get("policy_id") != policy.get("policy_id"):
        return {"status": "UNOBSERVED", "reason": "delegation_policy_mismatch"}

    if delegation.get("delegated_to") != action.get("agent_id"):
        return {"status": "UNOBSERVED", "reason": "delegated_agent_mismatch"}

    executed_at = parse_time(action["executed_at"])
    expires_at = parse_time(policy["expires_at"])
    if executed_at > expires_at:
        return {"status": "UNOBSERVED", "reason": "policy_expired"}

    allowed = policy["allowed"]
    for field in ["repo", "path", "action"]:
        if action.get(field) != allowed.get(field):
            return {"status": "UNOBSERVED", "reason": f"scope_mismatch:{field}"}

    if action.get("lines_changed", 0) > allowed.get("max_lines_changed", 0):
        return {"status": "UNOBSERVED", "reason": "line_change_limit_exceeded"}

    if tool.get("status") != "success":
        return {"status": "UNOBSERVED", "reason": "tool_execution_not_successful"}

    return {"status": "OBSERVED", "reason": "full_authority_chain_valid"}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: replay_engine.py <receipt.json>")
        return 2

    path = Path(sys.argv[1])
    receipt = json.loads(path.read_text())
    result = evaluate(receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "OBSERVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
