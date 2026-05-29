class RejectionError(Exception):
    pass


class Executor:
    def execute(self, request: dict) -> None:
        if 'receipt_hash' not in request:
            raise RejectionError('missing receipt_hash')
