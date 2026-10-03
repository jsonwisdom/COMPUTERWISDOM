"""Enforce batch membranes.

A search miss cannot delete an object.
A wallet cannot be promoted to a human identity.
A weaker source cannot override a stronger one.
An older snapshot cannot falsify a later object.
Missing data is not fabricated.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.gray_baby.constants import REPLAY_MODE, RULES, SOURCE_RANK
from tools.gray_baby.sources import (
    bound_tier_for,
    change_is_weaker,
    present_ranked,
    search_miss_of_stronger,
    sources_disagree,
)

_PROPOSAL_RULES = {
    "DELETE_ON_SEARCH_MISS": "SEARCH_MISS_CANNOT_DELETE",
    "WALLET_TO_HUMAN": "WALLET_CANNOT_PROMOTE_TO_HUMAN",
    "WEAKER_OVERRIDE": "WEAKER_SOURCE_CANNOT_OVERRIDE",
    "FALSIFY_LATER": "OLD_SNAPSHOT_CANNOT_FALSIFY_LATER",
    "FABRICATE_CHAIN": "MISSING_DATA_CANNOT_BE_FABRICATED",
}


def validate_object_membranes(obj: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    prevented: list[str] = []
    rejected_indexes: list[int] = []

    for proposal in obj.get("adversarial_proposals") or []:
        rule = _PROPOSAL_RULES.get(str(proposal))
        if rule:
            prevented.append(rule)

    if obj.get("identity_claim_requested"):
        prevented.append("WALLET_CANNOT_PROMOTE_TO_HUMAN")
    if obj.get("temporal_relation") == "OLD_SNAPSHOT_FALSIFIES_LATER":
        prevented.append("OLD_SNAPSHOT_CANNOT_FALSIFY_LATER")
    if search_miss_of_stronger(obj):
        prevented.append("SEARCH_MISS_CANNOT_DELETE")
        if sources_disagree(obj) or _weaker_present_against_prior(obj):
            prevented.append("WEAKER_SOURCE_CANNOT_OVERRIDE")

    for index, result in enumerate(results):
        rejected = False
        if result.get("delete_requested"):
            prevented.append("SEARCH_MISS_CANNOT_DELETE")
            rejected = True
        if result.get("identity_promotion") or result.get("human_identity"):
            prevented.append("WALLET_CANNOT_PROMOTE_TO_HUMAN")
            rejected = True
        if result.get("chain_data_fabricated"):
            prevented.append("MISSING_DATA_CANNOT_BE_FABRICATED")
            rejected = True
        tier = result.get("source_tier")
        if result.get("may_change_state") and change_is_weaker(obj, tier if isinstance(tier, str) else None):
            prevented.append("WEAKER_SOURCE_CANNOT_OVERRIDE")
            rejected = True
        if (
            obj.get("temporal_relation") == "OLD_SNAPSHOT_FALSIFIES_LATER"
            and result.get("may_change_state")
        ):
            prevented.append("OLD_SNAPSHOT_CANNOT_FALSIFY_LATER")
            rejected = True
        if rejected:
            rejected_indexes.append(index)

    unknown = [rule for rule in prevented if rule not in RULES]
    if unknown:
        raise ValueError(f"unhandled membrane rule: {unknown}")

    return {
        "object_id": obj["object_id"],
        "deleted": False,
        "human_identity": None,
        "identity_promoted": False,
        "wallet_ref": obj.get("wallet") if isinstance(obj.get("wallet"), str) else None,
        "bound_source_tier": bound_tier_for(obj),
        "prevented_rules": sorted(set(prevented)),
        "rejected_result_indexes": rejected_indexes,
        "authority_created": False,
        "chain_data_fabricated": False,
        "promotion_performed": False,
        "falsification_applied": False,
    }


def _weaker_present_against_prior(obj: dict[str, Any]) -> bool:
    prior = obj.get("prior_bound_tier")
    if prior not in SOURCE_RANK:
        return False
    return any(SOURCE_RANK[str(entry["tier"])] > SOURCE_RANK[str(prior)] for entry in present_ranked(obj))


def validate_batch(batch_input: dict[str, Any], replay: dict[str, Any]) -> dict[str, Any]:
    replay_by_id = {record["object_id"]: record for record in replay["objects"]}
    objects = []
    for obj in batch_input["objects"]:
        record = replay_by_id[obj["object_id"]]
        objects.append(validate_object_membranes(obj, record.get("results") or []))
    return {
        "batch_id": batch_input["batch_id"],
        "mode": batch_input["mode"],
        "authority_created": False,
        "objects": objects,
    }


def _assert_report(report: dict[str, Any]) -> None:
    for obj in report["objects"]:
        if obj["deleted"] or obj["identity_promoted"] or obj["human_identity"] or obj["authority_created"]:
            raise SystemExit(f"membrane honored an illegal transition for {obj['object_id']}")
        if obj["chain_data_fabricated"] or obj["promotion_performed"] or obj["falsification_applied"]:
            raise SystemExit(f"membrane honored an illegal transition for {obj['object_id']}")


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Validate Gray Baby replay membranes")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--mode", default=REPLAY_MODE)
    args = parser.parse_args(argv)
    if args.mode != REPLAY_MODE:
        raise SystemExit(f"unsupported mode: {args.mode}")
    workdir = Path(args.workdir)
    report = validate_batch(_load(workdir / "batch_input.json"), _load(workdir / "replay_batch.json"))
    _assert_report(report)
    _write(workdir / "membrane_report.json", report)
    print(workdir / "membrane_report.json")


if __name__ == "__main__":
    main()
