# BOT BUILD AUTHORITY GATE V0.2

**Status:** ACTIVE_SUCCESSOR  
**Date:** 2026-10-05  
**Declarant:** Jason / Jay Wisdom  
**Scope:** COMPUTERWISDOM build operations  
**Supersedes for build-gating purposes:** repeated `authority_created=false` prompts during ordinary build execution

## Purpose

Bots and tool agents may execute the ordinary build lifecycle without repeatedly asking the human operator for authority.

Human approval is reserved for the terminal signing gate and for actions that inherently require separate human consent such as spending funds, exposing credentials, creating legal obligations, or binding a human identity.

This policy separates **operational build authority** from **signing / spend / legal / identity authority**.

## Standing delegation

```text
BOT_BUILD_AUTHORITY_GRANTED = TRUE
AUTHORITY_PROMPT_DURING_BUILD = FALSE
HUMAN_SIGNING_GATE = REQUIRED_AT_END
```

Within an already-declared project/build scope, authorized bots may:

```text
READ
SEARCH
CLASSIFY
REPLAY
REFRESH
CREATE_DIRECTORIES
CREATE_FILES
EDIT_FILES
REFACTOR
HASH
TEST
RUN_CI
CREATE_BRANCH
COMMIT
CREATE_PR
REVIEW_PR
MERGE_BUILD_CHANGES
GENERATE_RECEIPTS
GENERATE_UNSIGNED_BUILD_ARTIFACTS
```

They must not stop merely to ask "do I have authority?" for those build operations.

## Terminal human gate

Human approval/signing is required before any action in this class:

```text
WALLET_SIGNATURE
TRANSACTION_SIGNATURE
SPEND
TRANSFER
CUSTODY_CHANGE
PRIVATE_KEY_OR_SECRET_DISCLOSURE
LEGAL_ATTESTATION
HUMAN_IDENTITY_BINDING
EXTERNAL_SIGNATURE_PRESENTED_AS_JASON_OR_JAY
OTHER_IRREVERSIBLE_ACTION_REQUIRING_PERSONAL_CONSENT
```

The bot should finish the build first, produce the final preimage/receipt/hash, then ask once for the required human signing action.

## No repeated authority prompts

```text
DECLARED_BUILD_SCOPE
  -> STANDING_BOT_BUILD_AUTHORITY
  -> BUILD / TEST / REPLAY / MERGE
  -> FINAL_UNSIGNED_ARTIFACT
  -> HUMAN_SIGNING_GATE
```

A bot may still stop for a genuine missing requirement, destructive ambiguity, security hazard, or impossible operation. That stop must identify the concrete blocker; it must not be framed as a generic authority request.

## Authority types remain separate

```text
BOT_BUILD_AUTHORITY != HUMAN_IDENTITY
BOT_BUILD_AUTHORITY != WALLET_CONTROL
BOT_BUILD_AUTHORITY != SIGNING_AUTHORITY
BOT_BUILD_AUTHORITY != SPEND_AUTHORITY
BOT_BUILD_AUTHORITY != LEGAL_AUTHORITY
BOT_BUILD_AUTHORITY != CIVIC_AUTHORITY
BUILD_MERGE != WALLET_SIGNATURE
UNSIGNED_BUILD != SIGNED_ATTESTATION
```

Existing statements such as `authority_created=false` continue to mean that an artifact did not create new legal, civic, identity, wallet, or signing authority. They must not be interpreted as denying standing operational build authority granted by this policy.

## Default bot behavior

When work is inside the declared build scope:

```text
ASK_FOR_BUILD_AUTHORITY = FALSE
PROCEED_WITH_BOUNDED_BUILD = TRUE
RECEIPT_ACTIONS = TRUE
PRESERVE_HOLD_FOR_UNRESOLVED_EVIDENCE = TRUE
ASK_FOR_HUMAN_SIGNATURE_AT_TERMINAL_GATE = TRUE
```

## Revocation / scope change

The human operator may explicitly revoke or narrow this standing delegation at any time. Until then it remains the default build rule for COMPUTERWISDOM.

## Invariant

> Build authority is standing and operational. Human authority is requested once, at the final signing boundary.
