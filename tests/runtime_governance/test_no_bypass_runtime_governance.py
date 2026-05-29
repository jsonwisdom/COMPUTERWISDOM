import unittest

from runtime_governance.interface import Executor, RejectionError


VALID_RECEIPT_HASH = 'a' * 64


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

    def test_executor_rejects_short_receipt_hash(self):
        executor = Executor()
        request = {'receipt_hash': 'a' * 63}

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_executor_rejects_non_string_receipt_hash(self):
        executor = Executor()
        request = {'receipt_hash': 123}

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_executor_rejects_deny_or_decompose(self):
        executor = Executor()
        request = {
            'receipt_hash': VALID_RECEIPT_HASH,
            'gate_decision': 'DENY_OR_DECOMPOSE',
        }

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_executor_rejects_unknown_gate_decision(self):
        executor = Executor()
        request = {
            'receipt_hash': VALID_RECEIPT_HASH,
            'gate_decision': 'ALIEN_DECISION',
        }

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_allow_with_gates_requires_safeguards(self):
        executor = Executor()
        request = {
            'receipt_hash': VALID_RECEIPT_HASH,
            'gate_decision': 'ALLOW_WITH_GATES',
        }

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_allow_with_gates_rejects_malformed_safeguards(self):
        executor = Executor()
        request = {
            'receipt_hash': VALID_RECEIPT_HASH,
            'gate_decision': 'ALLOW_WITH_GATES',
            'safeguards': 'not-a-dict',
        }

        with self.assertRaises(RejectionError):
            executor.execute(request)

    def test_allow_with_gates_executes_with_safeguards(self):
        executor = Executor()
        request = {
            'receipt_hash': VALID_RECEIPT_HASH,
            'gate_decision': 'ALLOW_WITH_GATES',
            'safeguards': {'produce_receipt': True},
        }

        self.assertEqual(executor.execute(request), 'EXECUTED_WITH_SAFEGUARDS')

    def test_allow_executes_with_valid_receipt_hash(self):
        executor = Executor()
        request = {
            'receipt_hash': VALID_RECEIPT_HASH,
            'gate_decision': 'ALLOW',
        }

        self.assertEqual(executor.execute(request), 'EXECUTED')


if __name__ == '__main__':
    unittest.main()
