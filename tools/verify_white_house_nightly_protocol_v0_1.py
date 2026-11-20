#!/usr/bin/env python3
"""Cross-receipt clerk for WHITE_HOUSE_NIGHTLY_PROTOCOL_V0.1.

This verifier checks internal protocol coherence only. It does not establish
claim truth, guilt, randomness quality, or authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LANE_MAP = ROOT / "fixtures/jaywisdom/fraud_ledger/JASONS_DICE_12_JUSTICE_LANES_V0_1.json"
TEST_VECTORS = ROOT / "fixtures/jaywisdom/fraud_ledger/WHITE_HOUSE_NIGHTLY_PROTOCOL_VERIFIER_TEST_VECTORS_V0_1.json"

VIOLATION_CLASSES = {
    "HASH_VIOLATION",
    "BINDING_VIOLATION",
    "ORDERING_VIOLATION",
    "LANE_MAP_VIOLATION",
    "AUTHORITY_VIOLATION",
}
RECEIPT_NAMES = (
    "claim_selection_receipt",
    "rng_event_receipt",
    "lane_selection_receipt",
    "source_bytes_receipt",
    "disposition_receipt",
)
TOTAL_CHECKS = 11


def _jcs_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def jcs_canonicalize(value: Any) -> str:
    """RFC 8785 JCS for the protocol's restricted JSON domain.

    Floats are rejected. Object keys are sorted by UTF-16 code units as JCS
    requires. Protocol receipts use strings, integers, booleans, null, arrays,
    and objects only.
    """
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        raise TypeError("FLOAT_NOT_ALLOWED_IN_PROTOCOL_JCS")
    if isinstance(value, str):
        return _jcs_string(value)
    if isinstance(value, list):
        return "[" + ",".join(jcs_canonicalize(item) for item in value) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise TypeError("NON_STRING_OBJECT_KEY")
        keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return "{" + ",".join(
            _jcs_string(key) + ":" + jcs_canonicalize(value[key]) for key in keys
        ) + "}"
    raise TypeError(f"UNSUPPORTED_JCS_TYPE:{type(value).__name__}")


def receipt_digest(receipt: dict[str, Any]) -> str:
    preimage = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    canonical = jcs_canonicalize(preimage).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _violation(cls: str, check_id: str, expected: Any, observed: Any) -> dict[str, Any]:
    if cls not in VIOLATION_CLASSES:
        raise ValueError(f"UNRECOGNIZED_VIOLATION_CLASS:{cls}")
    return {"class": cls, "check_id": check_id, "expected": expected, "observed": observed}


def _receipt(
    state: str,
    violations: list[dict[str, Any]],
    checks_executed: int,
    unverifiable_inputs: list[str],
) -> dict[str, Any]:
    return {
        "verifier": "WHITE_HOUSE_NIGHTLY_PROTOCOL_VERIFIER_V0.1",
        "protocol_integrity": state,
        "violations": violations,
        "unverifiable_inputs": unverifiable_inputs,
        "checks_executed": checks_executed,
        "checks_defined": TOTAL_CHECKS,
        "claim_truth_proven": False,
        "human_guilt_determined": False,
        "randomness_quality_proven": False,
        "authority_created": False,
    }


def verify_protocol(
    protocol: dict[str, Any] | None,
    lane_map_bytes: bytes | None,
    source_bytes: bytes | None,
) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    unverifiable_inputs: list[str] = []
    checks_executed = 0

    if protocol is None:
        return _receipt("UNVERIFIABLE", violations, checks_executed, ["PROTOCOL_OBJECT"])

    missing_receipts = [name for name in RECEIPT_NAMES if not isinstance(protocol.get(name), dict)]
    if missing_receipts:
        unverifiable_inputs.extend(name.upper() for name in missing_receipts)
    if lane_map_bytes is None:
        unverifiable_inputs.append("FROZEN_LANE_MAP_BYTES")
    if source_bytes is None:
        unverifiable_inputs.append("PRESERVED_SOURCE_BYTES")

    # Check 1: every receipt digest.
    if not missing_receipts:
        digest_check_complete = True
        for name in RECEIPT_NAMES:
            receipt = protocol[name]
            recorded = receipt.get("receipt_sha256")
            if not isinstance(recorded, str):
                unverifiable_inputs.append(f"{name.upper()}.RECEIPT_SHA256")
                digest_check_complete = False
                continue
            try:
                recomputed = receipt_digest(receipt)
            except (TypeError, ValueError) as exc:
                violations.append(_violation(
                    "HASH_VIOLATION", f"{name.upper()}_JCS_PREIMAGE",
                    "RFC8785_JCS_SUPPORTED_DOMAIN", str(exc)
                ))
                digest_check_complete = False
                continue
            if recorded != recomputed:
                violations.append(_violation(
                    "HASH_VIOLATION", f"{name.upper()}_SHA256", recomputed, recorded
                ))
        if digest_check_complete:
            checks_executed += 1

    rng = protocol.get("rng_event_receipt") if isinstance(protocol.get("rng_event_receipt"), dict) else None
    lane = protocol.get("lane_selection_receipt") if isinstance(protocol.get("lane_selection_receipt"), dict) else None
    claim = protocol.get("claim_selection_receipt") if isinstance(protocol.get("claim_selection_receipt"), dict) else None
    source = protocol.get("source_bytes_receipt") if isinstance(protocol.get("source_bytes_receipt"), dict) else None
    disposition = protocol.get("disposition_receipt") if isinstance(protocol.get("disposition_receipt"), dict) else None

    # Checks 2-3: die fields bind to ordered_pair.
    if rng is not None:
        pair = rng.get("ordered_pair")
        if isinstance(pair, list) and len(pair) == 2:
            checks_executed += 1
            if rng.get("die_a") != pair[0]:
                violations.append(_violation("BINDING_VIOLATION", "DIE_A_PAIR_BINDING", pair[0], rng.get("die_a")))
            checks_executed += 1
            if rng.get("die_b") != pair[1]:
                violations.append(_violation("BINDING_VIOLATION", "DIE_B_PAIR_BINDING", pair[1], rng.get("die_b")))
        else:
            unverifiable_inputs.append("RNG_EVENT_RECEIPT.ORDERED_PAIR")

    # Check 4: RNG pair equals lane-selection pair.
    if rng is not None and lane is not None:
        rng_pair = rng.get("ordered_pair")
        lane_pair = lane.get("ordered_pair")
        if isinstance(rng_pair, list) and isinstance(lane_pair, list):
            checks_executed += 1
            if rng_pair != lane_pair:
                violations.append(_violation("BINDING_VIOLATION", "RNG_PAIR_MATCH", rng_pair, lane_pair))
        else:
            unverifiable_inputs.append("RNG_OR_LANE_ORDERED_PAIR")

    # Checks 5-6: frozen lane-map bytes bind to digest and recorded lane.
    lane_map_doc = None
    if lane is not None and lane_map_bytes is not None:
        checks_executed += 1
        actual_map_sha = hashlib.sha256(lane_map_bytes).hexdigest()
        recorded_map_sha = lane.get("lane_map_sha256")
        if recorded_map_sha != actual_map_sha:
            violations.append(_violation("LANE_MAP_VIOLATION", "LANE_MAP_SHA256", actual_map_sha, recorded_map_sha))
        try:
            lane_map_doc = json.loads(lane_map_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            violations.append(_violation("LANE_MAP_VIOLATION", "LANE_MAP_PARSE", "VALID_UTF8_JSON", str(exc)))

        if lane_map_doc is not None:
            mapping = {
                (row.get("die_a"), row.get("die_b")): row.get("lane")
                for row in lane_map_doc.get("mapping", []) if isinstance(row, dict)
            }
            pair = lane.get("ordered_pair")
            if isinstance(pair, list) and len(pair) == 2:
                checks_executed += 1
                mapped_lane = mapping.get((pair[0], pair[1]))
                if mapped_lane is None:
                    violations.append(_violation(
                        "LANE_MAP_VIOLATION", "PAIR_PRESENT_IN_FROZEN_MAP", "MAPPED_ORDERED_PAIR", pair
                    ))
                elif lane.get("lane") != mapped_lane:
                    violations.append(_violation("LANE_MAP_VIOLATION", "RECORDED_LANE_MATCH", mapped_lane, lane.get("lane")))
            else:
                unverifiable_inputs.append("LANE_SELECTION_RECEIPT.ORDERED_PAIR")

    # Checks 7-8: disposition binds to selected claim and lane.
    if claim is not None and disposition is not None:
        checks_executed += 1
        selected_claim = claim.get("claim_selected_id")
        if disposition.get("claim_id") != selected_claim:
            violations.append(_violation(
                "BINDING_VIOLATION", "DISPOSITION_CLAIM_MATCH", selected_claim, disposition.get("claim_id")
            ))
    if lane is not None and disposition is not None:
        checks_executed += 1
        selected_lane = lane.get("lane")
        if disposition.get("lane") != selected_lane:
            violations.append(_violation(
                "BINDING_VIOLATION", "DISPOSITION_LANE_MATCH", selected_lane, disposition.get("lane")
            ))

    # Check 9: preserved source bytes bind to recorded digest and length.
    if source is not None and source_bytes is not None:
        checks_executed += 1
        actual_source_sha = hashlib.sha256(source_bytes).hexdigest()
        if source.get("sha256") != actual_source_sha:
            violations.append(_violation("HASH_VIOLATION", "SOURCE_BYTES_SHA256", actual_source_sha, source.get("sha256")))
        if source.get("byte_length") != len(source_bytes):
            violations.append(_violation("BINDING_VIOLATION", "SOURCE_BYTE_LENGTH", len(source_bytes), source.get("byte_length")))

    # Check 10: receipt timestamps respect dependency order.
    if all(item is not None for item in (claim, rng, lane, source, disposition)):
        timestamps = [
            claim.get("timestamp"), rng.get("timestamp"), lane.get("timestamp"),
            source.get("fetched_at"), disposition.get("timestamp")
        ]
        parsed = [_parse_timestamp(value) for value in timestamps]
        if all(value is not None for value in parsed):
            checks_executed += 1
            if not all(parsed[i] <= parsed[i + 1] for i in range(len(parsed) - 1)):
                violations.append(_violation(
                    "ORDERING_VIOLATION", "DEPENDENCY_TIMESTAMP_ORDER",
                    "claim<=rng<=lane<=source<=disposition", timestamps
                ))
        else:
            unverifiable_inputs.append("DEPENDENCY_TIMESTAMPS")

    # Check 11: authority must be explicitly false at root and every receipt.
    authority_targets: list[tuple[str, dict[str, Any]]] = [("PROTOCOL", protocol)]
    for name in RECEIPT_NAMES:
        value = protocol.get(name)
        if isinstance(value, dict):
            authority_targets.append((name.upper(), value))
    authority_missing = [name for name, obj in authority_targets if "authority_created" not in obj]
    if authority_missing:
        unverifiable_inputs.extend(f"{name}.AUTHORITY_CREATED" for name in authority_missing)
    else:
        checks_executed += 1
        for name, obj in authority_targets:
            if obj.get("authority_created") is not False:
                violations.append(_violation(
                    "AUTHORITY_VIOLATION", f"{name}_AUTHORITY_CREATED", False, obj.get("authority_created")
                ))

    if unverifiable_inputs:
        state = "UNVERIFIABLE"
    elif violations:
        state = "FAIL"
    else:
        state = "PASS"
    return _receipt(state, violations, checks_executed, sorted(set(unverifiable_inputs)))


def _stamp(receipt: dict[str, Any]) -> dict[str, Any]:
    receipt = copy.deepcopy(receipt)
    receipt["receipt_sha256"] = receipt_digest(receipt)
    return receipt


def build_synthetic_protocol(lane_map_bytes: bytes, source_bytes: bytes) -> dict[str, Any]:
    map_sha = hashlib.sha256(lane_map_bytes).hexdigest()
    source_sha = hashlib.sha256(source_bytes).hexdigest()

    claim = _stamp({
        "event_id": "SYNTHETIC_CLAIM_SELECTION", "claim_pool_frozen": True,
        "claim_selected_id": "SYNTHETIC_CLAIM_001", "timestamp": "2026-08-16T21:00:00Z",
        "authority_created": False,
    })
    rng = _stamp({
        "event_id": "SYNTHETIC_RNG", "die_a": 2, "die_b": 4, "ordered_pair": [2, 4],
        "generator_type": "SYNTHETIC_TEST_VECTOR", "generator_implementation": "DETERMINISTIC_FIXTURE",
        "raw_output": "0204", "timestamp": "2026-08-16T21:00:01Z",
        "independently_observable": False, "rng_source_verified": False,
        "randomness_quality_proven": False, "authority_created": False,
    })
    lane = _stamp({
        "event_id": "SYNTHETIC_LANE_SELECTION", "ordered_pair": [2, 4], "lane": 10,
        "lane_map_sha256": map_sha, "timestamp": "2026-08-16T21:00:02Z", "authority_created": False,
    })
    source = _stamp({
        "event_id": "SYNTHETIC_SOURCE_BYTES", "url": "https://example.invalid/synthetic-source",
        "fetched_at": "2026-08-16T21:00:03Z", "content_type": "text/plain",
        "byte_length": len(source_bytes), "sha256": source_sha, "raw_bytes_preserved": True,
        "authority_created": False,
    })
    disposition = _stamp({
        "event_id": "SYNTHETIC_DISPOSITION", "lane": 10, "claim_id": "SYNTHETIC_CLAIM_001",
        "disposition": "HOLD", "timestamp": "2026-08-16T21:00:04Z", "authority_created": False,
    })
    return {
        "format": "WHITE_HOUSE_NIGHTLY_PROTOCOL_V0.1",
        "classification": "NIGHTLY_REPLAY_PROTOCOL",
        "claim_selection_receipt": claim,
        "rng_event_receipt": rng,
        "lane_selection_receipt": lane,
        "source_bytes_receipt": source,
        "disposition_receipt": disposition,
        "authority_created": False,
    }


def apply_mutation(
    mutation: str, protocol: dict[str, Any], source_bytes: bytes | None
) -> tuple[dict[str, Any], bytes | None]:
    doc = copy.deepcopy(protocol)
    src = source_bytes
    if mutation == "NONE":
        return doc, src
    if mutation == "CLAIM_HASH_TAMPER":
        doc["claim_selection_receipt"]["event_id"] = "TAMPERED_EVENT_ID"
        return doc, src
    if mutation == "RNG_LANE_PAIR_MISMATCH":
        doc["rng_event_receipt"]["die_b"] = 5
        doc["rng_event_receipt"]["ordered_pair"] = [2, 5]
        doc["rng_event_receipt"] = _stamp(doc["rng_event_receipt"])
        return doc, src
    if mutation == "DISPOSITION_TIMESTAMP_REWIND":
        doc["disposition_receipt"]["timestamp"] = "2026-08-16T20:59:59Z"
        doc["disposition_receipt"] = _stamp(doc["disposition_receipt"])
        return doc, src
    if mutation == "LANE_MAP_MISMATCH":
        doc["lane_selection_receipt"]["lane"] = 11
        doc["lane_selection_receipt"] = _stamp(doc["lane_selection_receipt"])
        doc["disposition_receipt"]["lane"] = 11
        doc["disposition_receipt"] = _stamp(doc["disposition_receipt"])
        return doc, src
    if mutation == "AUTHORITY_PROMOTION":
        doc["disposition_receipt"]["authority_created"] = True
        doc["disposition_receipt"] = _stamp(doc["disposition_receipt"])
        return doc, src
    if mutation == "SOURCE_BYTES_MISSING":
        return doc, None
    raise ValueError(f"UNKNOWN_TEST_MUTATION:{mutation}")


def run_self_test() -> int:
    lane_map_bytes = LANE_MAP.read_bytes()
    source_bytes = b"SYNTHETIC_SOURCE_BYTES_V0_1\n"
    baseline = build_synthetic_protocol(lane_map_bytes, source_bytes)
    vectors = json.loads(TEST_VECTORS.read_text(encoding="utf-8"))

    failures: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    for vector in vectors["vectors"]:
        protocol, candidate_source_bytes = apply_mutation(vector["mutation"], baseline, source_bytes)
        receipt = verify_protocol(protocol, lane_map_bytes, candidate_source_bytes)
        classes = {item["class"] for item in receipt["violations"]}
        expected_class = vector.get("expected_violation_class")
        ok = receipt["protocol_integrity"] == vector["expected_integrity"]
        if expected_class is not None:
            ok = ok and classes == {expected_class}
        else:
            ok = ok and not classes
        result = {
            "id": vector["id"], "expected_integrity": vector["expected_integrity"],
            "observed_integrity": receipt["protocol_integrity"],
            "expected_violation_class": expected_class,
            "observed_violation_classes": sorted(classes), "pass": ok,
        }
        results.append(result)
        if not ok:
            failures.append(result)

    summary = {
        "verifier": "WHITE_HOUSE_NIGHTLY_PROTOCOL_VERIFIER_V0.1",
        "test_vector_count": len(results), "test_vectors_passed": len(results) - len(failures),
        "test_vectors_failed": len(failures), "roll_002_live": False,
        "claim_truth_proven": False, "human_guilt_determined": False,
        "authority_created": False, "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--protocol", type=Path)
    parser.add_argument("--lane-map", type=Path, default=LANE_MAP)
    parser.add_argument("--source-bytes", type=Path)
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.protocol is None:
        parser.error("--protocol is required unless --self-test is used")
    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    lane_map_bytes = args.lane_map.read_bytes() if args.lane_map.exists() else None
    source_bytes = args.source_bytes.read_bytes() if args.source_bytes is not None and args.source_bytes.exists() else None
    receipt = verify_protocol(protocol, lane_map_bytes, source_bytes)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["protocol_integrity"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
