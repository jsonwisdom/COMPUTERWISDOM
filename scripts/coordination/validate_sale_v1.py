# validate_sale_v1.py
# Pure-function validation utility for sale_v1 input geometry using JCS-style parameters

import json
import os
import sys


def validate_input_structure(receipt_path: str, schema_path: str) -> dict:
    if not os.path.exists(receipt_path) or not os.path.exists(schema_path):
        print("ERROR: MISSING_REQUIRED_NODES")
        sys.exit(1)

    with open(receipt_path, "r", encoding="utf-8") as f:
        receipt = json.load(f)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    state = receipt.get("receipt_metadata", {}).get("lifecycle_state", "UNKNOWN")

    if state == "PENDING_LIVE_VALUES":
        print("STATUS: RECEIPT_INERT_GEOMETRY_DETECTED")
        print("ACTION: EXECUTING_NULL_TEMPLATE_PASS")

        payload = receipt.get("sale_v1_payload", {})
        required_fields = schema.get("required", [])

        missing_keys = [key for key in required_fields if key not in payload]
        if missing_keys:
            print(f"FAIL: STRUCTURAL_GEOMETRY_DRIFT_DETECTED: {missing_keys}")
            sys.exit(1)

        non_null_keys = [key for key in required_fields if payload.get(key) is not None]
        if non_null_keys:
            print(f"FAIL: UNEXPECTED_LIVE_VALUES_DETECTED: {non_null_keys}")
            sys.exit(1)

        extra_keys = [key for key in payload.keys() if key not in required_fields]
        if extra_keys:
            print(f"FAIL: ADDITIONAL_PAYLOAD_KEYS_DETECTED: {extra_keys}")
            sys.exit(1)

        print("PASS: SKELETON_RECEIPT_CONFORMS_TO_SCHEMA")
        return {"status": "INERT_VERIFIED_PASS", "computed_hash": None}

    return {"status": "UNSUPPORTED_MUTATION_STATE", "computed_hash": None}


if __name__ == "__main__":
    TARGET_RECEIPT = "status/sale_verify_receipt_v1.json"
    TARGET_SCHEMA = "schema/sale_v1_input.json"

    result = validate_input_structure(TARGET_RECEIPT, TARGET_SCHEMA)
    if result["status"] == "INERT_VERIFIED_PASS":
        sys.exit(0)
    sys.exit(1)
