import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).parents[1] / "grok_output_gate.py"
SPEC = importlib.util.spec_from_file_location("grok_output_gate", MODULE_PATH)
gate_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(gate_module)


class GrokOutputGateTests(unittest.TestCase):
    def test_missing_receipt_holds_review_without_blocking_build(self):
        output = gate_module.gate({
            "REVIEW_FINDINGS": [{"code": "MISSING_GATE"}],
            "NONBINDING_RECOMMENDATION": "Add the receipt.",
            "FINAL_VERDICT": "PASS",
        })
        self.assertEqual(output["status"], "HOLD_REVIEW_ONLY")
        self.assertFalse(output["build_blocking"])
        self.assertEqual(output["review_findings"], [{"code": "MISSING_GATE"}])
        self.assertNotIn("FINAL_VERDICT", output)
        self.assertEqual(output["removed_fields"], ["$.FINAL_VERDICT"])

    def test_receipt_routes_to_human_but_never_emits_final_verdict(self):
        output = gate_module.gate({
            "batch_receipt_id": "batch-539-001",
            "FINAL_VERDICT": "PASS",
            "REVIEW_FINDINGS": [],
        })
        self.assertEqual(output["status"], "REVIEW_READY_FOR_HUMAN")
        self.assertEqual(output["batch_receipt_id"], "batch-539-001")
        self.assertFalse(output["grok_can_verify_self_as_final"])
        self.assertNotIn("FINAL_VERDICT", output)

    def test_nested_alias_is_detected_and_not_passed(self):
        output = gate_module.gate({
            "REVIEW_FINDINGS": [{"Final-Verdict": "PASS"}],
            "finalVerdict": "PASS",
            "unapproved": "drop me",
        })
        self.assertEqual(output["removed_fields"], [
            "$.REVIEW_FINDINGS[0].Final-Verdict",
            "$.finalVerdict",
        ])
        self.assertEqual(output["review_findings"], [{}])
        self.assertNotIn("unapproved", output)

    def test_non_object_rejected(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            gate_module.gate([])


if __name__ == "__main__":
    unittest.main()
