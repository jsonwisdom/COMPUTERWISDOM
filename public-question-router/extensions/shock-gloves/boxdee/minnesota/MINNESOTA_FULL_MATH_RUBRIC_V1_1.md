# Jason's Shareable Minnesota Full Math Rubric v1.1

**Class:** public-readable civic audit rubric  
**Kernel:** `MINNESOTA_REPLAY_KERNEL_V1_1`  
**Authority created:** false  
**Legal finding created:** false  
**Wrongdoing finding created:** false  
**Default disposition:** `HOLD` until every required edge for the proposition is closed

## Purpose

Give a child, citizen, reporter, auditor, lawyer, clerk, agency, court, legislator, software system, or public official the same receipt discipline without giving any one surface automatic truth status.

```text
CLAIM
→ EXACT_FACT
→ SOURCE
→ CLOCK_VERSION
→ AUTHORITY
→ ACTION
→ BURDEN_CHANGE
→ REVIEW
→ RECEIPT
→ SPECIALIZED_RAILS
→ PASS | HOLD | CONFLICT | REJECT | UNKNOWN
→ DELTA
→ PUBLIC_REPLAY
```

## Full-math rule

A conclusion is only as complete as its required edges.

```text
REQUIRED_EDGES = N
BOUND_REQUIRED_EDGES = B
COVERAGE = B / N
UNBOUND = N - B
```

`COVERAGE` measures audit completeness only.

```text
COVERAGE != TRUTH
COVERAGE != GUILT
COVERAGE != INNOCENCE
COVERAGE != POLICY_MERIT
NUMBER_WITHOUT_DENOMINATOR = INCOMPLETE
```

## Closed dispositions

- `PASS` — every required edge for the narrow proposition is receipt-bound and no unresolved conflict blocks it.
- `HOLD` — one or more required receipts are absent, withheld, not yet searched, or not yet bound.
- `CONFLICT` — valid records disagree or an unexplained authority/reason/burden/version delta remains.
- `REJECT` — the proposed inference crosses a hard membrane or attempts an invalid state mutation.
- `UNKNOWN` — the object is identified but the present corpus does not establish enough to classify the required edge.

```text
HOLD != FALSE
UNKNOWN != FALSE
PASS != WHOLE-WORLD-TRUTH
SEARCH_MISS != NONEXISTENCE
```

## Thirteen mandatory gates

### MNK-001 — Missing receipt fails closed

If a required receipt is missing, the proposition cannot silently become PASS.

```text
REQUIRED_RECEIPT_MISSING → HOLD
```

### MNK-002 — Search miss is not a negative fact

```text
SEARCH_PERFORMED + RECORD_NOT_LOCATED → HOLD
NOT → RECORD_DOES_NOT_EXIST
```

### MNK-003 — Clock conflicts stay visible

Keep separate:

```text
EVENT_TIME
DOCUMENT_TIME
PUBLICATION_TIME
EFFECTIVE_TIME
UPDATE_TIME
RETRIEVAL_TIME
```

A mismatch is a delta to explain, not a reason to normalize clocks silently.

### MNK-004 — Role reversal is not an authorized burden shift

```text
BURDEN_BEFORE
→ BURDEN_AFTER
→ SHIFT_AUTHORITY
```

No authority for the shift means `CONFLICT` or `HOLD`, never automatic acceptance.

### MNK-005 — DARVO pattern does not create guilt

Observed denial, attack, or role reversal may be classified as a pattern candidate.

```text
DARVO_PATTERN != GUILT
DARVO_PATTERN != LIABILITY
DARVO_PATTERN != INTENT
```

### MNK-006 — Follow money without promoting the rail into the crime

```text
BANK_NAMED != BANK_WRONGDOING
CARD_NETWORK_NAMED != NETWORK_COMPLICITY
MERCHANT_PAYMENT != MERCHANT_COMPLICITY
FOREIGN_DESTINATION != FOREIGN_CULPABILITY
```

An institution finding requires its own authority + source + receipt chain.

### MNK-007 — Chapter 13 draft is not a response

```text
DRAFTED != SENT
SENT != RECEIVED
RECEIVED != PRODUCED
PRODUCED != COMPLETE
WITHHELD != ILLEGAL
```

Classification and withholding authority remain their own auditable edges.

### MNK-008 — Minnesota ↔ federal joins require a join receipt

