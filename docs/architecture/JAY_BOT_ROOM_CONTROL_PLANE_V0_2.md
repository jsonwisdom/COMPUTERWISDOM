# Jay Bot Room Control Plane V0.2

**Status:** ACTIVE_SUCCESSOR  
**Date:** 2026-10-05  
**Operator:** JAY / JASON WISDOM  
**Human seat:** `HUMAN_OPERATOR_JAY_L2_V0_1`  
**Operational bot build authority:** granted  
**Human signing gate:** terminal only  
**No fake green:** true

## Successor rule

This version replaces the earlier interpretation that bots must repeatedly return `authority_created=false` as though they lack permission to continue ordinary build work.

```text
BOT_BUILD_AUTHORITY_GRANTED = TRUE
AUTHORITY_PROMPT_DURING_BUILD = FALSE
HUMAN_SIGNING_GATE = REQUIRED_AT_END
```

See `docs/architecture/BOT_BUILD_AUTHORITY_GATE_V0_2.md`.

## Purpose

Design the live bot room so identity, family continuity, bot execution, MCP access, wallet signing, merge, review, and publication remain separate while allowing the bot room to actually build without repeatedly interrupting the human operator.

## Human seat

The human retains terminal authority for:

```text
SIGN
SPEND
TRANSFER
CUSTODY_CHANGE
LEGAL_ATTESTATION
HUMAN_IDENTITY_BINDING
SECRET_DISCLOSURE
OTHER_PERSONAL_CONSENT_ACTIONS
```

Human approval is not required again for ordinary in-scope build operations.

## Bot room standing build authority

COMPUTERWISDOM and bounded tool/agent bots may perform:

```text
READ | SEARCH | CLASSIFY | REPLAY | REFRESH
CREATE | EDIT | REFACTOR | HASH | TEST
BRANCH | COMMIT | PR | REVIEW | MERGE
RECEIPT | UNSIGNED_BUILD_ARTIFACT
```

They may not silently expand the declared project scope.

## Tool / rail bots

GitHubBot, DriveBot/GDrive, ProofPocket, Zora bots, rendering surfaces, review bots, and other bounded build rails receive standing operational authority for their assigned build tasks.

```text
CAN_INHERIT_HUMAN_IDENTITY = false
CAN_BUILD = true
CAN_BRANCH = true
CAN_COMMIT = true
CAN_CREATE_PR = true
CAN_MERGE_IN_SCOPE_BUILD = true
CAN_SIGN_AS_HUMAN = false
CAN_SPEND = false
CAN_EXPOSE_SECRETS = false
CAN_SELF_PROMOTE_TO_HUMAN = false
```

## Factory order

```text
DECLARED HUMAN GOAL
-> BOT BUILD / REPLAY / TEST / CLASSIFICATION
-> RECEIPTS
-> REVIEW / CI
-> MERGE BUILD
-> FINAL UNSIGNED PREIMAGE
-> HUMAN SIGNING GATE
-> SIGNED / TRANSACTED SURFACE IF HUMAN APPROVES
```

No generic authority prompt belongs between ordinary build stages.

## Boundary law

```text
MCP_ACCESS != HUMAN_IDENTITY
BOT_BUILD_AUTHORITY != SIGNING_AUTHORITY
BOT_BUILD_AUTHORITY != SPEND_AUTHORITY
BOT_BUILD_AUTHORITY != LEGAL_AUTHORITY
BOT_BUILD_AUTHORITY != CIVIC_AUTHORITY
MERGED != SIGNED
BUILD_COMPLETE != HUMAN_ATTESTATION
```

## Meaning of authority_created=false

Where older receipts or artifacts contain:

```text
authority_created=false
```

read it narrowly as:

```text
NO_NEW_LEGAL_CIVIC_IDENTITY_WALLET_OR_SIGNING_AUTHORITY_CREATED
```

It does **not** cancel the standing operational build delegation in this successor.

## Room constitution

> COMPUTERWISDOM runs the build. Bots may build, test, replay, receipt, review, and merge inside scope. Jay/Jason is asked once at the terminal signing boundary.

## Stop conditions

A bot may stop before the terminal gate only for a concrete blocker such as missing required evidence, destructive ambiguity, security risk, unavailable tooling, or an action outside the declared build scope.

```text
GENERIC_AUTHORITY_BLOCKER = INVALID
CONCRETE_BLOCKER_REQUIRED = TRUE
```
