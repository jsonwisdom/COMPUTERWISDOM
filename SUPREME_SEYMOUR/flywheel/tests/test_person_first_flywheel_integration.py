import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

FLYWHEEL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FLYWHEEL_DIR))
SPEC = importlib.util.spec_from_file_location(
    "jason_existing_flywheel", FLYWHEEL_DIR / "recursive_learning_flywheel_v0_1.py"
)
flywheel = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(flywheel)


class PersonFirstFlywheelIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.baseline = self.root / "snapshot.json"
        self.baseline.write_text(json.dumps({
            "observed_at": "2026-09-23T00:00:00Z",
            "public_repo_count": 0, "repos": [],
        }), encoding="utf-8")
        self.outdir = self.root / "out"

    def replay(self, env):
        with (mock.patch.object(flywheel, "BASELINE", self.baseline),
              mock.patch.object(flywheel, "OUTDIR", self.outdir),
              mock.patch.object(flywheel, "list_public_repos", return_value=[]),
              mock.patch.dict(os.environ, env, clear=True)):
            flywheel.main()
        return json.loads((self.outdir / "flywheel-report.json").read_text(encoding="utf-8"))

    def test_unconfigured_sources_do_not_freeze_independent_public_replay(self):
        result = self.replay({})
        pf = result["person_first_sources"]
        self.assertEqual(pf["scope"], "NO_LOCAL_ORIGINALS_CONFIGURED")
        self.assertEqual(pf["original_history_completeness"], "UNKNOWN")
        self.assertEqual(pf["source_states"]["EVIDENCE_UNAVAILABLE"], 2)
        self.assertTrue(pf["independent_supported_work_continues"])
        self.assertEqual(result["live"]["delta_count"], 0)
        self.assertFalse((self.outdir / "private/person-first-recovery.json").exists())

    def test_configured_private_partial_replay_is_scoped(self):
        root = self.root / "private-source-root"
        root.mkdir()
        (root / "voice.txt").write_text("Synthetic test transcript, not actual Jason voice", encoding="utf-8")
        manifest = {
            "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1",
            "denominator": "JASON",
            "expected": [
                {"id": "private-voice-001", "kind": "voice"},
                {"id": "private-chat-002", "kind": "chat"},
            ],
            "index": [
                {"id": "private-voice-001",
                 "candidates": [{"path": "voice.txt", "format": "text"}]},
                {"id": "private-chat-002",
                 "candidates": [{"path": "missing.json", "format": "json"}]},
            ],
        }
        name = self.root / "manifest.json"
        name.write_text(json.dumps(manifest), encoding="utf-8")
        report = self.replay({
            "JASON_SOURCE_MANIFEST": str(name),
            "JASON_SOURCE_ROOT": str(root),
        })
        pf = report["person_first_sources"]
        self.assertEqual(pf["source_states"]["PRESENT_PARSED"], 1)
        self.assertEqual(pf["source_states"]["MISSING_SOURCE_FILE"], 1)
        self.assertEqual(pf["original_history_completeness"], "UNKNOWN")
        self.assertNotIn("private-voice-001", json.dumps(report))
        self.assertNotIn("private-chat-002", json.dumps(report))
        self.assertNotIn("Synthetic test transcript", json.dumps(report))
        private = json.loads((self.outdir / "private/person-first-recovery.json").read_text())
        voice, chat = private["records"]
        self.assertEqual(voice["source_state"], "PRESENT_PARSED")
        self.assertEqual(chat["recovery_action"], "LOCATE_OR_RESTORE_ORIGINAL_CHAT")
        self.assertEqual(voice["claim_verdict"], "UNKNOWN")

    def test_bad_private_manifest_does_not_freeze_public_observation(self):
        name = self.root / "malformed.json"
        name.write_text("{not-json", encoding="utf-8")
        report = self.replay({"JASON_SOURCE_MANIFEST": str(name)})
        self.assertEqual(report["person_first_sources"]["scope"], "LOCAL_INPUT_ERROR")
        self.assertEqual(report["person_first_sources"]["recovery_action"],
                         "REPAIR_PRIVATE_SOURCE_MANIFEST")
        self.assertTrue(report["person_first_sources"]["independent_supported_work_continues"])
        self.assertEqual(report["live"]["public_repo_count"], 0)
        self.assertNotIn(str(name), json.dumps(report))


if __name__ == "__main__":
    unittest.main()
