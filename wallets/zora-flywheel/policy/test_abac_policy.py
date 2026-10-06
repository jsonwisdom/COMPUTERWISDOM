import unittest
from abac_policy import decide


class AbacPolicyTest(unittest.TestCase):
    def test_missing_attribute_denies(self):
        result = decide({})
        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(result["reason"], "MISSING_ATTRIBUTE")

    def test_spend_denies_even_for_human(self):
        result = decide(
            {
                "subject": {"seat": "human_decider"},
                "object": {"kind": "wallet", "control_proven": True},
                "action": "spend",
            }
        )
        self.assertEqual(result["reason"], "SPEND_NOT_GRANTED_BY_POLICY")
        self.assertFalse(result["spend"])

    def test_declaration_is_not_control(self):
        result = decide(
            {
                "subject": {"seat": "human_decider"},
                "object": {
                    "kind": "wallet",
                    "control_proven": False,
                    "ownership_declared": True,
                },
                "action": "bind_control",
            }
        )
        self.assertEqual(result["reason"], "CONTROL_NOT_PROVEN")

    def test_incomplete_leaf_cannot_enter_forest(self):
        result = decide(
            {
                "subject": {"seat": "appender"},
                "object": {"kind": "leaf", "leaf_complete": False},
                "action": "append_forest",
            }
        )
        self.assertEqual(result["reason"], "LEAF_INCOMPLETE")

    def test_reader_cannot_append(self):
        result = decide(
            {
                "subject": {"seat": "reader"},
                "object": {"kind": "leaf"},
                "action": "append_leaf",
            }
        )
        self.assertEqual(result["reason"], "READER_READ_ONLY")

    def test_appender_may_append_leaf(self):
        result = decide(
            {
                "subject": {"seat": "appender"},
                "object": {"kind": "leaf"},
                "action": "append_leaf",
            }
        )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertFalse(result["authority_created"])

    def test_sister_unanswered_blocks_family_seat(self):
        result = decide(
            {
                "subject": {"seat": "human_decider"},
                "object": {"kind": "family_seat"},
                "action": "grant_family_seat",
                "context": {"sister_answered": False},
            }
        )
        self.assertEqual(result["reason"], "SISTER_UNANSWERED")


if __name__ == "__main__":
    unittest.main()