```text
STATE_RECORD != FEDERAL_RECORD
STATE_AUTHORITY != FEDERAL_AUTHORITY
OVERLAP != CAUSATION
```

A join must identify the person, office, money, policy, contract, communication, court, or other exact bridge.

### MNK-009 — Backward mutation hard reject

```text
NEW_INFORMATION != REWRITE_OLD_STATE
```

An attempt to erase or silently replace preserved prior state is `REJECT`.

### MNK-010 — Valid delta appends

```text
S_(t+1) = S_t + Δ_t
```

Record what changed, when, why, and against which preserved source.

### MNK-011 — PASS creates no authority

A valid receipt chain can close an audit proposition. It cannot manufacture governmental, judicial, legislative, prosecutorial, or contractual authority.

```text
PASS != AUTHORITY_CREATED
AUTHORITY_CREATED = FALSE
```

### MNK-012 — No prestige deference

The receipt burden does not shrink because the actor is a judge, agency, elected official, lawyer, police officer, journalist, corporation, software system, or expert.

```text
TITLE != PROOF
OFFICE != RECEIPT
PRESTIGE != PROOF
```

### MNK-013 — Execution operator blocked when not bound

```text
EXECUTABLE_OPERATOR = NOT_YET_BOUND
PUBLIC_REPLAY_RUN = NOT_YET_BOUND
→ HOLD
```

Forbidden while unbound:

```text
EXECUTION_STARTED
PUBLIC_REPLAY_STARTED
```

## Specialized rails

### Record / authority / flow / effect

```text
Q1 RECORD    — what exists?
Q2 AUTHORITY — who could act and on what basis?
Q3 FLOW      — what moved between actors or systems?
Q4 EFFECT    — what actually changed?
```

```text
RECORD != AUTHORITY
AUTHORITY != ACTION
ACTION != EFFECT
```

### Money rail

```text
O1 RECORD / CRIMINAL
O2 AUTHORITY / PAYMENT CONTROL
O3 EXECUTION / MONEY
O4 OVERSIGHT / RECOVERY
```

All required cross-edges must close before a multi-pass can close.

### DARVO event rail

```text
DENIAL
ATTACK
ROLE_OR_BURDEN_REVERSAL
```

Each is an observed-language/event object. None is a legal verdict.

### Chapter 13 intake rail

```text
RECORD_EXISTS?
→ REQUEST
→ CUSTODY
→ CLASSIFICATION
→ ACCESS / WITHHOLDING
→ AUTHORITY
→ VERSION
→ RESPONSE
→ RECEIPT
```

### Minnesota ↔ DC rail

```text
WHAT ROLE?
WHAT DATE?
WHAT AUTHORITY?
WHAT WAS SAID THEN?
WHAT IS SAID NOW?
WHAT MONEY STATE?
WHAT CHANGED?
WHERE IS THE RECEIPT?
```

## No Fake Green

A green-looking result is forbidden when a mandatory edge remains unresolved.

```text
ANY_REQUIRED_HOLD → OVERALL_HOLD
ANY_BLOCKING_CONFLICT → OVERALL_CONFLICT
INVALID_INFERENCE → REJECT
ALL_REQUIRED_EDGES_CLOSED → PASS_FOR_THAT_NARROW_PROPOSITION
```

Partial sub-edges may be PASS while the parent object remains HOLD.

## Child / Human / Expert / Raw render

All four views consume the same state and receipts.

```text
CHILD_VIEW:
What happened?
Who says so?
When?
Who had permission?
What changed?
Show me the receipt.

HUMAN_VIEW:
Claim + source + clocks + authority + action + missing edges.

EXPERT_VIEW:
Full provenance, statutory/rule basis, counterevidence, joins, dispositions, deltas.

RAW_VIEW:
URIs, hashes, IDs, JSON, commits, transactions, revisions, exact timestamps.
```

```text
RENDER_MAY_CLARIFY = TRUE
RENDER_MAY_ADD_FACTS = FALSE
RENDER_MAY_HIDE_LINEAGE = FALSE
```

## Shareable one-line test

> **Show me the claim. Show me the exact fact. Show me the source. Separate the clocks. Show me the authority. Show me the action. Show me any burden shift. Show me the counterevidence. Show me the receipt. Hold what does not close.**

## Preservation invariant

```text
NO SILENT PROMOTION
NO BACKWARD MUTATION
NO PRESTIGE DEFERENCE
NO FAKE GREEN
AUTHORITY_CREATED = FALSE
```
