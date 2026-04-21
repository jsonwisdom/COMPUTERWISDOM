#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path

from web3 import Web3
from web3.exceptions import TransactionNotFound

STATE_PATH = Path("_truth/state.json")
STALE_THRESHOLD = int(os.getenv("ANCHOR_STALE_SECONDS", "1800"))


def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def recover():
    rpc_url = os.getenv("BASE_RPC_URL")
    wallet_addr = os.getenv("ANCHOR_WALLET_ADDR")

    if not rpc_url or not wallet_addr:
        print("ERROR: Missing BASE_RPC_URL or ANCHOR_WALLET_ADDR")
        return

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("ERROR: RPC unreachable")
        return

    wallet_addr = w3.to_checksum_address(wallet_addr)
    state = load_state()

    if state.get("anchor_status") != "pending":
        print("No pending anchor. Nothing to recover.")
        return

    tx_hash = state.get("last_anchor_tx")
    start_time = state.get("anchoring_timestamp", time.time())
    last_nonce = state.get("last_anchor_nonce")

    if not tx_hash or last_nonce is None:
        print("ERROR: Pending state missing tx hash or nonce")
        return

    print(f"Monitoring pending anchor: {tx_hash}")

    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        if receipt is not None:
            if receipt["status"] == 1:
                print("Tx mined successfully. Waiting for finalizer to confirm depth.")
            else:
                print("Tx reverted on-chain. Marking failed.")
                state["anchor_status"] = "failed"
                state["failure_reason"] = "reverted_onchain"
                save_state(state)
            return
    except TransactionNotFound:
        elapsed = time.time() - start_time
        if elapsed <= STALE_THRESHOLD:
            print(f"Tx still in flight. Elapsed {int(elapsed)}s / {STALE_THRESHOLD}s")
            return

        print(f"STALE DETECTED: {int(elapsed)}s elapsed. Checking nonce...")
        current_nonce = w3.eth.get_transaction_count(wallet_addr)

        if current_nonce > last_nonce:
            print("Nonce consumed by different hash. Marking failed for manual audit.")
            state["anchor_status"] = "failed"
            state["failure_reason"] = "nonce_consumed_other_tx"
        else:
            print("Tx likely dropped from mempool. Resetting for re-sequencing.")
            state["anchor_status"] = None
            state["failure_reason"] = "dropped_from_mempool"
            state["last_anchor_tx"] = None
        save_state(state)
    except Exception as e:
        print(f"Recovery scan failed: {e}")


if __name__ == "__main__":
    recover()
