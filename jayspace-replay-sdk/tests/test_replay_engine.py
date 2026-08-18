import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from replay_engine import evaluate  # noqa: E402

FIXTURE = ROOT / "fixtures" / "GENERIC_SEVEN_NODE_MEMBRANE_V0_1.json"


class ReplayEngineTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_seven_node_fixture_rejects_identity_collapse(self):
        receipt = evaluate(self.load_fixture())
        self.assertEqual(receipt["disposition"], "REJECT")
        self.assertIn("REAL_SYNTHETIC_IDENTITY_COLLAPSE_BLOCKED:2", receipt["signals"])
        self.assertFalse(receipt["authority_created"])

    def test_missing_source_fails_closed_to_hold(self):
        case = self.load_fixture()
        case["edges"] = case["edges"][:2]
        case["nodes"] = [node for node in case["nodes"] if node["id"] not in {"n0", "n1", "n2"}]
        receipt = evaluate(case)
        self.assertEqual(receipt["disposition"], "PASS")
        case["nodes"][0]["source_status"] = "UNBOUND"
        receipt = evaluate(case)
        self.assertEqual(receipt["disposition"], "HOLD")

    def test_conflict_outranks_hold(self):
        case = self.load_fixture()
        case["edges"] = []
        case["nodes"][0]["source_status"] = "UNBOUND"
        case["nodes"][1]["source_status"] = "CONFLICT"
        receipt = evaluate(case)
        self.assertEqual(receipt["disposition"], "CONFLICT")

    def test_authority_attempt_is_rejected(self):
        case = self.load_fixture()
        case["edges"] = []
        case["nodes"] = [case["nodes"][3]]
        case["nodes"][0]["authority"] = True
        receipt = evaluate(case)
        self.assertEqual(receipt["disposition"], "REJECT")
        self.assertIn("NODE_AUTHORITY_FORBIDDEN:n3", receipt["signals"])


if __name__ == "__main__":
    unittest.main()
