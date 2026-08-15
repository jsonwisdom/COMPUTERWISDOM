# LeeAnn Witness Layer v0.1

**Scope:** Full witness geometry  
**Parent:** Gray Baby preparedness / Minnesota Public Sandbox  
**Place anchor:** Saint Cloud, Minnesota  
**Class:** design-only witness architecture  
**Evidence binding:** none  
**Authority created:** false

This document defines the full witness geometry for PR #474 without binding new evidence, promoting a factual claim, or creating civic, municipal, legal, repository, or protocol authority.

The purpose is to make the witness triad explicit before real Saint Cloud evidence enters the system.

## Frozen scope

```text
SCOPE                 = FULL_WITNESS_GEOMETRY
LEEANN_WITNESS_PATH   = DESIGN_ONLY
SOURCE_BINDING        = NONE
FACT_PROMOTION        = FALSE
CRAWLER               = DISABLED
AUTHORITY_CREATED     = FALSE
```

The existing Saint Cloud evidence lane remains unadvanced.

```text
LEAF_005_RECORDED_STATUS      = PENDING_REAL_EVIDENCE
LEAF_005_EXECUTION_DISPOSITION = HOLD_FOR_REAL_EVIDENCE
```

The prior recorded status is preserved. The execution disposition expresses the current gate; it does not rewrite the earlier receipt.

```text
PENDING_REAL_EVIDENCE -> HOLD_FOR_REAL_EVIDENCE
                       = gate posture
                       != evidence acquisition
                       != source promotion
```

## Minnesota Public Sandbox order

```text
MINNESOTA PUBLIC SANDBOX
        ↓
BOXD MINNESOTA
preservation / replay namespace
        ↓
JAY'S MINNESOTA GAMBIT
bounded replay pattern
        ↓
SAINT CLOUD
local observation anchor
        ↓
FULL WITNESS TRIAD
        ├─ GRAY BABY
        ├─ SAINT CLOUD
        └─ LEEANN
        ↓
MINNESOTA SUPREMESUBSTRATES
foundational provenance / stability plane
        ↓
MINNESOTA_RUNTIME_v0.2
read-only replay / evaluation logic
        ↓
SOURCE NODES
real source binding only after evidence gate
        ↓
VERSIONED PUBLIC VIEWS
public artifacts / replay surfaces
```

The witness layer sits between observation geometry and evidence promotion. It may preserve, classify, explain, and expose gaps. It may not manufacture the missing source.

## The witness triad

### 1. Gray Baby — gap observer

Gray Baby identifies the epistemic gap.

```text
ROLE                 = GAP_OBSERVER
CAN_OBSERVE          = TRUE
CAN_CLASSIFY_GAP     = TRUE
CAN_PRESERVE_CONTEXT = TRUE
CAN_BIND_SOURCE      = FALSE
CAN_PROMOTE_FACT     = FALSE
CAN_CREATE_AUTHORITY = FALSE
```

Gray Baby asks:

```text
What is visible?
What is missing?
What changed?
What is only inferred?
Which source would be required to advance?
```

Gray Baby does not fill the missing field with confidence.

```text
MISSING_EVIDENCE != MODEL_COMPLETION
UNCERTAINTY      != PERMISSION_TO_INVENT
```

### 2. Saint Cloud — local observation anchor

Saint Cloud supplies geographic and civic context for the replay lane.

```text
ROLE                    = LOCAL_OBSERVATION_ANCHOR
PLACE                    = SAINT_CLOUD_MINNESOTA
MUNICIPAL_AUTHORITY      = FALSE
INSTITUTIONAL_AFFILIATION = FALSE
SOURCE_BINDING           = NONE
```

Saint Cloud answers:

```text
Where is the observation situated?
Which public-record lane is being prepared?
Which local version / time / source would be needed for replay?
```

Saint Cloud is not an authority-bearing node.

```text
PLACE_ANCHOR != MUNICIPAL_AUTHORITY
LOCAL        != OFFICIAL
MAPPED       != VERIFIED_SOURCE
```

### 3. LeeAnn — witness / explanation layer

LeeAnn makes the reasoning path legible without replacing evidence.

```text
ROLE                  = WITNESS / EXPLANATION / CONTINUITY
PATH                  = DESIGN_ONLY
CAN_RESTATE_OBSERVED  = TRUE
CAN_EXPOSE_GAPS       = TRUE
CAN_LINK_PROVENANCE   = TRUE
CAN_BIND_SOURCE       = FALSE
CAN_PROMOTE_FACT      = FALSE
CAN_CREATE_AUTHORITY  = FALSE
```

LeeAnn answers:

```text
What did Gray Baby observe?
Where was the observation anchored?
Which evidence is actually present?
Which evidence is absent?
What must remain on HOLD?
What would a human need to review next?
```

LeeAnn is a witness layer, not a source oracle.

```text
WITNESS_PATH != EVIDENCE_BINDING
EXPLANATION  != VERIFICATION
CONTINUITY   != AUTHORITY
```

## Triad interaction

```text
GRAY BABY
OBSERVE + EXPOSE GAP
        ↓
SAINT CLOUD
ANCHOR LOCAL CONTEXT
        ↓
LEEANN
WITNESS + EXPLAIN + PRESERVE GAP
        ↓
HUMAN REVIEW GATE
        ↓
REAL SOURCE PRESENT?
   ├─ NO  -> HOLD_FOR_REAL_EVIDENCE
   └─ YES -> SOURCE VERIFICATION LANE
```

The triad cannot self-promote.

```text
GRAY_BABY + SAINT_CLOUD + LEEANN
                    !=
SOURCE_VERIFICATION
```

