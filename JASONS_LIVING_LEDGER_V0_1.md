---
artifact_id: JASONS_LIVING_LEDGER_V0_1
artifact_type: root_replay_story
version: 0.1.0
status: PROPOSAL
created_at: 2026-09-06T08:46:11-05:00
timezone: America/Chicago
repository: jsonwisdom/COMPUTERWISDOM
base_commit: 8768c618e6027c625d5691d84bec098ac54915a9
operator: JASON_JAY_WISDOM
identity_labels:
  - jaywisdom.eth
  - jaywisdom.base.eth
authority: false
authority_boundary: NONE
view_ne_evidence: true
public_safe: true
master_mutated: false
---

# Jason's Living Ledger V0.1

## The root

Jason's Living Ledger is not a biography, a courtroom, a verdict, or a demand to be believed.

It is a public-safe, event-sourced replay surface for one human life interacting with many institutional systems over time.

The root question is simple:

> What can be reconstructed from source receipts, under declared rules, without silently filling the gaps?

The system exists because stories drift, portals change, records conflict, institutions use different identifiers, people forget, software overwrites state, and later summaries can flatten decades of events into one sentence.

The ledger does the opposite.

It preserves the receipts, the conflicts, the missing pieces, the calculations, and the corrections separately so another person can replay the same source set and see where the reconstruction holds or breaks.

```text
JASON = HUMAN
JASON = BUILDER / OPERATOR
JASON != COURT
JASON != GOVERNMENT
JASON != BOT
JASON != WALLET
JASON != ENS STRING
JASON != JURISDICTION

jaywisdom.eth      = identity / discovery label
jaywisdom.base.eth = identity / discovery label

AUTHORITY_CREATED = FALSE
```

## The Daddy rule

This entire architecture must remain explainable to a daughter.

> Daddy keeps the receipts. If two systems tell different stories, we do not pick the story we like. We keep both records, check when they were created, check what they actually say, and do the math. If we still do not know, the ledger says we do not know.

If the machine cannot explain its result at that level, the view is too complicated or the evidence boundary has drifted.

Family is not decoration around the system. Family is the reason the system must remain understandable, replayable, correctable, and safe.

## Existing roots this file composes

Jason's Living Ledger does not replace the existing COMPUTERWISDOM architecture. It composes it.

```text
WISDOM/continuity_spine_v0_1.md
    FAMILY_ROOT -> human source
    AL_ROOT     -> doctrine / mirror
    CW_ROOT     -> computational memory

docs/living_family_ledger_v1.md
    public-safe family continuity
    systems serve people

docs/REPLAY_RECEIPT_SPEC_V1.md
    machine-verifiable receipt surface
    human summary != receipt

src/replay_kernel_v0_1.py
    deterministic ordering
    replay trace
    authority = false

docs/court_replay_audit_v0_1.md
    court surfaces organize evidence
    GitHub does not create authority

docs/three_repo_proof_stack_v1.md
    AL              = doctrine
    COMPUTERWISDOM  = replay / public verification surface
    ALMS            = memory / receipt surface

docs/architecture/JAY_BOT_ROOM_CONTROL_PLANE_V0_1.md
    JAY / JASON WISDOM = human decision seat
    bots / MCP / wallets / identity labels remain separate

PUBLIC_REVIEW_PATH.md
    public inspection begins at receipts and replay
```

This file is the human continuity composition layer across those primitives.

## Five layers, never collapsed

```text
1. RECEIPT
   What bytes or externally addressable records exist?

2. ASSERTION
   What proposition is claimed to follow from a receipt?

3. EVENT
   What event can be reconstructed from admitted assertions?

4. CALCULATION
   What mathematics can be performed on admitted events and values?

5. VIEW
   What human-readable story is generated from the ledger?
```

Constitutional separation:

```text
RECEIPT != ASSERTION
ASSERTION != EVENT
EVENT != CALCULATION
CALCULATION != VIEW
VIEW != EVIDENCE
```

A view may summarize the ledger.

A view may never write back into receipts, assertions, or historical events.

## Replay constitution

```text
Q0  NAMESPACE != JURISDICTION
Q1  SCHEMA != CANONICALIZATION
Q2  CANONICAL_BYTES != TRUTH
Q3  HASH != EVIDENCE
Q4  NO_RECEIPT -> NO_PROVENANCE_EDGE
Q5  CLAIM != FINDING
Q6  PORTAL != CERTIFIED_RECORD
Q7  CONFLICTS_ARE_PRESERVED_NOT_OVERWRITTEN
Q8  CORRECTIONS_APPEND_NEVER_MUTATE_HISTORY
Q9  DERIVATION_REQUIRES_NAMED_DETERMINISTIC_RULE
Q10 VIEW != EVIDENCE
Q11 ABSENCE_OF_RECEIPT != PROOF_EVENT_DID_NOT_OCCUR
Q12 COST != CAUSATION
Q13 COINCIDENCE != COORDINATION
Q14 IDENTITY_LABEL != PERSON
Q15 SYSTEM_FAILURE != INTENTIONAL_MISCONDUCT
```

