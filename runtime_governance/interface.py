class Executor:
    def execute(self, request_text, model_id, decision, receipt_hash):
        if receipt_hash is None:
            raise ValueError('receipt_hash required')
        return {'status': 'allowed', 'model_id': model_id}
