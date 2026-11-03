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
SPEC = importlib.util.spec_from_file_location("jason_flywheel_candidate_integration", BASE / "recursive_learning_flywheel_v0_1.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class CandidateFlywheelIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.baseline = self.root / "baseline.json"
        self.baseline.write_text(json.dumps({
            "observed_at": "2026-09-23T00:00:00Z",
            "public_repo_count": 0, "repos": [],
        }), encoding="utf-8")
        self.outdir = self.root / "build-output"

    def replay(self, env):
        with (mock.patch.object(mod, "BASELINE", self.baseline),
              mock.patch.object(mod, "OUTDIR", self.outdir),
              mock.patch.object(mod, "list_public_repos", return_value=[]),
              mock.patch.dict(os.environ, env, clear=True)):
            mod.main()
        return json.loads((self.outdir / "flywheel-report.json").read_text(encoding="utf-8"))

    def create_private_manifest(self):
        originals = self.root / "originals"
        originals.mkdir()
        (originals / "synthetic-chat.json").write_text(
            '{"messages":[{"text":"PRIVATE_CHAT_BODY_NEVER_PUBLIC"}]}',
            encoding="utf-8",
        )
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps({
            "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1",
            "denominator": "JASON",
            "expected": [
                {"id": "private-voice", "kind": "voice"},
                {"id": "private-chat", "kind": "chat"}
            ],
            "index": [
                {"id": "private-voice", "candidates": [{"path": "missing.txt", "format": "text"}]},
                {"id": "private-chat", "candidates": [{"path": "synthetic-chat.json", "format": "json"}]},
            ],
        }), encoding="utf-8")
        return manifest, originals

    def test_private_ceo_pipeline_stays_out_of_public_report(self):
        manifest, originals = self.create_private_manifest()
        result = self.replay({
            "JASON_SOURCE_MANIFEST": str(manifest),
            "JASON_SOURCE_ROOT": str(originals)
        })
        public = json.dumps(result)
        self.assertNotIn("PRIVATE_CHAT_BODY_NEVER_PUBLIC", public)
        self.assertNotIn("private-voice", public)
        self.assertNotIn("private-chat", public)
        summary = result["person_first_sources"]["jason_os_candidate_pipeline"]
        self.assertEqual(summary["candidate_text_count"], 1)
        self.assertEqual(summary["history_complete"], "UNKNOWN")
        self.assertEqual(summary["verified_claim_count"], 0)
        private = json.loads((self.outdir / "private/jason-os-candidates.json").read_text())
        self.assertEqual(private["ceo"]["class"], "CANDIDATE_ONLY_NOT_VALIDATED_CEO")
        self.assertEqual(private["query"]["rows"][0]["source_state"], "MISSING_SOURCE_FILE")
        self.assertEqual(private["query"]["rows"][1]["candidate_count"], 1)
        self.assertEqual(private["query"]["rows"][1]["claim_verdict"], "UNKNOWN")

    def test_unconfigured_still_replays_git_estate(self):
        result = self.replay({})
        self.assertEqual(result["person_first_sources"]["scope"], "NO_LOCAL_ORIGINALS_CONFIGURED")
        self.assertEqual(result["live"]["public_repo_count"], 0)
        self.assertFalse((self.outdir / "private/jason-os-candidates.json").exists())

    def test_invalid_private_manifest_does_not_block_public_git(self):
        bad = self.root / "bad-manifest.json"
        bad.write_text("{unparseable-json", encoding="utf-8")
        result = self.replay({"JASON_SOURCE_MANIFEST": str(bad)})
        self.assertEqual(result["person_first_sources"]["scope"], "LOCAL_INPUT_ERROR")
        self.assertTrue(result["person_first_sources"]["independent_supported_work_continues"])
        self.assertNotIn(str(bad), json.dumps(result))


if __name__ == "__main__":
    unittest.main()
