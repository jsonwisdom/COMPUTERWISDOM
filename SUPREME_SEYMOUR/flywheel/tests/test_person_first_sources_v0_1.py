import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "person_first_sources_v0_1.py"
SPEC = importlib.util.spec_from_file_location("person_first_sources", SOURCE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def specimen():
    return {
        "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1",
        "denominator": "JASON",
        "expected": [
            {"id": "v001", "kind": "voice"},
            {"id": "c001", "kind": "chat"},
        ],
        "index": [
            {"id": "v001", "candidates": [{"path": "voice/001.txt", "format": "text"}]},
            {"id": "c001", "candidates": [{"path": "chat/001.json", "format": "json"}]},
        ],
    }


class PersonFirstSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, data):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def state(self, result, key):
        return next(x for x in result["records"] if x["id"] == key)

    def test_missing_voice_has_specific_action(self):
        m = specimen()
        self.write("chat/001.json", b'{"messages":[{"text":"synthetic"}]}')
        r = mod.evaluate(m, self.root)
        self.assertEqual(self.state(r, "v001")["source_state"], "MISSING_SOURCE_FILE")
        self.assertEqual(self.state(r, "v001")["recovery_action"], "LOCATE_OR_RESTORE_ORIGINAL_VOICE")
        self.assertEqual(self.state(r, "c001")["source_state"], "PRESENT_PARSED")

    def test_missing_chat_has_specific_action(self):
        self.write("voice/001.txt", b"synthetic transcript")
        r = mod.evaluate(specimen(), self.root)
        self.assertEqual(self.state(r, "c001")["source_state"], "MISSING_SOURCE_FILE")
        self.assertEqual(self.state(r, "c001")["recovery_action"], "LOCATE_OR_RESTORE_ORIGINAL_CHAT")
        self.assertEqual(self.state(r, "v001")["source_state"], "PRESENT_PARSED")

    def test_parse_failure_is_not_missing(self):
        self.write("voice/001.txt", b"\xff\xfe")
        self.write("chat/001.json", b"{invalid json")
        r = mod.evaluate(specimen(), self.root)
        self.assertTrue(all(x["source_state"] == "PRESENT_UNREADABLE" for x in r["records"]))
        self.assertTrue(all(x["recovery_action"].startswith(("REPARSE", "RETRANSCRIBE")) for x in r["records"]))

    def test_missing_manifest_index_is_not_missing_evidence(self):
        m = specimen()
        m["index"] = [m["index"][1]]
        r = mod.evaluate(m, self.root)
        self.assertEqual(self.state(r, "v001")["source_state"], "MISSING_INDEX_REFERENCE")
        self.assertEqual(self.state(r, "v001")["recovery_action"], "REPAIR_VOICE_INDEX")

    def test_ambiguous_duplicate_is_scoped(self):
        m = specimen()
        m["index"][0]["candidates"].append({"path": "voice/other.txt", "format": "text"})
        self.write("chat/001.json", b'{"messages": ["synthetic"]}')
        r = mod.evaluate(m, self.root)
        self.assertEqual(self.state(r, "v001")["source_state"], "AMBIGUOUS_DUPLICATE_CONFLICT")
        self.assertEqual(self.state(r, "c001")["source_state"], "PRESENT_PARSED")

    def test_partial_evidence_does_not_claim_reconstruction_complete(self):
        self.write("chat/001.json", b'{"messages": ["synthetic"]}')
        r = mod.evaluate(specimen(), self.root)
        self.assertEqual(r["candidate_parsed_count"], 1)
        self.assertEqual(r["original_history_completeness"], "UNKNOWN")
        self.assertTrue(r["independent_supported_work_continues"])
        self.assertFalse(self.state(r, "c001")["dependent_path_hold"])
        self.assertTrue(self.state(r, "v001")["dependent_path_hold"])
        self.assertEqual(self.state(r, "c001")["claim_verdict"], "UNKNOWN")

    def test_deterministic_replay(self):
        self.write("chat/001.json", b'{"messages": ["synthetic"]}')
        self.assertEqual(mod.evaluate(specimen(), self.root), mod.evaluate(specimen(), self.root))

    def test_private_data_not_in_public_summary(self):
        self.write("voice/001.txt", b"private test words do not publish")
        self.write("chat/001.json", b'{"secret": "synthetic-private"}')
        r = mod.evaluate(specimen(), self.root)
        s = json.dumps(mod.safe_public_summary(r))
        self.assertNotIn("private", s)
        self.assertNotIn("v001", s)
        self.assertNotIn("c001", s)
        self.assertNotIn("synthetic", s)
        self.assertNotIn("sha256", s)
        self.assertNotIn(str(self.root), s)

    def test_audio_bytes_require_transcription(self):
        m = specimen()
        m["index"][0]["candidates"] = [{"path": "voice/clip.wav", "format": "audio"}]
        self.write("voice/clip.wav", b"not-verified-audio")
        r = mod.evaluate(m, self.root)
        self.assertEqual(self.state(r, "v001")["source_state"], "PRESENT_UNREADABLE")
        self.assertEqual(self.state(r, "v001")["recovery_action"], "TRANSCRIBE_VOICE_AUDIO")

    def test_confined_paths(self):
        m = specimen()
        m["index"][0]["candidates"] = [{"path": "../private.txt", "format": "text"}]
        with self.assertRaises(mod.ManifestError):
            mod.evaluate(m, self.root)

    def test_missing_root_is_unavailable_not_absent(self):
        r = mod.evaluate(specimen(), None)
        self.assertEqual(r["source_states"]["EVIDENCE_UNAVAILABLE"], 2)
        self.assertEqual(r["source_states"]["MISSING_SOURCE_FILE"], 0)

    def test_duplicate_ids_fail_closed(self):
        m = specimen()
        m["expected"][1]["id"] = "v001"
        with self.assertRaises(mod.ManifestError):
            mod.evaluate(m, self.root)

    def test_unconfigured_never_promotes_history(self):
        r = mod.not_configured_summary()
        self.assertEqual(r["original_history_completeness"], "UNKNOWN")
        self.assertEqual(r["source_states"]["EVIDENCE_UNAVAILABLE"], 2)
        self.assertTrue(r["independent_supported_work_continues"])


if __name__ == "__main__":
    unittest.main()
