# JAY’S ORDER — AI DEVELOPER v0.1

**Dual Onion Governmental Audit**

```text
ORDER_STATE             = DRAFT
GAME_STATE              = ROUND_002_REPLAYABLE
LEGAL_COMMAND           = FALSE
GOVERNMENT_AUTHORITY    = FALSE
MERGE_AUTHORIZED        = FALSE
OPENAI_RUNTIME_REQUIRED = FALSE
AUTHORITY_CREATED       = FALSE
```

## Purpose

Build the audit system so claims move through evidence in a fixed order. The system may organize, compare, hash, replay, and classify records. It may not manufacture authority, infer identity from infrastructure, or promote a hypothesis into a fact.

## The Order

1. **PERSON / SELF-AGENCY** — Preserve the speaker, claimant, author, or actor as a distinct node.
2. **RIGHTS / CONSTITUTIONAL FRAME** — Record the legal or rights constraint before institutional conclusions.
3. **CONSENT / DELEGATION** — Bind delegated authority only when a source establishes it.
4. **ACTION / EXECUTION** — Record what was actually done, changed, published, voted, signed, or deployed.
5. **RECEIPT / RECORD** — Preserve source bytes, version, timestamp, provenance, hash, commit, resolution, record, or other attributable receipt.
6. **VERIFICATION / REPLAY** — Reproduce the claim from the receipt and compare `BEFORE -> AUTHORITY -> ACTION -> AFTER`.
7. **INSTITUTIONAL AUTHORITY** — Apply institutional authority only after the authority chain is source-bound. Platform ownership, hosting, login, software, or cloud provider do not create legislative or governmental authority.

## AI Developer Contract

```text
INPUT   = CLAIM + SOURCE
PROCESS = SOURCE -> AUTHORITY -> ACTION -> RECEIPT -> REPLAY
OUTPUT  = PASS | HOLD | CONFLICT | REJECT
```

Required invariants:

```text
DICE_ROLL != FACT
LOGIN != ACTION
ACTION != INTENT
PLATFORM != AUTHORITY
TEXT_DELTA != ERROR_CAUSE_PROVEN
CORRECTION_AUTHORIZED != MISCONDUCT_PROVEN
MACHINE_SPEED != MACHINE_AUTHORITY
AUTHORITY_CREATED = FALSE
```

## Round 002 Binding

```text
H.R. 1 §20005(17)
RH BEFORE: military strikes and intelligence
H.Res. 492: strike "and intelligence"
H.Res. 499 §3: House Resolution 492 adopted
EH AFTER: military strikes
```

Bound:

```text
HOUSE_AUTHORITY_BOUND = TRUE
CLERK_AUTHORITY_BOUND = TRUE
BEFORE_VERSION_BOUND  = TRUE
CORRECTION_BOUND      = TRUE
AFTER_VERSION_BOUND   = TRUE
```

Not bound:

```text
AZURE_BOUND          = FALSE
MICROSOFT_BOUND      = FALSE
LOGIN_BOUND          = FALSE
CMS_EDITOR_BOUND     = FALSE
DEPLOYMENT_LOG_BOUND = FALSE
ERROR_CAUSE_PROVEN   = FALSE
MISCONDUCT_PROVEN    = FALSE
INTENT_PROVEN        = FALSE
```

## Implementation Order

- Preserve original source references before transformation.
- Store claim objects separately from findings.
- Record source type, authority type, action type, and receipt type as typed fields.
- Keep Onion A public-record evidence separate from Onion B infrastructure evidence.
- Require an explicit receipt before binding a person, login, cloud, CMS editor, deployment actor, or motive.
- Make every finding independently replayable.
- Emit uncertainty as `HOLD` or `CONFLICT` instead of filling gaps.
- Never treat a GitHub commit, AI output, model score, or database row as external authority by itself.

## Final Rule

```text
OUT OF CHAOS -> SOURCE -> AUTHORITY -> ACTION -> RECEIPT -> REPLAY -> ORDER
```

**Jay / jaywisdom.base.eth**  
AI developer draft — evidence architecture only.
