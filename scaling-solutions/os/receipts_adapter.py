#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from signer import sign_receipt_hash

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "_truth" / "state.json"
INVENTORY_PATH = ROOT / "os" / "agent_inventory.json"


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def merkle_root_hex(leaves: List[str]) -> str | None:
    if not leaves:
        return None
    level = [bytes.fromhex(x) for x in leaves]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        nxt = []
        for i in range(0, len(level), 2):
            nxt.append(hashlib.sha256(level[i] + level[i + 1]).digest())
        level = nxt
    return level[0].hex()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value: Dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def allowed_agent_ids(inventory: Dict[str, Any]) -> set[str]:
    out = set()
    for group in inventory.get("agents", {}).values():
        for agent in group:
            agent_id = agent.get("id")
            if agent_id:
                out.add(agent_id)
    return out


def pair_for_agent(inventory: Dict[str, Any], agent_id: str) -> str | None:
    for agent in inventory.get("agents", {}).get("treasury", []):
        if agent.get("id") == agent_id:
            return agent.get("pair")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run receipts adapter for scaling-solutions")
    parser.add_argument("--agent", required=True, help="Agent ENS id")
    parser.add_argument("--input", required=True, help="Input text")
    parser.add_argument("--result", required=True, help="Result text")
    parser.add_argument("--scope", default=None, help="Optional scope/pair, required for treasury agents")
    parser.add_argument("--mode", default="dry_run", choices=["dry_run"], help="Execution mode")
    args = parser.parse_args()

    state = load_json(STATE_PATH)
    inventory = load_json(INVENTORY_PATH)

    if args.agent not in allowed_agent_ids(inventory):
        raise SystemExit(f"unknown agent: {args.agent}")

    expected_pair = pair_for_agent(inventory, args.agent)
    if expected_pair is not None and args.scope != expected_pair:
        raise SystemExit(f"scope mismatch for {args.agent}: expected {expected_pair}, got {args.scope}")

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    input_payload = {"text": args.input, "scope": args.scope}
    result_payload = {"text": args.result}

    receipt = {
        "receipt_version": "0.2.0",
        "mode": args.mode,
        "owner_ens": state.get("owner_ens"),
        "agent_id": args.agent,
        "scope": args.scope,
        "created_at": now,
        "input_hash": sha256_hex_text(canon(input_payload)),
        "result_hash": sha256_hex_text(canon(result_payload))
    }
    receipt["receipt_hash"] = sha256_hex_text(canon(receipt))
    receipt["signature"] = sign_receipt_hash(args.agent, receipt["receipt_hash"])

    receipts = state.setdefault("receipts", [])
    receipts.append(receipt)
    state["last_merkle_root"] = merkle_root_hex([r["receipt_hash"] for r in receipts])
    state["last_updated"] = now
    state["agents"] = sorted(allowed_agent_ids(inventory))

    save_json(STATE_PATH, state)
    print(json.dumps({
        "status": "ok",
        "agent_id": args.agent,
        "receipt_hash": receipt["receipt_hash"],
        "signing_scheme": receipt["signature"]["signing_scheme"],
        "last_merkle_root": state["last_merkle_root"],
        "receipts_count": len(receipts)
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
