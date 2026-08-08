"""Human-authorization verification for the Locality Matrix.

This package contains no execution adapter.
"""

from authorization.claim import ClaimResult, FileBasedClaimStore
from authorization.decision import AuthorizationDecision, decide
from authorization.policy import AUTH_POLICY_DIGEST
from authorization.receipt_builder import build_authorization_receipt
from authorization.signature import SimulationSignatureVerifier, VerificationResult
from authorization.verifier import generate_task_id, verify_authorization, verify_routing_receipt

__all__ = [
    "AUTH_POLICY_DIGEST",
    "AuthorizationDecision",
    "ClaimResult",
    "FileBasedClaimStore",
    "SimulationSignatureVerifier",
    "VerificationResult",
    "build_authorization_receipt",
    "decide",
    "generate_task_id",
    "verify_authorization",
    "verify_routing_receipt",
]
