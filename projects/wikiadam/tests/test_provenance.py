import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import provenance as wiki


def fixture(root: Path):
    raw = b"synthetic, reviewed claim source -- not JASON's history"
    path = root / "source.txt"
    path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    return {
        "schema": wiki.SCHEMA,
        "denominator": "JASON",
        "scope": {
            "id": "synthetic-v0.1",
            "snapshot": "2026-11-03T00:00:00Z",
            "policy": wiki.POLICY,
            "candidate_ids": ["CWaaS"],
            "population_completeness": "UNKNOWN",
        },
        "candidates": [],
        "edges": [{
            "id": "e1", "from": "CWaaS", "to": "JASON",
            "type": "authored_by", "verification_state": "REVIEWED",
            "evidence_ids": ["ev1"], "contradictions": [],
        }],
        "evidence": [{
            "id": "ev1", "relative_path": "source.txt",
            "source_locator": "synthetic://reviewed-record-v0",
            "sha256": digest, "review_state": "REVIEWED",
        }],
    }


class WikiAdamProvenanceTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.doc = fixture(self.root)

    def test_direct_authored_only_policy_qualified(self):
        o = wiki.audit(self.doc, self.root)
        self.assertEqual(o["rows"][0]["verdict"], "POLICY_QUALIFIED")
        self.assertEqual(o["rows"][0]["evidence_path_edge_ids"], ["e1"])
        self.assertEqual(o["coverage"], {"numerator": 1, "denominator": 1})
        self.assertEqual(o["historical_completeness"], "UNKNOWN")
        self.assertFalse(o["source_authorship_authenticated_by_hash_alone"])

    def test_discussion_is_not_authorship(self):
        self.doc["edges"][0]["type"] = "discussed_by"
        self.assertEqual(wiki.audit(self.doc, self.root)["rows"][0]["verdict"], "UNKNOWN")
        self.assertEqual(wiki.audit(self.doc, self.root, "DISCUSSED_BY")["rows"][0]["verdict"], "POLICY_QUALIFIED")

    def test_derivation_does_not_promote_to_authorship(self):
        self.doc["edges"][0]["to"] = "EarlierWork"
        self.doc["edges"][0]["type"] = "derived_from"
        self.doc["edges"].append({
            "id": "e2", "from": "EarlierWork", "to": "JASON", "type": "authored_by",
            "verification_state": "REVIEWED", "evidence_ids": ["ev1"], "contradictions": []
        })
        self.assertEqual(wiki.audit(self.doc, self.root)["rows"][0]["verdict"], "UNKNOWN")
        derived = wiki.audit(self.doc, self.root, "DERIVED_FROM_PERSON_WORK")
        self.assertEqual(derived["rows"][0]["verdict"], "POLICY_QUALIFIED")
        self.assertEqual(derived["rows"][0]["evidence_path_edge_ids"], ["e1", "e2"])

    def test_attribution_is_not_authorship(self):
        self.doc["edges"][0]["type"] = "attributed_by"
        self.assertEqual(wiki.audit(self.doc, self.root)["coverage"]["numerator"], 0)

    def test_missing_source_is_unknown_not_false(self):
        (self.root / "source.txt").unlink()
        o = wiki.audit(self.doc, self.root)
        self.assertEqual(o["rows"][0]["verdict"], "UNKNOWN")
        self.assertIn("MISSING_SOURCE_FILE", o["evidence_byte_states"])
        self.assertEqual(o["rows"][0]["recovery_action"], "REPLAY_MISSING_OR_UNREVIEWED_SOURCE")

    def test_hash_conflict_not_promoted(self):
        (self.root / "source.txt").write_text("Different bytes", encoding="utf-8")
        o = wiki.audit(self.doc, self.root)
        self.assertEqual(o["rows"][0]["verdict"], "DISPUTED")
        self.assertEqual(o["coverage"]["numerator"], 0)

    def test_claim_conflict_not_silently_qualified(self):
        self.doc["edges"][0]["contradictions"] = ["dispute-1"]
        o = wiki.audit(self.doc, self.root)
        self.assertEqual(o["rows"][0]["verdict"], "DISPUTED")
        self.assertEqual(o["rows"][0]["evidence_path_edge_ids"], [])

    def test_empty_denominator_undefined(self):
        self.doc["scope"]["candidate_ids"] = []
        o = wiki.audit(self.doc, self.root)
        self.assertIsNone(o["coverage"])
        self.assertTrue(o["coverage_undefined"])
        self.assertEqual(o["candidate_count"], 0)

    def test_dedup_and_no_estate_completeness_from_100pct(self):
        self.doc["scope"]["candidate_ids"] = ["CWaaS", "CWaaS"]
        o = wiki.audit(self.doc, self.root)
        self.assertEqual(o["candidate_count"], 1)
        self.assertEqual(o["policy_qualified_count"], 1)
        self.assertEqual(o["historical_completeness"], "UNKNOWN")

    def test_missing_record_does_not_suppress_related_qualified_work(self):
        self.doc["scope"]["candidate_ids"].append("UnrelatedProject")
        self.doc["edges"].append({
            "id": "e2", "from": "UnrelatedProject", "to": "JASON",
            "type": "authored_by", "verification_state": "CLAIMED",
            "evidence_ids": ["missing"], "contradictions": []
        })
        o = wiki.audit(self.doc, self.root)
        self.assertEqual([r["verdict"] for r in o["rows"]], ["POLICY_QUALIFIED", "UNKNOWN"])
        self.assertEqual(o["coverage"], {"numerator": 1, "denominator": 2})

    def test_without_evidence_root_no_semantic_promotion(self):
        o = wiki.audit(self.doc, None)
        self.assertEqual(o["rows"][0]["verdict"], "UNKNOWN")
        self.assertIn("SOURCE_ROOT_UNAVAILABLE", o["evidence_byte_states"])

    def test_unreviewed_label_is_insufficient(self):
        self.doc["evidence"][0]["review_state"] = "UNREVIEWED"
        self.assertEqual(wiki.audit(self.doc, self.root)["rows"][0]["verdict"], "UNKNOWN")

    def test_undeclared_relation_raises(self):
        with self.assertRaises(wiki.AuditInputError):
            wiki.audit(self.doc, self.root, "PERSON_OWNS_EVERYTHING")

    def test_path_traversal_is_not_evidence(self):
        self.doc["evidence"][0]["relative_path"] = "../outside.txt"
        o = wiki.audit(self.doc, self.root)
        self.assertEqual(o["rows"][0]["verdict"], "UNKNOWN")
        self.assertIn("PATH_ESCAPE", o["evidence_byte_states"])

    def test_public_summary_has_no_private_evidence(self):
        o = wiki.audit(self.doc, self.root)
        s = json.dumps(wiki.public_summary(o))
        for secret in ("CWaaS", "source.txt", "synthetic://", "source_locator", "sha256"):
            self.assertNotIn(secret, s)
        self.assertEqual(wiki.public_summary(o)["historical_completeness"], "UNKNOWN")

    def test_cycle_does_not_invent_origin(self):
        self.doc["edges"][0]["to"] = "LoopA"
        self.doc["edges"][0]["type"] = "derived_from"
        self.doc["edges"].append({
            "id": "e2", "from": "LoopA", "to": "CWaaS", "type": "derived_from",
            "verification_state": "REVIEWED", "evidence_ids": ["ev1"], "contradictions": []
        })
        o = wiki.audit(self.doc, self.root, "DERIVED_FROM_PERSON_WORK")
        self.assertEqual(o["rows"][0]["verdict"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
