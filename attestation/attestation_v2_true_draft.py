#!/usr/bin/env python3
"""v2_true draft: cryptographic attestation verifier for AWS Nitro Enclaves.

WARNING:
- This is a draft prototype, not production trust logic.
- It should not be labeled final until validated against real Nitro samples,
  official AWS root material, and the exact COSE/x5chain encoding used in practice.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from typing import Dict, Tuple, Optional
import requests

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cose.messages import Sign1Message
import cbor2

AWS_NITRO_ROOT_URL = "https://aws-nitro-enclaves.amazonaws.com/AWS_Nitro_Enclaves_Root_CA.pem"
AWS_NITRO_ROOT_PIN_SHA256 = "REPLACE_WITH_VERIFIED_FINGERPRINT"


def get_aws_root_cert() -> x509.Certificate:
    resp = requests.get(AWS_NITRO_ROOT_URL, timeout=10)
    resp.raise_for_status()

    cert_bytes = resp.content
    fingerprint = hashlib.sha256(cert_bytes).hexdigest().upper()
    fingerprint_colon = ":".join(fingerprint[i:i+2] for i in range(0, len(fingerprint), 2))

    if AWS_NITRO_ROOT_PIN_SHA256 == "REPLACE_WITH_VERIFIED_FINGERPRINT":
        raise ValueError("root fingerprint placeholder not yet replaced")
    if fingerprint_colon != AWS_NITRO_ROOT_PIN_SHA256:
        raise ValueError(f"root cert fingerprint mismatch: {fingerprint_colon}")

    return x509.load_pem_x509_certificate(cert_bytes, default_backend())


def parse_cose_sign1_full(cose_data: bytes):
    msg = Sign1Message.decode(cose_data)
    protected = msg.phdr
    unprotected = msg.uhdr
    payload = msg.payload
    signature = msg.signature

    # Draft Sig_structure reconstruction. Must be validated against live Nitro samples.
    sig_structure = cbor2.dumps([
        "Signature1",
        protected if isinstance(protected, bytes) else b"",
        b"",
        payload,
    ])

    return protected, unprotected, payload, signature, sig_structure


def validate_cert_chain_v2(cert_chain_pems: list, root_cert: x509.Certificate) -> Tuple[bool, str]:
    try:
        certs = [x509.load_pem_x509_certificate(cert.encode(), default_backend()) for cert in cert_chain_pems]

        for cert in certs[:-1]:
            issuer = cert.issuer
            found = False
            for potential_issuer in certs[1:]:
                if potential_issuer.subject == issuer:
                    potential_issuer.public_key().verify(
                        cert.signature,
                        cert.tbs_certificate_bytes,
                        ec.ECDSA(hashes.SHA384())
                    )
                    found = True
                    break
            if not found:
                return False, "missing issuer in chain"

        root_cert.public_key().verify(
            certs[-1].signature,
            certs[-1].tbs_certificate_bytes,
            ec.ECDSA(hashes.SHA384())
        )

        now = datetime.utcnow()
        for cert in certs:
            if now < cert.not_valid_before or now > cert.not_valid_after:
                return False, f"certificate expired: {cert.subject}"

        return True, "chain valid"
    except Exception as e:
        return False, f"chain validation failed: {e}"


def verify_signature_sig_structure(sig_structure: bytes, signature: bytes, public_key_pem: bytes) -> bool:
    try:
        pub_key = serialization.load_pem_public_key(public_key_pem, default_backend())
        pub_key.verify(signature, sig_structure, ec.ECDSA(hashes.SHA384()))
        return True
    except Exception:
        return False


def parse_cbor_attestation(payload: bytes) -> Dict:
    return cbor2.loads(payload)


def extract_pcrs_v2(doc: Dict) -> Dict[str, str]:
    pcrs = {}
    if "pcrs" in doc:
        for key, value in doc["pcrs"].items():
            if isinstance(value, str) and value.startswith("0x"):
                pcrs[key] = value.lower()
    return pcrs


def verify_attestation_v2_true(attestation_file: str, expected_measurement: str, registry_rpc: Optional[str] = None, registry_address: Optional[str] = None) -> Dict:
    try:
        with open(attestation_file, "rb") as f:
            cose_data = f.read()
    except Exception as e:
        return {"status": "REJECTED", "reason": f"READ_ERROR: {e}"}

    try:
        protected, unprotected, payload, signature, sig_structure = parse_cose_sign1_full(cose_data)
    except Exception as e:
        return {"status": "REJECTED", "reason": f"INVALID_COSE: {e}"}

    cert_chain_pems = unprotected.get("x5chain", []) if isinstance(unprotected, dict) else []
    if not cert_chain_pems:
        return {"status": "REJECTED", "reason": "NO_CERT_CHAIN"}

    try:
        root_cert = get_aws_root_cert()
    except Exception as e:
        return {"status": "REJECTED", "reason": f"ROOT_CERT_FAILED: {e}"}

    chain_valid, chain_msg = validate_cert_chain_v2(cert_chain_pems, root_cert)
    if not chain_valid:
        return {"status": "REJECTED", "reason": f"CERT_CHAIN_INVALID: {chain_msg}"}

    try:
        leaf_cert = x509.load_pem_x509_certificate(cert_chain_pems[0].encode(), default_backend())
        leaf_pub_pem = leaf_cert.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    except Exception as e:
        return {"status": "REJECTED", "reason": f"LEAF_CERT_ERROR: {e}"}

    if not verify_signature_sig_structure(sig_structure, signature, leaf_pub_pem):
        return {"status": "REJECTED", "reason": "INVALID_SIGNATURE_OVER_SIG_STRUCTURE"}

    try:
        doc = parse_cbor_attestation(payload)
    except Exception as e:
        return {"status": "REJECTED", "reason": f"INVALID_CBOR_PAYLOAD: {e}"}

    pcrs = extract_pcrs_v2(doc)
    if "PCR0" not in pcrs or "PCR8" not in pcrs:
        return {"status": "REJECTED", "reason": "MISSING_PCR_VALUES"}

    module_id = doc.get("module_id", "")
    if not module_id:
        return {"status": "REJECTED", "reason": "MISSING_MODULE_ID"}

    if pcrs.get("PCR8") != expected_measurement.lower():
        return {
            "status": "REJECTED",
            "reason": f"PCR8_MISMATCH: {pcrs.get('PCR8')} != {expected_measurement.lower()}",
            "module_id": module_id,
        }

    # Registry binding intentionally left as future work pending live integration.
    return {
        "status": "ACCEPTED_DRAFT",
        "reason": "draft cryptographic path passed local checks",
        "pcrs": pcrs,
        "module_id": module_id,
        "timestamp": doc.get("timestamp"),
        "user_data": doc.get("user_data"),
    }


def main():
    parser = argparse.ArgumentParser(description="v2_true draft cryptographic attestation verifier")
    parser.add_argument("--attestation-file", required=True, help="COSE_Sign1 attestation file")
    parser.add_argument("--expected-measurement", required=True, help="Expected PCR8 value from registry")
    parser.add_argument("--registry-rpc", help="Base RPC URL for on-chain binding")
    parser.add_argument("--registry-address", help="Registry address for on-chain binding")
    args = parser.parse_args()

    result = verify_attestation_v2_true(
        args.attestation_file,
        args.expected_measurement,
        args.registry_rpc,
        args.registry_address,
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "ACCEPTED_DRAFT" else 1)


if __name__ == "__main__":
    main()
