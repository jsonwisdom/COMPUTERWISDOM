# PACER Auth

Status: IMPLEMENTED_V0_1
Authority: false
PACER QA validated: false
Production ready: false

Implementation: `pacer_auth.py`

Implemented semantics:
- official QA auth endpoint: `https://qa-login.uscourts.gov/services/cso-auth`
- official production auth endpoint: `https://pacer.login.uscourts.gov/services/cso-auth`
- user-managed 180-day password policy with day-179 reminder helper only
- server-controlled token lifetime; no local TTL is invented
- persistent token reuse by default; no re-authentication per search
- runtime MFA `otpCode` support; no OTP secret is stored here
- `redactFlag=1` only when the caller explicitly marks the account/use as filer-capable
- optional client code is runtime-only and is not serialized by the cache
- court-system cookie builder uses `nextGenCSO` and optional `PacerClientCode`
- no generic bearer-token assumption; PCL-specific header behavior belongs in the PCL adapter
- explicit logout via `/services/cso-logout`
- local invalidation hook for downstream authentication failures
- explicit replacement hook for PACER token re-issuance

Secrets boundary:
- no credentials, tokens, OTP secrets, client codes, or secret-derived hashes in Git
- runtime credentials are accepted only as in-memory inputs
- token persistence is delegated to the cache SecretStore

Validation:
- offline fake-transport validator exists at `scripts/validation/court/validate_pacer_auth_cache_v0_1.py`
- real PACER QA login has NOT been run
