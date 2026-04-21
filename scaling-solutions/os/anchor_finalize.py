import os
import json
from pathlib import Path
from web3 import Web3

STATE_PATH = Path("_truth/state.json")
CONFIRMATION_THRESHOLD = int(os.getenv("CONFIRM_THRESHOLD", "12"))


def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def check_finality():
    rpc_url = os.getenv("BASE_RPC_URL")
    if not rpc_url:
        print("FATAL: BASE_RPC_URL missing")
        return

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("RPC unreachable")
        return

    state = load_state()
    tx_hash = state.get("last_anchor_tx")

    if state.get("anchor_status") != "pending" or not tx_hash:
        print(f"Skipping: status={state.get('anchor_status')}")
        return

    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
    except Exception as e:
        print(f"RPC error: {e}")
        return

    if receipt is None:
        print("Transaction not yet mined or dropped")
        return

    current_block = w3.eth.block_number
    confirmations = current_block - receipt["blockNumber"]

    if confirmations < CONFIRMATION_THRESHOLD:
        print(f"WAITING: {confirmations}/{CONFIRMATION_THRESHOLD} confirmations")
        return

    if receipt["status"] == 1:
        state["anchor_status"] = "settled"
        state["anchored_root"] = state.get("anchoring_root")
        state["last_settled_block"] = receipt["blockNumber"]
        print(f"FINALIZED with {confirmations} confirmations")
    else:
        state["anchor_status"] = "failed"
        print("Transaction reverted")

    save_state(state)


if __name__ == "__main__":
    check_finality()
