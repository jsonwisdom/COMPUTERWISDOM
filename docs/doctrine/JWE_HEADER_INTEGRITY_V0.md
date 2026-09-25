# JWE HEADER INTEGRITY V0
Date: 2026-09-25
STATUS: LOCAL_WORKING_SHEET
CANON: false
AUTHORITY_CREATED: false

Purpose:
Keep JWE serialization, header placement, authentication, authorization, and account access as separate facts.

## Serialization split

JWE_COMPACT
- five base64url segments
- exactly one recipient
- no unprotected header
- no top-level aad member
- protected header is the authenticated JOSE header surface

JWE_JSON_GENERAL
- one ciphertext may be shared by multiple recipients
- recipients[].encrypted_key wraps the same content-encryption key for each recipient
- recipients[].header is the Per-Recipient Unprotected Header
- unprotected and recipients[].header are not integrity protected by the JWE authentication tag

JWE_JSON_FLATTENED
- exactly one recipient
- header and encrypted_key appear at the top level
- still JSON serialization, not compact serialization

GENERAL_JSON ≠ FLATTENED_JSON ≠ COMPACT

## Header integrity

protected = INTEGRITY_PROTECTED
unprotected = NOT_INTEGRITY_PROTECTED
recipients[i].header = NOT_INTEGRITY_PROTECTED
aad = AUTHENTICATED_NOT_ENCRYPTED
ciphertext = AUTHENTICATED

For JSON serialization, the AEAD Additional Authenticated Data is:
ASCII(BASE64URL(JWE Protected Header))
or, when aad is present:
ASCII(BASE64URL(JWE Protected Header) || "." || BASE64URL(JWE AAD))

TAG_VALID ≠ EVERY_HEADER_AUTHENTICATED

## enc correction

Withdrawn:
"enc is required to live only in protected."

RFC-level rule:
- enc is required.
- all recipients of one JWE use the same content-encryption treatment.
- zip, when present, must be integrity protected.

Application hardening:
- enc SHOULD be placed in protected.
- alg SHOULD be protected where the application profile permits.
- unprotected kid may steer key selection and is not authenticated by the JWE tag.

RFC_REQUIREMENT ≠ APPLICATION_HARDENING

## Non-collapse

ENCRYPTED ≠ SIGNED
SIGNED ≠ AUTHORIZED
AUTHORIZED ≠ EXECUTED
EXECUTED ≠ DELIVERED
JWE ≠ OAUTH_GRANT
JWE ≠ DOMAIN_WIDE_DELEGATION
JWE ≠ DRIVE_ACL
MULTI_RECIPIENT_JWE ≠ MULTI_ACCOUNT_ACCESS

JWE_JSON_BUILT = NOT_RUN
JWE_COMPACT_BUILT = NOT_RUN
DWD = NOT_OBSERVED
SERVICE_ACCOUNT_FLOW = NOT_OBSERVED
CANON = FALSE
