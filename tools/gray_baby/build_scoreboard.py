"""Factual batch rates. These counts are not a quality score."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.gray_baby.constants import GAME_STATES, PRODUCT, REPLAY_MODE, SCHEMA_VERSION_SCOREBOARD
from tools.gray_baby.operators import run_operator


def _rate(numerator: int, denominator: int) -> dict[str, Any]:
    if denominator == 0:
        return {"numerator": numerator, "denominator": 0, "status": "UNDEFINED_EMPTY_BATCH"}
    return {"numerator": numerator, "denominator": denominator, "status": "DEFINED"}


def build_scoreboard(batch_receipt: dict[str, Any], classified: dict[str, Any]) -> dict[str, Any]:
    objects = classified["objects"]
    counts = {state: 0 for state in GAME_STATES}
    for obj in objects:
        state = obj["game_state"]
        if state not in counts:
            raise ValueError(f"unhandled game state: {state}")
        counts[state] += 1
    prevented = sum(len(obj["prevented_rules"]) for obj in objects)
    manual = sum(1 for obj in objects if "HUMAN_REVIEW_GATE" in obj["specialists"])
    chain_bound = sum(1 for obj in objects if obj.get("bound_source_tier") == "RAW_CHAIN")
    hold_like = counts["HOLD"] + counts["MISSING_RECEIPT"]
    population = int(batch_receipt["INPUT_OBJECTS"])
    keeper = run_operator(
        "BATCH_SCOREKEEPER",
        {"object_id": batch_receipt["batch_id"]},
        [],
        1,
    )
    used = sorted(set(batch_receipt["OPERATORS_USED"]) | {"BATCH_SCOREKEEPER"})
    return {
        "schema_version": SCHEMA_VERSION_SCOREBOARD,
        "product": PRODUCT,
        "batch_id": batch_receipt["batch_id"],
        "receipt_id": batch_receipt["receipt_id"],
        "INPUT_OBJECTS": population,
        "state_counts": counts,
        "REPEATED_ERRORS_PREVENTED": prevented,
        "MANUAL_REVIEWS": manual,
        "REPEATED_ERROR_RATE": _rate(prevented, population),
        "MANUAL_RECOVERY_RATE": _rate(manual, population),
        "CHAIN_BOUND_OBJECTS": chain_bound,
        "UNRESOLVED_HOLD_RATE": _rate(hold_like, population),
        "OPERATORS_USED": used,
        "scorekeeper_status": keeper["status"],
        "AUTHORITY_CREATED": False,
        "quality_score_emitted": False,
        "rate_definitions": {
            "REPEATED_ERROR_RATE": "blocked illegal transitions / INPUT_OBJECTS",
            "MANUAL_RECOVERY_RATE": "objects routed to HUMAN_REVIEW_GATE / INPUT_OBJECTS",
            "UNRESOLVED_HOLD_RATE": "(HOLD + MISSING_RECEIPT) / INPUT_OBJECTS",
            "CHAIN_BOUND_OBJECTS": "count of objects whose bound_source_tier is RAW_CHAIN",
        },
        "note": "Rates are counts. They are not a quality score and grant no authority.",
    }


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build a Gray Baby batch scoreboard")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--mode", default=REPLAY_MODE)
    args = parser.parse_args(argv)
    if args.mode != REPLAY_MODE:
        raise SystemExit(f"unsupported mode: {args.mode}")
    workdir = Path(args.workdir)
    classified = _load(workdir / "classified.json")
    batch_dir = workdir / "receipts" / "batches"
    receipts = sorted(batch_dir.glob("GRAY_BABY_BATCH_*.json"))
    if len(receipts) != 1:
        raise SystemExit(f"expected one batch receipt, found {len(receipts)}")
    scoreboard = build_scoreboard(_load(receipts[0]), classified)
    destination = workdir / "scoreboard.json"
    _write(destination, scoreboard)
    print(destination)


if __name__ == "__main__":
    main()
