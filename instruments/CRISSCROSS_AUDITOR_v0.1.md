# CrissCross Auditor v0.1

Class: `COMPUTERWISDOM_INSTRUMENT`

## Question

Given stored evidence, can a claimed upstream fact be recovered uniquely, or have multiple distinct facts collapsed into the same evidence representation?

CrissCross audits backward:

```text
FORWARD: claim/fact -> process -> stored evidence
REVERSE: stored evidence -> what facts are actually recoverable?
```

If two cases contain different values for the audited claim but produce identical selected evidence, the exact claim is not recoverable from that evidence alone.

```text
E(a) = E(b) AND C(a) != C(b)
    -> CLAIM_RECOVERABLE = FALSE
```

Case IDs, filenames, directory names, and human labels are excluded from evidence unless explicitly selected as evidence fields.

## Boundaries

CrissCross does not determine whether the original claim was true. It determines whether the retained evidence is sufficient to distinguish competing claims.

It creates no authorization and performs no external action.

```text
LABEL_NOT_EVIDENCE=true
AUTHORITY_CREATED=false
```

## Implementation

Canonical executable: `executables/crisscross_auditor_v0_1.py`

Canonical reusable vectors: `fixtures/crisscross_auditor_v0_1/`

Project-specific adapters may construct vectors from their own domain receipts, but must not redefine the core reverse-audit rule.
