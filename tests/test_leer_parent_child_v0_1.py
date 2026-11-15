"""Local tests of the bounded synthetic-curriculum prototype."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "tools" / "leer" / "leer.py"
spec = importlib.util.spec_from_file_location("leer", path)
leer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leer)

class TestLeer(unittest.TestCase):
    def test_authority_is_false(self):
        self.assertFalse(leer.POLICY["authority"])
        self.assertFalse(leer.POLICY["human_child_records"])
        self.assertFalse(leer.POLICY["external_writes"])
    def test_synthetic_children(self):
        ids = leer.run(["get", "children"])["children"]
        self.assertEqual(ids, ["AL-01", "MN-13"])
        self.assertTrue(all(leer.LESSONS[i]["synthetic"] for i in ids))
    def test_missing_child(self):
        self.assertEqual(leer.run(["get", "child", "PERSON"])["status"], "UNKNOWN")
    def test_vote_math(self):
        r = leer.run(["vote", "3"])
        self.assertEqual((r["credits_required"], r["credits_remaining"]), (9, 91))
        self.assertFalse(r["real_election_action"])
    def test_vote_limits(self):
        for arg in ("-1", "11", "garbage"):
            self.assertEqual(leer.run(["vote", arg])["status"], "REJECT")
    def test_replay_is_deterministic(self):
        a, b = leer.run(["replay"]), leer.run(["replay"])
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertFalse(a["authority"])

if __name__ == "__main__":
    unittest.main()
