"""Slice an inventory into one deterministic batch."""

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
    DESIGN_BATCH_SIZE,
    DESIGN_INVENTORY_SIZE,
    FIXTURE_NOTE,
    REPLAY_MODE,
)

DEFAULT_INVENTORY = Path("fixtures/gray_baby/synthetic_inventory_v1.json")


def batch_id_for(batch_start: int, batch_size: int) -> str:
    index = (batch_start // batch_size) + 1
    return f"GRAY_BABY_BATCH_{index:03d}"


def build_batch(
    inventory: dict[str, Any],
    *,
    batch_start: int,
    batch_size: int,
    mode: str,
    inventory_uri: str,
) -> dict[str, Any]:
    if mode != REPLAY_MODE:
        raise ValueError(f"unsupported mode: {mode}")
    if batch_start < 0 or batch_size < 1:
        raise ValueError("batch_start must be >= 0 and batch_size must be >= 1")
    objects = sorted(
        inventory.get("objects") or [],
        key=lambda obj: (str(obj.get("observed_at") or ""), str(obj.get("object_id") or "")),
    )
    selected = objects[batch_start : batch_start + batch_size]
    inventory_class = str(inventory.get("inventory_class") or "UNSPECIFIED")
    return {
        "batch_id": batch_id_for(batch_start, batch_size),
        "batch_start": batch_start,
        "batch_size": batch_size,
        "mode": mode,
        "inventory_class": inventory_class,
        "inventory_count": len(objects),
        "selected_count": len(selected),
        "design_inventory_size": DESIGN_INVENTORY_SIZE,
        "design_batch_size": DESIGN_BATCH_SIZE,
        "fixture_note": FIXTURE_NOTE if inventory_class == "SYNTHETIC_TEST_ONLY" else "",
        "inventory_uri": inventory_uri,
        "authority_created": False,
        "objects": selected,
    }


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build one Gray Baby replay batch")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY))
    parser.add_argument("--batch-start", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=DESIGN_BATCH_SIZE)
    parser.add_argument("--mode", default=REPLAY_MODE)
    args = parser.parse_args(argv)
    inventory_path = Path(args.inventory)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    try:
        payload = build_batch(
            inventory,
            batch_start=args.batch_start,
            batch_size=args.batch_size,
            mode=args.mode,
            inventory_uri=args.inventory,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    destination = Path(args.workdir) / "batch_input.json"
    _write(destination, payload)
    print(destination)


if __name__ == "__main__":
    main()
