"""Run the selected operators for one batch. Offline. No secrets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.gray_baby.classify_deltas import preliminary_state
from tools.gray_baby.constants import REPLAY_MODE
from tools.gray_baby.operators import run_operator
from tools.gray_baby.router import route_object


def replay_object(obj: dict[str, Any]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    selected: list[str] = []
    preliminary: str | None = None
    passes = 0
    for pass_index in (1, 2):
        operators = route_object(
            obj,
            pass_index=pass_index,
            prior_results=results,
            prior_state=preliminary,
        )
        if not operators:
            break
        passes = pass_index
        for name in operators:
            selected.append(name)
            results.append(run_operator(name, obj, results, pass_index))
        preliminary = preliminary_state(obj, results)
        if preliminary is not None:
            break
    if preliminary is None:
        passes = 2
        selected.append("ALIEN_ROUTER")
        results.append(run_operator("ALIEN_ROUTER", obj, results, passes))
    return {
        "object_id": obj["object_id"],
        "operators_selected": selected,
        "passes": passes,
        "preliminary_state": preliminary,
        "results": results,
    }


def replay_loaded_batch(batch_input: dict[str, Any]) -> dict[str, Any]:
    if batch_input.get("mode") != REPLAY_MODE:
        raise ValueError(f"unsupported mode: {batch_input.get('mode')}")
    return {
        "batch_id": batch_input["batch_id"],
        "mode": batch_input["mode"],
        "authority_created": False,
        "objects": [replay_object(obj) for obj in batch_input["objects"]],
    }


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Replay one Gray Baby batch")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--mode", default=REPLAY_MODE)
    args = parser.parse_args(argv)
    if args.mode != REPLAY_MODE:
        raise SystemExit(f"unsupported mode: {args.mode}")
    workdir = Path(args.workdir)
    try:
        payload = replay_loaded_batch(_load(workdir / "batch_input.json"))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    destination = workdir / "replay_batch.json"
    _write(destination, payload)
    print(destination)


if __name__ == "__main__":
    main()
