from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

_STATUSES = {"VERIFIED", "INVALID", "INDETERMINATE"}


@dataclass(frozen=True)
class VerificationResult:
    status: str
    reason: str
    authorized: bool

    def __post_init__(self) -> None:
        if self.status not in _STATUSES:
            raise ValueError("invalid signature verification status")
        if not isinstance(self.reason, str) or not self.reason:
            raise ValueError("signature verification reason is required")
        if self.authorized is not (self.status == "VERIFIED"):
            raise ValueError("authorized must be true exactly when status is VERIFIED")


class SignatureVerifier(ABC):
    @abstractmethod
    def verify(
        self, ens_name: str, message_hash: bytes, signature: bytes
    ) -> VerificationResult: ...


class SimulationSignatureVerifier(SignatureVerifier):
    def verify(
        self, ens_name: str, message_hash: bytes, signature: bytes
    ) -> VerificationResult:
        return VerificationResult(
            status="INDETERMINATE",
            reason="SIMULATION_SIGNATURE_VERIFICATION_NOT_IMPLEMENTED",
            authorized=False,
        )
