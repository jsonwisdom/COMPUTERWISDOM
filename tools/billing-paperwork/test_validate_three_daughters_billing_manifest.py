#!/usr/bin/env python3

import copy
import json
import unittest
from pathlib import Path

from validate_three_daughters_billing_manifest import validate


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent.parent / "corporate" / "billing" / "three_daughters" / "paperwork_manifest.template.json"


def template():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


class BillingManifestValidationTests(unittest.TestCase):
    def test_template_passes(self):
        self.assertEqual(validate(template()), [])

    def test_authority_true_rejects(self):
        data = template()
        data["authority"] = True
        self.assertTrue(any("authority must be false" in error for error in validate(data)))

    def test_named_participant_key_rejects(self):
        data = template()
        data["family_superposition"]["mirrors"][0]["daughter_name"] = "PRIVATE"
        self.assertTrue(any("private key name" in error for error in validate(data)))

    def test_public_role_assignment_rejects(self):
        data = template()
        data["family_superposition"]["mirrors"][0]["state"] = "RECEIPT_READER"
        self.assertTrue(any("must remain UNASSIGNED" in error for error in validate(data)))

    def test_payment_execution_rejects(self):
        data = template()
        data["financial_state"]["payment_executed"] = True
        self.assertTrue(any("payment_executed must be false" in error for error in validate(data)))

    def test_fake_green_rejects(self):
        data = template()
        data["leeloo_multi_pass"]["overall"] = "PASS"
        self.assertTrue(any("overall must be HOLD" in error for error in validate(data)))

    def test_reject_precedes_conflict_and_hold(self):
        data = template()
        data["leeloo_multi_pass"]["record_reality"] = "REJECT"
        data["leeloo_multi_pass"]["authority_law"] = "CONFLICT"
        data["leeloo_multi_pass"]["overall"] = "REJECT"
        self.assertEqual(validate(data), [])


if __name__ == "__main__":
    unittest.main()


