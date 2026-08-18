# SOURCE_BYTES_RECEIPT_V0.1

## Purpose

Freeze and classify the exact bytes observed from an external or supplied source without silently promoting transport success, a URL, a digest, a source label, or the source's own statement into truth or authority.

## Replay chain

```text
SOURCE LOCATOR
↓
FETCH STATUS
↓
OBSERVED BYTES
↓
SHA-256 + BYTE LENGTH
↓
OPTIONAL EXPECTED DIGEST COMPARISON
↓
SOURCE IDENTITY STATUS
↓
CONTENT ASSERTION CLASS
↓
TYPED RECEIPT
```

## Core membranes

```text
LOCATOR_EXISTS != BYTES_FETCHED
BYTES_FETCHED != BYTES_MATCH_REFERENCE
BYTES_MATCH_REFERENCE != SOURCE_IDENTITY_AUTHENTICATED
SOURCE_IDENTITY_AUTHENTICATED != CONTENT_ASSERTION_TRUE
SOURCE_BYTES_AUTHENTICATED != WORLD_FACT_PROVEN
SAME_DIGEST != SAME_SOURCE_IDENTITY
SAME_LOCATOR != SAME_BYTES_OVER_TIME
RECEIPT != TRUTH
RECEIPT != AUTHORITY
```

A fetched object with no expected digest may still produce a reproducible observation receipt: the machine can prove which digest and byte length it observed. That is **not** the same claim as proving the bytes match a previously committed reference.

## Typed disposition

```text
SEMANTIC_TYPE = BOUNDED_SOURCE_BYTES_RECEIPT_DISPOSITION
DISPOSITION   = PROVEN | HOLD | REJECTED
```

`PROVEN` means only that the bounded byte-receipt gates for the supplied fixture resolved successfully. It never means an allegation, factual proposition, source identity, legal conclusion, or government endorsement is proven.

```text
VALUE = PROVEN
WITHOUT SEMANTIC_TYPE = BOUNDED_SOURCE_BYTES_RECEIPT_DISPOSITION
→ INVALID EXTERNAL OUTPUT
```

## v0.1 scope

`v0.1` is intentionally synthetic and fail-closed.

```text
LIVE_NETWORK_FETCH          = OUT_OF_SCOPE
MODEL_EXECUTION             = FALSE
SOURCE_IDENTITY_AUTHORITY   = NOT_CREATED
CLAIM_VERIFICATION          = FALSE
WORLD_FACT_PROVEN           = FALSE
AUTHORITY_CREATED           = FALSE
```

The deterministic verifier tests semantic and byte-comparison behavior only. A later live-ingestion layer may fetch external bytes, but that layer must emit this receipt shape and may not widen it.

## Iron Bowl translation

```text
URL              = LABEL ON THE FILM CAN
FETCH             = PUT THE FILM IN THE MACHINE
SHA-256           = FINGERPRINT THE FILM
EXPECTED SHA      = RECEIPT FOR THE FILM WE EXPECTED
MATCH             = SAME FILM BYTES AS THE RECEIPT
SOURCE IDENTITY   = WHO ACTUALLY ISSUED THE FILM
CONTENT ASSERTION = WHAT THE FILM SAYS OR SHOWS
REFEREE / COURT   = SEPARATE AUTHORITY
```

Opening the file is not a touchdown. Matching the file is not a verdict.
