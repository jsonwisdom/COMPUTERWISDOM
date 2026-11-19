"""CI-FIRST continuity checks: synthetic receipts only."""
import copy
import unittest

from continuity import reconcile

PASS = {
    "claim_id": "wallet-message-signature",
    "scope": "exact-eip191-message",
    "status": "PASS_PREVIOUSLY_VERIFIED",
    "source": "synthetic://receipt-001",
    "test_id": "synthetic-signature-recovery-test",
    "evidence_sha256": "a" * 64,
}


class ContinuityTests(unittest.TestCase):
    def test_not_searched_is_not_unverified(self):
        self.assertEqual(reconcile("claim", [], [])["status"], "UNKNOWN_NOT_SEARCHED")

    def test_search_without_proof_is_not_verified(self):
        self.assertEqual(reconcile("claim", [], ["github"])["status"],
                         "UNKNOWN_NOT_VERIFIED")

    def test_prior_pass_reused_only_for_exact_scope(self):
        result = reconcile(PASS["claim_id"], [PASS], ["github"], PASS["scope"])
        self.assertEqual(result["status"], "PASS_PREVIOUSLY_VERIFIED")
        self.assertFalse(result["external_verification_performed"])

    def test_prior_pass_cannot_prove_ens_control(self):
        result = reconcile(PASS["claim_id"], [PASS], ["github"], "ens-control")
        self.assertEqual(result["status"], "UNKNOWN_NOT_VERIFIED")

    def test_pass_requires_provenance_fields(self):
        receipt = copy.deepcopy(PASS)
        del receipt["test_id"]
        self.assertEqual(reconcile(PASS["claim_id"], [receipt], ["github"])["status"],
                         "UNKNOWN_NOT_VERIFIED")

    def test_conflicting_receipts(self):
        failure = {**PASS, "status": "FAIL"}
        self.assertEqual(reconcile(PASS["claim_id"], [PASS, failure], ["github"])["status"],
                         "CONFLICT")

    def test_single_failure_remains_failure(self):
        failure = {**PASS, "status": "FAIL"}
        self.assertEqual(reconcile(PASS["claim_id"], [failure], ["github"])["status"],
                         "FAIL")

    def test_no_authority_from_receipts(self):
        self.assertFalse(reconcile(PASS["claim_id"], [PASS], ["github"])["new_authority_granted"])


if __name__ == "__main__":
    unittest.main()
