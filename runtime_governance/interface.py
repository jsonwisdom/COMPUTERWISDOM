import re


class RejectionError(Exception):
    pass


_SHA256_RE = re.compile(r'^[a-fA-F0-9]{64}$')


class Executor:
    def execute(self, request: dict) -> None:
        receipt_hash = request.get('receipt_hash')

        if receipt_hash is None:
            raise RejectionError('missing receipt_hash')

        if not isinstance(receipt_hash, str) or not _SHA256_RE.match(receipt_hash):
            raise RejectionError('invalid receipt_hash')
