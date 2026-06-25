#!/usr/bin/env python3
"""
Graphiti Read-Only Ingest Prototype v0.1

Builds deterministic, Graphiti-shaped memory episodes from sealed local COMPUTERWISDOM artifacts.

No Graphiti server.
No DB writes.
No network.
No LLM extraction.
No wallet/signing/execution/merge/EAS authority.

Invariant: memory is not authority.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "jaytree" / "memory" / "ingest-ro" / "out"
EPISODES_JSONL = OUT_DIR / "episodes.jsonl"
INDEX_JSON = OUT_DIR / "index.json"

REQUIRED_INVARIANT = "memory is not authority"
AUTHORITY = "NONE"
RUNTIME = "NOT_PERMITTED"
GROUP_ID = "computerwisdom_v0.1"

SOURCES = [
    "jaytree/memory/graphiti-memory-v0.1.json",
    "jaytree/memory/receipts/graphiti-memory-v0.1.eas-receipt.json",
    "jaytree/operations-manual/receipt-log-v0.1.json",
    "jaytree/operations-manual/lattice-snapshot-v0.1.json",
    "jaytree/external-roots/receipts/al-base-mcp-v0.1.eas-receipt.json",
]


@dataclass(frozen=True)
class Episode:
    episode_id: str
    group_id: str
    source_path: str
    source_sha256: str
    episode_type: str
    authority: str
    runtime: str
    invariant: str
    body: dict[str, Any]


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def episode_for_source(rel_path: str) -> Episode | None:
    path = ROOT / rel_path
    if not path.exists():
        return None

    raw = path.read_bytes()
    source_hash = sha256_bytes(raw)
    body = load_json(path)

    if body.get("authority") not in (None, AUTHORITY):
        raise SystemExit(f"authority drift in {rel_path}: {body.get('authority')!r}")

    if body.get("runtime") not in (None, RUNTIME):
        raise SystemExit(f"runtime drift in {rel_path}: {body.get('runtime')!r}")

    if body.get("required_invariant") not in (None, REQUIRED_INVARIANT):
        raise SystemExit(f"invariant drift in {rel_path}: {body.get('required_invariant')!r}")

    episode_core = {
        "source_path": rel_path,
        "source_sha256": source_hash,
        "authority": AUTHORITY,
        "runtime": RUNTIME,
        "invariant": REQUIRED_INVARIANT,
    }
    episode_id = "episode:sha256:" + hashlib.sha256(
        json.dumps(episode_core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return Episode(
        episode_id=episode_id,
        group_id=GROUP_ID,
        source_path=rel_path,
        source_sha256=source_hash,
        episode_type="sealed_local_artifact",
        authority=AUTHORITY,
        runtime=RUNTIME,
        invariant=REQUIRED_INVARIANT,
        body=body,
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    episodes: list[Episode] = []
    missing: list[str] = []

    for rel_path in SOURCES:
        episode = episode_for_source(rel_path)
        if episode is None:
            missing.append(rel_path)
            continue
        episodes.append(episode)

    index = {
        "version": "graphiti-ingest-ro-v0.1",
        "status": "READ_ONLY_INDEX_BUILT",
        "group_id": GROUP_ID,
        "authority": AUTHORITY,
        "runtime": RUNTIME,
        "required_invariant": REQUIRED_INVARIANT,
        "episode_count": len(episodes),
        "missing_optional_sources": missing,
        "episodes": [
            {
                "episode_id": ep.episode_id,
                "source_path": ep.source_path,
                "source_sha256": ep.source_sha256,
            }
            for ep in episodes
        ],
    }

    with EPISODES_JSONL.open("w", encoding="utf-8") as fh:
        for ep in episodes:
            fh.write(json.dumps(asdict(ep), sort_keys=True) + "\n")

    INDEX_JSON.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(index, indent=2, sort_keys=True))
    print(f"WROTE: {EPISODES_JSONL.relative_to(ROOT)}")
    print(f"WROTE: {INDEX_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
