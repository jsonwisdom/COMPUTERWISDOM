#!/usr/bin/env python3
"""Persistent PACER token cache with delegated secret storage.

The metadata cache is content-light and contains no PACER token, password,
OTP secret, client code, or secret-derived hash. The token itself is stored
through a SecretStore implementation (KeyringSecretStore in normal use).
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Protocol

CACHE_VERSION = "0.1"
VALID_ENVIRONMENTS = {"qa", "production"}
_SAFE_LABEL = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


class CacheError(RuntimeError):
    pass


class CacheCorruptionError(CacheError):
    pass


class SecretStoreUnavailable(CacheError):
    pass


class SecretStore(Protocol):
    def get(self, ref: str) -> Optional[str]: ...
    def put(self, ref: str, value: str) -> None: ...
    def delete(self, ref: str) -> None: ...


class KeyringSecretStore:
    """Delegate token persistence to the operating-system keyring."""

    def __init__(self, service_name: str = "replay-genesis-pacer") -> None:
        self.service_name = service_name

    @staticmethod
    def _keyring():
        try:
            import keyring  # type: ignore
        except ImportError as exc:
            raise SecretStoreUnavailable(
                "python package 'keyring' is required for persistent PACER secrets"
            ) from exc
        return keyring

    def get(self, ref: str) -> Optional[str]:
        return self._keyring().get_password(self.service_name, ref)

    def put(self, ref: str, value: str) -> None:
        if not value:
            raise ValueError("secret value must be non-empty")
        self._keyring().set_password(self.service_name, ref, value)

    def delete(self, ref: str) -> None:
        keyring = self._keyring()
        try:
            keyring.delete_password(self.service_name, ref)
        except Exception as exc:
            # Backends differ in their exact not-found exception type.
            # A missing secret is already equivalent to deleted here.
            if "not found" not in str(exc).lower():
                raise


@dataclass(frozen=True)
class TokenMetadata:
    cache_version: str
    environment: str
    account_label: str
    secret_ref: str
    state: str
    issued_at: str
    updated_at: str
    client_code_present: bool
    server_validity: str = "UNKNOWN"


@dataclass(frozen=True)
class CachedToken:
    token: str
    metadata: TokenMetadata


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _validate_environment(environment: str) -> str:
    if environment not in VALID_ENVIRONMENTS:
        raise ValueError("environment must be 'qa' or 'production'")
    return environment


def _validate_label(account_label: str) -> str:
    if not _SAFE_LABEL.fullmatch(account_label):
        raise ValueError(
            "account_label must contain only letters, digits, dot, underscore, or hyphen"
        )
    return account_label


class PacerTokenCache:
    """Metadata-on-disk + token-in-secret-store persistent cache.

    A cache hit means only that a token was previously issued and has not been
    locally invalidated. PACER remains the authority on server-side validity.
    """

    def __init__(
        self,
        cache_root: Path,
        environment: str,
        account_label: str,
        secret_store: SecretStore,
    ) -> None:
        self.environment = _validate_environment(environment)
        self.account_label = _validate_label(account_label)
        self.cache_root = Path(cache_root)
        self.secret_store = secret_store
        self.meta_dir = self.cache_root / self.environment
        self.meta_path = self.meta_dir / f"{self.account_label}.json"
        self.secret_ref = f"pacer:{self.environment}:{self.account_label}:nextGenCSO"

    def _read_metadata(self) -> Optional[TokenMetadata]:
        if not self.meta_path.exists():
            return None
        try:
            raw = json.loads(self.meta_path.read_text(encoding="utf-8"))
            meta = TokenMetadata(**raw)
        except Exception as exc:
            raise CacheCorruptionError(
                f"unreadable or invalid PACER cache metadata: {self.meta_path}"
            ) from exc
        if meta.cache_version != CACHE_VERSION:
            raise CacheCorruptionError("unsupported PACER cache version")
        if meta.environment != self.environment:
            raise CacheCorruptionError("PACER cache environment mismatch")
        if meta.account_label != self.account_label:
            raise CacheCorruptionError("PACER cache account-label mismatch")
        if meta.secret_ref != self.secret_ref:
            raise CacheCorruptionError("PACER cache secret reference mismatch")
        if meta.state not in {"ACTIVE", "INVALIDATED"}:
            raise CacheCorruptionError("PACER cache state invalid")
        if meta.server_validity != "UNKNOWN":
            raise CacheCorruptionError("cache must not claim server-side token validity")
        return meta

    def _write_metadata(self, meta: TokenMetadata) -> None:
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            asdict(meta), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ) + "\n"
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{self.account_label}.",
            suffix=".tmp",
            dir=self.meta_dir,
            text=True,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(tmp_name, 0o600)
            os.replace(tmp_name, self.meta_path)
        finally:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass

    def get(self) -> Optional[CachedToken]:
        meta = self._read_metadata()
        if meta is None or meta.state != "ACTIVE":
            return None
        token = self.secret_store.get(meta.secret_ref)
        if not token:
            raise CacheCorruptionError(
                "PACER metadata says ACTIVE but delegated secret is missing"
            )
        return CachedToken(token=token, metadata=meta)

    def put(self, token: str, *, client_code_present: bool) -> TokenMetadata:
        if not token:
            raise ValueError("token must be non-empty")
        current = self._read_metadata()
        now = _utc_now()
        issued_at = (
            current.issued_at
            if current is not None
            and current.state == "ACTIVE"
            and self.secret_store.get(self.secret_ref) == token
            else now
        )
        self.secret_store.put(self.secret_ref, token)
        meta = TokenMetadata(
            cache_version=CACHE_VERSION,
            environment=self.environment,
            account_label=self.account_label,
            secret_ref=self.secret_ref,
            state="ACTIVE",
            issued_at=issued_at,
            updated_at=now,
            client_code_present=bool(client_code_present),
            server_validity="UNKNOWN",
        )
        self._write_metadata(meta)
        return meta

    def observe_reissued_token(
        self, token: str, *, client_code_present: bool
    ) -> TokenMetadata:
        """Replace the delegated token when PACER re-issues it."""
        return self.put(token, client_code_present=client_code_present)

    def invalidate(self) -> TokenMetadata:
        current = self._read_metadata()
        now = _utc_now()
        issued_at = current.issued_at if current is not None else now
        try:
            self.secret_store.delete(self.secret_ref)
        finally:
            meta = TokenMetadata(
                cache_version=CACHE_VERSION,
                environment=self.environment,
                account_label=self.account_label,
                secret_ref=self.secret_ref,
                state="INVALIDATED",
                issued_at=issued_at,
                updated_at=now,
                client_code_present=(
                    current.client_code_present if current is not None else False
                ),
                server_validity="UNKNOWN",
            )
            self._write_metadata(meta)
        return meta

    def metadata(self) -> Optional[TokenMetadata]:
        return self._read_metadata()
