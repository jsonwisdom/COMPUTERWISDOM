import os
import sys
import json
import subprocess
from pathlib import Path
from web3 import Web3

STATE_PATH = Path("_truth/state.json")
ABI = '[{"inputs":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"name":"anchor","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


def validate_env():
    required = ["BASE_RPC_URL", "ANCHOR_WALLET_KEY", "ANCHOR_REGISTRY_ADDR", "CHAIN_ID"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print(f"FATAL: missing env vars: {missing}")
        sys.exit(1)


def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def run_audit():
    result = subprocess.run(["./verify.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"AUDIT FAILED: {result.stdout}{result.stderr}")
        return False
    return True


def estimate_fees(w3):
    latest = w3.eth.get_block("latest")
    base_fee = latest.get("baseFeePerGas", w3.eth.gas_price)
    priority = w3.to_wei("0.1", "gwei")
    max_fee = int(base_fee * 2 + priority)
    return max_fee, priority


def submit_root():
    validate_env()
    state = load_state()

    current_root = state.get("last_merkle_root")
    anchored_root = state.get("anchored_root")
    status = state.get("anchor_status")

    if status == "pending":
        print("ABORT: anchor in-flight")
        return

    if current_root and current_root == anchored_root and status == "settled":
        print("SKIP: current root already settled on-chain")
        return

    if not current_root:
        print("No merkle root. Abort.")
        return

    if not run_audit():
        return

    rpc_url = os.getenv("BASE_RPC_URL")
    wallet_key = os.getenv("ANCHOR_WALLET_KEY")
    contract_addr = os.getenv("ANCHOR_REGISTRY_ADDR")
    chain_id = int(os.getenv("CHAIN_ID"))

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("FATAL: RPC unreachable")
        sys.exit(1)

    acct = w3.eth.account.from_key(wallet_key)
    contract = w3.eth.contract(address=contract_addr, abi=ABI)
    max_fee, priority_fee = estimate_fees(w3)

    tx = contract.functions.anchor(Web3.to_bytes(hexstr=current_root)).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 100000,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": priority_fee,
        "chainId": chain_id,
    })

    signed = w3.eth.account.sign_transaction(tx, acct.key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    state["last_anchor_tx"] = tx_hash.hex()
    state["anchor_status"] = "pending"
    state["anchoring_root"] = current_root
    save_state(state)

    print(f"Anchored: {tx_hash.hex()}")


if __name__ == "__main__":
    submit_root()
