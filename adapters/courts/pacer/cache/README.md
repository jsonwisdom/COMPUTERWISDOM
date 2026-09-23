# PACER Token Cache

Status: IMPLEMENTED_V0_1
Authority: false
PACER QA validated: false
Production ready: false

Implementation: `pacer_token_cache.py`

Storage model:
- metadata is persisted on disk and partitioned by `qa` vs `production`
- the actual `nextGenCSO` token is delegated to a SecretStore
- normal persistent backend: operating-system keyring via optional Python `keyring` package
- metadata contains only account label, opaque secret reference, timestamps, state, and booleans
- metadata always records server-side validity as `UNKNOWN`

Implemented guarantees:
- no PACER token, password, OTP secret, client code, or secret-derived hash in metadata
- token reuse across process/cron restarts when the delegated secret store persists
- atomic metadata replacement using temporary file + `os.replace`
- explicit environment partitioning
- token replacement when PACER re-issues a token
- logout/auth-failure invalidation removes the delegated token
- ACTIVE metadata with a missing delegated secret fails closed
- unreadable, malformed, mismatched, or unsupported metadata fails closed
- cache existence never claims PACER server validity

Crash boundary:
- secret replacement occurs before metadata replacement
- invalidation deletes the secret before writing INVALIDATED metadata
- if a crash leaves ACTIVE metadata without a secret, the next read hard-fails instead of treating the cache as valid

Do not point `cache_root` into the repository. Runtime cache state belongs in an external application-state directory.

Validation:
- offline fake-secret-store validator exists at `scripts/validation/court/validate_pacer_auth_cache_v0_1.py`
- real OS-keyring persistence and PACER QA login remain unvalidated in this milestone
