"""Operator pool for the cheap lane and conditional passes.

Handlers read local object fields only. When chain, RPC, or Drive bytes are
absent they return MISSING_RECEIPT or HOLD. They do not invent those bytes.
"""

from __future__ import annotations

from typing import Any, Callable

from tools.gray_baby.classify_deltas import create2_complete, effect_for_state, preliminary_state
from tools.gray_baby.constants import OPERATORS, SOURCE_ORDER, SPECIALISTS
from tools.gray_baby.sources import (
    bound_tier_for,
    is_stronger,
    present_ranked,
    strongest_source,
    unranked_present,
)

Handler = Callable[[dict[str, Any], list[dict[str, Any]], int], dict[str, Any]]


def make_result(
    *,
    operator: str,
    object_id: str,
    status: str,
    finding: str,
    pass_index: int,
    source_tier: str | None = None,
    state_effect: str = "NONE",
    may_change_state: bool = False,
    delete_requested: bool = False,
    identity_promotion: bool = False,
    specialist: str | None = None,
    evidence_refs: list[str] | None = None,
    stub: bool = False,
) -> dict[str, Any]:
    if specialist is not None and specialist not in SPECIALISTS:
        raise ValueError(f"unhandled specialist: {specialist}")
    return {
        "operator": operator,
        "object_id": object_id,
        "status": status,
        "source_tier": source_tier,
        "finding": finding,
        "state_effect": state_effect,
        "may_change_state": may_change_state,
        "delete_requested": delete_requested,
        "identity_promotion": identity_promotion,
        "specialist": specialist,
        "evidence_refs": sorted(evidence_refs or []),
        "authority_created": False,
        "stub": stub,
        "chain_data_fabricated": False,
        "pass_index": pass_index,
    }


def _refs(entries: list[dict[str, Any]]) -> list[str]:
    refs: list[str] = []
    for entry in entries:
        if entry.get("payload_hash"):
            refs.append(str(entry["payload_hash"]))
        elif entry.get("ref"):
            refs.append(str(entry["ref"]))
    return refs


