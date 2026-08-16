#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.courts.pacer.auth.pacer_auth import (
    PacerAuthClient,
    PacerCredentials,
    password_rotation_status,
)
from adapters.courts.pacer.cache.pacer_token_cache import (
    CacheCorruptionError,
    PacerTokenCache,
)


class FakeSecretStore:
    def __init__(self) -> None:
        self.values = {}

    def get(self, ref):
        return self.values.get(ref)

    def put(self, ref, value):
        self.values[ref] = value

    def delete(self, ref):
        self.values.pop(ref, None)


class FakeResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


class FakeTransport:
    def __init__(self) -> None:
        self.calls = []
        self.auth_token = "A" * 128

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if url.endswith("/cso-auth"):
            return FakeResponse(
                200,
                {
                    "loginResult": "0",
                    "nextGenCSO": self.auth_token,
                    "errorDescription": "",
                },
            )
        if url.endswith("/cso-logout"):
            return FakeResponse(200, {"loginResult": "0", "errorDescription": ""})
        raise AssertionError(f"unexpected URL: {url}")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        secrets = FakeSecretStore()
        cache = PacerTokenCache(root / "cache", "qa", "fixture", secrets)
        transport = FakeTransport()
        client = PacerAuthClient("qa", cache, transport=transport)

        creds = PacerCredentials(
            login_id="fixture-user",
            password="fixture-password",
            otp_code="123456",
            client_code="fixture-client",
            filer=True,
        )
        body = creds.request_body()
        assert body["redactFlag"] == "1"
        assert body["otpCode"] == "123456"

        first = client.get_or_authenticate(creds)
        assert first.source == "AUTHENTICATION"
        assert first.server_validity == "ISSUED_BY_PACER"
        assert len(transport.calls) == 1

        metadata_text = cache.meta_path.read_text(encoding="utf-8")
        assert transport.auth_token not in metadata_text
        assert "fixture-password" not in metadata_text
        assert "123456" not in metadata_text
        assert "fixture-client" not in metadata_text
        metadata = json.loads(metadata_text)
        assert metadata["environment"] == "qa"
        assert metadata["server_validity"] == "UNKNOWN"

        second = client.get_or_authenticate()
        assert second.source == "CACHE"
        assert second.server_validity == "UNKNOWN"
        assert len(transport.calls) == 1

        replacement = "B" * 128
        client.observe_reissued_token(replacement, client_code_present=True)
        assert cache.get().token == replacement

        # ACTIVE metadata without its delegated secret must fail closed.
        secrets.delete(cache.secret_ref)
        try:
            cache.get()
        except CacheCorruptionError:
            pass
        else:
            raise AssertionError("missing delegated token did not fail closed")

        # Restore then validate explicit logout invalidation.
        cache.put(replacement, client_code_present=True)
        assert client.logout() is True
        assert cache.get() is None
        assert cache.metadata().state == "INVALIDATED"
        assert len(transport.calls) == 2

        d179 = password_rotation_status(date(2026, 1, 1), today=date(2026, 6, 29))
        assert d179.age_days == 179
        assert d179.reminder_due is True
        assert d179.update_required is False

        d180 = password_rotation_status(date(2026, 1, 1), today=date(2026, 6, 30))
        assert d180.age_days == 180
        assert d180.update_required is True

    print(
        json.dumps(
            {
                "state": "GREEN",
                "network_calls": 0,
                "real_credentials_used": False,
                "persistent_cache_semantics": "VALIDATED_WITH_FAKE_SECRET_STORE",
                "second_auth_call_avoided": True,
                "reissued_token_replaced": True,
                "missing_secret_fail_closed": True,
                "logout_invalidated": True,
                "password_day_179_reminder": True,
                "password_day_180_required": True,
                "authority": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
