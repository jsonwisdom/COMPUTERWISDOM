# logicBoy — ReverseReplay Inside BoxD v0.1

**Lane:** `AMERICAN_CITIZEN_PUBLIC_RECORD`  
**Container:** `BOXD`  
**Internal operator:** `ReverseReplay`  
**Executor:** `logicBoy`  
**Model required:** `FALSE`  
**Authority created:** `FALSE`

## Placement correction

`ReverseReplay` is not a neighboring system beside BoxD.

```text
BOXD
├── BIND ORIGINAL
├── OBSERVE CURRENT STATE
├── FREEZE EVIDENCE GRAPH
├── ReverseReplay()
│   ├── walk claim backward
│   ├── expose transformations
│   ├── expose source records
│   ├── expose claimed authority when relevant
│   └── classify every edge
├── ForwardReplay()
│   └── test whether the claim can be reconstructed without invented edges
├── EMIT SCOPED DISPOSITION
├── APPEND RECEIPT
└── LOCK HISTORY
```

```text
ReverseReplay IN BOXD
ReverseReplay != BOXD
ReverseReplay != TRUTH_SOURCE
ReverseReplay != AUTHORITY
logicBoy != JUDGE
logicBoy != FACT_CREATOR
```

## BoxD execution law

The original statement is frozen before replay. ReverseReplay never edits the claim in order to make the path work.

```text
CURRENT CLAIM
        ↑
DERIVED RECORD
        ↑
TRANSFORM / ACTION
        ↑
SOURCE RECORD
        ↑
AUTHORITY — ONLY IF CLAIMED
        ↑
ORIGINAL STATE
```

The arrow points backward because the operator is testing provenance.

Every transition receives its own state:

```text
MISSING REQUIRED EDGE             -> HOLD
VALID RECORDS DISAGREE             -> CONFLICT
BOUND RECORD CONTRADICTS CLAIM     -> REJECT
ALL REQUIRED EDGES RECONCILE       -> PASS
```

ReverseReplay does **not** stop at the first broken edge. It preserves the complete path so later evidence can be appended without destroying the earlier audit state.

## ForwardReplay is the second half of BoxD

Once the reverse path is exposed, BoxD walks the bound path forward again:

```text
ORIGINAL STATE
→ SOURCE RECORD
→ TRANSFORM / ACTION
→ DERIVED RECORD
→ CURRENT CLAIM
```

Atomic test:

> Can the current claim be rebuilt from bound evidence without inventing a transition?

```text
CURRENT_STATE != PROOF_OF_TRANSITION
SOURCE_EXISTS != TRANSFORMATION_PROVEN
TRANSFORMATION_PROVEN != AUTHORITY_VALIDATED
HASH_MATCH != SEMANTIC_TRUTH
```

## logicBoy

`logicBoy` is the deterministic executor for these BoxD mechanics. Its job is deliberately boring:

1. Read a frozen BoxD state.
2. Traverse declared edges backward.
3. Preserve every edge result.
4. Traverse the surviving path forward.
5. Emit only the narrowest supported terminal.
6. Append a receipt.
7. Never rewrite parent history.

No personality, reputation, vote, model output, or operator confidence can satisfy an evidence edge.

```text
LOGICBOY_EXECUTION != FACT
MODEL_OUTPUT != RECEIPT
POPULARITY != AUTHORITY
CONFIDENCE != VERIFICATION
```

## Teaching fixture — CITIZEN_LEDGER_ITEM_001

The Base Sepolia teaching case now reads as a BoxD internal replay, not a separate ReverseReplay system:

```text
BOXD OPEN
↓
BIND REPOSITORY CLAIM
↓
OBSERVE NO INDEPENDENT CHAIN RECEIPT
↓
HOLD
↓
ReverseReplay(USER-SUPPLIED RPC)
↓
CONFLICT
↓
ReverseReplay(DIRECT UID / RPC / CONTRACT STATE)
↓
DECODER ERROR DETECTED
↓
APPEND FAILED DECODER ATTEMPT
↓
CORRECT DECODER
↓
ReverseReplay(REPEAT DIRECT CALLS)
↓
CHILD REJECT
↓
ForwardReplay()
↓
CLAIM CANNOT BE RECONSTRUCTED ON DECLARED BASE SEPOLIA STATE
↓
BOXD APPEND RECEIPT
↓
LOCK HISTORY
```

Final scope:

```text
PARENT_HISTORICAL_STATE = CONFLICT_PRESERVED
CHILD_RECOVERY_STATE = REJECT_DECLARED_BASE_SEPOLIA_ANCHOR_OBJECTS
GLOBAL_ABSENCE = NOT_PROVEN
MOTIVE = NOT_PROVEN
WRONGDOING = NOT_PROVEN
IDENTITY = NOT_CREATED
```

## Gray Baby translation

```text
RUMOR
→ PUT IT IN THE BOX
→ FREEZE IT
→ REVERSE THE PATH
→ CHECK EVERY TOOTH
→ RUN IT FORWARD
→ KEEP THE RECEIPT
```

The Reverse Screw is therefore a **BoxD mechanic**.

> Don't reverse the answer. Reverse the path inside the box that produced it.

## Permanent boundaries

```text
AMERICAN_CITIZEN != AMERICAN_FAMILY
CITIZEN_RESEARCH = PUBLIC_RECORD_ONLY
JOY_FAMILY_PRIVACY = SEALED
ROUND_06_EXECUTIVE = READY_NOT_ROLLED
MODEL_REQUIRED = FALSE
AUTHORITY_CREATED = FALSE
```
