"""Routing, membranes, classification, and receipt schema tests."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import jsonschema
import pytest

from src.replay_kernel_v0_1 import AUTHORITY, canonical_json, sha256_text
from tools.gray_baby.build_batch import build_batch
from tools.gray_baby.build_scoreboard import build_scoreboard
from tools.gray_baby.classify_deltas import classify_batch, preliminary_state
from tools.gray_baby.constants import (
    CHEAP_LANE,
    GAME_STATES,
    OPERATORS,
    REPLAY_MODE,
    ROUTES,
    SPECIALISTS,
)
from tools.gray_baby.operators import make_result, run_operator
from tools.gray_baby.replay_batch import replay_loaded_batch
from tools.gray_baby.router import route_object
from tools.gray_baby.validate_membranes import validate_batch, validate_object_membranes
from tools.gray_baby.write_receipts import write_all

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "fixtures" / "gray_baby" / "synthetic_inventory_v1.json"
SCHEMAS = ROOT / "schemas" / "gray_baby"
WORKFLOW = ROOT / ".github" / "workflows" / "gray-baby-bulk-replay-v1.yml"

EXPECTED_STATES = {
    "synth-clean": "CLEAN",
    "synth-upgraded": "UPGRADED",
    "synth-corrected": "CORRECTED",
    "synth-demoted": "DEMOTED",
    "synth-weaker-label": "CLEAN",
    "synth-search-miss": "CLEAN",
    "synth-missing": "MISSING_RECEIPT",
    "synth-indexer-drift": "INDEXER_DRIFT",
    "synth-temporal": "TEMPORAL_DRIFT",
    "synth-role": "ROLE_COLLAPSE",
    "synth-identity": "CONFLICT",
    "synth-erc4337": "HOLD",
    "synth-create2": "CLEAN",
    "synth-metadata": "CORRECTED",
    "synth-preserve-stronger": "HOLD",
    "synth-alien": "ALIEN",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator(name: str) -> jsonschema.Draft202012Validator:
    schema = _load(SCHEMAS / name)
    return jsonschema.Draft202012Validator(schema)


def _inventory() -> dict:
    return _load(INVENTORY_PATH)


def _run(tmp_path: Path, *, batch_start: int = 0, batch_size: int = 32):
    inventory = _inventory()
    batch_input = build_batch(
        inventory,
        batch_start=batch_start,
        batch_size=batch_size,
        mode=REPLAY_MODE,
        inventory_uri=str(INVENTORY_PATH),
    )
    replay = replay_loaded_batch(batch_input)
    membranes = validate_batch(batch_input, replay)
    classified = classify_batch(batch_input, replay, membranes)
    receipt = write_all(batch_input, classified, tmp_path)
    scoreboard = build_scoreboard(receipt, classified)
    return {
        "batch_input": batch_input,
        "replay": replay,
        "membranes": membranes,
        "classified": classified,
        "receipt": receipt,
        "scoreboard": scoreboard,
    }


def _by_id(rows: list[dict]) -> dict[str, dict]:
    return {row["object_id"]: row for row in rows}


def test_every_game_state_and_operator_is_routed():
    assert set(ROUTES) == set(GAME_STATES)
    assert len(OPERATORS) == 20
    assert len(SPECIALISTS) == 16
    for state in GAME_STATES:
        assert ROUTES[state] in {"RECEIPT", "QUEUE", "SPECIALIST", "DEEP_REPLAY"}


def test_clean_object_uses_only_the_cheap_lane():
    inventory = _inventory()
    clean = next(obj for obj in inventory["objects"] if obj["object_id"] == "synth-clean")
    selected = route_object(clean, pass_index=1, prior_results=[], prior_state=None)
    assert selected == list(CHEAP_LANE)
    assert 4 <= len(selected) <= 6
    assert "ALIEN_ROUTER" not in selected
    assert len(selected) < len(OPERATORS)


def test_conditionals_follow_uncertainty_not_pool_size():
    inventory = {obj["object_id"]: obj for obj in _inventory()["objects"]}
    missing_tx = route_object(inventory["synth-missing"], pass_index=1, prior_results=[], prior_state=None)
    erc = route_object(inventory["synth-erc4337"], pass_index=1, prior_results=[], prior_state=None)
    create2 = route_object(inventory["synth-create2"], pass_index=1, prior_results=[], prior_state=None)
    role = route_object(inventory["synth-role"], pass_index=1, prior_results=[], prior_state=None)
    identity = route_object(inventory["synth-identity"], pass_index=1, prior_results=[], prior_state=None)
    drift = route_object(inventory["synth-indexer-drift"], pass_index=1, prior_results=[], prior_state=None)
    alien = route_object(inventory["synth-alien"], pass_index=1, prior_results=[], prior_state=None)
    assert "TX_ORIGIN_FINDER" in missing_tx
    assert "ERC4337_DECODER" in erc
    assert "CREATE2_DECODER" in create2
    assert "ROLE_COLLAPSE_SENTINEL" in role
    assert "IDENTITY_MEMBRANE" in identity
    assert "INDEXER_DRIFT_DETECTOR" in drift
    assert "SOURCE_RANKER" in alien
    assert "ALIEN_ROUTER" not in alien
    assert len(erc) > len(CHEAP_LANE)
    assert len(erc) < len(OPERATORS)


def test_second_pass_adds_alien_router_only_after_two_passes():
    inventory = {obj["object_id"]: obj for obj in _inventory()["objects"]}
    alien = inventory["synth-alien"]
    first = route_object(alien, pass_index=1, prior_results=[], prior_state=None)
    assert "ALIEN_ROUTER" not in first
    replay = replay_loaded_batch(
        build_batch(
            {"inventory_class": "SYNTHETIC_TEST_ONLY", "objects": [alien]},
            batch_start=0,
            batch_size=32,
            mode=REPLAY_MODE,
            inventory_uri=str(INVENTORY_PATH),
        )
    )
    record = replay["objects"][0]
    assert record["passes"] == 2
    assert record["preliminary_state"] is None
    assert record["operators_selected"][-1] == "ALIEN_ROUTER"
    assert record["operators_selected"].count("ALIEN_ROUTER") == 1


def test_search_miss_cannot_delete():
    obj = {
        "object_id": "unit-search-miss",
        "sources": [
            {
                "tier": "REPO_RECEIPTS",
                "present": True,
                "payload_hash": "sha256:" + "ab" * 32,
                "ref": "fixture:repo",
            }
        ],
        "prior_game_state": "CLEAN",
        "prior_bound_tier": "REPO_RECEIPTS",
    }
    bad = make_result(
        operator="CHAIN_BINDER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="SEARCH_MISS",
        pass_index=1,
        delete_requested=True,
        stub=True,
    )
    _validator("operator_result.schema.json").validate(bad)
    report = validate_object_membranes(obj, [bad])
    assert report["deleted"] is False
    assert "SEARCH_MISS_CANNOT_DELETE" in report["prevented_rules"]


def test_wallet_is_never_promoted_to_human():
    obj = {
        "object_id": "unit-wallet",
        "wallet": "0x" + "ab" * 20,
        "identity_claim_requested": True,
        "requested_human_label": "NOT_A_HUMAN_BINDING",
        "sources": [],
    }
    bad = make_result(
        operator="IDENTITY_MEMBRANE",
        object_id=obj["object_id"],
        status="CONFLICT",
        finding="WALLET_TO_HUMAN",
        pass_index=1,
        identity_promotion=True,
        specialist="HUMAN_REVIEW_GATE",
    )
    _validator("operator_result.schema.json").validate(bad)
    report = validate_object_membranes(obj, [bad])
    assert report["human_identity"] is None
    assert report["identity_promoted"] is False
    assert report["wallet_ref"] == obj["wallet"]
    assert "WALLET_CANNOT_PROMOTE_TO_HUMAN" in report["prevented_rules"]


def test_weaker_source_cannot_override_stronger():
    chain_hash = "sha256:" + "11" * 32
    label_hash = "sha256:" + "22" * 32
    obj = {
        "object_id": "unit-weaker",
        "relation": "CONTRADICTION",
        "prior_payload_hash": chain_hash,
        "prior_bound_tier": "RAW_CHAIN",
        "prior_claim_tier": "RAW_CHAIN",
        "sources": [
            {"tier": "RAW_CHAIN", "present": True, "payload_hash": chain_hash, "ref": "chain"},
            {"tier": "PAGE_LABELS", "present": True, "payload_hash": label_hash, "ref": "label"},
        ],
    }
    bad = make_result(
        operator="RECEIPT_COMPARATOR",
        object_id=obj["object_id"],
        status="CONFLICT",
        finding="PAGE_LABEL_OVERRIDE",
        pass_index=1,
        source_tier="PAGE_LABELS",
        state_effect="CORRECT",
        may_change_state=True,
    )
    report = validate_object_membranes(obj, [bad])
    assert "WEAKER_SOURCE_CANNOT_OVERRIDE" in report["prevented_rules"]
    assert report["bound_source_tier"] == "RAW_CHAIN"
    assert preliminary_state(obj, [bad]) == "CLEAN"


def test_stronger_receipt_supersedes_without_erasure(tmp_path: Path):
    ran = _run(tmp_path)
    corrected = _by_id(ran["classified"]["objects"])["synth-corrected"]
    assert corrected["game_state"] == "CORRECTED"
    assert corrected["route"] == "RECEIPT"
    assert corrected["bound_source_tier"] == "RAW_CHAIN"
    assert corrected["deleted"] is False
    assert corrected["prior_preserved"] is True
    assert corrected["prior_payload_hash"] is not None
    assert corrected["prior_claim_tier"] == "PUBLIC_INDEXES"


def test_fixture_classification_and_receipts(tmp_path: Path):
    ran = _run(tmp_path)
    classified = _by_id(ran["classified"]["objects"])
    assert set(classified) == set(EXPECTED_STATES)
    for object_id, state in EXPECTED_STATES.items():
        assert classified[object_id]["game_state"] == state
        assert classified[object_id]["route"] == ROUTES[state]
        assert classified[object_id]["deleted"] is False
        assert classified[object_id]["human_identity"] is None
        assert classified[object_id]["identity_promoted"] is False
        assert classified[object_id]["authority_created"] is False
        assert classified[object_id]["chain_data_fabricated"] is False
        assert classified[object_id]["promotion_performed"] is False
        _validator("object_state.schema.json").validate(classified[object_id])

    preserve = classified["synth-preserve-stronger"]
    assert preserve["bound_source_tier"] == "RAW_CHAIN"
    assert "SEARCH_MISS_CANNOT_DELETE" in preserve["prevented_rules"]
    assert "WEAKER_SOURCE_CANNOT_OVERRIDE" in preserve["prevented_rules"]
    assert "synth-preserve-stronger" in ran["receipt"]["object_ids"]

    identity = classified["synth-identity"]
    assert identity["wallet_ref"] == "synthetic-wallet:identity"
    assert "HUMAN_REVIEW_GATE" in identity["specialists"]
    assert "WALLET_CANNOT_PROMOTE_TO_HUMAN" in identity["prevented_rules"]

    weaker = classified["synth-weaker-label"]
    assert weaker["bound_source_tier"] == "RAW_CHAIN"
    assert weaker["game_state"] == "CLEAN"

    search_miss = classified["synth-search-miss"]
    assert "SEARCH_MISS_CANNOT_DELETE" in search_miss["prevented_rules"]
    assert search_miss["deleted"] is False

    alien = classified["synth-alien"]
    assert alien["route"] == "DEEP_REPLAY"
    assert alien["passes"] == 2
    assert "ALIEN" in alien["specialists"]

    clean = classified["synth-clean"]
    assert clean["operators_selected"] == list(CHEAP_LANE)

    for record in ran["replay"]["objects"]:
        assert len(record["operators_selected"]) < len(OPERATORS)
        for result in record["results"]:
            _validator("operator_result.schema.json").validate(result)
            assert result["delete_requested"] is False
            assert result["identity_promotion"] is False
            assert result["chain_data_fabricated"] is False

    receipt = ran["receipt"]
    _validator("batch_receipt.schema.json").validate(receipt)
    assert receipt["spec"] == "REPLAY_RECEIPT_SPEC_V1"
    assert receipt["AUTHORITY_CREATED"] is False
    assert receipt["authority"] is AUTHORITY
    assert receipt["kernel_replay_invoked"] is False
    assert receipt["INPUT_OBJECTS"] == 16
    assert receipt["state_counts"]["CLEAN"] == 4
    assert receipt["state_counts"]["UPGRADED"] == 1
    assert receipt["state_counts"]["CORRECTED"] == 2
    assert receipt["state_counts"]["HOLD"] == 2
    assert receipt["state_counts"]["ALIEN"] == 1
    assert receipt["MANUAL_REVIEWS"] == 1
    assert receipt["REPEATED_ERRORS_PREVENTED"] == 5
    assert sum(receipt["state_counts"].values()) == 16
    assert "REPLAY_RECEIPT_WRITER" in receipt["OPERATORS_USED"]
    assert "BATCH_SCOREKEEPER" not in receipt["OPERATORS_USED"]

    scoreboard = ran["scoreboard"]
    assert scoreboard["CHAIN_BOUND_OBJECTS"] == 12
    assert scoreboard["REPEATED_ERROR_RATE"] == {"numerator": 5, "denominator": 16, "status": "DEFINED"}
    assert scoreboard["MANUAL_RECOVERY_RATE"]["numerator"] == 1
    assert scoreboard["UNRESOLVED_HOLD_RATE"] == {"numerator": 3, "denominator": 16, "status": "DEFINED"}
    assert scoreboard["quality_score_emitted"] is False
    assert scoreboard["AUTHORITY_CREATED"] is False
    assert "BATCH_SCOREKEEPER" in scoreboard["OPERATORS_USED"]

    alien_path = tmp_path / "receipts" / "aliens" / "synth-alien.json"
    alien_case = _load(alien_path)
    _validator("alien_case.schema.json").validate(alien_case)
    assert alien_case["route"] == "DEEP_REPLAY"

    for object_id in EXPECTED_STATES:
        object_receipt = _load(tmp_path / "receipts" / "objects" / f"{object_id}.json")
        for key in ("spec", "receipt_id", "identity_ref", "action_ref", "source_artifacts", "replay_parameters", "output"):
            assert key in object_receipt
        assert object_receipt["identity_class"] == "OBJECT"
        assert object_receipt["identity_ref"] == f"object:{object_id}"
        assert object_receipt["human_identity"] is None
        assert object_receipt["authority_created"] is False
        assert object_receipt["deleted"] is False
        assert object_receipt["wallet_ref"] != object_receipt["identity_ref"]
        assert object_receipt["receipt_id"].startswith("sha256:")
        assert object_receipt["output"]["output_hash"].startswith("sha256:")


def test_pipeline_is_deterministic(tmp_path: Path):
    first = _run(tmp_path / "one")
    second = _run(tmp_path / "two")
    assert first["receipt"] == second["receipt"]
    assert first["scoreboard"] == second["scoreboard"]
    assert first["classified"] == second["classified"]


def test_empty_batch_is_idle_and_valid(tmp_path: Path):
    ran = _run(tmp_path, batch_start=1000, batch_size=32)
    assert ran["receipt"]["batch_id"] == "GRAY_BABY_BATCH_032"
    assert ran["receipt"]["INPUT_OBJECTS"] == 0
    assert ran["receipt"]["AUTHORITY_CREATED"] is False
    assert all(count == 0 for count in ran["receipt"]["state_counts"].values())
    assert ran["scoreboard"]["REPEATED_ERROR_RATE"]["status"] == "UNDEFINED_EMPTY_BATCH"
    assert ran["scoreboard"]["CHAIN_BOUND_OBJECTS"] == 0
    _validator("batch_receipt.schema.json").validate(ran["receipt"])


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        build_batch(
            _inventory(),
            batch_start=0,
            batch_size=32,
            mode="live_rpc",
            inventory_uri=str(INVENTORY_PATH),
        )


def test_stub_operators_do_not_fabricate_missing_data():
    bare = {"object_id": "unit-bare", "sources": [], "erc4337": True, "create2": True}
    for name in ("CHAIN_BINDER", "TX_ORIGIN_FINDER", "ERC4337_DECODER", "CREATE2_DECODER"):
        result = run_operator(name, bare, [], 1)
        _validator("operator_result.schema.json").validate(result)
        assert result["status"] == "MISSING_RECEIPT"
        assert result["stub"] is True
        assert result["chain_data_fabricated"] is False
        assert result["may_change_state"] is False
        assert result["delete_requested"] is False


def test_export_version_guard_and_equal_tier_conflict_are_known_states():
    divergent = {
        "object_id": "unit-export",
        "export_versions": ["v1", "v2"],
        "sources": [
            {"tier": "REPO_RECEIPTS", "present": True, "payload_hash": "sha256:" + "aa" * 32, "ref": "repo"}
        ],
        "creation_tx": "fixture-tx:unit-export",
    }
    assert "EXPORT_VERSION_GUARD" in route_object(divergent, pass_index=1, prior_results=[], prior_state=None)
    assert preliminary_state(divergent, []) == "HOLD"
    tied = {
        "object_id": "unit-tie",
        "sources": [
            {"tier": "PUBLIC_INDEXES", "present": True, "payload_hash": "sha256:" + "a1" * 32, "ref": "a"},
            {"tier": "PUBLIC_INDEXES", "present": True, "payload_hash": "sha256:" + "b2" * 32, "ref": "b"},
        ],
        "creation_tx": "fixture-tx:unit-tie",
    }
    assert preliminary_state(tied, []) == "CONFLICT"


def test_specialists_are_routing_targets_only():
    obj = {
        "object_id": "unit-routes",
        "platform": "ZORA",
        "protocol": "UNISWAP_V4",
        "ipfs_cid_claimed": "bafy-synthetic",
        "ipfs_bytes_local": False,
        "expects_drive": True,
        "expects_repo_receipt": True,
        "sources": [
            {"tier": "PAGE_LABELS", "present": True, "payload_hash": "sha256:" + "cd" * 32, "ref": "label"}
        ],
        "creation_tx": "fixture-tx:unit-routes",
    }
    state = preliminary_state(obj, [])
    assert state == "CLEAN"
    batch_input = build_batch(
        {"inventory_class": "UNIT", "objects": [obj]},
        batch_start=0,
        batch_size=32,
        mode=REPLAY_MODE,
        inventory_uri="unit",
    )
    replay = replay_loaded_batch(batch_input)
    membranes = validate_batch(batch_input, replay)
    classified = classify_batch(batch_input, replay, membranes)["objects"][0]
    for name in ("ZORA", "UNISWAP_V4", "IPFS", "DRIVE_HISTORY", "GITHUB_RECEIPT"):
        assert name in classified["specialists"]
        assert name in SPECIALISTS
        assert name not in OPERATORS


def test_kernel_hash_is_reused_and_authority_stays_false():
    assert AUTHORITY is False
    digest = sha256_text(canonical_json({"b": 1, "a": 2}))
    assert digest == sha256_text(canonical_json({"a": 2, "b": 1}))
    assert digest.startswith("sha256:")


def test_package_does_not_import_network_clients():
    root = ROOT / "tools" / "gray_baby"
    banned = {"urllib", "requests", "httpx", "aiohttp", "socket", "web3"}
    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            else:
                continue
            assert banned.isdisjoint(names), f"{path.name} imports {names}"


def test_workflow_is_manual_read_only_and_additive():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in text
    assert "contents: read" in text
    for forbidden in ("pull_request:", "push:", "schedule:", "cron:"):
        assert forbidden not in text
    for step in (
        "build_batch",
        "replay_batch",
        "validate_membranes",
        "classify_deltas",
        "write_receipts",
        "build_scoreboard",
    ):
        assert step in text
    assert "upload-artifact" in text
