# Reputation Layer — Claim-Scoped, Replayable, Non-Scalar

```text
LAYER                 = REPUTATION
SUBJECT_ROOT          = jaywisdom.base.eth
GLOBAL_SCORE          = PROHIBITED_BY_DEFAULT
AUTHORITY_CREATED     = FALSE
NO_FAKE_GREEN         = TRUE
```

The reputation layer exists around the Mr. Wisdom resume without becoming the resume itself.

Its job is to answer:

- Who is speaking about a claim?
- What relationship do they have to that claim?
- What exactly are they asserting?
- What evidence supports the assertion?
- How good is the receipt?
- How much does the evidence support the particular claim?
- Is the statement current, disputed, superseded, or revoked?

## Canonical reputation states

```text
USER_ATTESTED
DOCUMENT_VERIFIED
THIRD_PARTY_VERIFIED
INFERRED
CONFLICTED
UNVERIFIED
HOLD
```

Existing resume claim-status strings are not silently rewritten. Any migration from legacy status labels requires an explicit mapping and replay receipt.

## Two-field evidence rule

```text
RECEIPT_QUALITY
!=
CLAIM_SUPPORT
```

A complete authentic document may perfectly prove that an institution issued a notice while failing to prove the broader interpretation someone attaches to it.

## No scalar throne

Reputation is represented as scoped edges, not one universal score.

```text
SOURCE --[supports / contradicts / witnesses / supersedes]--> CLAIM
```

Every edge should preserve:

- source identity or source class;
- relationship to the claim;
- exact assertion;
- evidence pointer;
- time window;
- receipt-quality state;
- claim-support state;
- dispute or correction state;
- revocation/supersession status where applicable.

## Institutional scaling

Institutions are evidence providers and decision makers within defined scopes. Institutional status never makes an assertion infallible.

```text
INSTITUTIONAL_RECORD != GLOBAL_TRUTH
INSTITUTIONAL_DECISION != UNREVIEWABLE_TRUTH
REPUTATION != AUTHORITY
```

See `../institutions/` for institution-specific adapters and `mrs-wisdom/` for the human-facing guardian/witness layer.
