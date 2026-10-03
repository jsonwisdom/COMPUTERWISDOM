"""Local source-tier helpers. No network lookups."""

from __future__ import annotations

from typing import Any

from tools.gray_baby.constants import SOURCE_RANK


def source_entries(obj: dict[str, Any]) -> list[dict[str, Any]]:
    entries = obj.get("sources") or []
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def present_ranked(obj: dict[str, Any]) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    for entry in source_entries(obj):
        tier = entry.get("tier")
        if entry.get("present") and tier in SOURCE_RANK and entry.get("payload_hash"):
            ranked.append(entry)
    return ranked


def unranked_present(obj: dict[str, Any]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for entry in source_entries(obj):
        if entry.get("present") and entry.get("tier") not in SOURCE_RANK:
            found.append(entry)
    return found


def has_present(obj: dict[str, Any], tier: str) -> bool:
    return any(entry.get("tier") == tier for entry in present_ranked(obj))


def strongest_source(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    ranked = [entry for entry in entries if entry.get("tier") in SOURCE_RANK]
    if not ranked:
        return None
    return min(
        ranked,
        key=lambda entry: (
            SOURCE_RANK[str(entry["tier"])],
            str(entry.get("ref") or ""),
            str(entry.get("payload_hash") or ""),
        ),
    )


def is_stronger(left: str, right: str) -> bool:
    """True when left outranks right on SOURCE_ORDER."""
    if left not in SOURCE_RANK or right not in SOURCE_RANK:
        raise ValueError(f"unranked source tier in comparison: {left!r}, {right!r}")
    return SOURCE_RANK[left] < SOURCE_RANK[right]


def bound_tier_for(obj: dict[str, Any]) -> str | None:
    """Strongest tier that remains bound.

    A missing stronger receipt stays bound. A weaker present source does not
    replace it.
    """
    prior = obj.get("prior_bound_tier")
    present = present_ranked(obj)
    if prior in SOURCE_RANK and not has_present(obj, str(prior)):
        return str(prior)
    winner = strongest_source(present)
    if winner is not None:
        return str(winner["tier"])
    if prior in SOURCE_RANK:
        return str(prior)
    return None


def search_miss_of_stronger(obj: dict[str, Any]) -> bool:
    prior = obj.get("prior_bound_tier")
    if prior not in SOURCE_RANK:
        return False
    return not has_present(obj, str(prior))


def sources_disagree(obj: dict[str, Any]) -> bool:
    present = present_ranked(obj)
    hashes = {str(entry.get("payload_hash")) for entry in present}
    if len(hashes) > 1:
        return True
    prior_hash = obj.get("prior_payload_hash")
    if prior_hash and hashes and str(prior_hash) not in hashes:
        return True
    return False


def change_is_weaker(obj: dict[str, Any], tier: str | None) -> bool:
    if tier not in SOURCE_RANK:
        return False
    anchor = bound_tier_for(obj)
    if anchor is None or anchor not in SOURCE_RANK:
        return False
    return SOURCE_RANK[str(tier)] > SOURCE_RANK[anchor]


def source_hashes(obj: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in source_entries(obj):
        if not entry.get("present"):
            continue
        rows.append(
            {
                "tier": entry.get("tier"),
                "payload_hash": entry.get("payload_hash"),
            }
        )
    rows.sort(key=lambda row: (str(row["tier"]), str(row["payload_hash"])))
    return rows
