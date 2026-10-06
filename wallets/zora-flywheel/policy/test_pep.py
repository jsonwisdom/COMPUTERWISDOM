import unittest
from abac_policy import decide
from pep import EnforcementDenied, PolicyEnforcementPoint


class PolicyEnforcementPointTest(unittest.TestCase):
    def test_deny_does_not_call_handler(self):
        called = {"n": 0}

        def handler(_request):
            called["n"] += 1
            return "ran"

        point = PolicyEnforcementPoint({"append_leaf": handler})
        with self.assertRaises(EnforcementDenied) as raised:
            point.enforce(
                {
                    "subject": {"seat": "reader"},
                    "object": {"kind": "leaf"},
                    "action": "append_leaf",
                }
            )
        self.assertEqual(called["n"], 0)
        self.assertEqual(raised.exception.decision["reason"], "READER_READ_ONLY")

    def test_allow_calls_registered_handler(self):
        point = PolicyEnforcementPoint({"append_leaf": lambda _request: "appended"})
        out = point.enforce(
            {
                "subject": {"seat": "appender"},
                "object": {"kind": "leaf"},
                "action": "append_leaf",
            }
        )
        self.assertEqual(out["result"], "appended")
        self.assertFalse(out["spend"])

    def test_spend_handler_is_rejected(self):
        point = PolicyEnforcementPoint({"spend": lambda _request: "sent"})
        self.assertNotIn("spend", point.handlers)
        with self.assertRaises(EnforcementDenied):
            point.enforce(
                {
                    "subject": {"seat": "human_decider"},
                    "object": {"kind": "wallet", "control_proven": True},
                    "action": "spend",
                }
            )

    def test_policy_deny_matches_direct_decision(self):
        request = {
            "subject": {"seat": "appender"},
            "object": {"kind": "leaf", "leaf_complete": False},
            "action": "append_forest",
        }
        point = PolicyEnforcementPoint()
        with self.assertRaises(EnforcementDenied) as raised:
            point.enforce(request)
        self.assertEqual(raised.exception.decision["reason"], decide(request)["reason"])


if __name__ == "__main__":
    unittest.main()
