#!/usr/bin/env python3
"""Independent oversight clerk for WHITE_HOUSE_NIGHTLY_PROTOCOL_V0.1.

This implementation intentionally does not import the primary verifier.
It cross-checks the same frozen protocol mechanics and never establishes
world truth, source authenticity, guilt, randomness fairness, or authority.
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

RECEIPTS = (
    "claim_selection_receipt",
    "rng_event_receipt",
    "lane_selection_receipt",
    "source_bytes_receipt",
    "disposition_receipt",
)
ALLOWED_VIOLATIONS = {
    "HASH_VIOLATION",
    "BINDING_VIOLATION",
    "ORDERING_VIOLATION",
    "LANE_MAP_VIOLATION",
    "AUTHORITY_VIOLATION",
}
CHECKS_DEFINED = 11


def _encode_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def canonical_json(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        raise TypeError("FLOAT_NOT_ALLOWED")
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("NON_STRING_KEY")
        ordered = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return "{" + ",".join(
            _encode_string(key) + ":" + canonical_json(value[key]) for key in ordered
        ) + "}"
    raise TypeError(f"UNSUPPORTED_TYPE:{type(value).__name__}")


def digest_receipt(receipt: dict[str, Any]) -> str:
    preimage = copy.deepcopy(receipt)
    preimage.pop("receipt_sha256", None)
    return hashlib.sha256(canonical_json(preimage).encode("utf-8")).hexdigest()


def stamp(receipt: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(receipt)
    result["receipt_sha256"] = digest_receipt(result)
    return result


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def violation(kind: str, check_id: str, expected: Any, observed: Any) -> dict[str, Any]:
    if kind not in ALLOWED_VIOLATIONS:
        raise ValueError(f"INVALID_VIOLATION_CLASS:{kind}")
    return {"class": kind, "check_id": check_id, "expected": expected, "observed": observed}


def result_receipt(
    integrity: str,
    violations: list[dict[str, Any]],
    missing: list[str],
    checks_executed: int,
) -> dict[str, Any]:
    return {
        "verifier": "WHITE_HOUSE_NIGHTLY_PROTOCOL_VERIFIER_V0.1_OVERSIGHT",
        "implementation_dependency_on_primary": False,
        "protocol_integrity": integrity,
        "violations": violations,
        "unverifiable_inputs": sorted(set(missing)),
        "checks_executed": checks_executed,
        "checks_defined": CHECKS_DEFINED,
        "oversight_run_performed": True,
        "claim_truth_proven": False,
        "source_authenticity_proven": False,
        "human_guilt_determined": False,
        "randomness_quality_proven": False,
        "authority_created": False,
    }


def verify(
    protocol: dict[str, Any] | None,
    lane_map_bytes: bytes | None,
    source_bytes: bytes | None,
) -> dict[str, Any]:
    problems: list[dict[str, Any]] = []
    missing: list[str] = []
    executed = 0

    if not isinstance(protocol, dict):
        return result_receipt("UNVERIFIABLE", [], ["PROTOCOL_OBJECT"], 0)

    docs: dict[str, dict[str, Any] | None] = {}
    for name in RECEIPTS:
        value = protocol.get(name)
        docs[name] = value if isinstance(value, dict) else None
        if docs[name] is None:
            missing.append(name.upper())

    if lane_map_bytes is None:
        missing.append("FROZEN_LANE_MAP_BYTES")
    if source_bytes is None:
        missing.append("PRESERVED_SOURCE_BYTES")

    # 1 — receipt digest coherence.
    if all(docs[name] is not None for name in RECEIPTS):
        complete = True
        for name in RECEIPTS:
            rec = docs[name]
            assert rec is not None
            recorded = rec.get("receipt_sha256")
            if not isinstance(recorded, str):
                missing.append(f"{name.upper()}.RECEIPT_SHA256")
                complete = False
                continue
            try:
                actual = digest_receipt(rec)
            except (TypeError, ValueError) as exc:
                problems.append(violation(
                    "HASH_VIOLATION", f"{name.upper()}_CANONICAL_PREIMAGE",
                    "SUPPORTED_JCS_DOMAIN", str(exc)
                ))
                complete = False
                continue
            if actual != recorded:
                problems.append(violation(
                    "HASH_VIOLATION", f"{name.upper()}_SHA256", actual, recorded
                ))
        if complete:
            executed += 1

    rng = docs["rng_event_receipt"]
    lane = docs["lane_selection_receipt"]
    claim = docs["claim_selection_receipt"]
    source = docs["source_bytes_receipt"]
    disposition = docs["disposition_receipt"]

    # 2-4 — pair bindings.
    if rng is not None:
        pair = rng.get("ordered_pair")
        if isinstance(pair, list) and len(pair) == 2:
            executed += 1
            if rng.get("die_a") != pair[0]:
                problems.append(violation(
                    "BINDING_VIOLATION", "DIE_A_PAIR_BINDING", pair[0], rng.get("die_a")
                ))
            executed += 1
            if rng.get("die_b") != pair[1]:
                problems.append(violation(
                    "BINDING_VIOLATION", "DIE_B_PAIR_BINDING", pair[1], rng.get("die_b")
                ))
        else:
            missing.append("RNG_EVENT_RECEIPT.ORDERED_PAIR")

    if rng is not None and lane is not None:
        rp = rng.get("ordered_pair")
        lp = lane.get("ordered_pair")
        if isinstance(rp, list) and isinstance(lp, list):
            executed += 1
            if tuple(rp) != tuple(lp):
                problems.append(violation("BINDING_VIOLATION", "RNG_PAIR_MATCH", rp, lp))
        else:
            missing.append("RNG_OR_LANE_ORDERED_PAIR")

    # 5-6 — frozen map digest and pair->lane lookup.
    if lane is not None and lane_map_bytes is not None:
        executed += 1
        map_sha = hashlib.sha256(lane_map_bytes).hexdigest()
        if lane.get("lane_map_sha256") != map_sha:
            problems.append(violation(
                "LANE_MAP_VIOLATION", "LANE_MAP_SHA256", map_sha, lane.get("lane_map_sha256")
            ))
        try:
            map_doc = json.loads(lane_map_bytes)
            rows = map_doc.get("mapping", [])
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError) as exc:
            rows = []
            problems.append(violation(
                "LANE_MAP_VIOLATION", "LANE_MAP_PARSE", "VALID_JSON_OBJECT", str(exc)
            ))

        pair = lane.get("ordered_pair")
        if isinstance(pair, list) and len(pair) == 2:
            executed += 1
            candidates = [
                row.get("lane") for row in rows
                if isinstance(row, dict)
                and row.get("die_a") == pair[0]
                and row.get("die_b") == pair[1]
            ]
            if len(candidates) != 1:
                problems.append(violation(
                    "LANE_MAP_VIOLATION", "PAIR_PRESENT_ONCE", 1, len(candidates)
                ))
            elif lane.get("lane") != candidates[0]:
                problems.append(violation(
                    "LANE_MAP_VIOLATION", "RECORDED_LANE_MATCH", candidates[0], lane.get("lane")
                ))
        else:
            missing.append("LANE_SELECTION_RECEIPT.ORDERED_PAIR")

    # 7-8 — claim/lane bind to disposition.
    if claim is not None and disposition is not None:
        executed += 1
        wanted = claim.get("claim_selected_id")
        if disposition.get("claim_id") != wanted:
            problems.append(violation(
                "BINDING_VIOLATION", "DISPOSITION_CLAIM_MATCH", wanted, disposition.get("claim_id")
            ))

    if lane is not None and disposition is not None:
        executed += 1
        wanted = lane.get("lane")
        if disposition.get("lane") != wanted:
            problems.append(violation(
                "BINDING_VIOLATION", "DISPOSITION_LANE_MATCH", wanted, disposition.get("lane")
            ))

    # 9 — preserved bytes bind to source receipt.
    if source is not None and source_bytes is not None:
        executed += 1
        actual_sha = hashlib.sha256(source_bytes).hexdigest()
        if source.get("sha256") != actual_sha:
            problems.append(violation(
                "HASH_VIOLATION", "SOURCE_BYTES_SHA256", actual_sha, source.get("sha256")
            ))
        actual_len = len(source_bytes)
        if source.get("byte_length") != actual_len:
            problems.append(violation(
                "BINDING_VIOLATION", "SOURCE_BYTE_LENGTH", actual_len, source.get("byte_length")
            ))

    # 10 — dependency order.
    if all(x is not None for x in (claim, rng, lane, source, disposition)):
        assert claim and rng and lane and source and disposition
        raw_times = [
            claim.get("timestamp"), rng.get("timestamp"), lane.get("timestamp"),
            source.get("fetched_at"), disposition.get("timestamp")
        ]
        times = [parse_time(value) for value in raw_times]
        if all(value is not None for value in times):
            executed += 1
            if any(times[i] > times[i + 1] for i in range(len(times) - 1)):
                problems.append(violation(
                    "ORDERING_VIOLATION", "DEPENDENCY_TIMESTAMP_ORDER", "NONDECREASING", raw_times
                ))
        else:
            missing.append("DEPENDENCY_TIMESTAMPS")

    # 11 — no authority anywhere.
    targets: list[tuple[str, dict[str, Any]]] = [("PROTOCOL", protocol)]
    for name in RECEIPTS:
        rec = docs[name]
        if rec is not None:
            targets.append((name.upper(), rec))
    if any("authority_created" not in obj for _, obj in targets):
        for name, obj in targets:
            if "authority_created" not in obj:
                missing.append(f"{name}.AUTHORITY_CREATED")
    else:
        executed += 1
        for name, obj in targets:
            if obj["authority_created"] is not False:
                problems.append(violation(
                    "AUTHORITY_VIOLATION", f"{name}_AUTHORITY_CREATED", False, obj["authority_created"]
                ))

    integrity = "UNVERIFIABLE" if missing else ("FAIL" if problems else "PASS")
    return result_receipt(integrity, problems, missing, executed)


def synthetic_protocol(lane_map_bytes: bytes, source_bytes: bytes) -> dict[str, Any]:
    map_sha = hashlib.sha256(lane_map_bytes).hexdigest()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    return {
        "format": "WHITE_HOUSE_NIGHTLY_PROTOCOL_V0.1",
        "classification": "NIGHTLY_REPLAY_PROTOCOL",
        "claim_selection_receipt": stamp({
            "event_id": "SYNTHETIC_CLAIM_SELECTION", "claim_pool_frozen": True,
            "claim_selected_id": "SYNTHETIC_CLAIM_001", "timestamp": "2026-08-16T21:00:00Z",
            "authority_created": False,
        }),
        "rng_event_receipt": stamp({
            "event_id": "SYNTHETIC_RNG", "die_a": 2, "die_b": 4, "ordered_pair": [2, 4],
            "generator_type": "SYNTHETIC_TEST_VECTOR", "generator_implementation": "DETERMINISTIC_FIXTURE",
            "raw_output": "0204", "timestamp": "2026-08-16T21:00:01Z",
            "independently_observable": False, "rng_source_verified": False,
            "randomness_quality_proven": False, "authority_created": False,
        }),
        "lane_selection_receipt": stamp({
            "event_id": "SYNTHETIC_LANE_SELECTION", "ordered_pair": [2, 4], "lane": 10,
            "lane_map_sha256": map_sha, "timestamp": "2026-08-16T21:00:02Z",
            "authority_created": False,
        }),
        "source_bytes_receipt": stamp({
            "event_id": "SYNTHETIC_SOURCE_BYTES", "url": "https://example.invalid/synthetic-source",
            "fetched_at": "2026-08-16T21:00:03Z", "content_type": "text/plain",
            "byte_length": len(source_bytes), "sha256": source_sha, "raw_bytes_preserved": True,
            "authority_created": False,
        }),
        "disposition_receipt": stamp({
            "event_id": "SYNTHETIC_DISPOSITION", "lane": 10,
            "claim_id": "SYNTHETIC_CLAIM_001", "disposition": "HOLD",
            "timestamp": "2026-08-16T21:00:04Z", "authority_created": False,
        }),
        "authority_created": False,
    }


def mutate(name: str, protocol: dict[str, Any], source_bytes: bytes | None) -> tuple[dict[str, Any], bytes | None]:
    doc = copy.deepcopy(protocol)
    data = source_bytes
    if name == "NONE":
        return doc, data
    if name == "CLAIM_HASH_TAMPER":
        doc["claim_selection_receipt"]["event_id"] = "TAMPERED_EVENT_ID"
    elif name == "RNG_LANE_PAIR_MISMATCH":
        doc["rng_event_receipt"]["die_b"] = 5
        doc["rng_event_receipt"]["ordered_pair"] = [2, 5]
        doc["rng_event_receipt"] = stamp(doc["rng_event_receipt"])
    elif name == "DISPOSITION_TIMESTAMP_REWIND":
        doc["disposition_receipt"]["timestamp"] = "2026-08-16T20:59:59Z"
        doc["disposition_receipt"] = stamp(doc["disposition_receipt"])
    elif name == "LANE_MAP_MISMATCH":
        doc["lane_selection_receipt"]["lane"] = 11
        doc["lane_selection_receipt"] = stamp(doc["lane_selection_receipt"])
        doc["disposition_receipt"]["lane"] = 11
        doc["disposition_receipt"] = stamp(doc["disposition_receipt"])
    elif name == "AUTHORITY_PROMOTION":
        doc["disposition_receipt"]["authority_created"] = True
        doc["disposition_receipt"] = stamp(doc["disposition_receipt"])
    elif name == "SOURCE_BYTES_MISSING":
        data = None
    else:
        raise ValueError(f"UNKNOWN_MUTATION:{name}")
    return doc, data


def run_self_test() -> int:
    lane_map = LANE_MAP.read_bytes()
    source = b"SYNTHETIC_SOURCE_BYTES_V0_1\n"
    baseline = synthetic_protocol(lane_map, source)
    vectors = json.loads(TEST_VECTORS.read_text(encoding="utf-8"))["vectors"]

    results = []
    failed = 0
    for vector in vectors:
        candidate, candidate_source = mutate(vector["mutation"], baseline, source)
        receipt = verify(candidate, lane_map, candidate_source)
        seen = {item["class"] for item in receipt["violations"]}
        expected_class = vector.get("expected_violation_class")
        ok = receipt["protocol_integrity"] == vector["expected_integrity"]
        ok = ok and (seen == ({expected_class} if expected_class else set()))
        results.append({
            "id": vector["id"],
            "expected_integrity": vector["expected_integrity"],
            "observed_integrity": receipt["protocol_integrity"],
            "expected_violation_class": expected_class,
            "observed_violation_classes": sorted(seen),
            "pass": ok,
        })
        failed += 0 if ok else 1

    summary = {
        "verifier": "WHITE_HOUSE_NIGHTLY_PROTOCOL_VERIFIER_V0.1_OVERSIGHT",
        "implementation_dependency_on_primary": False,
        "oversight_run_performed": True,
        "test_vector_count": len(results),
        "test_vectors_passed": len(results) - failed,
        "test_vectors_failed": failed,
        "roll_002_live": False,
        "claim_truth_proven": False,
        "source_authenticity_proven": False,
        "human_guilt_determined": False,
        "randomness_quality_proven": False,
        "authority_created": False,
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if failed == 0 else 1


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
    lane_map = args.lane_map.read_bytes() if args.lane_map.exists() else None
    source = args.source_bytes.read_bytes() if args.source_bytes and args.source_bytes.exists() else None
    print(json.dumps(verify(protocol, lane_map, source), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
