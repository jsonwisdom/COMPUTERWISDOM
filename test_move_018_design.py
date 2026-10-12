from pathlib import Path
import unittest


TEXT = (Path(__file__).parent / "docs" / "PURPOSE_REPLAY_INTEGRATION_MOVE_018_V0_1.md").read_text(encoding="utf-8")


class Move018DesignTests(unittest.TestCase):
    def test_state_is_bounded(self):
        for value in (
            "PROTOCOL_CLAIM       = FALSE",
            "IMPLEMENTED          = FALSE",
            "AUTHORITY_CREATED    = FALSE",
            "NEXT_TRANSITION      = HUMAN_REVIEWS_PURPOSE_INTEGRATION",
        ):
            self.assertIn(value, TEXT)

    def test_repository_roles_do_not_create_truth_authority(self):
        self.assertIn("Not a source-of-truth authority", TEXT)
        self.assertIn("Not a universal identity constant or routing authority", TEXT)
        self.assertIn("digest-bound pointers", TEXT)

    def test_purpose_cannot_change_verification(self):
        self.assertIn("Purpose must not:", TEXT)
        self.assertIn("change validation results", TEXT)
        self.assertIn("bypass required checks", TEXT)

    def test_alms_remains_unresolved(self):
        self.assertIn("ALMS_EXPANSION_ACCEPTED = FALSE", TEXT)
        self.assertIn("ALMS_SERVICE_CREATED    = FALSE", TEXT)
        self.assertIn("ALMS_STORAGE_VERIFIED   = FALSE", TEXT)

    def test_failure_and_amendment_sections_exist(self):
        self.assertIn("## How we will fail", TEXT)
        self.assertIn("## Amendment history", TEXT)


if __name__ == "__main__":
    unittest.main()
