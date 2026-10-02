# WisdomPrimeLogic — Scaling Tree Root

```text
SPEC                    = WISDOM_PRIME_LOGIC_V0_1
STATUS                  = DESIGN_PREPARED
DIRECTORIES_FIRST       = TRUE
ONCHAIN_WRITE           = FALSE
RESUME_BYTES_MUTATED    = FALSE
EXECUTION_PERMITTED     = FALSE
AUTHORITY_CREATED       = FALSE
NO_FAKE_GREEN           = TRUE
```

WisdomPrimeLogic is the scaling grammar for `jaywisdom.base.eth`.

It is **not** an institution, authority source, reputation score, truth oracle, or execution engine. Its job is to let the architecture grow without allowing new branches to collapse constitutional types.

## Prime invariant

The typed chain does not change when the system scales:

```text
C1   OBSERVATION
C2   RELATIONSHIP
C3   INTENT
S4   AUTHORIZATION
L5   EXECUTION
L6a  RECEIPT QUALITY
L6b  CLAIM SUPPORT
```

A larger tree gets more nodes and more edges. It does not get permission to skip layers.

## Scaling tree

```text
WISDOM_PRIME_LOGIC
│
├── constitutional-types
│   └── C1 → C2 → C3 → S4 → L5 → L6a / L6b
│
├── subject-graphs
│   ├── Mr. Wisdom résumé / claims
│   └── future subjects
│
├── witness-membrane
│   └── Mrs. Wisdom
│
├── institution-adapters
│   ├── SSA
│   ├── VA
│   ├── banking
│   ├── medical
│   ├── courts
│   ├── education
│   └── employers
│
├── reputation-edges
│   └── claim-scoped / non-scalar
│
├── language-mapping
│   └── ReverseRhetoric → law-mapping vernacular
│
└── replay
    ├── fixtures
    ├── receipts
    ├── corrections
    └── disputes
```

## Prime laws

```text
BRANCH_INHERITS_CONSTRAINTS != BRANCH_INHERITS_AUTHORITY
WITNESS                     != AUTHORITY
INSTITUTION                 != INFALLIBILITY
IDENTITY                    != AUTHORIZATION
REPUTATION                  != TRUTH
RECEIPT_QUALITY             != CLAIM_SUPPORT
MATCHING_RECORDS            != INDEPENDENT_CONSENSUS
CHAIN_WITNESS               != LEGITIMACY
ENS_DISCOVERY               != PERMISSION
```

## Four dimensions of logical scale

### 1. Horizontal scale — more institutions

Add institution-specific adapters while preserving one common constitutional interface.

### 2. Vertical scale — deeper evidence lineage

A claim may acquire sources, receipts, witnesses, contradictions, corrections, supersessions, and revocations without rewriting the original claim.

### 3. Temporal scale — policy and state versions

Rules and decisions are evaluated in the context and time in which they operated. Current policy does not silently rewrite historical state.

### 4. Social scale — more witnesses, not one throne

People and institutions contribute bounded edges. No global reputation score is required.

## Node contract

Every meaningful transition should be able to answer:

```text
WHAT EXISTS?
WHO / WHAT IS RELATED TO IT?
WHAT ACTION IS PROPOSED?
WHAT AUTHORITY SOURCE IS CLAIMED?
IS THAT AUTHORITY VERIFIED FOR THIS ACTION / CONTEXT / TIME?
WHAT ACTION WAS ATTEMPTED?
WHAT ACTUALLY OCCURRED?
WHAT RECEIPT EXISTS?
HOW GOOD IS THE RECEIPT?
WHAT DOES THE EVIDENCE SUPPORT?
WHAT REMAINS DISPUTED OR UNKNOWN?
```

## Promotion rule

Scaling does not manufacture authorization.

```text
OBSERVED
→ CLASSIFIED
→ WITNESSED
→ REPLAYED
→ REVIEWED
→ EXPLICITLY AUTHORIZED
→ EXECUTED
→ RECEIPTED
```

Any missing required transition may produce `HOLD`.

## Canonical replay outcomes

```text
MATCH
DIVERGENCE
INDETERMINATE
INVALID
HOLD
```

These describe replay results. They do not create legal authority or global truth.

## Directory surfaces

- `tree/` — logical growth rules and branch topology.
- `mrs-wisdom/` — witness membrane and anti-laundering discipline.
- `institution-adapters/` — bounded institutional interfaces.
- `replay/` — fixtures, receipts, correction, dispute, and deterministic re-evaluation.

## Plain-language doctrine

> Scale the tree by adding accountable branches. Never scale by silently inheriting authority.