def _object_selector(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    return make_result(
        operator="OBJECT_SELECTOR",
        object_id=obj["object_id"],
        status="OK",
        finding="SELECTED",
        pass_index=pass_index,
        evidence_refs=[str(obj["object_id"])],
    )


def _temporal_guard(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    if obj.get("temporal_relation") == "OLD_SNAPSHOT_FALSIFIES_LATER":
        return make_result(
            operator="TEMPORAL_GUARD",
            object_id=obj["object_id"],
            status="CONFLICT",
            finding="OLD_SNAPSHOT_CANNOT_FALSIFY_LATER",
            pass_index=pass_index,
            state_effect="DRIFT",
            may_change_state=False,
            specialist="TEMPORAL",
            evidence_refs=[str(obj.get("later_object_id") or obj["object_id"])],
        )
    return make_result(
        operator="TEMPORAL_GUARD",
        object_id=obj["object_id"],
        status="OK",
        finding="NO_TEMPORAL_CONFLICT",
        pass_index=pass_index,
    )


def _source_ranker(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    unranked = unranked_present(obj)
    if unranked:
        return make_result(
            operator="SOURCE_RANKER",
            object_id=obj["object_id"],
            status="HOLD",
            finding="UNRANKED_SOURCE_TIER",
            pass_index=pass_index,
            state_effect="NONE",
            specialist="GRAY_BABY",
            evidence_refs=[str(entry.get("tier")) for entry in unranked],
        )
    ordered = sorted(present_ranked(obj), key=lambda entry: SOURCE_ORDER.index(str(entry["tier"])))
    return make_result(
        operator="SOURCE_RANKER",
        object_id=obj["object_id"],
        status="OK",
        finding="RANKED_" + ">".join(str(entry["tier"]) for entry in ordered),
        pass_index=pass_index,
        source_tier=str(ordered[0]["tier"]) if ordered else None,
        evidence_refs=_refs(ordered),
    )


def _chain_binder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    chain = [entry for entry in present_ranked(obj) if entry["tier"] == "RAW_CHAIN"]
    if chain:
        return make_result(
            operator="CHAIN_BINDER",
            object_id=obj["object_id"],
            status="OK",
            finding="RAW_CHAIN_PRESENT_IN_INPUT",
            pass_index=pass_index,
            source_tier="RAW_CHAIN",
            state_effect="CONFIRM",
            evidence_refs=_refs(chain),
        )
    return make_result(
        operator="CHAIN_BINDER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="RAW_CHAIN_ABSENT",
        pass_index=pass_index,
        state_effect="HOLD",
        specialist="CHAIN",
        stub=True,
    )


def _tx_origin_finder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    creation_tx = obj.get("creation_tx")
    if isinstance(creation_tx, str) and creation_tx:
        return make_result(
            operator="TX_ORIGIN_FINDER",
            object_id=obj["object_id"],
            status="OK",
            finding="CREATION_TX_PRESENT_IN_INPUT",
            pass_index=pass_index,
            source_tier="RAW_CHAIN" if any(entry["tier"] == "RAW_CHAIN" for entry in present_ranked(obj)) else None,
            evidence_refs=[creation_tx],
        )
    return make_result(
        operator="TX_ORIGIN_FINDER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="CREATION_TX_ABSENT",
        pass_index=pass_index,
        specialist="CHAIN",
        stub=True,
    )


def _erc4337_decoder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    user_op = obj.get("user_operation")
    if isinstance(user_op, dict) and user_op:
        return make_result(
            operator="ERC4337_DECODER",
            object_id=obj["object_id"],
            status="OK",
            finding="LOCAL_USER_OPERATION_BOUND",
            pass_index=pass_index,
            evidence_refs=sorted(str(key) for key in user_op.keys()),
            specialist="ERC4337",
        )
    return make_result(
        operator="ERC4337_DECODER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="USER_OPERATION_ABSENT",
        pass_index=pass_index,
        specialist="ERC4337",
        stub=True,
    )


def _create2_decoder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    if create2_complete(obj):
        local = obj["create2_local"]
        return make_result(
            operator="CREATE2_DECODER",
            object_id=obj["object_id"],
            status="OK",
            finding="LOCAL_CREATE2_FIELDS_BOUND",
            pass_index=pass_index,
            evidence_refs=[f"{key}:{local[key]}" for key in ("deployer", "salt", "init_code_hash")],
            specialist="CHAIN",
        )
    return make_result(
        operator="CREATE2_DECODER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="CREATE2_FIELDS_ABSENT",
        pass_index=pass_index,
        specialist="CHAIN",
        stub=True,
    )


def _initializer_decoder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    local = obj.get("initializer_local")
    if isinstance(local, dict) and local:
        return make_result(
            operator="INITIALIZER_DECODER",
            object_id=obj["object_id"],
            status="OK",
            finding="LOCAL_INITIALIZER_BOUND",
            pass_index=pass_index,
            evidence_refs=sorted(str(key) for key in local.keys()),
        )
    return make_result(
        operator="INITIALIZER_DECODER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="INITIALIZER_ABSENT",
        pass_index=pass_index,
        specialist="CHAIN",
        stub=True,
    )


def _event_topic_decoder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    topics = obj.get("event_topics_local")
    if isinstance(topics, list) and topics:
        return make_result(
            operator="EVENT_TOPIC_DECODER",
            object_id=obj["object_id"],
            status="OK",
            finding="LOCAL_EVENT_TOPICS_BOUND",
            pass_index=pass_index,
            evidence_refs=[str(topic) for topic in topics],
        )
    return make_result(
        operator="EVENT_TOPIC_DECODER",
        object_id=obj["object_id"],
        status="MISSING_RECEIPT",
        finding="EVENT_TOPICS_ABSENT",
        pass_index=pass_index,
        specialist="CHAIN",
        stub=True,
    )


def _metadata_binder(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    views = [
        view
        for view in (obj.get("metadata_views") or [])
        if isinstance(view, dict) and view.get("present", True) and view.get("payload_hash")
    ]
    ranked = [view for view in views if view.get("tier") in SOURCE_ORDER]
    if len(ranked) < 2:
        return make_result(
            operator="METADATA_BINDER",
            object_id=obj["object_id"],
            status="MISSING_RECEIPT",
            finding="METADATA_SIDE_ABSENT",
            pass_index=pass_index,
            specialist="SCHEMA",
            stub=True,
        )
    winner = strongest_source(ranked)
    assert winner is not None
    hashes = {view.get("payload_hash") for view in ranked}
    if len(hashes) == 1:
        return make_result(
            operator="METADATA_BINDER",
            object_id=obj["object_id"],
            status="OK",
            finding="METADATA_AGREES",
            pass_index=pass_index,
            source_tier=str(winner["tier"]),
            state_effect="CONFIRM",
            evidence_refs=_refs(ranked),
        )
    others = [view for view in ranked if view.get("payload_hash") != winner.get("payload_hash")]
    if all(is_stronger(str(winner["tier"]), str(view["tier"])) for view in others):
        return make_result(
            operator="METADATA_BINDER",
            object_id=obj["object_id"],
            status="CONFLICT",
            finding="METADATA_STRONGER_SOURCE_DIFFERS",
            pass_index=pass_index,
            source_tier=str(winner["tier"]),
            state_effect="CORRECT",
            may_change_state=True,
            specialist="SCHEMA",
            evidence_refs=_refs(ranked),
        )
    return make_result(
        operator="METADATA_BINDER",
        object_id=obj["object_id"],
        status="CONFLICT",
        finding="METADATA_UNRESOLVED",
        pass_index=pass_index,
        state_effect="CONFLICT",
        specialist="SCHEMA",
        evidence_refs=_refs(ranked),
    )


def _indexer_drift_detector(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    present = present_ranked(obj)
    chain = [entry for entry in present if entry["tier"] == "RAW_CHAIN"]
    index = [entry for entry in present if entry["tier"] == "PUBLIC_INDEXES"]
    if not chain or not index:
        return make_result(
            operator="INDEXER_DRIFT_DETECTOR",
            object_id=obj["object_id"],
            status="MISSING_RECEIPT",
            finding="INDEX_OR_CHAIN_ABSENT",
            pass_index=pass_index,
            specialist="CHAIN",
            stub=True,
        )
    if chain[0].get("payload_hash") != index[0].get("payload_hash"):
        return make_result(
            operator="INDEXER_DRIFT_DETECTOR",
            object_id=obj["object_id"],
            status="CONFLICT",
            finding="INDEXER_DRIFT",
            pass_index=pass_index,
            source_tier="RAW_CHAIN",
            state_effect="DRIFT",
            specialist="CHAIN",
            evidence_refs=_refs(chain + index),
        )
    return make_result(
        operator="INDEXER_DRIFT_DETECTOR",
        object_id=obj["object_id"],
        status="OK",
        finding="INDEX_MATCHES_RAW_CHAIN",
        pass_index=pass_index,
        source_tier="RAW_CHAIN",
        state_effect="CONFIRM",
        evidence_refs=_refs(chain + index),
    )


def _export_version_guard(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    versions = [str(version) for version in (obj.get("export_versions") or [])]
    if len(set(versions)) > 1:
        return make_result(
            operator="EXPORT_VERSION_GUARD",
            object_id=obj["object_id"],
            status="HOLD",
            finding="EXPORT_VERSION_DIVERGENCE",
            pass_index=pass_index,
            state_effect="HOLD",
            specialist="SCHEMA",
            evidence_refs=sorted(set(versions)),
        )
    return make_result(
        operator="EXPORT_VERSION_GUARD",
        object_id=obj["object_id"],
        status="OK" if versions else "NO_OP",
        finding="EXPORT_VERSION_STABLE" if versions else "EXPORT_VERSION_ABSENT",
        pass_index=pass_index,
        evidence_refs=versions,
    )


def _role_collapse_sentinel(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    if obj.get("address_role_ambiguous"):
        roles = [str(role) for role in (obj.get("roles") or [])]
        return make_result(
            operator="ROLE_COLLAPSE_SENTINEL",
            object_id=obj["object_id"],
            status="CONFLICT",
            finding="ROLE_COLLAPSE",
            pass_index=pass_index,
            state_effect="CONFLICT",
            specialist="PROVENANCE",
            evidence_refs=roles,
        )
    return make_result(
        operator="ROLE_COLLAPSE_SENTINEL",
        object_id=obj["object_id"],
        status="OK",
        finding="ROLE_UNAMBIGUOUS",
        pass_index=pass_index,
    )


def _identity_membrane(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    wallet = obj.get("wallet")
    refs = [str(wallet)] if isinstance(wallet, str) and wallet else []
    if obj.get("identity_claim_requested"):
        return make_result(
            operator="IDENTITY_MEMBRANE",
            object_id=obj["object_id"],
            status="CONFLICT",
            finding="WALLET_IS_NOT_HUMAN_IDENTITY",
            pass_index=pass_index,
            state_effect="NONE",
            specialist="HUMAN_REVIEW_GATE",
            evidence_refs=refs,
        )
    return make_result(
        operator="IDENTITY_MEMBRANE",
        object_id=obj["object_id"],
        status="OK",
        finding="NO_IDENTITY_CLAIM",
        pass_index=pass_index,
        evidence_refs=refs,
    )


def _receipt_comparator(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    present = present_ranked(obj)
    if not present:
        return make_result(
            operator="RECEIPT_COMPARATOR",
            object_id=obj["object_id"],
            status="MISSING_RECEIPT",
            finding="NO_PRESENT_RECEIPT",
            pass_index=pass_index,
            state_effect="HOLD",
            specialist="GRAY_BABY",
            stub=True,
        )
    winner = strongest_source(present)
    assert winner is not None
    hashes = {entry.get("payload_hash") for entry in present}
    if len(hashes) == 1:
        return make_result(
            operator="RECEIPT_COMPARATOR",
            object_id=obj["object_id"],
            status="OK",
            finding="RECEIPTS_AGREE",
            pass_index=pass_index,
            source_tier=str(winner["tier"]),
            state_effect="CONFIRM",
            evidence_refs=_refs(present),
        )
    others = [entry for entry in present if entry.get("payload_hash") != winner.get("payload_hash")]
    if all(is_stronger(str(winner["tier"]), str(entry["tier"])) for entry in others):
        prior_hash = obj.get("prior_payload_hash")
        if prior_hash and prior_hash != winner.get("payload_hash"):
            return make_result(
                operator="RECEIPT_COMPARATOR",
                object_id=obj["object_id"],
                status="CONFLICT",
                finding="STRONGER_RECEIPT_DIFFERS",
                pass_index=pass_index,
                source_tier=str(winner["tier"]),
                state_effect="CORRECT",
                may_change_state=True,
                specialist="CONTRADICTION",
                evidence_refs=_refs(present),
            )
        return make_result(
            operator="RECEIPT_COMPARATOR",
            object_id=obj["object_id"],
            status="CONFLICT",
            finding="WEAKER_DISAGREEMENT_IGNORED",
            pass_index=pass_index,
            source_tier=str(winner["tier"]),
            evidence_refs=_refs(present),
        )
    return make_result(
        operator="RECEIPT_COMPARATOR",
        object_id=obj["object_id"],
        status="CONFLICT",
        finding="EQUAL_TIER_CONFLICT",
        pass_index=pass_index,
        state_effect="CONFLICT",
        specialist="CONTRADICTION",
        evidence_refs=_refs(present),
    )


def _delta_classifier(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    state = preliminary_state(obj, prior)
    if state is None:
        return make_result(
            operator="DELTA_CLASSIFIER",
            object_id=obj["object_id"],
            status="HOLD",
            finding="UNCLASSIFIED",
            pass_index=pass_index,
            specialist="GRAY_BABY",
        )
    return make_result(
        operator="DELTA_CLASSIFIER",
        object_id=obj["object_id"],
        status="OK",
        finding=state,
        pass_index=pass_index,
        source_tier=bound_tier_for(obj),
        state_effect=effect_for_state(state),
        may_change_state=state in ("UPGRADED", "CORRECTED", "DEMOTED"),
    )


def _alien_router(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    return make_result(
        operator="ALIEN_ROUTER",
        object_id=obj["object_id"],
        status="ALIEN",
        finding="NO_KNOWN_GAME_STATE",
        pass_index=pass_index,
        state_effect="ALIEN",
        specialist="ALIEN",
    )


def _replay_receipt_writer(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    return make_result(
        operator="REPLAY_RECEIPT_WRITER",
        object_id=obj["object_id"],
        status="OK",
        finding="RECEIPTS_WRITTEN",
        pass_index=pass_index,
        evidence_refs=[str(obj["object_id"])],
    )


def _batch_scorekeeper(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    del prior
    return make_result(
        operator="BATCH_SCOREKEEPER",
        object_id=obj["object_id"],
        status="OK",
        finding="SCOREBOARD_WRITTEN",
        pass_index=pass_index,
        evidence_refs=[str(obj["object_id"])],
    )


def _regression_sentinel(obj: dict[str, Any], prior: list[dict[str, Any]], pass_index: int) -> dict[str, Any]:
    proposals = [str(item) for item in (obj.get("adversarial_proposals") or [])]
    illegal = [
        result["operator"]
        for result in prior
        if result.get("delete_requested") or result.get("identity_promotion") or result.get("chain_data_fabricated")
    ]
    if not proposals and not illegal:
        return make_result(
            operator="REGRESSION_SENTINEL",
            object_id=obj["object_id"],
            status="NO_OP",
            finding="NO_REPEATED_ERROR",
            pass_index=pass_index,
        )
    return make_result(
        operator="REGRESSION_SENTINEL",
        object_id=obj["object_id"],
        status="OK",
        finding="KNOWN_RULE_BLOCKED",
        pass_index=pass_index,
        specialist="TEST",
        evidence_refs=proposals + illegal,
    )


OPERATOR_HANDLERS: dict[str, Handler] = {
    "OBJECT_SELECTOR": _object_selector,
    "TEMPORAL_GUARD": _temporal_guard,
    "SOURCE_RANKER": _source_ranker,
    "CHAIN_BINDER": _chain_binder,
    "TX_ORIGIN_FINDER": _tx_origin_finder,
    "ERC4337_DECODER": _erc4337_decoder,
    "CREATE2_DECODER": _create2_decoder,
    "INITIALIZER_DECODER": _initializer_decoder,
    "EVENT_TOPIC_DECODER": _event_topic_decoder,
    "METADATA_BINDER": _metadata_binder,
    "INDEXER_DRIFT_DETECTOR": _indexer_drift_detector,
    "EXPORT_VERSION_GUARD": _export_version_guard,
    "ROLE_COLLAPSE_SENTINEL": _role_collapse_sentinel,
    "IDENTITY_MEMBRANE": _identity_membrane,
    "RECEIPT_COMPARATOR": _receipt_comparator,
    "DELTA_CLASSIFIER": _delta_classifier,
    "ALIEN_ROUTER": _alien_router,
    "REPLAY_RECEIPT_WRITER": _replay_receipt_writer,
    "BATCH_SCOREKEEPER": _batch_scorekeeper,
    "REGRESSION_SENTINEL": _regression_sentinel,
}

_MISSING_HANDLERS = [name for name in OPERATORS if name not in OPERATOR_HANDLERS]
if _MISSING_HANDLERS:
    raise RuntimeError(f"unhandled operators: {_MISSING_HANDLERS}")


def run_operator(
    name: str,
    obj: dict[str, Any],
    prior_results: list[dict[str, Any]],
    pass_index: int,
) -> dict[str, Any]:
    try:
        handler = OPERATOR_HANDLERS[name]
    except KeyError as exc:
        raise ValueError(f"unhandled operator: {name}") from exc
    result = handler(obj, prior_results, pass_index)
    result["operator"] = name
    result["object_id"] = obj["object_id"]
    result["pass_index"] = pass_index
    result["authority_created"] = False
    result["chain_data_fabricated"] = False
    # Pool operators refuse these requests. Membrane tests inject them directly.
    result["delete_requested"] = False
    result["identity_promotion"] = False
    return result
