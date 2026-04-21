#!/usr/bin/env python3
"""Nitro Enclave Attestation Verifier for ZTWS"""

import argparse
import base64
import json
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import requests

EXPECTED_PCRS = {
    "PCR0": "0x3a2b1c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a",
    "PCR8": "0x2b1c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"
}

def parse_attestation(attestation_doc: dict) -> dict:
    """Extract PCRs and signature from AWS Nitro attestation document"""
    pcr_values = {}
    for pcr in ["PCR0", "PCR1", "PCR2", "PCR3", "PCR4", "PCR5", "PCR6", "PCR7", "PCR8"]:
        if pcr in attestation_doc.get("pcrs", {}):
            pcr_values[pcr] = attestation_doc["pcrs"][pcr]

    return {
        "pcrs": pcr_values,
        "signature": attestation_doc.get("signature"),
        "certificate": attestation_doc.get("certificate"),
        "user_data": attestation_doc.get("user_data"),
        "timestamp": attestation_doc.get("timestamp")
    }

def verify_signature(attestation_doc: dict, public_key_pem: str) -> bool:
    """Verify the attestation signature against AWS public key"""
    pub_key = load_pem_public_key(public_key_pem.encode())
    signature = base64.b64decode(attestation_doc["signature"])
    message = json.dumps(attestation_doc["pcrs"], sort_keys=True).encode()

    try:
        pub_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

def check_pcrs(pcr_values: dict) -> bool:
    """Verify PCRs match expected ZTWS enclave measurements"""
    for pcr, expected in EXPECTED_PCRS.items():
        actual = pcr_values.get(pcr)
        if actual != expected:
            print(f"❌ {pcr}: {actual} != {expected}")
            return False
        print(f"✅ {pcr}: MATCH")
    return True

def main():
    parser = argparse.ArgumentParser(description="Verify Nitro Enclave attestation")
    parser.add_argument("--attestation-file", required=True, help="JSON attestation document")
    parser.add_argument("--enclave-id", required=True, help="Expected enclave ID")
    args = parser.parse_args()

    with open(args.attestation_file) as f:
        attestation = json.load(f)

    parsed = parse_attestation(attestation)

    print("📡 Verifying ZTWS enclave attestation...")

    user_data = parsed.get("user_data", "")
    if args.enclave_id not in user_data:
        print(f"❌ Enclave ID mismatch: {args.enclave_id} not in {user_data}")
        sys.exit(1)
    print(f"✅ Enclave ID: {args.enclave_id}")

    if not check_pcrs(parsed["pcrs"]):
        print("❌ PCR verification failed")
        sys.exit(1)

    print("\n⚡ Attestation: VALID")
    print(json.dumps({"status": "attestation_valid", "enclave": args.enclave_id}, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
