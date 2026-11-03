import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
SPEC = importlib.util.spec_from_file_location("canonical_schema_gate", BASE / "canonical_schema_gate_v0_1.py")
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def projection():
    return {
        "denominator": "JASON",
        "ceo": {"class": "CANDIDATE_ONLY_NOT_VALIDATED_CEO", "observations": [
            {"source_id": "private-voice", "source_kind": "voice",
             "source_sha256": "a" * 64, "declared_event_time": None}]},
        "graph": {"class": "EXPLICIT_EDGES_ONLY", "nodes": [], "edges": []},
        "fold": {"class": "UNCERTAINTY_PRESERVING", "rows": []},
        "query": {"class": "SOURCE_STATUS_VISIBLE", "rows": []},
    }


class CanonicalGateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def _bundle(self, alternate=None):
        pinned = {}
        for stage in gate.HISTORICAL_PINS:
            schema = {"$schema": "https://json-schema.org/draft/2020-12/schema",
                      "type": "object",
                      "required": ["class"],
                      "properties": {"class": {"type": "string"}}}
            if alternate and stage in alternate:
                schema = alternate[stage]
            source = json.dumps(schema, sort_keys=True).encode()
            (self.root / gate.LAYER_FILENAMES[stage]).write_bytes(source)
            pinned[stage] = hashlib.sha256(source).hexdigest()
        return pinned

    def test_no_original_bytes_all_unknown(self):
        r = gate.verify_canonical_schema_bundle(projection(), None)
        self.assertEqual(r["canonical_compatibility"], "UNKNOWN")
        self.assertTrue(all(x["schema_gate"] == "UNKNOWN" for x in r["stages"].values()))

    def test_real_historical_hashes_not_replaced_by_synthetic(self):
        self._bundle()
        r = gate.verify_canonical_schema_bundle(projection(), self.root)
        self.assertEqual(r["canonical_compatibility"], "FAIL")
        self.assertTrue(all(x["digest_verdict"] == "FAIL" for x in r["stages"].values()))
        self.assertEqual(r["truth_verdict"], "UNKNOWN")

    def test_synthetic_valid_bundle_only_fixture_pass(self):
        pins = self._bundle()
        r = gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins, test_profile=True)
        self.assertEqual(r["canonical_compatibility"], "FIXTURE_PASS_ONLY")
        self.assertTrue(all(x["schema_gate"] == "PASS" for x in r["stages"].values()))
        self.assertEqual(r["history_complete"], "UNKNOWN")

    def test_synthetic_override_refused_for_real_audit(self):
        pins = self._bundle()
        with self.assertRaises(ValueError):
            gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins)

    def test_valid_hash_with_invalid_instance_is_fail(self):
        schema = {"type": "object", "required": ["not_present"],
                  "properties": {"not_present": {"const": "must_be_there"}}}
        pins = self._bundle({"ceo": schema})
        r = gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins, test_profile=True)
        self.assertEqual(r["stages"]["ceo"]["digest_verdict"], "PASS")
        self.assertEqual(r["stages"]["ceo"]["validation_verdict"], "FAIL")
        self.assertEqual(r["canonical_compatibility"], "FAIL")

    def test_absent_one_canonical_file_keeps_unknown_not_zero(self):
        pins = self._bundle()
        (self.root / "query.schema.json").unlink()
        r = gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins, test_profile=True)
        self.assertEqual(r["canonical_compatibility"], "UNKNOWN")
        self.assertEqual(r["stages"]["query"]["recovery_action"], "LOCATE_ORIGINAL_CANONICAL_SCHEMA")
        self.assertEqual(r["stages"]["ceo"]["schema_gate"], "PASS")

    def test_external_ref_does_not_fetch_network(self):
        pins = self._bundle({"ceo": {"$ref": "https://example.com/private.json"}})
        r = gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins, test_profile=True)
        self.assertEqual(r["canonical_compatibility"], "UNKNOWN")
        self.assertEqual(r["stages"]["ceo"]["recovery_action"], "RESOLVE_EXTERNAL_SCHEMA_REFERENCES_OFFLINE")

    def test_duplicate_json_keys_rejected_even_at_matching_digest(self):
        raw = b'{"type":"object","type":"string"}'
        pins = self._bundle()
        (self.root / "fold.schema.json").write_bytes(raw)
        pins["fold"] = hashlib.sha256(raw).hexdigest()
        r = gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins, test_profile=True)
        self.assertEqual(r["stages"]["fold"]["validation_verdict"], "FAIL")
        self.assertEqual(r["canonical_compatibility"], "FAIL")

    def test_missing_one_stage_rejects_false_pass(self):
        p = projection()
        p.pop("query")
        with self.assertRaises(ValueError):
            gate.verify_canonical_schema_bundle(p, None)

    def test_private_ingestion_receipt_binds_source_without_truth_promotion(self):
        manifest = {
            "denominator": "JASON",
            "expected": [{"id": "private-voice", "kind": "voice",
                          "transcriber_version": "DECLARED_NOT_VERIFIED"}],
            "index": [{"id": "private-voice", "candidates": [
                {"path": "voice/one.txt", "format": "text"}]}],
        }
        r = gate.private_ingestion_receipt(manifest, projection(),
             observed_at_utc="2026-11-03T21:30:00Z")
        item = r["rows"][0]
        self.assertEqual(item["source_sha256"], "a" * 64)
        self.assertEqual(item["private_local_pointer"], "voice/one.txt")
        self.assertEqual(item["ingested_at_utc"], "2026-11-03T21:30:00Z")
        self.assertEqual(item["parser_version"], gate.PARSER_VERSION)
        self.assertFalse(item["transcriber_version_verified"])
        self.assertEqual(item["claim_verdict"], "UNKNOWN")
        self.assertIsNone(item["delivery_time"])

    def test_naive_ingestion_clock_is_rejected(self):
        m = {"denominator": "JASON", "expected": [], "index": []}
        with self.assertRaises(ValueError):
            gate.private_ingestion_receipt(m, projection(), observed_at_utc="2026-11-03T21:30:00")

    def test_wrong_denominator_fails_closed(self):
        m = {"denominator": "NOT_JASON", "expected": [], "index": []}
        with self.assertRaises(ValueError):
            gate.private_ingestion_receipt(m, projection(), observed_at_utc="2026-11-03T21:30:00Z")

    def test_public_output_no_paths_content_or_ids(self):
        pins = self._bundle()
        r = gate.verify_canonical_schema_bundle(projection(), self.root, expected_pins=pins, test_profile=True)
        public = json.dumps(gate.public_gate_summary(r))
        self.assertNotIn(str(self.root), public)
        self.assertNotIn("private-voice", public)
        self.assertNotIn("a" * 64, public)
        self.assertNotIn("voice/one.txt", public)
        self.assertNotIn("PRIVATE_SOURCE_TEXT", public)

    def test_pinned_historical_hashes_are_exactly_declared(self):
        expected = {
            "ceo": "9b43f71d7dd261cf3d7854f36e9c4a86896710d68576b787fc7a80a03746823c",
            "graph": "d05f637f92b04ae2c57cac5308bc9f55a5c4e8f1d80012e48930f1f2c6672e8c",
            "fold": "96db1f57b6413bc9fad4f3c20d46236d1cae0a4d868ee9e20c218cabed10ed6c",
            "query": "093c5601d23805ab9e73e36d201c8181170aabb47f7919a730f9c3091419a0e4",
        }
        self.assertEqual(gate.HISTORICAL_PINS, expected)


if __name__ == "__main__":
    unittest.main()
