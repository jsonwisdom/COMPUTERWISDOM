import importlib.util
import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
SPEC = importlib.util.spec_from_file_location("jason_os_candidate_pipeline", BASE / "jason_os_candidate_pipeline_v0_1.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def sample():
    return {
        "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1",
        "denominator": "JASON",
        "expected": [
            {"id": "voice-001", "kind": "voice"},
            {"id": "chat-002", "kind": "chat"},
        ],
        "index": [
            {"id": "voice-001", "candidates": [{"path": "voice/transcript.txt", "format": "text"}]},
            {"id": "chat-002", "candidates": [{"path": "chats/original.json", "format": "json"}]},
        ],
    }


class JASONOSCandidateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def write(self, filename, data: bytes):
        target = self.root / filename
        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_bytes(data)

    def one(self, report, sid):
        return next(o for o in report["ceo"]["observations"] if o["source_id"] == sid)

    def test_voice_is_candidate_even_when_transcript_parsed(self):
        self.write("voice/transcript.txt", b"Synthetic voice words")
        p = mod.compile_private_candidates(sample(), self.root)
        o = self.one(p, "voice-001")
        self.assertEqual(o["source_state"], "PRESENT_PARSED")
        self.assertEqual(o["candidate_stage"], "EXTRACTED_CANDIDATES_ONLY")
        self.assertEqual(o["source_sha256"], hashlib.sha256(b"Synthetic voice words").hexdigest())
        self.assertEqual(o["audio_original_link"], "AUDIO_INDEX_REFERENCE_MISSING")
        self.assertEqual(o["recovery_action"], "REPAIR_AUDIO_REFERENCE")
        self.assertEqual(o["evidence_verdict"], "UNKNOWN")
        self.assertFalse(o["event_time_verified"])
        self.assertTrue(all(o[k] is None for k in ("observation_time", "generation_time", "delivery_time", "operator_acknowledgment_time")))

    def test_voice_link_to_original_audio_bytes_not_identity(self):
        m = sample()
        m["expected"][0]["audio_original_path"] = "voice/clip.wav"
        self.write("voice/transcript.txt", b"Sample transcript")
        self.write("voice/clip.wav", b"not a real audio sample")
        p = mod.compile_private_candidates(m, self.root)
        o = self.one(p, "voice-001")
        self.assertEqual(o["audio_original_link"], "BYTES_OBSERVED_NOT_AUTHENTICATED")
        self.assertEqual(o["audio_original_sha256"], hashlib.sha256(b"not a real audio sample").hexdigest())
        self.assertTrue(any(e["type"] == "DECLARED_TRANSCRIPT_OF" and e["relation_verdict"] == "UNKNOWN" for e in p["graph"]["edges"]))
        self.assertEqual(p["verified_claim_count"], 0)

    def test_chat_original_bytes_link_to_extracted_candidate(self):
        raw = b'{"messages":[{"text":"first synthetic"},{"content":"second synthetic"}]}'
        self.write("chats/original.json", raw)
        p = mod.compile_private_candidates(sample(), self.root)
        o = self.one(p, "chat-002")
        self.assertEqual(o["source_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(o["candidates"]), 2)
        self.assertEqual(o["candidates"][0]["ordinal"], 0)
        self.assertEqual(o["candidates"][1]["ordinal"], 1)
        self.assertTrue(any(e["from"] == "candidate:chat-002:0" and e["to"] == "source:chat-002" for e in p["graph"]["edges"]))
        self.assertEqual(o["source_authenticity"], "UNKNOWN")

    def test_original_live_format_fixture_shape(self):
        self.write("chats/original.json", b'[{"chat":{"messages":[{"text":"replay"}]}}]')
        p = mod.compile_private_candidates(sample(), self.root)
        self.assertEqual(self.one(p, "chat-002")["candidates"][0]["candidate_text"], "replay")

    def test_missing_source_has_specific_query_recovery_action(self):
        p = mod.compile_private_candidates(sample(), self.root)
        q = mod.query_private_pipeline(p, "chat-002")
        self.assertEqual(q["source_state"], "MISSING_SOURCE_FILE")
        self.assertEqual(q["recovery_action"], "LOCATE_OR_RESTORE_ORIGINAL_CHAT")
        self.assertEqual(q["claim_verdict"], "UNKNOWN")

    def test_missing_manifest_index_is_not_missing_file(self):
        m = sample()
        m["index"].pop()
        p = mod.compile_private_candidates(m, self.root)
        q = mod.query_private_pipeline(p, "chat-002")
        self.assertEqual(q["source_state"], "MISSING_INDEX_REFERENCE")
        self.assertEqual(q["recovery_action"], "REPAIR_CHAT_INDEX")

    def test_parse_failure_does_not_become_missing(self):
        self.write("chats/original.json", b"not-json")
        p = mod.compile_private_candidates(sample(), self.root)
        self.assertEqual(self.one(p, "chat-002")["source_state"], "PRESENT_UNREADABLE")
        self.assertEqual(mod.query_private_pipeline(p, "chat-002")["claim_verdict"], "UNKNOWN")

    def test_duplicate_candidate_keeps_conflict(self):
        m = sample()
        m["index"][1]["candidates"].append({"path": "chats/other.json", "format": "json"})
        p = mod.compile_private_candidates(m, self.root)
        q = mod.query_private_pipeline(p, "chat-002")
        self.assertEqual(q["source_state"], "AMBIGUOUS_DUPLICATE_CONFLICT")
        self.assertEqual(p["fold"]["rows"][1]["fold_state"], "CONFLICT")

    def test_one_missing_voice_does_not_suppress_chat(self):
        self.write("chats/original.json", b'{"messages":[{"text":"supported"}]}')
        p = mod.compile_private_candidates(sample(), self.root)
        self.assertEqual(self.one(p, "voice-001")["source_state"], "MISSING_SOURCE_FILE")
        self.assertEqual(self.one(p, "chat-002")["source_state"], "PRESENT_PARSED")
        self.assertEqual(p["fold"]["rows"][1]["candidate_count"], 1)
        self.assertEqual(p["history_complete"], "UNKNOWN")

    def test_no_verified_claims_even_if_both_sources_parsed(self):
        self.write("voice/transcript.txt", b"Synthetic voice words")
        self.write("chats/original.json", b'{"messages":[{"text":"synthetic"}]}')
        p = mod.compile_private_candidates(sample(), self.root)
        self.assertEqual(p["verified_claim_count"], 0)
        self.assertTrue(all(r["claim_verdict"] == "UNKNOWN" and not r["reconstruction_complete"] for r in p["fold"]["rows"]))
        self.assertTrue(all(r["claim_verdict"] == "UNKNOWN" for r in p["query"]["rows"]))

    def test_unsupported_chat_schema_cannot_fake_extraction(self):
        self.write("chats/original.json", b'{"unexpected":"metadata only"}')
        p = mod.compile_private_candidates(sample(), self.root)
        o = self.one(p, "chat-002")
        self.assertEqual(o["source_state"], "PRESENT_PARSED")
        self.assertEqual(o["candidate_stage"], "UNSUPPORTED_CHAT_MESSAGE_LAYOUT")
        self.assertEqual(o["candidates"], [])
        self.assertEqual(o["recovery_action"], "IMPLEMENT_EXPLICIT_CHAT_LAYOUT_EXTRACTOR")

    def test_public_summary_excludes_secret_text_and_metadata(self):
        self.write("voice/transcript.txt", b"PRIVACY_MARKER_SECRET_SENTENCE")
        self.write("chats/original.json", b'{"messages":[{"text":"PRIVATE_CHAT_MARKER"}]}')
        p = mod.compile_private_candidates(sample(), self.root)
        s = json.dumps(mod.safe_public_pipeline_summary(p))
        for private in ("PRIVACY_MARKER", "PRIVATE_CHAT_MARKER", "voice-001", "chat-002", "source_sha256", "candidate_text", str(self.root)):
            self.assertNotIn(private, s)
        self.assertEqual(mod.safe_public_pipeline_summary(p)["history_complete"], "UNKNOWN")

    def test_deterministic_replay_same_sources(self):
        self.write("chats/original.json", b'{"messages":[{"text":"synthetic"}]}')
        self.assertEqual(mod.compile_private_candidates(sample(), self.root), mod.compile_private_candidates(sample(), self.root))

    def test_undeclared_query_cannot_invent_a_source(self):
        p = mod.compile_private_candidates(sample(), self.root)
        q = mod.query_private_pipeline(p, "not-enumerated")
        self.assertEqual(q["source_state"], "NOT_ENUMERATED")
        self.assertEqual(q["claim_verdict"], "UNKNOWN")

    def test_manifest_path_traversal_fails_closed(self):
        m = sample()
        m["index"][1]["candidates"][0]["path"] = "../outside.json"
        with self.assertRaises(ValueError):
            mod.compile_private_candidates(m, self.root)

    def test_unavailable_source_root_keeps_partial_state(self):
        p = mod.compile_private_candidates(sample(), None)
        self.assertTrue(all(r["source_state"] == "EVIDENCE_UNAVAILABLE" for r in p["query"]["rows"]))
        self.assertEqual(p["history_complete"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
