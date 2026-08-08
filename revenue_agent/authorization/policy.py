from __future__ import annotations

import hashlib
import json
from types import MappingProxyType
from typing import Tuple

AUTHORIZATION_POLICY_VERSION = "LOCALITY_AUTHORIZATION_POLICY_V0_1"

_LOCALITY_ROLE_MATRIX = MappingProxyType(
    {
        "R2-COUNTY042": ("emergency_management", "public_works"),
        "R3-CITYSTCLOUD": ("public_works",),
    }
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _policy_document() -> dict:
    return {
        "version": AUTHORIZATION_POLICY_VERSION,
        "locality_role_matrix": {
            locality: list(roles) for locality, roles in sorted(_LOCALITY_ROLE_MATRIX.items())
        },
    }


AUTH_POLICY_DIGEST = hashlib.sha256(_canonical_bytes(_policy_document())).hexdigest()

# Exact digest exported by LOCALITY_MATRIX_ROUTER_V0_1 in PR #439.
KNOWN_ROUTER_POLICY_DIGESTS = frozenset(
    {"df206d84b75d1913607a01f1410fb28aa7c8999c56c8b21e39cc9fa100a3a016"}
)


def get_allowed_roles(locality_scope: str) -> Tuple[str, ...]:
    return _LOCALITY_ROLE_MATRIX.get(locality_scope, ())
