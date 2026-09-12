from __future__ import annotations
from collections import Counter
from .models import EventLeaf, ProofState


def denominator(events: list[EventLeaf]) -> dict:
    states = Counter(e.state.value for e in events)
    receipt_states = Counter(e.receipt_state.value for e in events)
    identity_states = Counter(e.identity_state.value for e in events)
    fee_states = Counter(e.fee_state.value for e in events)
    types = Counter(e.event_type for e in events)
    rails = Counter(e.source.rail for e in events)
    timestamps = sorted([e.source.timestamp for e in events if e.source.timestamp])
    return {
        "event_count": len(events),
        "state_counts": dict(states),
        "receipt_state_counts": dict(receipt_states),
        "identity_state_counts": dict(identity_states),
        "fee_state_counts": dict(fee_states),
        "event_types": dict(types),
        "rails": dict(rails),
        "oldest_timestamp": timestamps[0] if timestamps else None,
        "newest_timestamp": timestamps[-1] if timestamps else None,
        "history_complete": False,
        "history_state": ProofState.HOLD.value,
        "rule": "EVENT_RECEIPT_PASS != IDENTITY_PASS != HISTORY_PASS; MISSING != ZERO; ONE_RAIL != WHOLE_BOOK",
    }
