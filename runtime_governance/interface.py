import re


class RejectionError(Exception):
    pass


_SHA256_RE = re.compile(r'^[a-fA-F0-9]{64}$')


class Executor:
    def execute(self, request: dict):
        receipt_hash = request.get('receipt_hash')

        if receipt_hash is None:
            raise RejectionError('missing receipt_hash')

        if not isinstance(receipt_hash, str) or not _SHA256_RE.match(receipt_hash):
            raise RejectionError('invalid receipt_hash')

        decision = request.get('gate_decision')

        if decision == 'DENY_OR_DECOMPOSE':
            raise RejectionError('execution denied by gate decision')

        if decision == 'ALLOW_WITH_GATES':
            if not request.get('safeguards'):
                raise RejectionError('safeguards required for ALLOW_WITH_GATES')
            return 'EXECUTED_WITH_SAFEGUARDS'

        if decision == 'ALLOW':
            return 'EXECUTED'

        raise RejectionError('unknown gate decision')
