import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate import validate, check_source_receipts, check_fiscal, check_labels, check_lineage, safe_margin_test


DATA = Path(__file__).with_name("NY_REFERENCE.json")
NY = json.loads(DATA.read_text(encoding="utf-8"))


class GovernorConformanceTests(unittest.TestCase):
    def test_ny_reconciliation_passes_but_release_closed(self):
        result = validate(NY)
        self.assertEqual(result["gates"]["G1"], "UNKNOWN")
        self.assertEqual(result["detail"]["math"]["arithmetic_only_status"], "PASS")
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

    def test_safe_margin_geometry_and_painted_content(self):
        try:
            import fitz
        except ImportError:
            self.skipTest("fitz unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "safe.pdf"
            doc = fitz.open()
            pg = doc.new_page(width=NY["page_geometry"]["width_pt"],
                              height=NY["page_geometry"]["height_pt"])
            pg.insert_text((65, 65), "Text inside A4 safety box")
            doc.save(str(path))
            doc.close()
            self.assertEqual(safe_margin_test(path, 15)[0], "PASS")
            doc = fitz.open()
            pg = doc.new_page(width=NY["page_geometry"]["width_pt"],
                              height=NY["page_geometry"]["height_pt"])
            pg.insert_text((65, 65), "Text inside A4 safety box")
            pg.draw_rect(fitz.Rect(0, 0, 200, 12), color=(0, 0, 0), fill=(0, 0, 0))
            doc.save(str(path), incremental=False)
            doc.close()
            self.assertEqual(safe_margin_test(path, 15)[0], "FAIL")

    def test_hashed_synthetic_pdf_fiscal_lineage(self):
        import hashlib
        try:
            import fitz
        except ImportError:
            self.skipTest("fitz unavailable")
        labels = (
            ("revenues", "Total revenues 283957"),
            ("expenses", "Total expenses 266785"),
            ("balance_before_transfers", "Balance before transfers 17172"),
            ("net_transfers", "Net transfers -5107"),
            ("change_in_net_position", "Change in net position 12065"),
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = root / "synthetic.pdf"
            d = fitz.open()
            p = d.new_page(width=595.2756, height=841.8898)
            for i, (_, text) in enumerate(labels):
                p.insert_text((60, 70 + 22 * i), text)
            d.save(str(original))
            d.close()
            digest = hashlib.sha256(original.read_bytes()).hexdigest()
            raw = root / "sha256" / digest
            raw.parent.mkdir()
            raw.write_bytes(original.read_bytes())
            packet = copy.deepcopy(NY)
            packet["sources"] = [{
                "source_id": "NY_ACFR_FY2025", "url": "https://example.test/synthetic.pdf",
                "observed_at": "2026-11-14T10:00:00Z", "sha256": digest,
                "byte_count": len(raw.read_bytes()), "cas_path": "sha256/" + digest
            }]
            packet["reconciliation"]["source_sha256"] = digest
            packet["reconciliation"]["line_receipts"] = {
                key: {"page_index": 0, "excerpt": text} for key, text in labels
            }
            self.assertEqual(check_source_receipts(packet, root)[0], "PASS")
            self.assertEqual(check_lineage(packet, root)[0], "PASS")
            result = validate(packet, source_root=root)
            self.assertEqual(result["gates"]["G1"], "PASS")
            self.assertEqual(result["release"], "CLOSED")
            packet["reconciliation"]["line_receipts"]["revenues"]["excerpt"] = "Wrong line 283957"
            self.assertEqual(check_lineage(packet, root)[0], "FAIL")

    def test_new_york_primary_government_is_distinct_scope(self):
        packet = json.loads((DATA.parent / "NY_FY2025_SCOPE_ROLLUP_REFERENCE.json").read_text(encoding="utf-8"))
        scopes = packet["scope_rows"]
        gov = scopes["governmental_activities"]
        business = scopes["business_type"]
        primary = scopes["primary_government"]
        for group in (gov, business, primary):
            self.assertEqual(group["revenues"] - group["expenses"], group["before_transfers"])
            self.assertEqual(group["before_transfers"] + group["transfers"], group["change_in_net_position"])
        for field in ("revenues", "expenses", "before_transfers", "transfers", "change_in_net_position"):
            self.assertEqual(gov[field] + business[field], primary[field], field)
        self.assertEqual(primary["change_in_net_position"], 15435)
        self.assertEqual(packet["source_original_sha256"], None)
        self.assertEqual(packet["validation"]["byte_bound_reconciliation"], "UNKNOWN")
        self.assertEqual(packet["validation"]["state_coverage"]["structural_reference"], 1)
        self.assertEqual(packet["release"], "CLOSED")

    def test_sc_reference_arithmetic_only_in_ci(self):
        from validate import check_fiscal, check_labels
        sc = json.loads((DATA.parent / "SC_FY2025_REFERENCE.json").read_text(encoding="utf-8"))
        self.assertEqual(sc["reconciliation"]["unit"], "USD_thousands")
        self.assertEqual(check_fiscal(sc)[0], "PASS")
        self.assertEqual(check_labels(sc)[0], "PASS")
        result = validate(sc)
        self.assertEqual(result["gates"]["G0"], "UNKNOWN")
        self.assertEqual(result["gates"]["G1"], "UNKNOWN")
        self.assertEqual(result["release"], "CLOSED")

    def test_sc_three_scope_rollup_reported_values(self):
        row = json.loads((DATA.parent / "SC_FY2025_SCOPE_ROLLUP.json").read_text(encoding="utf-8"))
        vals = row["scope_values_usd_thousands"]
        gov = vals["governmental_activities"]
        bus = vals["business_type"]
        primary = vals["primary_government"]
        for scope in (gov, bus, primary):
            self.assertEqual(scope["revenues"] - scope["expenses"], scope["before_transfers"])
            self.assertEqual(scope["before_transfers"] + scope["net_transfers"], scope["change_in_net_position"])
        for key in gov:
            self.assertEqual(gov[key] + bus[key], primary[key])
        self.assertEqual(row["verified_sha256_issuer_authenticity"], "UNKNOWN")

    def test_a4_exact_conversion(self):
        p = NY["page_geometry"]
        self.assertAlmostEqual(p["width_pt"], 595.27559055, places=6)
        self.assertAlmostEqual(p["height_pt"], 841.88976378, places=6)


if __name__ == "__main__":
    unittest.main()
