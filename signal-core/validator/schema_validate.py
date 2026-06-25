import json
import re
from pathlib import Path

HASH_RE = re.compile(r'^sha256:[0-9a-f]{64}$')
RECEIPT_RE = re.compile(r'^vr:sha256:[0-9a-f]{64}$')


class ReceiptSchemaError(ValueError):
    pass


def require_keys(receipt):
    required = {
        'receipt_id',
        'artifact_hash',
        'claim_graph_hash',
        'claims_count',
        'receipt_core_hash',
        'confidence',
    }
    missing = sorted(required - set(receipt))
    if missing:
        raise ReceiptSchemaError('missing required fields: ' + ', '.join(missing))
    extra = sorted(set(receipt) - required)
    if extra:
        raise ReceiptSchemaError('unexpected fields: ' + ', '.join(extra))


def validate_receipt(receipt):
    require_keys(receipt)
    if not RECEIPT_RE.match(receipt['receipt_id']):
        raise ReceiptSchemaError('receipt_id must match vr:sha256:<64 hex>')
    for key in ('artifact_hash', 'claim_graph_hash', 'receipt_core_hash'):
        if not HASH_RE.match(receipt[key]):
            raise ReceiptSchemaError(key + ' must match sha256:<64 hex>')
    if not isinstance(receipt['claims_count'], int) or receipt['claims_count'] < 0:
        raise ReceiptSchemaError('claims_count must be a non-negative integer')
    confidence = receipt['confidence']
    if not isinstance(confidence, dict):
        raise ReceiptSchemaError('confidence must be an object')
    if set(confidence.keys()) != {'authority'}:
        raise ReceiptSchemaError('confidence may only contain authority')
    if confidence['authority'] != 'NONE':
        raise ReceiptSchemaError('confidence.authority must be NONE')
    return True


def validate_receipt_file(path):
    receipt = json.loads(Path(path).read_text(encoding='utf-8'))
    return validate_receipt(receipt)
