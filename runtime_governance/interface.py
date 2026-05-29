class RejectionError(Exception):
    pass


class Executor:
    def _validate_receipt_hash(self, receipt_hash):
        if not receipt_hash or not isinstance(receipt_hash, str):
            raise RejectionError('missing or invalid receipt_hash')

        if len(receipt_hash) != 64 or not all(
            c in '0123456789abcdef' for c in receipt_hash.lower()
        ):
            raise RejectionError('receipt_hash must be valid SHA256')

    def execute(self, request: dict):
        receipt_hash = request.get('receipt_hash')
        self._validate_receipt_hash(receipt_hash)

        decision = request.get('gate_decision')

        if decision == 'DENY_OR_DECOMPOSE':
            raise RejectionError('execution denied by gate decision')

        if decision == 'ALLOW_WITH_GATES':
            safeguards = request.get('safeguards')
            if not isinstance(safeguards, dict) or not safeguards:
                raise RejectionError('non-empty safeguards dict required for ALLOW_WITH_GATES')
            return {'status': 'SUCCESS', 'mode': 'PROTECTED'}

        if decision == 'ALLOW':
            return {'status': 'SUCCESS', 'mode': 'OPEN'}

        raise RejectionError('unknown gate decision')
