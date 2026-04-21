#!/usr/bin/env python3
import os
import sys
from web3 import Web3

ROLES_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "role", "type": "bytes32"},
            {"internalType": "address", "name": "member", "type": "address"}
        ],
        "name": "removeMember",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]


def revoke():
    rpc_url = os.getenv("BASE_MAINNET_RPC")
    modifier_addr = os.getenv("ROLES_MODIFIER_ADDR")
    owner_priv_key = os.getenv("OWNER_PRIVATE_KEY")

    if not all([rpc_url, modifier_addr, owner_priv_key]):
        print("ERROR: Missing BASE_MAINNET_RPC, ROLES_MODIFIER_ADDR, or OWNER_PRIVATE_KEY")
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: python3 revoke_agent.py <ROLE_ID_HEX> <AGENT_ADDRESS>")
        sys.exit(1)

    role_id = sys.argv[1]
    agent_to_revoke = sys.argv[2]

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("ERROR: RPC unreachable")
        sys.exit(1)

    if not Web3.is_hex(role_id):
        print("ERROR: ROLE_ID_HEX must be 0x-prefixed hex bytes32")
        sys.exit(1)

    agent_to_revoke = w3.to_checksum_address(agent_to_revoke)
    modifier_addr = w3.to_checksum_address(modifier_addr)

    owner_account = w3.eth.account.from_key(owner_priv_key)
    modifier_contract = w3.eth.contract(address=modifier_addr, abi=ROLES_ABI)

    tx = modifier_contract.functions.removeMember(
        Web3.to_bytes(hexstr=role_id),
        agent_to_revoke
    ).build_transaction({
        "from": owner_account.address,
        "nonce": w3.eth.get_transaction_count(owner_account.address),
        "gas": 100000,
        "maxFeePerGas": w3.eth.gas_price,
        "maxPriorityFeePerGas": w3.eth.max_priority_fee,
        "chainId": 8453
    })

    signed_tx = w3.eth.account.sign_transaction(tx, owner_priv_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"REVOCATION BROADCAST: {tx_hash.hex()}")
    print("Monitor Basescan and the Safe UI to confirm member removal.")


if __name__ == "__main__":
    revoke()
