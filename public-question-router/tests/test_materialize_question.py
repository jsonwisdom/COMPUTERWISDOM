import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "materialize_question.py"
spec = importlib.util.spec_from_file_location("materialize_question", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class MaterializeQuestionTest(unittest.TestCase):
    def test_materializes_fail_closed_tree_and_24h_portal_clock(self):
        intake = {
            "question_id": "Q-20260818-AUTHORITY_DEMO",
            "submitted_at": "2026-08-18T23:37:00-05:00",
            "question_text": "What office claims authority for this action, and what primary record proves it?",
            "question_class": ["AUTHORITY", "PUBLIC_RECORD"],
            "authority_candidates": [
                {
                    "office": "UNRESOLVED",
                    "person": None,
                    "basis": "AI may propose; source binding required",
                    "source_url": None,
                    "status": "PROPOSED_BY_AI"
                }
            ],
            "record_requests": [],
            "legal_clocks": [],
            "replay_state": "HOLD",
            "authority_created": False
        }

        with tempfile.TemporaryDirectory() as tmp:
            case_dir = module.materialize(intake, Path(tmp))
            self.assertTrue((case_dir / "QUESTION.md").exists())
            self.assertTrue((case_dir / "authority" / "candidates.json").exists())
            self.assertTrue((case_dir / "records" / "court" / "README.md").exists())
            self.assertTrue((case_dir / "responses" / "oig" / "README.md").exists())

            portal = json.loads((case_dir / "clocks" / "portal_24h.json").read_text())
            self.assertEqual(portal["sla_hours"], 24)
            self.assertFalse(portal["legal_deadline_created"])
            self.assertEqual(portal["status_due_at"], "2026-08-20T04:37:00Z")

            normalized = json.loads((case_dir / "intake.json").read_text())
            self.assertFalse(normalized["authority_created"])
            self.assertEqual(normalized["replay_state"], "HOLD")

    def test_rejects_invalid_question_id(self):
        intake = {
            "question_id": "bad-id",
            "submitted_at": "2026-08-18T23:37:00-05:00",
            "question_text": "test"
        }
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                module.materialize(intake, Path(tmp))


if __name__ == "__main__":
    unittest.main()
