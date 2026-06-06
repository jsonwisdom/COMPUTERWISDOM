#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

directory = Path("artifacts/GITHUB_KITTYKREW_MINIMAL")
artifact = directory / "artifact.txt"
sbom = json.loads((directory / "sbom.json").read_text())
expected = sbom["artifact"]["sha256"]
actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
size = len(artifact.read_bytes())
expected_size = sbom["artifact"]["size_bytes"]

if actual == expected and size == expected_size:
    print(json.dumps({
        "status": "PASS",
        "artifact_hash_match": True,
        "artifact_size_match": True,
        "sha256": actual,
        "size_bytes": size,
        "authority": False
    }, sort_keys=True))
raise SystemExit(0)

print(json.dumps({
    "status": "FAIL",
    "artifact_hash_match": actual == expected,
    "artifact_size_match": size == expected_size,
    "expected_sha256": expected,
    "actual_sha256": actual,
    "expected_size_bytes": expected_size,
    "actual_size_bytes": size,
    "authority": False
}, sort_keys=True))
raise SystemExit(1)
