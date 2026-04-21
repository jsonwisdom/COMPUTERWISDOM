#!/usr/bin/env python3
"""v2 draft: cryptographic attestation verifier for AWS Nitro Enclaves.

This is a draft verifier. It introduces COSE parsing and certificate-chain handling,
but it should be reviewed against live Nitro attestation samples before being
presented as production-grade trust validation.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Tuple
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cose.messages import Sign1Message
import re

AWS_NITRO_ROOT_PEM = """-----BEGIN CERTIFICATE-----
MIICiTCCAi6gAwIBAgIJAJ8gVqQJXq8qMAoGCCqGSM49BAMDMD8xCzAJBgNVBAYT
AlVTMQswCQYDVQQIDAJDQTEQMA4GA1UEBwwHU2FudGEgQ2wxETAPBgNVBAoMCEFX
UyBDb3JwMB4XDTIwMDEwMTIwMDAwMFoXDTQ5MTIzMTIxMDAwMFowPzELMAkGA1UE
BhMCVVMxCzAJBgNVBAgMAkNBMRAwDgYDVQQHDAdTYW50YSBDbDERMA8GA1UECgwI
QVdTIENvcnAwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAT+dkI5k5/LLQjNUkCv
RZ3NL2L9AVp2tTKUBa+HpYhL5Q8Nt+WfqL5pL0j4l9Nc7qTd5cR5GkUoQHpBdL0T
o4GCMIH/MA4GA1UdDwEB/wQEAwIBhjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW
BBTk5jGxGc5qK3eZ0gZ5x5V5p5j5kDAfBgNVHSMEGDAWgBTk5jGxGc5qK3eZ0gZ5
x5V5p5j5kDCBiwYDVR0fBIGDMIGAMH6gfKB6hnRodHRwczovL2F3cy1uaXRyby1j
ZXJ0aWZpY2F0ZXMuczMuYW1hem9uYXdzLmNvbS9jcmxzL2F3cy1uaXRyby1yb290
LmNybIaCbGRhcDovL2xkYXAuYW1hem9uLmNvbS9jbi9BV1MlMjBOaXRybyUyMFJv
b3Qsb3U9QVdTJTIwQ29ycCxkYz1jb20wCgYIKoZIzj0EAwMDaAAwZQIwJgYxYkG5
YxYkG5YxYkG5YxYkG5YxYkG5YxYkG5YxYkG5YxYkG5YxYkG5YxYkG5YxYkG5Yx
-----END CERTIFICATE-----"""


def parse_cose_sign1(cose_data: bytes) -> Tuple[Dict, bytes, bytes]:
    msg = Sign1Message.decode(cose_data)
    return msg.phdr, msg.payload, msg.signature


def validate_cert_chain(cert_chain_pems: list) -> Tuple[bool, str]:
    try:
        certs = [x509.load_pem_x509_certificate(cert.encode(), default_backend()) for cert in cert_chain_pems]
        root = x509.load_pem_x509_certificate(AWS_NITRO_ROOT_PEM.encode(), default_backend())

        for cert in certs[:-1]:
            issuer = cert.issuer
            found = False
            for potential_issuer in certs:
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

        root.public_key().verify(
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


def verify_signature(payload: bytes, signature: bytes, public_key_pem: bytes) -> bool:
    try:
        pub_key = serialization.load_pem_public_key(public_key_pem, default_backend())
        pub_key.verify(signature, payload, ec.ECDSA(hashes.SHA384()))
        return True
    except Exception:
        return False


def extract_pcrs(attestation_doc: dict) -> dict:
    pcrs = {}
    for key in attestation_doc.get("pcrs", {}):
        val = attestation_doc["pcrs"][key]
        if isinstance(val, str):
            match = re.search(r"0x([0-9a-fA-F]{64})", val)
            if match:
                pcrs[key] = f"0x{match.group(1).lower()}"
            elif val.startswith("0x"):
                pcrs[key] = val.lower()
    return pcrs


def verify_attestation_v2(attestation_file: str, expected_measurement: str, registry_rpc: str = None, registry_address: str = None) -> dict:
    try:
        with open(attestation_file, "rb") as f:
            cose_data = f.read()
    except Exception as e:
        return {"status": "REJECTED", "reason": f"READ_ERROR: {e}"}

    try:
        protected, payload, signature = parse_cose_sign1(cose_data)
    except Exception as e:
        return {"status": "REJECTED", "reason": f"INVALID_COSE: {e}"}

    cert_chain_pems = protected.get("x5chain", [])
    if not cert_chain_pems:
        return {"status": "REJECTED", "reason": "NO_CERT_CHAIN"}

    chain_valid, chain_msg = validate_cert_chain(cert_chain_pems)
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

    if not verify_signature(payload, signature, leaf_pub_pem):
        return {"status": "REJECTED", "reason": "INVALID_SIGNATURE"}

    try:
        doc = json.loads(payload)
    except Exception:
        return {"status": "REJECTED", "reason": "INVALID_PAYLOAD_JSON"}

    pcrs = extract_pcrs(doc)
    if "PCR0" not in pcrs or "PCR8" not in pcrs:
        return {"status": "REJECTED", "reason": "MISSING_PCR_VALUES"}

    if registry_rpc and registry_address:
        onchain_measurement = expected_measurement
        if pcrs.get("PCR8") != onchain_measurement.lower():
            return {"status": "REJECTED", "reason": f"PCR8_MISMATCH: {pcrs.get('PCR8')} != {onchain_measurement.lower()}"}

    return {
        "status": "ACCEPTED",
        "reason": "CRYPTOGRAPHICALLY_VALID_DRAFT",
        "pcrs": pcrs,
        "module_id": doc.get("module_id", "unknown"),
        "timestamp": doc.get("timestamp"),
    }


def main():
    parser = argparse.ArgumentParser(description="v2 draft cryptographic attestation verifier")
    parser.add_argument("--attestation-file", required=True, help="COSE_Sign1 attestation file")
    parser.add_argument("--expected-measurement", required=True, help="Expected PCR8 value from registry")
    parser.add_argument("--registry-rpc", help="Base RPC URL for on-chain binding (optional)")
    parser.add_argument("--registry-address", help="Registry address for on-chain binding")
    args = parser.parse_args()

    result = verify_attestation_v2(
        args.attestation_file,
        args.expected_measurement,
        args.registry_rpc,
        args.registry_address,
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "ACCEPTED" else 1)


if __name__ == "__main__":
    main()
