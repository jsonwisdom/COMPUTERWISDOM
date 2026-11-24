"""Negative regression tests for draft-only quadratic scaffolding."""
import copy
import json
import unittest
from pathlib import Path
from quadratic import EXPECTED_PAIRS, review

HERE = Path(__file__).resolve().parent
POLICY = json.loads((HERE / "OWNER_POLICY.json").read_text(encoding="utf-8"))
MATRIX = json.loads((HERE / "quadratic_edges.json").read_text(encoding="utf-8"))
ARCH = json.loads((HERE / "architecture.json").read_text(encoding="utf-8"))


class QuadraticGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.policy = copy.deepcopy(POLICY)
        self.matrix = copy.deepcopy(MATRIX)
        self.arch = copy.deepcopy(ARCH)

    def findings(self):
        return review(self.policy, self.matrix, self.arch)

    def test_baseline_passes_without_claiming_external_proof(self):
        self.assertEqual([], self.findings())
        self.assertTrue(all(x["status"] == "UNKNOWN" for x in self.matrix["edges"]))

    def test_six_unique_quadratic_pairs(self):
        pairs = {frozenset((e["from"], e["to"])) for e in self.matrix["edges"]}
        self.assertEqual(pairs, EXPECTED_PAIRS)
        self.assertEqual(len(pairs), 6)

    def test_each_edge_checked_for_unproven_promotion(self):
        for index in range(6):
            with self.subTest(edge=index + 1):
                bad = copy.deepcopy(self.matrix)
                bad["edges"][index]["status"] = "PASS"
                self.assertIn("unsupported_edge_promotion:E0" + str(index + 1),
                              review(self.policy, bad, self.arch))

    def test_missing_edge_detected(self):
        self.matrix["edges"].pop()
        self.assertIn("edge_count_mismatch", self.findings())
        self.assertIn("incomplete_pair_coverage", self.findings())

    def test_duplicate_edge_detected(self):
        self.matrix["edges"][5] = copy.deepcopy(self.matrix["edges"][0])
        self.assertTrue(any(x.startswith("duplicate_pair:") for x in self.findings()))

    def test_owner_cannot_be_replaced_by_agent(self):
        self.policy["owner"]["name"] = "JSONWisdom"
        self.assertIn("owner_mismatch", self.findings())

    def test_no_unauthorized_merge(self):
        self.policy["permissions"]["merge"] = True
        self.assertIn("unauthorized_permission:merge", self.findings())

    def test_signing_not_a_build_precondition(self):
        self.policy["safeguards"]["signature_required_for_build"] = True
        self.assertIn("duplicate_authentication_gate", self.findings())

    def test_global_hold_does_not_recur(self):
        self.policy["safeguards"]["global_hold"] = True
        self.assertIn("global_hold", self.findings())

    def test_architecture_rail_drift(self):
        self.arch["rails"]["public"]["identity"] = "jaywisdom.eth"
        self.assertIn("public_rail_drift", self.findings())


if __name__ == "__main__":
    unittest.main()
