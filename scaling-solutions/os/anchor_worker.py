import os
import json
import subprocess
from pathlib import Path
from web3 import Web3

RPC_URL = os.getenv("BASE_SEPOLIA_RPC")
WALLET_KEY = os.getenv("ANCHOR_WALLET_KEY")
CONTRACT_ADDR = os.getenv("ANCHOR_REGISTRY_ADDR")
STATE_PATH = Path("_truth/state.json")

ABI = '[{"inputs":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"}],"name":"anchor","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


def run_audit():
    result = subprocess.run(["./verify.sh"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"AUDIT FAILED: {result.stdout}")
        return False
    return True


def submit_root():
    if not run_audit():
        return

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    acct = w3.eth.account.from_key(WALLET_KEY)

    with open(STATE_PATH) as f:
        state = json.load(f)

    root = state.get("last_merkle_root")
    if not root:
        print("No merkle root. Abort.")
        return

    contract = w3.eth.contract(address=CONTRACT_ADDR, abi=ABI)

    tx = contract.functions.anchor(Web3.to_bytes(hexstr=root)).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 100000,
        "maxFeePerGas": w3.to_wei("1.5", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("0.1", "gwei"),
        "chainId": 84532
    })

    signed = w3.eth.account.sign_transaction(tx, acct.key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    state["last_anchor_tx"] = tx_hash.hex()
    state["anchor_status"] = "pending"

    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

    print(f"Anchored: {tx_hash.hex()}")


if __name__ == "__main__":
    submit_root()
