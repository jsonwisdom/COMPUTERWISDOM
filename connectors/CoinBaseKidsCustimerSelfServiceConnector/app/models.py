from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional

class ProofState(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    CONFLICT = "CONFLICT"

@dataclass(frozen=True)
class SourceRef:
    rail: str
    object_type: str
    object_id: Optional[str] = None
    timestamp: Optional[str] = None
    raw_locator: Optional[str] = None

@dataclass
class EventLeaf:
    event_id: str
    source: SourceRef
    event_type: str
    asset: Optional[str] = None
    quantity: Optional[str] = None
    native_value: Optional[str] = None
    fee: Optional[str] = None
    direction: Optional[str] = None
    portfolio_id: Optional[str] = None
    account_id: Optional[str] = None
    counterparty: str = "UNKNOWN"
    receipt_state: ProofState = ProofState.HOLD
    identity_state: ProofState = ProofState.HOLD
    fee_state: ProofState = ProofState.HOLD
    state: ProofState = ProofState.HOLD
    missing_fields: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["receipt_state"] = self.receipt_state.value
        data["identity_state"] = self.identity_state.value
        data["fee_state"] = self.fee_state.value
        data["state"] = self.state.value
        return data

@dataclass
class RouteReceipt:
    route_id: str
    from_state: str
    attempted_branch: str
    result: ProofState
    reason: str
    next_safe_move: Optional[str]
    authority_created: bool = False
    write: bool = False
