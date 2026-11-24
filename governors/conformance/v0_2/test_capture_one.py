import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from capture_one import record_bytes, verify_one, assert_safe_url

class AcquisitionTests(unittest.TestCase):
    def test_allowlist_blocks_nonpublisher(self):
        assert_safe_url("https://accountingfiles.delaware.gov/docs/2025acfr.pdf",{"accountingfiles.delaware.gov"})
        with self.assertRaises(ValueError):
            assert_safe_url("http://accountingfiles.delaware.gov/docs/2025acfr.pdf",{"accountingfiles.delaware.gov"})
        with self.assertRaises(ValueError):
            assert_safe_url("https://fake.delaware.gov/docs/2025acfr.pdf",{"accountingfiles.delaware.gov"})

    def test_synthetic_pdf_receipt_is_not_government_authentication(self):
        raw = b"%PDF-1.7\nsynthetic fixture only\n%%EOF\n"
        expected = hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as folder:
            receipt = record_bytes(io.BytesIO(raw),Path(folder),"TEST",
                "https://example.test","https://example.test/source.pdf",
                "SYNTHETIC","2026-11-14T00:00:00Z","unit_test_bytes")
            self.assertEqual(receipt["sha256"],expected)
            self.assertEqual(receipt["cas_readback"],"PASS")
            self.assertEqual(receipt["issuer_authenticity"],"UNKNOWN")
            self.assertEqual(receipt["reconciliation_source_binding"],"UNKNOWN")
            path = Path(folder) / "test-receipt.json"
            path.write_text(json.dumps(receipt))
            self.assertEqual(verify_one(path,folder),0)
            (Path(folder)/receipt["cas_path"]).write_bytes(raw+b"altered")
            with self.assertRaises(ValueError):
                verify_one(path,folder)

    def test_non_pdf_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                record_bytes(io.BytesIO(b"<html>no report</html>"),folder,"TEST","","",
                             "SYNTHETIC","2026-11-14T00:00:00Z","unit_test_bytes")

if __name__=="__main__":
    unittest.main()
