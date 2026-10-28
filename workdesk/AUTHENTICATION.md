# JASON WORKDESK — AUTHENTICATION CONTRACT V0.1

STATUS: HOLD — NOT IMPLEMENTED

PUBLIC: jsonwisdom.com
PRIVATE: Jason's Workdesk

REQUIREMENTS:
1. Passwordless FIDO2/WebAuthn authentication.
2. User verification required (YubiKey PIN or supported biometric).
3. Only Jason's enrolled credentials are authorized.
4. Server verifies the challenge, origin, and signature.
5. Unauthorized requests cannot retrieve private content.
6. Authentication does not authorize wallet signing or payments.
7. Recovery credentials must be separately enrolled and secured.

ACCEPTANCE TEST:
Public homepage -> Enter Workdesk ->
YubiKey challenge -> PIN/touch ->
Server verification -> Private desktop.

WRONG KEY: DENY
CANCEL: DENY
NO KEY: DENY
VALID KEY + AUTHORIZED USER: ALLOW
