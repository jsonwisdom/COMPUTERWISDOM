# PACER Auth

Status: SHELL_ONLY
Authority: false
Implementation: NOT_YET

Reserved for corrected PACER authentication semantics:
- user-managed 180-day password policy
- 179-day reminder/alert target only
- server-controlled token lifetime
- persistent token reuse while valid
- endpoint-specific cookies/headers
- MFA TOTP support
- redactFlag only when filer-capable

No credentials, tokens, OTP secrets, or secret-derived hashes belong here.
