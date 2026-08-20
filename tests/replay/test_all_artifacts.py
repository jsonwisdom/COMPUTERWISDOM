"""Permanent replay regression contract.

Every artifact admitted to the regression manifest must replay to the exact
stored hash under the registry-declared canonicalizer, serializer, and hash
algorithm. This test does not assert real-world truth or authority.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from replay_registry_v0_2 import (  # noqa: E402
    REGISTRY,
    canonical_artifact_hash,
    registry_metadata,
)

MANIFEST = ROOT / "tests" / "fixtures" / "replay_regression_manifest_v0_2.json"


class TestAllReplayArtifacts(unittest.TestCase):
    def test_registry_axes_are_explicit(self):
        for schema_version, meta in REGISTRY.items():
            self.assertIn("canonical_version", meta)
            self.assertIn("serializer_version", meta)
            self.assertIn("hash_algorithm", meta)
            self.assertIn("canonicalizer", meta)
            self.assertNotEqual(schema_version, meta["canonical_version"])

    def test_all_manifest_artifacts_replay_exactly(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertTrue(manifest["artifacts"], "regression manifest must not be empty")

        for entry in manifest["artifacts"]:
            with self.subTest(path=entry["path"]):
                artifact_path = ROOT / entry["path"]
                artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
                replay_hash = canonical_artifact_hash(artifact)
                self.assertEqual(replay_hash, entry["expected_replay_hash"])

    def test_receipt_exposes_all_version_axes(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        first = json.loads((ROOT / manifest["artifacts"][0]["path"]).read_text(encoding="utf-8"))
        meta = registry_metadata(first["schema_version"])
        self.assertEqual(meta["schema_version"], first["schema_version"])
        self.assertIn("canonical_version", meta)
        self.assertIn("serializer_version", meta)
        self.assertIn("hash_algorithm", meta)


if __name__ == "__main__":
    unittest.main()
