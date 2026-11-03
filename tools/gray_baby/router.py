"""Select the minimum operator set for an object.

AGENT_COUNT follows uncertainty flags. The size of the operator pool does not
increase the set. Idle (no extra operators, and an empty batch) is valid.
"""

from __future__ import annotations

from typing import Any, Callable

from tools.gray_baby.constants import CHEAP_LANE, OPERATORS
from tools.gray_baby.sources import sources_disagree, unranked_present

Flag = Callable[[dict[str, Any]], bool]

# Conditional operators in a fixed order. Cheap-lane operators always run first.
CONDITIONALS: tuple[tuple[str, Flag], ...] = (
    ("TX_ORIGIN_FINDER", lambda obj: not obj.get("creation_tx")),
    ("ERC4337_DECODER", lambda obj: bool(obj.get("erc4337"))),
    ("CREATE2_DECODER", lambda obj: bool(obj.get("create2"))),
    ("INITIALIZER_DECODER", lambda obj: bool(obj.get("initializer_claimed"))),
    ("EVENT_TOPIC_DECODER", lambda obj: bool(obj.get("event_topics_claimed"))),
    ("METADATA_BINDER", lambda obj: bool(obj.get("metadata_conflict"))),
    ("INDEXER_DRIFT_DETECTOR", lambda obj: bool(obj.get("index_disagrees_with_raw_chain"))),
    (
        "EXPORT_VERSION_GUARD",
        lambda obj: len(set(obj.get("export_versions") or [])) > 1,
    ),
    ("ROLE_COLLAPSE_SENTINEL", lambda obj: bool(obj.get("address_role_ambiguous"))),
    ("IDENTITY_MEMBRANE", lambda obj: bool(obj.get("identity_claim_requested"))),
    ("SOURCE_RANKER", lambda obj: sources_disagree(obj) or bool(unranked_present(obj))),
    ("REGRESSION_SENTINEL", lambda obj: bool(obj.get("adversarial_proposals"))),
)


def route_object(
    obj: dict[str, Any],
    *,
    pass_index: int,
    prior_results: list[dict[str, Any]] | None = None,
    prior_state: str | None = None,
) -> list[str]:
    if pass_index == 1:
        selected = list(CHEAP_LANE)
        for name, flag in CONDITIONALS:
            if flag(obj):
                selected.append(name)
        return _dedupe(selected)
    if pass_index == 2:
        if prior_state is not None:
            return []
        already = {result["operator"] for result in (prior_results or [])}
        extra: list[str] = []
        if unranked_present(obj) and "SOURCE_RANKER" not in already:
            extra.append("SOURCE_RANKER")
        if obj.get("adversarial_proposals") and "REGRESSION_SENTINEL" not in already:
            extra.append("REGRESSION_SENTINEL")
        if not extra and "REGRESSION_SENTINEL" not in already:
            # One second-pass check, not the rest of the pool.
            extra.append("REGRESSION_SENTINEL")
        return extra
    raise ValueError(f"unhandled pass_index: {pass_index}")


def _dedupe(names: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for name in names:
        if name not in OPERATORS:
            raise ValueError(f"unhandled operator: {name}")
        if name in seen:
            continue
        seen.add(name)
        ordered.append(name)
    return ordered
