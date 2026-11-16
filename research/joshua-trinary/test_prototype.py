"""Deterministic sanity tests for fictional civilian game. Run python -m unittest discover."""
import unittest
from prototype import Player, digest, verify_notification, escalation_flag, step, manifest

class FictionalGameTests(unittest.TestCase):
    def test_score_bounds_grid(self):
        for c in (0,.5,1):
            for t in (0,.5,1):
                for r in (0,.5,1):
                    s=Player("A",c,t,r).score()
                    self.assertGreaterEqual(s,0)
                    self.assertLessEqual(s,1)
    def test_notify_evidence_gate(self):
        record={"message":"fictional"}
        self.assertEqual(verify_notification(record,None),"UNKNOWN")
        self.assertEqual(verify_notification(record,"0"*64),"FAIL")
        self.assertEqual(verify_notification(record,digest(record)),"PASS")
    def test_silence_penalty(self):
        players={"A":Player("A")}
        step(players,{"A":"silence"},{"A":0.1},{"A":None},{"A":None})
        self.assertAlmostEqual(players["A"].credibility,.44)
    def test_unknown_no_reward(self):
        players={"A":Player("A")}
        step(players,{"A":"notify"},{"A":0.8},{"A":{"msg":"test"}},{"A":None})
        self.assertEqual(players["A"].credibility,.5)
    def test_inquiry_not_automatically_transparent(self):
        players={"A":Player("A")}
        step(players,{"A":"inquire"},{"A":0.1},{"A":None},{"A":None})
        self.assertEqual(players["A"].transparency,.5)
    def test_escalation_predicate(self):
        for h in (0,.5,1):
            for c in (0,.5,1):
                for a in ("notify","inquire","silence"):
                    self.assertEqual(escalation_flag(h,c,a),h>c and a!="notify")
    def test_manifest_not_signed(self):
        m=manifest([{"entry_id":"SCENARIO_01","msg":"fictional"}])
        self.assertEqual(m["circuit_status"],"UNKNOWN")
        self.assertIsNone(m["human_signature"])
        self.assertEqual(len(m["manifest_hash"]),64)
if __name__=="__main__": unittest.main()
