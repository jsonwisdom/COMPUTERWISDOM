"""Pure-function tests for metadata replay. SYNTHETIC fixtures, not historical proof."""
import importlib.util
import pathlib
import tempfile
import unittest
import json

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("quadonion", ROOT / "tools/quadonion/event_proof_rotation.py")
quadonion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quadonion)

def event(n=1, kind="SOURCE_RECEIPT_ADDED", hash_text=None):
    return {"event_id": f"synthetic_{n:04d}", "kind": kind,
            "receipt_ref": f"FIXTURE_ONLY_{n}", "receipt_sha256": hash_text or ("f" * 64)}

def case(events=None, sources=None, topic="women_public_accountability"):
    return {"case_id": "SYNTHETIC_WOMEN_RECORDS_001",
            "topic": topic, "exact_claim": "Test fixture; no statement about any person.",
            "sources": [] if sources is None else sources,
            "events": [] if events is None else events, "fixture_only": True}

class QuadOnionEventTests(unittest.TestCase):
    def test_no_event_no_cycle_or_art(self):
        o = quadonion.evaluate(case())
        self.assertEqual(o["processed_unique_event_count"], 0)
        self.assertEqual(o["event_rotations"], [])
        self.assertEqual(o["case_state"], "HOLD")

    def test_rotation_has_no_identity_or_authority_promotion(self):
        o = quadonion.evaluate(case([event(i) for i in range(1, 6)]))
        self.assertEqual([r["lead_reviewer"] for r in o["event_rotations"]],
                         ["Leanne", "LeahPrime", "BoxDee", "Supreme Seymour", "Leanne"])
        self.assertTrue(all(not r["bot_dispatched"] for r in o["event_rotations"]))
        self.assertFalse(o["authority_created"])
        self.assertFalse(o["publication_enabled"])
        self.assertFalse(o["joy_deployment_enabled"])

    def test_exact_retransmit_idempotent(self):
        e = event()
        o = quadonion.evaluate(case([e, dict(e)]))
        self.assertEqual(o["processed_unique_event_count"], 1)
        self.assertEqual(o["duplicate_event_count"], 1)
        self.assertEqual(o["errors"], [])

    def test_changed_receipt_same_id_conflict(self):
        e = event()
        changed = dict(e, receipt_sha256="a" * 64)
        o = quadonion.evaluate(case([e, changed]))
        self.assertTrue(any("CONFLICT" in x for x in o["errors"]))
        self.assertEqual(o["case_state"], "HOLD")

    def test_proxy_count_not_independence(self):
        sources = [
            {"url": f"https://example.invalid/proxy/{i}",
             "declared_origin_id": "one_test_origin", "witness_independent": True}
            for i in range(3)
        ]
        c = quadonion.classify_sources(sources)
        self.assertEqual(c["observation_count"], 3)
        self.assertEqual(c["declared_origin_count"], 1)
        self.assertEqual(c["independent_witness_count_verified"], 0)
        self.assertTrue(c["flags"])

    def test_equal_count_does_not_establish_independence(self):
        c = quadonion.classify_sources([{"declared_origin_id": "one"}])
        self.assertEqual(c["observation_count"], c["declared_origin_count"])
        self.assertEqual(c["independent_witness_count_verified"], 0)

    def test_questions_are_not_triggers(self):
        o = quadonion.evaluate(case([event(1, "QUESTION_GENERATED")]))
        self.assertTrue(o["errors"])
        self.assertEqual(o["processed_unique_event_count"], 0)

    def test_art_is_only_numbered_candidates(self):
        o = quadonion.evaluate(case([event(1),event(2)]))
        ids = [a["draft_id"] for r in o["event_rotations"] for a in r["art_candidates"]]
        self.assertEqual(len(ids), 6)
        self.assertEqual(len(set(ids)), 6)
        self.assertTrue(all(a["aspect_ratio"] == "3:4" and
                            a["triggerdeck_id"] is None and
                            a["editorial_state"] == "HOLD" and
                            not a["pixel_art_generated"] and
                            not a["release_authorized"]
                            for r in o["event_rotations"] for a in r["art_candidates"]))

    def test_source_hash_is_not_historical_truth(self):
        o = quadonion.evaluate(case([event(1)]))
        self.assertFalse(o["verification_boundaries"]["source_content_verified"])
        self.assertFalse(o["verification_boundaries"]["historical_truth_established"])
        self.assertFalse(o["event_rotations"][0]["receipt_bytes_fetched_or_verified"])

    def test_oversize_event_list_holds(self):
        o = quadonion.evaluate(case([event(i) for i in range(300)]))
        self.assertEqual(o["processed_unique_event_count"], 0)
        self.assertTrue(o["errors"])

    def test_no_private_fact_inference_or_review_authority(self):
        o = quadonion.evaluate(case([event(1)]))
        self.assertEqual(o["final_release_authority"], "Jason")
        self.assertFalse(o["verification_boundaries"]["family_consents_obtained"])
        self.assertFalse(o["verification_boundaries"]["actual_marydeebot_dispatched"])

    def test_input_digest_determinism(self):
        c = case([event(1)])
        self.assertEqual(quadonion.evaluate(c)["input_digest"],quadonion.evaluate(c)["input_digest"])

if __name__ == "__main__":
    unittest.main()
