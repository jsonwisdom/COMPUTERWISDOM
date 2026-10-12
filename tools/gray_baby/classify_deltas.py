"""Assign one factual game state per object after membranes have run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.gray_baby.constants import (
    GAME_STATES,
    REPLAY_MODE,
    ROUTES,
    SOURCE_RANK,
    SPECIALISTS,
)
from tools.gray_baby.sources import (
    bound_tier_for,
    has_present,
    is_stronger,
    present_ranked,
    search_miss_of_stronger,
    source_hashes,
    strongest_source,
    unranked_present,
)

# Maps every game state to the operator effect vocabulary. A new game state
# fails at import until it is added here.
EFFECT_FOR_STATE = {
    "CLEAN": "CONFIRM",
    "UPGRADED": "UPGRADE",
    "CORRECTED": "CORRECT",
    "DEMOTED": "DEMOTE",
    "HOLD": "HOLD",
    "CONFLICT": "CONFLICT",
    "INDEXER_DRIFT": "DRIFT",
    "TEMPORAL_DRIFT": "DRIFT",
    "ROLE_COLLAPSE": "CONFLICT",
    "MISSING_RECEIPT": "HOLD",
    "ALIEN": "ALIEN",
}
_MISSING_EFFECTS = [state for state in GAME_STATES if state not in EFFECT_FOR_STATE]
if _MISSING_EFFECTS:
    raise RuntimeError(f"unhandled game states in EFFECT_FOR_STATE: {_MISSING_EFFECTS}")


def effect_for_state(state: str | None) -> str:
    if state is None:
        return "NONE"
    try:
        return EFFECT_FOR_STATE[state]
    except KeyError as exc:
        raise ValueError(f"unhandled game state: {state}") from exc


def route_for_state(state: str) -> str:
    try:
        return ROUTES[state]
    except KeyError as exc:
        raise ValueError(f"unhandled game state: {state}") from exc


def _metadata_state(obj: dict[str, Any]) -> str | None:
    views = [
        view
        for view in (obj.get("metadata_views") or [])
        if isinstance(view, dict) and view.get("present", True)
    ]
    ranked = [view for view in views if view.get("tier") in SOURCE_RANK and view.get("payload_hash")]
    if len(ranked) < 2:
        return "HOLD"
    winner = strongest_source(ranked)
    if winner is None:
        return "HOLD"
    hashes = {view.get("payload_hash") for view in ranked}
    if len(hashes) <= 1:
        return None
    others = [view for view in ranked if view.get("payload_hash") != winner.get("payload_hash")]
    if others and all(is_stronger(str(winner["tier"]), str(view["tier"])) for view in others):
        if obj.get("relation") == "NARROWING":
            return "DEMOTED"
        return "CORRECTED"
    return "CONFLICT"


def preliminary_state(obj: dict[str, Any], results: list[dict[str, Any]] | None = None) -> str | None:
    """Return a known game state, or None when no known pattern fits.

    None is not a silent delete. The router sends that object through a second
    pass and then to ALIEN_ROUTER.
    """
    del results  # classification reads the object and its local receipts
    if unranked_present(obj):
        return None
    if obj.get("temporal_relation") == "OLD_SNAPSHOT_FALSIFIES_LATER":
        return "TEMPORAL_DRIFT"
    if obj.get("address_role_ambiguous"):
        return "ROLE_COLLAPSE"
    if obj.get("identity_claim_requested"):
        return "CONFLICT"
    if (
        obj.get("index_disagrees_with_raw_chain")
        and has_present(obj, "RAW_CHAIN")
        and has_present(obj, "PUBLIC_INDEXES")
    ):
        chain = next(entry for entry in present_ranked(obj) if entry["tier"] == "RAW_CHAIN")
        index = next(entry for entry in present_ranked(obj) if entry["tier"] == "PUBLIC_INDEXES")
        if chain.get("payload_hash") != index.get("payload_hash"):
            return "INDEXER_DRIFT"

    present = present_ranked(obj)
    if search_miss_of_stronger(obj):
        # The prior object remains. Replaying without its stronger receipt
        # records a gap. It does not delete the object or adopt a weaker source.
        return "HOLD"
    if not present:
        return "MISSING_RECEIPT"

    relation = obj.get("relation") or "NONE"
    winner = strongest_source(present)
    prior_tier = obj.get("prior_claim_tier")
    if (
        winner is not None
        and relation == "NARROWING"
        and prior_tier in SOURCE_RANK
        and is_stronger(str(winner["tier"]), str(prior_tier))
    ):
        return "DEMOTED"
    if (
        winner is not None
        and relation == "ADDITIVE"
        and prior_tier in SOURCE_RANK
        and is_stronger(str(winner["tier"]), str(prior_tier))
    ):
        hashes = {entry.get("payload_hash") for entry in present}
        if len(hashes) == 1:
            return "UPGRADED"
    if obj.get("metadata_conflict"):
        meta = _metadata_state(obj)
        if meta is not None:
            return meta

    disagreement = _disagreement_state(obj, present)
    if disagreement is not None:
        return disagreement
    if _primary_claim_unresolved(obj):
        return "HOLD"
    versions = obj.get("export_versions") or []
    if isinstance(versions, list) and len(set(versions)) > 1:
        return "HOLD"
    return "CLEAN"


def _disagreement_state(obj: dict[str, Any], present: list[dict[str, Any]]) -> str | None:
    hashes = {entry.get("payload_hash") for entry in present}
    if len(hashes) <= 1:
        return None
    winner = strongest_source(present)
    if winner is None:
        return "CONFLICT"
    others = [entry for entry in present if entry.get("payload_hash") != winner.get("payload_hash")]
    if others and all(is_stronger(str(winner["tier"]), str(entry["tier"])) for entry in others):
        prior_hash = obj.get("prior_payload_hash")
        if prior_hash and prior_hash != winner.get("payload_hash"):
            return "CORRECTED"
        return "CLEAN"
    return "CONFLICT"


def _primary_claim_unresolved(obj: dict[str, Any]) -> bool:
    claim = obj.get("primary_claim") or "OBJECT_BINDING"
    if claim == "USER_OPERATION":
        return not obj.get("user_operation")
    if claim == "CREATE2_ADDRESS":
        local = obj.get("create2_local") or {}
        if not isinstance(local, dict):
            return True
        return any(not local.get(key) for key in ("deployer", "salt", "init_code_hash"))
    if claim == "CREATION_TX":
        return not obj.get("creation_tx")
    if claim == "METADATA":
        return bool(obj.get("metadata_conflict"))
    if claim == "INITIALIZER":
        return bool(obj.get("initializer_claimed")) and not obj.get("initializer_local")
    if claim == "EVENT_TOPICS":
        return bool(obj.get("event_topics_claimed")) and not obj.get("event_topics_local")
    return False


def create2_complete(obj: dict[str, Any]) -> bool:
    local = obj.get("create2_local") or {}
    if not isinstance(local, dict):
        return False
    return all(local.get(key) for key in ("deployer", "salt", "init_code_hash"))


def gaps_for(obj: dict[str, Any], state: str) -> list[str]:
    gaps: list[str] = []
    if not has_present(obj, "RAW_CHAIN"):
        gaps.append("RAW_CHAIN")
    if not obj.get("creation_tx"):
        gaps.append("creation_tx")
    if obj.get("erc4337") and not obj.get("user_operation"):
        gaps.append("erc4337_user_operation")
    if obj.get("create2") and not create2_complete(obj):
        gaps.append("create2_local")
    if obj.get("initializer_claimed") and not obj.get("initializer_local"):
        gaps.append("initializer")
    if obj.get("event_topics_claimed") and not obj.get("event_topics_local"):
        gaps.append("event_topics")
    if obj.get("ipfs_cid_claimed") and not obj.get("ipfs_bytes_local"):
        gaps.append("ipfs_bytes")
    if obj.get("expects_drive") and not has_present(obj, "DRIVE_HISTORY"):
        gaps.append("DRIVE_HISTORY")
    if state == "MISSING_RECEIPT":
        gaps.append("receipt")
    if state == "HOLD" and search_miss_of_stronger(obj):
        gaps.append("prior_bound_receipt")
    return sorted(set(gaps))


def specialists_for(obj: dict[str, Any], state: str, prevented: list[str]) -> list[str]:
    specs: list[str] = []
    if state == "TEMPORAL_DRIFT":
        specs.append("TEMPORAL")
    if state == "ROLE_COLLAPSE":
        specs.append("PROVENANCE")
    if state == "INDEXER_DRIFT":
        specs.append("CHAIN")
    if state == "CONFLICT":
        specs.append("CONTRADICTION")
    if state == "ALIEN":
        specs.append("ALIEN")
    if state in ("HOLD", "MISSING_RECEIPT"):
        specs.append("GRAY_BABY")
    if state in ("HOLD", "MISSING_RECEIPT") and not has_present(obj, "RAW_CHAIN"):
        specs.append("CHAIN")
    if obj.get("identity_claim_requested"):
        specs.append("HUMAN_REVIEW_GATE")
    if obj.get("erc4337"):
        specs.append("ERC4337")
    if obj.get("platform") == "ZORA":
        specs.append("ZORA")
    if obj.get("protocol") == "UNISWAP_V4":
        specs.append("UNISWAP_V4")
    if obj.get("ipfs_cid_claimed") and not obj.get("ipfs_bytes_local"):
        specs.append("IPFS")
    if obj.get("expects_drive") and not has_present(obj, "DRIVE_HISTORY"):
        specs.append("DRIVE_HISTORY")
    if obj.get("expects_repo_receipt") and not has_present(obj, "REPO_RECEIPTS"):
        specs.append("GITHUB_RECEIPT")
    if obj.get("metadata_conflict") and state == "CONFLICT":
        specs.append("SCHEMA")
    if obj.get("adversarial_proposals"):
        specs.append("ADVERSARIAL")
    if prevented:
        specs.append("TEST")
    unknown = [name for name in specs if name not in SPECIALISTS]
    if unknown:
        raise ValueError(f"unhandled specialist: {unknown}")
    return sorted(set(specs))


def classify_object(
    obj: dict[str, Any],
    replay_record: dict[str, Any],
    membrane: dict[str, Any],
    batch_id: str,
) -> dict[str, Any]:
    preliminary = replay_record.get("preliminary_state")
    if preliminary is None:
        state = "ALIEN"
    elif preliminary not in GAME_STATES:
        raise ValueError(f"unhandled game state: {preliminary}")
    else:
        state = str(preliminary)
    if membrane.get("deleted") or membrane.get("identity_promoted") or membrane.get("human_identity"):
        raise ValueError("membrane output violated a hard boundary")
    prevented = list(membrane.get("prevented_rules") or [])
    wallet = obj.get("wallet")
    return {
        "object_id": obj["object_id"],
        "batch_id": batch_id,
        "game_state": state,
        "route": route_for_state(state),
        "specialists": specialists_for(obj, state, prevented),
        "bound_source_tier": bound_tier_for(obj),
        "prior_game_state": obj.get("prior_game_state"),
        "prior_claim_tier": obj.get("prior_claim_tier"),
        "prior_bound_tier": obj.get("prior_bound_tier"),
        "prior_payload_hash": obj.get("prior_payload_hash"),
        "operators_selected": list(replay_record.get("operators_selected") or []),
        "passes": int(replay_record.get("passes") or 1),
        "deleted": False,
        "human_identity": None,
        "wallet_ref": wallet if isinstance(wallet, str) and wallet else None,
        "identity_promoted": False,
        "authority_created": False,
        "gaps": gaps_for(obj, state),
        "prior_preserved": True,
        "chain_data_fabricated": False,
        "prevented_rules": sorted(set(prevented)),
        "promotion_performed": False,
        "falsification_applied": False,
        "source_hashes": source_hashes(obj),
        "fixture_class": obj.get("fixture_class"),
    }


def classify_batch(batch_input: dict[str, Any], replay: dict[str, Any], membranes: dict[str, Any]) -> dict[str, Any]:
    by_id = {record["object_id"]: record for record in replay["objects"]}
    membrane_by_id = {record["object_id"]: record for record in membranes["objects"]}
    classified = []
    for obj in batch_input["objects"]:
        object_id = obj["object_id"]
        classified.append(
            classify_object(obj, by_id[object_id], membrane_by_id[object_id], batch_input["batch_id"])
        )
    return {
        "batch_id": batch_input["batch_id"],
        "mode": batch_input["mode"],
        "authority_created": False,
        "objects": classified,
    }


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Classify Gray Baby replay deltas")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--mode", default=REPLAY_MODE)
    args = parser.parse_args(argv)
    if args.mode != REPLAY_MODE:
        raise SystemExit(f"unsupported mode: {args.mode}")
    workdir = Path(args.workdir)
    classified = classify_batch(
        _load(workdir / "batch_input.json"),
        _load(workdir / "replay_batch.json"),
        _load(workdir / "membrane_report.json"),
    )
    for obj in classified["objects"]:
        if obj["deleted"] or obj["identity_promoted"] or obj["human_identity"] or obj["authority_created"]:
            raise SystemExit("classification violated a membrane")
        if obj["game_state"] not in GAME_STATES:
            raise SystemExit(f"unhandled game state: {obj['game_state']}")
    _write(workdir / "classified.json", classified)
    print(workdir / "classified.json")


if __name__ == "__main__":
    main()
