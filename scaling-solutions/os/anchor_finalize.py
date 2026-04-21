import os
import json
from pathlib import Path
from web3 import Web3

RPC_URL = os.getenv("BASE_SEPOLIA_RPC")
STATE_PATH = Path("_truth/state.json")


def check_finality():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    with open(STATE_PATH, "r") as f:
        state = json.load(f)

    tx_hash = state.get("last_anchor_tx")
    status = state.get("anchor_status")

    if status != "pending" or not tx_hash:
        print(f"Skipping: status={status}")
        return

    print(f"Checking finality for {tx_hash}...")

    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt["status"] == 1:
            state["anchor_status"] = "settled"
            state["last_settled_block"] = receipt["blockNumber"]
            print("Settlement confirmed.")
        else:
            state["anchor_status"] = "failed"
            print("Transaction reverted.")

        with open(STATE_PATH, "w") as f:
            json.dump(state, f, indent=2)

    except Exception as e:
        print(f"Finality check timed out or failed: {e}")


if __name__ == "__main__":
    check_finality()
