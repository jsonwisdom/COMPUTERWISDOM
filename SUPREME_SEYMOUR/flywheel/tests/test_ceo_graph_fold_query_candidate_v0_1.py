import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
spec = importlib.util.spec_from_file_location(
    "jason_provenance", BASE / "ceo_graph_fold_query_candidate_v0_1.py"
)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class JasonProvenanceBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.voice = b"synthetic voice says foo"
        self.chat = b'{"messages":["synthetic chat says bar"]}'
        self.write("voice/001.txt", self.voice)
        self.write("chat/001.json", self.chat)
        self.manifest = {
            "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1",
            "denominator": "JASON",
            "expected": [
                {"id": "v1", "kind": "voice", "topics": ["memory"]},
                {"id": "c1", "kind": "chat", "topics": ["memory", "unrelated"]},
            ],
            "index": [
                {"id": "v1", "candidates": [{
                    "path": "voice/001.txt", "format": "text",
                    "expected_sha256": hashlib.sha256(self.voice).hexdigest(),
                }]},
                {"id": "c1", "candidates": [{
                    "path": "chat/001.json", "format": "json",
                    "expected_sha256": hashlib.sha256(self.chat).hexdigest(),
                }]},
            ],
        }

    def write(self, path, payload):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(payload)

    def claim(self, source_id="v1", topic="memory", interpretation="Claim A"):
        raw = self.voice if source_id == "v1" else self.chat
        return {
            "source_id": source_id, "topic": topic,
            "interpretation": interpretation, "byte_start": 0,
            "byte_end": len(raw), "expected_excerpt": raw.decode("utf-8"),
            "reported_event_time_utc": "2026-09-21T12:00:00Z",
        }

    def test_byte_hash_recomputed_passes(self):
        r = engine.compile_pipeline(self.manifest, self.root, [self.claim()])
        o = r["observations"][0]
        self.assertEqual(o["source_sha256"], hashlib.sha256(self.voice).hexdigest())
        self.assertEqual(o["source_span_sha256"], hashlib.sha256(self.voice).hexdigest())
        self.assertEqual(o["parser_version"], engine.PARSER)
        self.assertEqual(o["claim_verdict"], "UNKNOWN")
        self.assertEqual(o["reported_time_authority"], "DECLARED_UNVERIFIED")

    def test_digest_mismatch_quarantines_only_affected_source(self):
        self.manifest["index"][0]["candidates"][0]["expected_sha256"] = "0" * 64
        r = engine.compile_pipeline(
            self.manifest, self.root,
            [self.claim("v1"), self.claim("c1", "unrelated")])
        self.assertEqual(len(r["observations"]), 1)
        self.assertEqual(r["observations"][0]["source_id"], "c1")
        self.assertEqual(r["scoped_holds"][0]["reason"], "SOURCE_DIGEST_MISMATCH")
        self.assertTrue(r["independent_supported_work_continues"])

    def test_missing_voice_does_not_block_chat(self):
        (self.root / "voice/001.txt").unlink()
        r = engine.compile_pipeline(
            self.manifest, self.root,
            [self.claim("v1"), self.claim("c1", "unrelated")])
        self.assertEqual(len(r["observations"]), 1)
        self.assertEqual(r["scoped_holds"][0]["recovery_action"],
                         "LOCATE_OR_RESTORE_ORIGINAL_VOICE")
        self.assertEqual(r["fold_query"]["unrelated"]["observation_ids"],
                         [r["observations"][0]["observation_id"]])
        self.assertEqual(r["historical_completeness"], "UNKNOWN")

    def test_parsing_failure_distinct_from_missing_bytes(self):
        self.write("chat/001.json", b"{bad json")
        r = engine.compile_pipeline(self.manifest, self.root, [self.claim("c1")])
        self.assertEqual(r["scoped_holds"][0]["reason"], "PRESENT_UNREADABLE")
        self.assertEqual(r["scoped_holds"][0]["recovery_action"], "REPARSE_CHAT")

    def test_missing_index_is_distinct(self):
        self.manifest["index"] = [self.manifest["index"][1]]
        r = engine.compile_pipeline(self.manifest, self.root, [self.claim()])
        self.assertEqual(r["scoped_holds"][0]["reason"], "MISSING_INDEX_REFERENCE")

    def test_bad_excerpt_never_becomes_claim(self):
        p = self.claim()
        p["expected_excerpt"] = "invented quote"
        r = engine.compile_pipeline(self.manifest, self.root, [p])
        self.assertEqual(len(r["observations"]), 0)
        self.assertEqual(r["scoped_holds"][0]["reason"], "SPAN_BYTES_DISAGREE")

    def test_corrupt_byte_range_fails_scoped(self):
        p = self.claim()
        p["byte_end"] = len(self.voice) + 100
        r = engine.compile_pipeline(self.manifest, self.root, [p])
        self.assertEqual(r["scoped_holds"][0]["reason"], "INVALID_BYTE_SPAN")

    def test_duplicate_ingestion_is_idempotent(self):
        r1 = engine.compile_pipeline(self.manifest, self.root, [self.claim()])
        r2 = engine.compile_pipeline(self.manifest, self.root, [self.claim()], previous=r1)
        self.assertEqual(len(r2["observations"]), 1)
        self.assertEqual(r2["new_unique_observations"], 0)
        self.assertEqual(r1["observations"], r2["observations"])

    def test_conflicts_survive_fold_without_truth_promotion(self):
        r = engine.compile_pipeline(
            self.manifest, self.root,
            [self.claim("v1", interpretation="A"),
             self.claim("c1", interpretation="B")])
        m = r["fold_query"]["memory"]
        self.assertEqual(len(m["observation_ids"]), 2)
        self.assertTrue(m["conflict_candidate"])
        self.assertIn("CONFLICTING_INTERPRETATIONS_PRESERVED",
                      [w["warning"] for w in m["warnings"]])
        self.assertEqual(m["claim_verdict"], "UNKNOWN")
        self.assertEqual(len(r["graph_edges"]), 2)

    def test_disappeared_original_retains_prior_without_fake_success(self):
        prior = engine.compile_pipeline(self.manifest, self.root, [self.claim()])
        (self.root / "voice/001.txt").unlink()
        r = engine.compile_pipeline(self.manifest, self.root, [], previous=prior)
        self.assertEqual(r["observations"], prior["observations"])
        warnings = [w["warning"] for w in r["fold_query"]["memory"]["warnings"]]
        self.assertIn("SOURCE_UNAVAILABLE_PRIOR_OBSERVATION_RETAINED", warnings)
        self.assertEqual(r["fold_query"]["memory"]["claim_verdict"], "UNKNOWN")

    def test_bad_private_manifest_fails_without_promotion(self):
        m = copy.deepcopy(self.manifest)
        m["denominator"] = "OTHER"
        with self.assertRaises(engine.ManifestError):
            engine.compile_pipeline(m, self.root, [self.claim()])

    def test_source_path_escape_rejected(self):
        m = copy.deepcopy(self.manifest)
        m["index"][0]["candidates"][0]["path"] = "../outside.txt"
        with self.assertRaises(engine.ManifestError):
            engine.compile_pipeline(m, self.root, [self.claim()])

    def test_public_report_excludes_private_bytes_and_ids(self):
        r = engine.compile_pipeline(self.manifest, self.root, [self.claim()])
        public = json.dumps(engine.safe_public_summary(r))
        for sensitive in ("synthetic voice", "v1", "voice/001.txt",
                          hashlib.sha256(self.voice).hexdigest(), str(self.root)):
            self.assertNotIn(sensitive, public)
        self.assertEqual(r["authority_created"], False)

    def test_deterministic_replay_and_unproven_completion(self):
        p = [self.claim()]
        r1 = engine.compile_pipeline(self.manifest, self.root, p)
        r2 = engine.compile_pipeline(self.manifest, self.root, p)
        self.assertEqual(r1, r2)
        self.assertEqual(r1["historical_completeness"], "UNKNOWN")
        self.assertTrue(r1["private_only"])

    def test_utc_required_and_not_proven_event_time(self):
        p = self.claim()
        p["reported_event_time_utc"] = "2026-09-21T12:00:00"
        with self.assertRaises(engine.ManifestError):
            engine.compile_pipeline(self.manifest, self.root, [p])


if __name__ == "__main__":
    unittest.main()
