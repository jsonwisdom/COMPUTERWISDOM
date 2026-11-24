"""Synthetic-only regression checks for CI-FIRST forensic events."""
import importlib.util
import pathlib
import unittest

module_path = pathlib.Path(__file__).with_name("validator.py")
spec = importlib.util.spec_from_file_location("forensic_validator", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def event(**changes):
    base = {
        "event_id": "SYNTHETIC-E001",
        "date_utc": "2012-09-11",
        "provider": "FAKE_PROVIDER",
        "asset": "BTC",
        "event_type": "deposit",
        "state": "reported",
        "amount": "8.573693",
        "source_ref": "FAKE-REFERENCE-NOT-A-GMAIL-ID",
        "provider_order_ref": "FAKE-ORDER-1",
    }
    base.update(changes)
    return base


class Tests(unittest.TestCase):
    def test_valid_report_never_claims_balance_or_recovery(self):
        r = module.audit([event()])
        self.assertEqual(r["status"], "PASS")
        self.assertIsNone(r["portfolio_total"])
        self.assertIsNone(r["asset_recovered"])
        self.assertFalse(r["loss_inferred"])
        self.assertFalse(r["signing_authority"])
        self.assertFalse(r["reconciliation_complete"])

    def test_same_order_twice_does_not_count_twice(self):
        r = module.audit([event(), event(event_id="SYNTHETIC-E002")])
        self.assertEqual(r["status"], "HOLD")
        self.assertTrue(any("duplicate order-event" in x for x in r["findings"]))

    def test_balance_snapshot_not_portfolio(self):
        r = module.audit([event(event_type="balance_snapshot", amount="0.00000587")])
        self.assertIsNone(r["portfolio_total"])

    def test_requests_not_confirmations(self):
        r = module.audit([event(event_type="withdrawal", state="requested")])
        self.assertFalse(r["reconciliation_complete"])

    def test_secret_fields_rejected(self):
        self.assertIn("sensitive field prohibited: secret", module.validate(event(secret="forbidden")))

    def test_nondecimal_amount_rejected(self):
        self.assertIn("amount must be a decimal string", module.validate(event(amount="1 BTC")))

    def test_negative_amount_rejected(self):
        self.assertIn("amount must be nonnegative finite decimal", module.validate(event(amount="-0.5")))


if __name__ == "__main__":
    unittest.main()
