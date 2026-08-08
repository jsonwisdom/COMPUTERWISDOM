from __future__ import annotations

import re
from dataclasses import dataclass

_RING_LOCALITY_RE = re.compile(r"^R([0-5])-([A-Z0-9]+)$")


@dataclass(frozen=True)
class RingLocality:
    locality_id: str
    ring: int
    code: str


def resolve_ring(locality: str) -> RingLocality:
    """Parse and validate a privacy-preserving R0-R5 locality identifier."""
    if not isinstance(locality, str):
        raise TypeError("locality must be a ring-locality string")
    normalized = locality.strip().upper()
    match = _RING_LOCALITY_RE.fullmatch(normalized)
    if not match:
        raise ValueError("locality must match ^R[0-5]-[A-Z0-9]+$")
    return RingLocality(
        locality_id=normalized,
        ring=int(match.group(1)),
        code=match.group(2),
    )
