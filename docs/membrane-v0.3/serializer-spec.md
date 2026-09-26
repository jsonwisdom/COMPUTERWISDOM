# ReplayOS canonical serializer v1 — draft

Status: DELTA. This document and its code are proposed test artifacts, not a
canonical Membrane specification and not authority.

## Profile

The candidate profile emits UTF-8 canonical JSON using RFC 8785 object-key and
string behavior, with a stricter numeric policy: JSON numbers MUST be signed
integers in the JavaScript safe range [-9007199254740991, 9007199254740991].
Fractions and exponent notation are rejected.

The closed top-level envelope contains exactly:

- `schema_version = replayos-snapshot/1`
- `serializer_version = rfc8785-jcs-int53/1`
- `builder_version = replayos-snapshot-builder/1`
- `lanes`, an object containing state only

`STATE_HASH = lowercase_hex(SHA256(canonical_utf8_bytes))`.

Unicode is preserved; no NFC/NFD normalization occurs. Duplicate object keys,
lone surrogates, unknown envelope fields, versionless envelopes, and forbidden
wall-clock metadata are rejected. Array order is significant. Missing and
`null` are distinct.

## Boundary

This draft deliberately excludes receipts, model rationale, confidence, audit
records, host metadata, paths, process IDs, randomness, and wall-clock values
from snapshot bytes.

Passing these fixtures proves agreement only on the frozen corpus. It does not
prove full RFC 8785 conformance, commit authorization, world truth, or authority.