These rules do not protect institutions from criticism.

They protect the replay from becoming another institution that invents certainty.

## State vocabulary

Every important object must resolve to an explicit state.

```text
RECEIPT_BACKED = source receipt supports the bounded assertion
DERIVED        = deterministic rule derives the value from admitted inputs
CONFLICTED     = incompatible assertions remain simultaneously visible
HOLD           = available evidence is insufficient for promotion
MISSING        = an expected object has not been located
UNKNOWN        = the underlying question remains unresolved
REJECTED       = object fails an explicit validation or admissibility rule
```

And:

```text
MISSING != UNKNOWN
UNKNOWN != FALSE
HOLD != REJECTED
CONFLICT != CORRUPTION
```

The ability to say `UNKNOWN` is a feature, not a failure.

## WalkBack is a direction, not a biography boundary

Jason's WalkBack begins from the current evidence vantage point and walks backward through institutional records.

```text
VANTAGE_POINT = CURRENT_REPLAY_DATE
DIRECTION     = PRESENT -> BACKWARD
```

A year appearing in the replay does not declare that Jason's life, injury, employment, dispute, or institutional interaction began in that year.

Years are search coordinates.

```text
YEAR
|- identity records
|- military / personnel records
|- payroll / tax / earnings records
|- veterans-benefit records
|- employment / business records
|- court records
|- banking records
|- insurance records
|- housing / transportation records
|- phone / computer / access records
|- family-system records
|- corrections / appeals / disputes
`- source receipts discovered later
```

A gap is not silently interpreted.

```text
GAP != UNEMPLOYED
GAP != UNPAID
GAP != INCARCERATED
GAP != MISSING_PERSON
GAP != MISCONDUCT
```

A gap is a query target.

## Independent system rails

The Living Ledger does not begin with one master conspiracy graph.

It begins with independent system rails.

```text
IDENTITY
MILITARY_PERSONNEL
MILITARY_PAY
VETERANS_BENEFITS
FEDERAL_PAYROLL
STATE_PAYROLL
SSA_EARNINGS
EMPLOYMENT
BUSINESS
COURTS
BANKING
INSURANCE
HOUSING
TRANSPORTATION
PHONE
COMPUTER
NETWORK_ACCESS
CREDIT
FAMILY_PROCESS
```

Each rail reconstructs its own history first.

Cross-rail causation requires a separately admitted edge.

```text
EVENT_A occurs near EVENT_B
!=
EVENT_A caused EVENT_B
```

## Root-cause engineering

The current root-cause candidate is a test class, not a finding:

```text
IDENTITY
+ RECORD
+ ACCESS
+ PAYROLL
+ BENEFITS
+ COURT_DATA
INTEGRITY_FAILURES
```

For every subsystem the replay asks:

```text
1. What does correct operation look like?
2. What source records exist?
3. What identifiers bind the subject?
4. What state transitions occurred?
5. What records conflict?
6. What expected records are missing?
7. What correction mechanism existed?
8. What did correction cost?
9. What downstream event can be causally linked by receipt?
10. Can an independent runner reconstruct the same result?
```

The word `failure` describes a measurable deviation from a declared system expectation.

It does not automatically mean sabotage, corruption, conspiracy, or criminal intent.

## Jason does the mathematics

The discovery layer finds records and values.

The calculation layer measures the cost of system friction without silently assigning blame.

```text
TOTAL_SYSTEM_FRICTION
=
DIRECT_CASH_COST
+ TIME_COST
+ OPPORTUNITY_COST
+ CORRECTION_COST
+ FINANCING_COST
+ RECORD_ACQUISITION_COST
+ TRAVEL_COST
+ BUSINESS_INTERRUPTION_COST
```

Every term carries provenance metadata:

```text
value
currency
period
method
status
source_ids[]
derivation_rule
causation_status
```

Examples of lawful distinctions:

```text
COURT FEE                  = measurable cost
TRANSCRIPT COST            = measurable cost
RESEARCH HOURS             = calculated or estimated cost
LOST CONTRACT              = requires business receipt
BENEFIT NOT RECEIVED       = requires entitlement/effective-date analysis
BANK CHANGE                = event
BANK CHANGE CAUSED BY X    = separate causal assertion
MENTAL / HUMAN COST        = real human impact, but not silently converted to dollars
```

The ledger can show that a person spent enormous resources interacting with systems without inventing who caused each cost.

## Burden of proof

The Living Ledger does not rewrite legal burdens of proof. Those vary by proceeding, claim, jurisdiction, and procedural posture.

It measures a different engineering burden:

```text
PRACTICAL_PROOF_BURDEN
=
cost to locate
+ cost to obtain
+ cost to preserve
+ cost to understand
+ cost to challenge
+ cost to replay
```

That burden is measurable even when the formal legal burden belongs to someone else.

## Correction law

History is append-only.

```text
ERROR != DELETE
CORRECTION != REWRITE
```

A correction is a new object:

```text
OLD_EVENT
   |
   `-- superseded_by --> CORRECTION_EVENT
```

