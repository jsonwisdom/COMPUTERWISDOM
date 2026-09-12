from app.normalizer import normalize_row
from app.models import ProofState


def test_send_unknown_counterparty_holds_identity_and_overall_state():
    row = {
        "id": "send-1",
        "timestamp": "2026-09-12T00:00:00Z",
        "type": "SEND",
        "asset": "ETH",
        "quantity": "0.01",
        "fee": "0.0001",
    }
    leaf = normalize_row(row, rail="TEST", object_type="CSV_ROW")
    assert leaf.receipt_state == ProofState.PASS
    assert leaf.identity_state == ProofState.HOLD
    assert leaf.state == ProofState.HOLD
    assert "counterparty_identity" in leaf.missing_fields


def test_missing_fee_does_not_become_zero_or_pass():
    row = {
        "id": "send-2",
        "timestamp": "2026-09-12T00:00:00Z",
        "type": "SEND",
        "asset": "ETH",
        "quantity": "0.01",
        "counterparty": "0xabc",
    }
    leaf = normalize_row(row, rail="TEST", object_type="CSV_ROW")
    assert leaf.identity_state == ProofState.PASS
    assert leaf.fee is None
    assert leaf.fee_state == ProofState.HOLD
    assert leaf.state == ProofState.HOLD
    assert "fee" in leaf.missing_fields


def test_buy_with_required_fields_and_fee_can_pass():
    row = {
        "id": "buy-1",
        "timestamp": "2026-09-12T00:00:00Z",
        "type": "BUY",
        "asset": "BTC-USD",
        "quantity": "0.001",
        "native_value": "100",
        "fee": "1.00",
    }
    leaf = normalize_row(row, rail="TEST", object_type="CSV_ROW")
    assert leaf.receipt_state == ProofState.PASS
    assert leaf.identity_state == ProofState.PASS
    assert leaf.fee_state == ProofState.PASS
    assert leaf.state == ProofState.PASS
