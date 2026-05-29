"""
Caseflow State Machine Engine Tests v0.2
Constitutional Game Stack - Rules Phase

These tests verify that the v0.2 engine enforces transition rules,
preserves authority=false, blocks invalid promotions, and records receipts
without granting truth, legal effect, Base anchoring, ENS authority, or merge authority.
"""

import copy
import unittest

from caseflow.state_machine.engine_v0_2 import CaseflowEngine


class TestCaseflowEngineV02(unittest.TestCase):
    def setUp(self):
        self.engine = CaseflowEngine()
        self.base_case = {
            "case_id": "CASE-TEST-001",
            "current_state": "UNDER_REVIEW",
            "history": [],
            "metadata": {
                "authority_level": 0,
                "boundary_honest": True,
                "legal_effect": False,
                "satisfied_checks": [
                    "review_context_present",
                    "receipt_or_pointer_present",
                    "authority_false",
                ],
            },
        }

    def test_valid_under_review_to_governance_check(self):
        """VALID_UNDER_REVIEW_TO_GOVERNANCE_CHECK"""
        case = copy.deepcopy(self.base_case)

        result = self.engine.apply_transition(case, "GOVERNANCE_CHECK", "GROK_WITNESS")

        self.assertEqual(result["current_state"], "GOVERNANCE_CHECK")
        self.assertEqual(len(result["history"]), 1)
        self.assertEqual(result["history"][0]["actor"], "GROK_WITNESS")
        self.assertIn("receipts", result)
        self.assertEqual(result["receipts"][0]["authority"], False)
        self.assertEqual(result["receipts"][0]["legal_effect"], False)
        self.assertIn("receipt_hash", result["receipts"][0])

    def test_invalid_draft_to_merged_is_blocked_without_mutation(self):
        """INVALID_DRAFT_TO_MERGED"""
        case = copy.deepcopy(self.base_case)
        case["current_state"] = "DRAFT"

        result = self.engine.apply_transition(case, "MERGED", "AGENT")

        self.assertEqual(result["current_state"], "DRAFT")
        self.assertIn("denials", result)
        self.assertIn("transition_not_allowed:DRAFT->MERGED", result["denials"][-1]["reason"])
        self.assertEqual(result["denials"][-1]["authority"], False)
        self.assertNotIn("receipts", result)

    def test_forbidden_promotion_blocked(self):
        """FORBIDDEN_PROMOTION_BLOCKED"""
        case = copy.deepcopy(self.base_case)
        case["forbidden_promotions_detected"] = ["witness_output_to_verified_truth"]

        result = self.engine.apply_transition(case, "GOVERNANCE_CHECK", "GROK_WITNESS")

        self.assertEqual(result["current_state"], "UNDER_REVIEW")
        self.assertIn("denials", result)
        self.assertIn("forbidden_promotion_detected", result["denials"][-1]["reason"])

    def test_authority_level_nonzero_blocked(self):
        """AUTHORITY_LEVEL_NONZERO_BLOCKED"""
        case = copy.deepcopy(self.base_case)
        case["metadata"]["authority_level"] = 1

        result = self.engine.apply_transition(case, "GOVERNANCE_CHECK", "GROK_WITNESS")

        self.assertEqual(result["current_state"], "UNDER_REVIEW")
        self.assertIn("denials", result)
        self.assertEqual(result["denials"][-1]["reason"], "authority_level_must_remain_zero")

    def test_missing_required_check_blocked(self):
        """MISSING_REQUIRED_CHECK_BLOCKED"""
        case = copy.deepcopy(self.base_case)
        case["metadata"]["satisfied_checks"] = ["authority_false"]

        result = self.engine.apply_transition(case, "GOVERNANCE_CHECK", "GROK_WITNESS")

        self.assertEqual(result["current_state"], "UNDER_REVIEW")
        self.assertIn("denials", result)
        self.assertIn("missing_required_checks", result["denials"][-1]["reason"])
        self.assertIn("receipt_or_pointer_present", result["denials"][-1]["reason"])
        self.assertIn("review_context_present", result["denials"][-1]["reason"])

    def test_ghost_anchor_blocked(self):
        """GHOST_ANCHOR_BLOCKED"""
        case = copy.deepcopy(self.base_case)
        case["metadata"]["ghost_anchor"] = True

        result = self.engine.apply_transition(case, "GOVERNANCE_CHECK", "GROK_WITNESS")

        self.assertEqual(result["current_state"], "UNDER_REVIEW")
        self.assertIn("denials", result)
        self.assertEqual(result["denials"][-1]["reason"], "ghost_anchor_blocked")


if __name__ == "__main__":
    unittest.main()
