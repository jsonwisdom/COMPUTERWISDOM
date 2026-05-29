import unittest

from runtime_governance.interface import Executor, RejectionError


class RuntimeGovernanceNoBypassTest(unittest.TestCase):
    def test_executor_rejects_missing_receipt_hash(self):
        executor = Executor()
        request = {}

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_executor_rejects_invalid_receipt_hash(self):
        executor = Executor()
        request = {'receipt_hash': 'not-a-valid-sha256'}

        with self.assertRaises(RejectionError):
            executor.execute(request)


if __name__ == '__main__':
    unittest.main()
