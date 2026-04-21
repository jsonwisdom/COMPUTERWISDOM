#!/usr/bin/env python3
import json
import os
import time
import subprocess
from pathlib import Path
from web3 import Web3

STATE_PATH = Path("_truth/state.json")
REGISTRY_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "root", "type": "bytes32"}],
        "name": "anchor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
POLL_SECONDS = int(os.getenv("ANCHOR_LOOP_POLL_SECONDS", "30"))


def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def run_audit() -> bool:
    result = subprocess.run(["./verify.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"AUDIT FAILED: {result.stdout}{result.stderr}")
        return False
    return True


def validate_env():
    required = ["BASE_RPC_URL", "ANCHOR_WALLET_KEY", "ANCHOR_REGISTRY_ADDR", "CHAIN_ID"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing env vars: {missing}")


def estimate_fees(w3):
    latest = w3.eth.get_block("latest")
    base_fee = latest.get("baseFeePerGas", w3.eth.gas_price)
    priority = w3.to_wei("0.1", "gwei")
    max_fee = int(base_fee * 2 + priority)
    return max_fee, priority


def try_anchor_once():
    validate_env()
    state = load_state()
    current_root = state.get("last_merkle_root")
    anchored_root = state.get("anchored_root")
    status = state.get("anchor_status")

    if not current_root:
        print("No merkle root. Waiting.")
        return

    if status == "pending":
        print("Anchor pending. Waiting for finalizer/recovery.")
        return

    if current_root == anchored_root and status == "settled":
        print("Current root already settled. Idle.")
        return

    if not run_audit():
        return

    rpc_url = os.getenv("BASE_RPC_URL")
    wallet_key = os.getenv("ANCHOR_WALLET_KEY")
    registry_addr = Web3.to_checksum_address(os.getenv("ANCHOR_REGISTRY_ADDR"))
    chain_id = int(os.getenv("CHAIN_ID"))

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise RuntimeError("RPC unreachable")

    account = w3.eth.account.from_key(wallet_key)
    registry = w3.eth.contract(address=registry_addr, abi=REGISTRY_ABI)
    max_fee, priority_fee = estimate_fees(w3)
    nonce = w3.eth.get_transaction_count(account.address)

    tx = registry.functions.anchor(Web3.to_bytes(hexstr=current_root)).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "chainId": chain_id,
        "gas": 150000,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": priority_fee
    })

    signed = w3.eth.account.sign_transaction(tx, wallet_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    state["anchor_status"] = "pending"
    state["last_anchor_tx"] = tx_hash.hex()
    state["anchoring_root"] = current_root
    state["last_anchor_nonce"] = nonce
    save_state(state)

    print(f"Anchored root {current_root} in tx {tx_hash.hex()}")


def run_loop():
    print("Anchor loop started")
    while True:
        try:
            try_anchor_once()
        except Exception as e:
            print(f"Sequencer error: {e}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run_loop()
