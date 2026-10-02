#!/usr/bin/env python3
"""PACER Authentication API client with persistent token reuse.

No credentials, tokens, OTP secrets, or client codes are logged or serialized
by this module. Tokens are delegated to PacerTokenCache's SecretStore.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Dict, Optional, Protocol

import requests

from adapters.courts.pacer.cache.pacer_token_cache import PacerTokenCache

AUTH_ENDPOINTS = {
    "qa": "https://qa-login.uscourts.gov/services/cso-auth",
    "production": "https://pacer.login.uscourts.gov/services/cso-auth",
}
LOGOUT_ENDPOINTS = {
    "qa": "https://qa-login.uscourts.gov/services/cso-logout",
    "production": "https://pacer.login.uscourts.gov/services/cso-logout",
}
PASSWORD_REMINDER_DAY = 179
PASSWORD_REQUIRED_DAY = 180


class PacerAuthError(RuntimeError):
    pass


class PacerTransport(Protocol):
    def post(self, url: str, **kwargs: Any): ...


@dataclass(frozen=True)
class PacerCredentials:
    login_id: str
    password: str
    otp_code: Optional[str] = None
    client_code: Optional[str] = None
    filer: bool = False

    def request_body(self) -> Dict[str, str]:
        if not self.login_id or not self.password:
            raise ValueError("PACER login_id and password are required")
        body = {"loginId": self.login_id, "password": self.password}
        if self.client_code:
            body["clientCode"] = self.client_code
        if self.otp_code:
            body["otpCode"] = self.otp_code
        if self.filer:
            body["redactFlag"] = "1"
        return body


@dataclass(frozen=True)
class AuthResult:
    token: str
    source: str
    server_validity: str
    error_description: str = ""


@dataclass(frozen=True)
class PasswordRotationStatus:
    age_days: int
    reminder_due: bool
    update_required: bool


def password_rotation_status(
    last_changed: date, *, today: Optional[date] = None
) -> PasswordRotationStatus:
    """180-day password policy; day 179 is a local reminder only."""
    current = today or datetime.now(timezone.utc).date()
    age = (current - last_changed).days
    if age < 0:
        raise ValueError("last_changed cannot be in the future")
    return PasswordRotationStatus(
        age_days=age,
        reminder_due=age >= PASSWORD_REMINDER_DAY,
        update_required=age >= PASSWORD_REQUIRED_DAY,
    )


class PacerAuthClient:
    def __init__(
        self,
        environment: str,
        cache: PacerTokenCache,
        *,
        transport: Optional[PacerTransport] = None,
        timeout_seconds: int = 30,
    ) -> None:
        if environment not in AUTH_ENDPOINTS:
            raise ValueError("environment must be 'qa' or 'production'")
        if cache.environment != environment:
            raise ValueError("cache environment must match auth environment")
        self.environment = environment
        self.cache = cache
        self.transport = transport or requests.Session()
        self.timeout_seconds = timeout_seconds

    def cached_token(self) -> Optional[AuthResult]:
        cached = self.cache.get()
        if cached is None:
            return None
        return AuthResult(
            token=cached.token,
            source="CACHE",
            server_validity="UNKNOWN",
        )

    def get_or_authenticate(
        self,
        credentials: Optional[PacerCredentials] = None,
        *,
        force_reauthenticate: bool = False,
    ) -> AuthResult:
        """Reuse the persisted token by default; do not re-auth per search."""
        if not force_reauthenticate:
            cached = self.cached_token()
            if cached is not None:
                return cached
        if credentials is None:
            raise PacerAuthError(
                "no cached token available; runtime credentials are required"
            )
        return self.authenticate(credentials)

    def authenticate(self, credentials: PacerCredentials) -> AuthResult:
        response = self.transport.post(
            AUTH_ENDPOINTS[self.environment],
            json=credentials.request_body(),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=self.timeout_seconds,
        )
        if getattr(response, "status_code", None) != 200:
            raise PacerAuthError(
                f"PACER authentication HTTP status {getattr(response, 'status_code', 'UNKNOWN')}"
            )
        try:
            data = response.json()
        except Exception as exc:
            raise PacerAuthError("PACER authentication returned non-JSON") from exc

        login_result = str(data.get("loginResult", ""))
        token = data.get("nextGenCSO")
        error_description = str(data.get("errorDescription") or "")
        if login_result != "0" or not isinstance(token, str) or not token:
            raise PacerAuthError(
                "PACER authentication failed"
                + (f": {error_description}" if error_description else "")
            )

        self.cache.put(token, client_code_present=bool(credentials.client_code))
        return AuthResult(
            token=token,
            source="AUTHENTICATION",
            server_validity="ISSUED_BY_PACER",
            error_description=error_description,
        )

    def observe_reissued_token(
        self, token: str, *, client_code_present: bool = False
    ) -> None:
        """Persist a replacement token observed from a PACER response."""
        self.cache.observe_reissued_token(
            token, client_code_present=client_code_present
        )

    def invalidate_on_auth_failure(self) -> None:
        """Local invalidation after a downstream endpoint rejects the token."""
        self.cache.invalidate()

    def logout(self) -> bool:
        cached = self.cache.get()
        if cached is None:
            return False
        response = self.transport.post(
            LOGOUT_ENDPOINTS[self.environment],
            json={"nextGenCSO": cached.token},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=self.timeout_seconds,
        )
        if getattr(response, "status_code", None) != 200:
            raise PacerAuthError(
                f"PACER logout HTTP status {getattr(response, 'status_code', 'UNKNOWN')}"
            )
        try:
            data = response.json()
        except Exception as exc:
            raise PacerAuthError("PACER logout returned non-JSON") from exc
        if str(data.get("loginResult", "")) != "0":
            error_description = str(data.get("errorDescription") or "")
            raise PacerAuthError(
                "PACER logout failed"
                + (f": {error_description}" if error_description else "")
            )
        self.cache.invalidate()
        return True

    @staticmethod
    def court_cookies(
        token: str, *, client_code: Optional[str] = None
    ) -> Dict[str, str]:
        """Cookie semantics for court systems; not for the PCL API."""
        if not token:
            raise ValueError("token must be non-empty")
        cookies = {"nextGenCSO": token}
        if client_code:
            cookies["PacerClientCode"] = client_code
        return cookies
