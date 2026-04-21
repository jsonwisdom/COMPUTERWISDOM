#!/usr/bin/env python3
"""ZTWS Nitro measurement verifier.

This verifier checks enclave measurement consistency against known-good PCRs.
It does NOT claim full AWS certificate-chain attestation validation.
"""

import argparse
import json
import sys
from pathlib import Path

REQUIRED_PCRS = ["PCR0", "PCR8"]


def load_expected(path: Path) -> dict:
    data = json.loads(path.read_text())
    profile = data.get("ztws_verifier_v1", {})
    pcrs = profile.get("pcrs", {})
    if not pcrs:
        raise ValueError("missing expected PCR set in measurements.json")
    return pcrs


def parse_attestation(attestation_doc: dict) -> dict:
    pcrs = attestation_doc.get("pcrs")
    if not isinstance(pcrs, dict):
        raise ValueError("attestation doc missing pcrs map")

    user_data = attestation_doc.get("user_data")
    if user_data is None:
        raise ValueError("attestation doc missing user_data")

    return {
        "pcrs": pcrs,
        "user_data": user_data,
        "timestamp": attestation_doc.get("timestamp")
    }


def check_enclave_id(user_data, enclave_id: str) -> bool:
    if isinstance(user_data, str):
        return enclave_id in user_data
    if isinstance(user_data, list):
        return enclave_id in user_data
    return enclave_id in str(user_data)


def check_pcrs(actual_pcrs: dict, expected_pcrs: dict) -> bool:
    ok = True
    for pcr in REQUIRED_PCRS:
        expected = expected_pcrs.get(pcr)
        actual = actual_pcrs.get(pcr)
        if expected is None:
            print(f"❌ {pcr}: expected value missing from measurements.json")
            ok = False
            continue
        if actual != expected:
            print(f"❌ {pcr}: {actual} != {expected}")
            ok = False
            continue
        print(f"✅ {pcr}: MATCH")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Nitro enclave measurement consistency")
    parser.add_argument("--attestation-file", required=True, help="JSON attestation document")
    parser.add_argument("--enclave-id", required=True, help="Expected enclave ID")
    parser.add_argument(
        "--measurements-file",
        default=str(Path(__file__).with_name("measurements.json")),
        help="Path to known-good measurements.json"
    )
    args = parser.parse_args()

    try:
        attestation = json.loads(Path(args.attestation_file).read_text())
        expected_pcrs = load_expected(Path(args.measurements_file))
        parsed = parse_attestation(attestation)
    except Exception as exc:
        print(f"❌ verifier setup failed: {exc}")
        return 1

    print("📡 Verifying ZTWS enclave measurement...")

    if not check_enclave_id(parsed["user_data"], args.enclave_id):
        print(f"❌ Enclave ID mismatch: {args.enclave_id} not present in user_data")
        return 1
    print(f"✅ Enclave ID: {args.enclave_id}")

    if not check_pcrs(parsed["pcrs"], expected_pcrs):
        print("❌ Measurement verification failed")
        return 1

    print("\n⚡ Measurement: VALID")
    print(json.dumps({
        "status": "measurement_valid",
        "enclave": args.enclave_id,
        "required_pcrs": REQUIRED_PCRS
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
