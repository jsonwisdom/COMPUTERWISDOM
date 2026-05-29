import unittest


class RuntimeGovernanceNoBypassTest(unittest.TestCase):
    def test_executor_cannot_run_without_receipt_hash(self):
        self.fail(
            "RUNTIME_GOVERNANCE_INTERFACE_V0_1 pending: "
            "executor must reject execution without receipt_hash."
        )


if __name__ == "__main__":
    unittest.main()
