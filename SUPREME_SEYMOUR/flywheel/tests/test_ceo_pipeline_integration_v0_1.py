import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
spec = importlib.util.spec_from_file_location(
    "jason_flywheel", BASE / "recursive_learning_flywheel_v0_1.py"
)
flywheel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flywheel)


class CandidateIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.baseline = self.root / "snapshot.json"
        self.baseline.write_text(json.dumps({
            "observed_at": "2026-09-21T00:00:00Z", "public_repo_count": 0, "repos": []
        }), encoding="utf-8")
        self.out = self.root / "output"

    def run_flywheel(self, env):
        with (mock.patch.object(flywheel, "BASELINE", self.baseline),
              mock.patch.object(flywheel, "OUTDIR", self.out),
              mock.patch.object(flywheel, "list_public_repos", return_value=[]),
              mock.patch.dict(os.environ, env, clear=True)):
            flywheel.main()
        return json.loads((self.out / "flywheel-report.json").read_text(encoding="utf-8"))

    def fixture(self):
        private_root = self.root / "private-sources"
        private_root.mkdir()
        voice = b"synthetic voice only"
        (private_root / "v.txt").write_bytes(voice)
        original = {
            "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1", "denominator": "JASON",
            "expected": [
                {"id": "private-v", "kind": "voice", "topics": ["purpose"]},
                {"id": "private-c", "kind": "chat", "topics": ["purpose"]},
            ],
            "index": [
                {"id": "private-v", "candidates": [
                    {"path": "v.txt", "format": "text"}]},
                {"id": "private-c", "candidates": [
                    {"path": "missing.json", "format": "json"}]},
            ],
        }
        source_path = self.root / "original-manifest.json"
        source_path.write_text(json.dumps(original), encoding="utf-8")
        claim_path = self.root / "claims.json"
        claim_path.write_text(json.dumps({
            "proposed_claims": [
                {"source_id": "private-v", "topic": "purpose",
                 "interpretation": "candidate only", "byte_start": 0,
                 "byte_end": len(voice), "expected_excerpt": voice.decode("utf-8")},
                {"source_id": "private-c", "topic": "purpose",
                 "interpretation": "not established", "byte_start": 0,
                 "byte_end": 4, "expected_excerpt": "abcd"},
            ]
        }), encoding="utf-8")
        return {
            "JASON_SOURCE_MANIFEST": str(source_path),
            "JASON_SOURCE_ROOT": str(private_root),
            "JASON_CLAIMS_MANIFEST": str(claim_path),
        }

    def test_configured_pipeline_public_summary_is_counts_only(self):
        report = self.run_flywheel(self.fixture())
        state = report["person_first_sources"]["provenance_pipeline"]
        self.assertEqual(state["candidate_observation_count"], 1)
        self.assertEqual(state["scoped_hold_reason_counts"]["MISSING_SOURCE_FILE"], 1)
        self.assertEqual(state["historical_completeness"], "UNKNOWN")
        self.assertEqual(report["live"]["delta_count"], 0)
        text = json.dumps(report)
        for needle in ("private-v", "private-c", "synthetic voice only",
                       "private-sources", "candidate only"):
            self.assertNotIn(needle, text)
        private = json.loads((self.out / "private/ceo-graph-fold-query-candidate.json").read_text())
        self.assertEqual(len(private["observations"]), 1)
        self.assertEqual(len(private["scoped_holds"]), 1)
        self.assertTrue(private["private_only"])

    def test_no_claims_configured_does_not_claim_learning(self):
        env = self.fixture()
        del env["JASON_CLAIMS_MANIFEST"]
        report = self.run_flywheel(env)
        self.assertEqual(report["person_first_sources"]["provenance_pipeline"]["scope"],
                         "NO_LOCAL_CLAIM_ANNOTATIONS_CONFIGURED")
        self.assertFalse((self.out / "private/ceo-graph-fold-query-candidate.json").exists())

    def test_invalid_claim_packet_does_not_stop_independent_repo_replay(self):
        env = self.fixture()
        path = Path(env["JASON_CLAIMS_MANIFEST"])
        path.write_text('{"wrong":1}', encoding="utf-8")
        report = self.run_flywheel(env)
        state = report["person_first_sources"]
        self.assertEqual(state["scope"], "LOCAL_INPUT_ERROR")
        self.assertEqual(state["recovery_action"], "REPAIR_PRIVATE_SOURCE_MANIFEST")
        self.assertEqual(report["live"]["public_repo_count"], 0)
        self.assertNotIn(str(path), json.dumps(report))


if __name__ == "__main__":
    unittest.main()
