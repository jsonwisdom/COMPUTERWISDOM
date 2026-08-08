from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from authorization.claim import ClaimResult
from authorization.signature import VerificationResult


@dataclass(frozen=True)
class AuthorizationDecision:
    action_authorized: bool
    authority_created: bool
    verification_status: str
    claim_status: str
    reason: str


def decide(
    verifier_result: VerificationResult,
    claim_result: Optional[ClaimResult],
) -> AuthorizationDecision:
    authorized = (
        verifier_result.status == "VERIFIED"
        and verifier_result.authorized
        and claim_result is not None
        and claim_result.status == "CLAIMED"
    )
    return AuthorizationDecision(
        action_authorized=authorized,
        authority_created=False,
        verification_status=verifier_result.status,
        claim_status=claim_result.status if claim_result else "NOT_ATTEMPTED",
        reason="ACTION_AUTHORIZED" if authorized else verifier_result.reason,
    )
