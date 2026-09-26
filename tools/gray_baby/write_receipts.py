"""Write one sealed receipt per boundary. Do not commit CI output."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.replay_kernel_v0_1 import (
    AUTHORITY,
    AUTHORITY_BOUNDARY,
    CONSTITUTIONAL_ROOT,
    KERNEL_VERSION,
    canonical_json,
    sha256_text,
)
from tools.gray_baby.constants import (
    CANONICALIZATION,
    CLOCK,
    DESIGN_BATCH_SIZE,
    DESIGN_INVENTORY_SIZE,
    FIXTURE_NOTE,
    GAME_STATES,
    HUMAN_SUMMARY_REF,
    NETWORK,
    OPERATORS,
    PRODUCT,
    REPLAY_MODE,
    ROLE,
    SCOREKEEPER_NOTE,
    SPEC,
    SCHEMA_VERSION_ALIEN,
    SCHEMA_VERSION_BATCH,
    SOURCE_ORDER,
)
from tools.gray_baby.operators import run_operator

_SPEC_DIVERGENCE = {
    "MISSING_RECEIPT": "MISSING_ARTIFACT",
    "INDEXER_DRIFT": "HASH_MISMATCH",
}


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def seal_receipt(body: dict[str, Any]) -> dict[str, Any]:
    sealed = dict(body)
    output = dict(sealed["output"])
    output_core = {key: value for key, value in output.items() if key != "output_hash"}
    output["output_hash"] = sha256_text(canonical_json(output_core))
    sealed["output"] = output
    unsigned = {key: value for key, value in sealed.items() if key != "receipt_id"}
    sealed["receipt_id"] = sha256_text(canonical_json(unsigned))
    return sealed


def _state_counts(objects: list[dict[str, Any]]) -> dict[str, int]:
    counts = {state: 0 for state in GAME_STATES}
    for obj in objects:
        state = obj["game_state"]
        if state not in counts:
            raise ValueError(f"unhandled game state: {state}")
        counts[state] += 1
    return counts


def _batch_timestamp(batch_input: dict[str, Any]) -> str:
    stamps = [str(obj["observed_at"]) for obj in batch_input["objects"] if obj.get("observed_at")]
    if not stamps:
        return "UNAVAILABLE"
    return max(stamps)


def _inventory_artifact(batch_input: dict[str, Any]) -> dict[str, str]:
    uri = str(batch_input.get("inventory_uri") or "inventory")
    path = Path(uri)
    if path.is_file():
        digest = sha256_bytes(path.read_bytes())
    else:
        digest = sha256_text(canonical_json(batch_input["objects"]))
    commit = "SYNTHETIC_TEST_ONLY" if batch_input.get("inventory_class") == "SYNTHETIC_TEST_ONLY" else "CONTENT_HASH_BOUND"
    return {"uri": uri, "commit": commit, "sha256": digest, "role": "batch_inventory"}


def _replay_parameters(scope: str) -> dict[str, str]:
    return {
        "canonicalization": CANONICALIZATION,
        "hash_algorithm": "SHA-256",
        "verifier_version": PRODUCT,
        "scope": scope,
        "network": NETWORK,
        "clock": CLOCK,
    }


def _object_sources(obj_input: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = []
    for entry in obj_input.get("sources") or []:
        if not isinstance(entry, dict) or not entry.get("present"):
            continue
        artifacts.append(
            {
                "uri": str(entry.get("ref") or entry.get("tier")),
                "commit": "SYNTHETIC_TEST_ONLY" if obj_input.get("fixture_class") == "SYNTHETIC_TEST_ONLY" else "CONTENT_HASH_BOUND",
                "sha256": str(entry.get("payload_hash") or "ABSENT"),
                "role": str(entry.get("tier")),
            }
        )
    if artifacts:
        return artifacts
    return [
        {
            "uri": f"object:{obj_input['object_id']}",
            "commit": "NO_PRESENT_SOURCE",
            "sha256": sha256_text(canonical_json({"object_id": obj_input["object_id"], "sources": []})),
            "role": "gap",
        }
    ]


def object_receipt(obj_input: dict[str, Any], classified: dict[str, Any], batch_timestamp: str) -> dict[str, Any]:
    state = classified["game_state"]
    body = {
        "spec": SPEC,
        "schema_version": "GRAY_BABY_OBJECT_RECEIPT_V1",
        "identity_ref": f"object:{classified['object_id']}",
        "identity_class": "OBJECT",
        "human_identity": None,
        "action_ref": f"{PRODUCT}:{REPLAY_MODE}:{classified['object_id']}",
        "timestamp": str(obj_input.get("observed_at") or batch_timestamp),
        "source_artifacts": _object_sources(obj_input),
        "replay_parameters": _replay_parameters("single object membrane classification over local inputs"),
        "output": {
            "claim": f"game_state={state} route={classified['route']} deleted=false",
            "output_hash": "",
        },
        "object_id": classified["object_id"],
        "batch_id": classified["batch_id"],
        "game_state": state,
        "route": classified["route"],
        "bound_source_tier": classified["bound_source_tier"],
        "operators_used": list(classified["operators_selected"]),
        "wallet_ref": classified["wallet_ref"],
        "deleted": False,
        "identity_promoted": False,
        "authority": AUTHORITY,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "authority_created": False,
        "prior_preserved": True,
        "prior_payload_hash": classified["prior_payload_hash"],
        "prior_claim_tier": classified["prior_claim_tier"],
        "gaps": list(classified["gaps"]),
        "specialists": list(classified["specialists"]),
        "chain_data_fabricated": False,
        "promotion_performed": False,
        "falsification_applied": False,
        "kernel_version": KERNEL_VERSION,
        "kernel_replay_invoked": False,
        "fixture_class": classified["fixture_class"],
    }
    return seal_receipt(body)


def _spec_divergence(classified: dict[str, Any]) -> str | None:
    state = classified["game_state"]
    if state == "CONFLICT":
        hashes = {row.get("payload_hash") for row in classified.get("source_hashes") or []}
        hashes.discard(None)
        if len(hashes) > 1:
            return "HASH_MISMATCH"
        return "HUMAN_INTERPRETATION_CONFLICT"
    return _SPEC_DIVERGENCE.get(state)


def conflict_record(obj_input: dict[str, Any], classified: dict[str, Any]) -> dict[str, Any]:
    state = classified["game_state"]
    observed = {
        "game_state": state,
        "source_hashes": classified["source_hashes"],
        "bound_source_tier": classified["bound_source_tier"],
    }
    body = {
        "spec": SPEC,
        "receipt_id": "",
        "object_id": classified["object_id"],
        "batch_id": classified["batch_id"],
        "game_state": state,
        "divergence_class": _spec_divergence(classified),
        "expected_value": classified.get("prior_payload_hash"),
        "observed_value": canonical_json(observed),
        "verifier_identity": f"role:{ROLE}",
        "verifier_version": PRODUCT,
        "timestamp": str(obj_input.get("observed_at") or "UNAVAILABLE"),
        "notes_ref": HUMAN_SUMMARY_REF,
        "authority_created": False,
        "deleted": False,
        "human_identity": None,
    }
    sealed_core = {key: value for key, value in body.items() if key != "receipt_id"}
    body["receipt_id"] = sha256_text(canonical_json(sealed_core))
    return body


def alien_case(classified: dict[str, Any]) -> dict[str, Any]:
    reason = "NO_KNOWN_GAME_STATE"
    tiers = [row.get("tier") for row in classified.get("source_hashes") or []]
    if any(tier not in SOURCE_ORDER for tier in tiers):
        reason = "UNRANKED_SOURCE_TIER"
    body = {
        "spec": SCHEMA_VERSION_ALIEN,
        "object_id": classified["object_id"],
        "batch_id": classified["batch_id"],
        "reason": reason,
        "passes_completed": classified["passes"],
        "operators_used": list(classified["operators_selected"]),
        "route": "DEEP_REPLAY",
        "specialist": "ALIEN",
        "authority_created": False,
        "chain_data_fabricated": False,
        "human_identity": None,
    }
    body["case_id"] = sha256_text(canonical_json(body))
    return body


def batch_receipt(batch_input: dict[str, Any], classified: dict[str, Any]) -> dict[str, Any]:
    objects = classified["objects"]
    used = {name for obj in objects for name in obj["operators_selected"]}
    used.add("REPLAY_RECEIPT_WRITER")
    manual = [obj["object_id"] for obj in objects if "HUMAN_REVIEW_GATE" in obj["specialists"]]
    prevented = sum(len(obj["prevented_rules"]) for obj in objects)
    counts = _state_counts(objects)
    writer = run_operator(
        "REPLAY_RECEIPT_WRITER",
        {"object_id": batch_input["batch_id"]},
        [],
        1,
    )
    body = {
        "spec": SPEC,
        "schema_version": SCHEMA_VERSION_BATCH,
        "identity_ref": f"role:{ROLE}",
        "identity_class": "ROLE",
        "human_identity": None,
        "action_ref": f"{PRODUCT}:{REPLAY_MODE}:{batch_input['batch_id']}",
        "timestamp": _batch_timestamp(batch_input),
        "source_artifacts": [_inventory_artifact(batch_input)],
        "replay_parameters": _replay_parameters(
            "batch membrane classification over local inventory inputs"
        ),
        "output": {
            "claim": (
                f"batch={batch_input['batch_id']} input_objects={len(objects)} "
                f"authority_created=false"
            ),
            "output_hash": "",
        },
        "batch_id": batch_input["batch_id"],
        "INPUT_OBJECTS": len(objects),
        "state_counts": counts,
        "OPERATORS_AVAILABLE": list(OPERATORS),
        "OPERATORS_USED": sorted(used),
        "MANUAL_REVIEWS": len(manual),
        "manual_review_object_ids": manual,
        "REPEATED_ERRORS_PREVENTED": prevented,
        "AUTHORITY_CREATED": False,
        "authority": AUTHORITY,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "mode": REPLAY_MODE,
        "batch_start": batch_input["batch_start"],
        "batch_size": batch_input["batch_size"],
        "inventory_class": batch_input["inventory_class"],
        "kernel_version": KERNEL_VERSION,
        "kernel_replay_invoked": False,
        "constitutional_root": CONSTITUTIONAL_ROOT,
        "network": NETWORK,
        "secrets_used": False,
        "chain_data_fabricated": False,
        "promotion_performed": False,
        "design_inventory_size": DESIGN_INVENTORY_SIZE,
        "design_batch_size": DESIGN_BATCH_SIZE,
        "fixture_note": batch_input.get("fixture_note") or FIXTURE_NOTE,
        "object_ids": [obj["object_id"] for obj in objects],
        "queue_object_ids": sorted(obj["object_id"] for obj in objects if obj["route"] == "QUEUE"),
        "specialist_object_ids": sorted(obj["object_id"] for obj in objects if obj["route"] == "SPECIALIST"),
        "deep_replay_object_ids": sorted(obj["object_id"] for obj in objects if obj["route"] == "DEEP_REPLAY"),
        "receipt_object_ids": sorted(obj["object_id"] for obj in objects if obj["route"] == "RECEIPT"),
        "human_summary_ref": HUMAN_SUMMARY_REF,
        "scorekeeper_note": SCOREKEEPER_NOTE,
        "receipt_writer_status": writer["status"],
    }
    return seal_receipt(body)


def write_all(batch_input: dict[str, Any], classified: dict[str, Any], workdir: Path) -> dict[str, Any]:
    receipt_root = workdir / "receipts"
    batches = receipt_root / "batches"
    objects = receipt_root / "objects"
    conflicts = receipt_root / "conflicts"
    aliens = receipt_root / "aliens"
    for directory in (batches, objects, conflicts, aliens):
        directory.mkdir(parents=True, exist_ok=True)
    inputs = {obj["object_id"]: obj for obj in batch_input["objects"]}
    stamped = _batch_timestamp(batch_input)
    written_objects = []
    for classified_obj in classified["objects"]:
        obj_input = inputs[classified_obj["object_id"]]
        receipt = object_receipt(obj_input, classified_obj, stamped)
        _write(objects / f"{classified_obj['object_id']}.json", receipt)
        written_objects.append(receipt)
        if classified_obj["game_state"] in ("CONFLICT", "INDEXER_DRIFT", "TEMPORAL_DRIFT", "ROLE_COLLAPSE"):
            _write(conflicts / f"{classified_obj['object_id']}.json", conflict_record(obj_input, classified_obj))
        if classified_obj["game_state"] == "ALIEN":
            _write(aliens / f"{classified_obj['object_id']}.json", alien_case(classified_obj))
    sealed = batch_receipt(batch_input, classified)
    _write(batches / f"{sealed['batch_id']}.json", sealed)
    return sealed


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Write Gray Baby replay receipts")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--mode", default=REPLAY_MODE)
    args = parser.parse_args(argv)
    if args.mode != REPLAY_MODE:
        raise SystemExit(f"unsupported mode: {args.mode}")
    workdir = Path(args.workdir)
    sealed = write_all(_load(workdir / "batch_input.json"), _load(workdir / "classified.json"), workdir)
    print(workdir / "receipts" / "batches" / f"{sealed['batch_id']}.json")


if __name__ == "__main__":
    main()
