import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate import validate, check_source_receipts, check_fiscal, check_labels


DATA = Path(__file__).with_name("NY_REFERENCE.json")
NY = json.loads(DATA.read_text(encoding="utf-8"))


class GovernorConformanceTests(unittest.TestCase):
    def test_ny_reconciliation_passes_but_release_closed(self):
        result = validate(NY)
        self.assertEqual(result["gates"]["G1"], "PASS")
        self.assertEqual(result["gates"]["G2"], "PASS")
        self.assertEqual(result["gates"]["G0"], "UNKNOWN")
        self.assertEqual(result["gates"]["G3"], "UNKNOWN")
        self.assertEqual(result["gates"]["G4"], "UNKNOWN")
        self.assertEqual(result["gates"]["G5"], "UNKNOWN")
        self.assertEqual(result["release"], "CLOSED")

    def test_172_billion_is_not_net_change(self):
        broken = copy.deepcopy(NY)
        broken["reconciliation"]["reported"]["change_in_net_position"] = 17172
        self.assertEqual(check_fiscal(broken)[0], "FAIL")

    def test_mislabeled_before_transfer_fails(self):
        broken = copy.deepcopy(NY)
        before = broken["reconciliation"]["reported"].pop("balance_before_transfers")
        broken["reconciliation"]["reported"]["surplus"] = before
        self.assertEqual(check_labels(broken)[0], "FAIL")

    def test_source_sha256_requires_actual_matching_bytes(self):
        import hashlib
        payload = b"synthetic bytes; not an NY ACFR"
        digest = hashlib.sha256(payload).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "sha256" / digest
            raw.parent.mkdir()
            raw.write_bytes(payload)
            row = copy.deepcopy(NY)
            row["sources"] = [{"source_id": "TEST", "url": "https://example.test/",
                               "observed_at": "2026-11-14T10:00:00Z",
                               "sha256": digest, "byte_count": len(payload),
                               "cas_path": "sha256/" + digest}]
            self.assertEqual(check_source_receipts(row, root)[0], "PASS")
            raw.write_bytes(payload + b"!")
            self.assertEqual(check_source_receipts(row, root)[0], "FAIL")

    def test_unknown_without_payment_samples(self):
        self.assertIsNone(validate(NY)["detail"]["linkage"]["coverage"])

    def test_a4_exact_conversion(self):
        p = NY["page_geometry"]
        self.assertAlmostEqual(p["width_pt"], 595.27559055, places=6)
        self.assertAlmostEqual(p["height_pt"], 841.88976378, places=6)


if __name__ == "__main__":
    unittest.main()
