import importlib.util
import json
import pathlib
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("jason_hold_tally", BASE / "scripts/jason_hold_tally.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class HoldTallyTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((BASE / "audit/JASON_HOLD_EVIDENCE_SAMPLE_V0_1.json").read_text())

    def test_bounded_tally_and_no_global_claim(self):
        out = mod.audit(self.data)
        n = len(self.data["cases"])
        self.assertEqual(n, 14)
        self.assertEqual(out["denominator"]["observed_cases"], n)
        self.assertEqual(out["denominator"]["total_estate_cases"], "UNKNOWN")
        self.assertEqual(sum(out["reason_counts"].values()), n)
        self.assertEqual(sum(out["declared_evidence_verdict_counts"].values()), n)
        self.assertEqual(sum(out["observed_source_gate_counts"].values()), n)

    def test_hold_not_a_verdict(self):
        self.data["cases"][0]["evidence_verdict"] = "HOLD"
        with self.assertRaises(ValueError):
            mod.audit(self.data)

    def test_duplicate_case_fails_closed(self):
        self.data["cases"].append(dict(self.data["cases"][0]))
        with self.assertRaises(ValueError):
            mod.audit(self.data)

    def test_missing_provenance_fails_closed(self):
        self.data["cases"][0]["source_locator"] = ""
        with self.assertRaises(ValueError):
            mod.audit(self.data)

    def test_no_fictional_complete_denominator(self):
        self.data["denominator"]["coverage"] = "ESTATE_WIDE"
        with self.assertRaises(ValueError):
            mod.audit(self.data)

    def test_source_gate_label_never_rewritten(self):
        out = mod.audit(self.data)
        self.assertEqual(out["observed_source_gate_counts"]["HOLD"], 3)
        self.assertEqual(out["observed_source_gate_counts"]["BLOCKED"], 4)

    def test_missing_status_rejected(self):
        del self.data["cases"][0]["source_gate"]
        with self.assertRaises(ValueError):
            mod.audit(self.data)

    def test_legitimate_protective_hold_kept(self):
        out = mod.audit(self.data)
        p = next(c for c in self.data["cases"] if c["protective_gate"])
        self.assertNotIn(p["id"], out["unfixed"])


if __name__ == "__main__":
    unittest.main()