No combination of three non-authoritative layers creates authority by accumulation.

```text
FALSE + FALSE + FALSE != TRUE
OBSERVATION + PLACE + EXPLANATION != AUTHORITY
```

## Real-evidence gate

The next legitimate evidence transition requires a real Saint Cloud source package.

Minimum fields remain:

```text
source_url
observed_at
sha256
file_name
byte_size
```

Until those fields are obtained from a real source and independently checked:

```text
SOURCE_PRESENT       = FALSE
SOURCE_VERIFIED      = FALSE
BYTE_IDENTITY        = NOT_BOUND
LEAF_005             = HOLD_FOR_REAL_EVIDENCE
RUNTIME_PROMOTION    = BLOCKED
```

No placeholder may satisfy the gate.

```text
NO INVENTED URL
NO INVENTED TIMESTAMP
NO INVENTED SHA256
NO INVENTED FILE NAME
NO INVENTED BYTE SIZE
```

## Source-node transition

Once real evidence exists, it enters through a separate verification path.

```text
REAL PUBLIC SOURCE
        ↓
CAPTURE ORIGINAL
        ↓
HASH BYTES
        ↓
RECORD TIME + VERSION
        ↓
VERIFY READ-BACK
        ↓
HUMAN REVIEW
        ↓
SOURCE NODE
        ↓
VERSIONED RECEIPT
```

The witness layer does not move downstream merely because a source appears.

```text
SOURCE_APPEARS != SOURCE_VERIFIED
SOURCE_VERIFIED != CLAIM_TRUE
CLAIM_SUPPORTED != AUTHORITY_CREATED
```

## Relationship to BoxD Minnesota

BoxD Minnesota remains the preservation / replay namespace.

```text
BOXD_MINNESOTA:
  ROLE = PRESERVATION / REPLAY
  WRITABLE_BY_WITNESS_LAYER = FALSE
  AUTHORITY = FALSE
```

Witness outputs may reference preserved objects. They may not rewrite the preserved original.

```text
WITNESS_OUTPUT -> DESCENDANT RECEIPT
WITNESS_OUTPUT -X-> ORIGINAL REWRITE
```

## Relationship to Minnesota SupremeSubstrates

The witness geometry does not become a SupremeSubstrate merely because it is complete.

```text
WITNESS_LAYER          = DOWNSTREAM INTERPRETIVE / CONTINUITY LAYER
SUPREMESUBSTRATES      = FOUNDATIONAL PROVENANCE / STABILITY LAYER
WITNESS_IS_SUBSTRATE   = FALSE
```

The foundational order remains:

```text
BOXD
  ↓
MINNESOTA SUPREMESUBSTRATES
  ↓
MINNESOTA_RUNTIME_v0.2
  ↓
SOURCE NODES
  ↓
VERSIONED VIEWS
```

The witness triad is a bounded observation interface around this order; it does not replace it.

## Runtime boundary

Runtime v0.2 may consume verified source objects and preserved receipts. It may not convert a witness statement into a verified source.

```text
WITNESS_STATEMENT -> CONTEXT
VERIFIED_SOURCE   -> SOURCE INPUT
```

Forbidden collapse:

```text
WITNESS_STATEMENT -X-> VERIFIED_SOURCE
DESIGN_GEOMETRY   -X-> FACT
PLACE_LABEL       -X-> GOVERNMENT AFFILIATION
```

## Versioned public views

Public views may expose the state of the witness geometry itself.

Allowed examples:

```text
SAINT_CLOUD_MAPPING_STATUS = OBSERVATION_ONLY
LEEANN_WITNESS_PATH        = DESIGN_ONLY
LEAF_005                   = HOLD_FOR_REAL_EVIDENCE
SOURCE_BINDING             = NONE
```

They must distinguish readiness from evidence.

```text
MAPPED     != SOURCED
PREPARED   != VERIFIED
VISIBLE    != AUTHORITATIVE
```

## Human gate

Human review is mandatory before any source promotion.

The human may:

```text
ACCEPT SOURCE PACKAGE FOR VERIFICATION
REJECT SOURCE PACKAGE
REQUEST MORE CONTEXT
KEEP HOLD
```

The human gate does not convert an unsupported claim into a supported claim.

```text
HUMAN_REVIEW != MAGIC FACT PROMOTION
```

It authorizes a bounded transition in the workflow, not truth itself.

## Full witness state

```text
SCOPE                         = FULL_WITNESS_GEOMETRY
GRAY_BABY_ROLE                = GAP_OBSERVER
SAINT_CLOUD_ROLE              = LOCAL_OBSERVATION_ANCHOR
LEEANN_ROLE                   = WITNESS_EXPLANATION_CONTINUITY
LEEANN_WITNESS_PATH           = DESIGN_ONLY
LEAF_005_RECORDED_STATUS      = PENDING_REAL_EVIDENCE
LEAF_005                      = HOLD_FOR_REAL_EVIDENCE
SOURCE_BINDING                = NONE
FACT_PROMOTION                = FALSE
CRAWLER                       = DISABLED
MUNICIPAL_AFFILIATION         = FALSE
STATE_AUTHORITY               = FALSE
LEGAL_AUTHORITY               = FALSE
AUTHORITY_CREATED             = FALSE
```

## Closing invariant

```text
OBSERVATION != AUTHORITY
WITNESS     != SOURCE
PLACE       != INSTITUTION
DESIGN      != EVIDENCE
PENDING     != PROMOTED
HOLD        != FAILURE
```

Full witness geometry is complete when the system can explain exactly what it knows, where the observation is anchored, what remains missing, and which gate must be crossed next — without inventing the evidence needed to cross it.

`AUTHORITY_CREATED = FALSE`