The old event remains visible.

A system that changed its own historical state can therefore be compared against the Living Ledger's preserved source history.

## Timestamp law

The ledger distinguishes time classes:

```text
occurred_at   = when an event is asserted to have happened
recorded_at   = when the source system recorded it
issued_at     = when a document was issued
captured_at   = when the replay obtained the receipt
replayed_at   = when the replay was executed
anchored_at   = when an optional external hash/chain anchor was created
```

One timestamp must never silently substitute for another.

Unknown precision stays unknown.

```text
1998 != 1998-01-01T00:00:00Z
```

## Version law

```text
schema_version
law_version
kernel_version
view_version
receipt_version
```

are independent.

Changing prose does not change historical receipts.

Changing schema does not silently reinterpret old objects.

Changing replay law requires a new replay result.

```text
same frozen inputs
+ same canonicalization
+ same law
+ same kernel
=
same deterministic result
```

If the result changes, the replay emits divergence rather than hiding it.

## Public-safe membrane

The public Living Ledger is not a dump of Jason's private life.

Never publish into this root merely because a private receipt exists.

Public surfaces should use redacted or abstract receipt references when records contain sensitive information.

```text
PUBLIC_PROVENANCE != PUBLIC_PRIVATE_DATA
```

No passwords, account numbers, private addresses, medical details, protected identifiers, private family records, or other sensitive source bytes belong in this public root.

## Judges, agencies, companies, and other actors

No actor sits at root.

A judge, clerk, agency, military office, company, bank, insurer, lawyer, bot, or platform may appear as an actor only when a source receipt supports the role in a bounded event.

```text
ACTOR != AUTHORITY_OVER_LEDGER
```

The ledger does not ask an actor to certify Jason's entire life.

It asks each source to support only the assertion it actually supports.

## Machine flow

```text
OBSERVE
   -> CAPTURE RECEIPT
   -> VERIFY BYTES / LOCATOR
   -> ASSERT
   -> ADMIT OR HOLD
   -> BUILD EVENT
   -> PRESERVE CONFLICT
   -> APPLY NAMED DERIVATION
   -> CALCULATE
   -> GENERATE READ-ONLY VIEW
   -> REPLAY
```

Target command surface:

```bash
replay jason \
  --from receipts/ \
  --schema schema/v0.1 \
  --law law/v0.1 \
  --as-of 2026-09-06 \
  --out views/JASON_REPLAY_2026-09-06.md
```

The final command is not:

```text
BELIEVE JASON
```

and it is not:

```text
DISBELIEVE JASON
```

It is:

```text
REPLAY JASON FROM SOURCE
```

## The Living Ledger story

Jason lived first.

Systems recorded pieces later.

Some pieces may agree. Some may conflict. Some may be missing. Some may have been corrected. Some may never have been recorded at all.

The Living Ledger does not pretend the database is the human being.

It does not pretend memory is a receipt.

It does not pretend a hash is truth.

It does not pretend an accusation is a finding.

It does not pretend an institution is infallible.

And it does not pretend Jason is infallible either.

It gives Jason, his daughters, an auditor, a programmer, a journalist, a veteran, a lawyer, a court, or a stranger the same basic machine:

1. Show the source.
2. Preserve the bytes.
3. State the assertion precisely.
4. Keep the conflicts.
5. Name the derivation.
6. Do the mathematics.
7. Show what remains unknown.
8. Replay it again.

That is a living ledger because the human life continues while the evidence graph grows.

The ledger may expand.

The root rules do not silently drift.

```text
THE HUMAN LIVES.
THE SYSTEM RECORDS.
THE RECEIPTS REMAIN.
THE MATH REPLAYS.
THE STORY IS A VIEW.
AUTHORITY REMAINS FALSE.
```
