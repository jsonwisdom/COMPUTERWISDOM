#!/usr/bin/env python3
"""Read-only query helper for Graphiti-shaped memory episodes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
EPISODES_JSONL = ROOT / "jaytree" / "memory" / "ingest-ro" / "out" / "episodes.jsonl"


def iter_values(obj: Any):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_values(value)
    else:
        yield obj


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: query.py <field> <value>")

    field, needle = sys.argv[1], sys.argv[2]

    if not EPISODES_JSONL.exists():
        raise SystemExit("missing episodes.jsonl; run prototype.py first")

    matches = []
    for line in EPISODES_JSONL.read_text(encoding="utf-8").splitlines():
        episode = json.loads(line)
        haystack = episode.get("body", {})
        found = False

        if field in episode and str(episode[field]) == needle:
            found = True
        elif isinstance(haystack, dict) and str(haystack.get(field)) == needle:
            found = True
        else:
            found = any(str(value) == needle for value in iter_values(haystack))

        if found:
            matches.append(
                {
                    "episode_id": episode["episode_id"],
                    "source_path": episode["source_path"],
                    "source_sha256": episode["source_sha256"],
                    "authority": episode["authority"],
                    "runtime": episode["runtime"],
                    "invariant": episode["invariant"],
                }
            )

    print(json.dumps({"matches": matches, "count": len(matches)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
