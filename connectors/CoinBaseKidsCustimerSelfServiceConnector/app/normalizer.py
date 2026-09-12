from __future__ import annotations
import hashlib, json
from .models import EventLeaf, ProofState, SourceRef

TRANSFER_LIKE_TYPES = {"SEND", "RECEIVE", "TRANSFER", "WITHDRAW", "WITHDRAWAL", "DEPOSIT"}
FEE_EXPECTED_TYPES = {"BUY", "SELL", "SEND", "RECEIVE", "TRANSFER", "WITHDRAW", "WITHDRAWAL", "CONVERT"}


def stable_event_id(payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def normalize_row(row: dict, *, rail: str, object_type: str) -> EventLeaf:
    oid = row.get("id") or row.get("order_id") or row.get("trade_id") or row.get("transaction_id")
    ts = row.get("created_at") or row.get("timestamp") or row.get("completed_at")
    event_type = str(row.get("type") or row.get("side") or object_type).upper()
    counterparty = str(row.get("counterparty") or row.get("to") or row.get("from") or "UNKNOWN")
    fee = _string(row.get("fee") or row.get("total_fees") or row.get("commission"))

    payload = {"rail": rail, "object_type": object_type, "object_id": oid, "timestamp": ts, "row": row}
    missing = []
    notes = []

    if not oid:
        missing.append("object_id")
    if not ts:
        missing.append("timestamp")

    receipt_state = ProofState.HOLD if missing else ProofState.PASS

    if event_type in TRANSFER_LIKE_TYPES and counterparty.strip().upper() in {"", "UNKNOWN", "NONE", "NULL"}:
        identity_state = ProofState.HOLD
        missing.append("counterparty_identity")
        notes.append("TX_PRESENT != COUNTERPARTY_IDENTIFIED")
    else:
        identity_state = ProofState.PASS

    if event_type in FEE_EXPECTED_TYPES and fee is None:
        fee_state = ProofState.HOLD
        missing.append("fee")
        notes.append("MISSING_FEE != ZERO")
    else:
        fee_state = ProofState.PASS

    component_states = (receipt_state, identity_state, fee_state)
    state = ProofState.HOLD if ProofState.HOLD in component_states else ProofState.PASS

    leaf = EventLeaf(
        event_id=stable_event_id(payload),
        source=SourceRef(rail=rail, object_type=object_type, object_id=oid, timestamp=ts),
        event_type=event_type,
        asset=row.get("asset") or row.get("product_id"),
        quantity=_string(row.get("quantity") or row.get("filled_size") or row.get("size")),
        native_value=_string(row.get("native_value") or row.get("quote_size") or row.get("value")),
        fee=fee,
        direction=row.get("direction") or row.get("side"),
        portfolio_id=row.get("portfolio_id"),
        account_id=row.get("account_id"),
        counterparty=counterparty,
        receipt_state=receipt_state,
        identity_state=identity_state,
        fee_state=fee_state,
        state=state,
        missing_fields=sorted(set(missing)),
        notes=notes,
    )
    return leaf


def _string(value):
    return None if value in (None, "") else str(value)
