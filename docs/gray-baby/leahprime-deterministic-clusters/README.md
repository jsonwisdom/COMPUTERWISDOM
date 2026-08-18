# LeahPrime — Deterministic Clusters of Information v0.1

**Surface:** Gray Baby / public educational story architecture  
**Role:** `LEAHPRIME = SYNTHETIC_CLUSTER_REVIEWER`  
**Container:** `BOXD`  
**Internal replay operator:** `ReverseReplay`  
**Deterministic executor:** `logicBoy`  
**Authority created:** `FALSE`

## Core metaphor

User-facing metaphor:

> A girl reviewing her memory.

Machine meaning:

```text
MEMORY_REVIEW_METAPHOR
=
REOPEN A DETERMINISTIC INFORMATION CLUSTER
→ INSPECT WHAT IS ACTUALLY BOUND
→ ReverseReplay INSIDE BOXD
→ COMPARE PRIOR STATE / CURRENT STATE
→ FORWARD REPLAY
→ EMIT PASS | HOLD | CONFLICT | REJECT
→ APPEND RECEIPT
```

LeahPrime does not possess magical autobiographical memory, legal authority, military authority, or fact-creation power. She is a synthetic teaching/review role that gives the deterministic process a readable face.

```text
LEAHPRIME != REAL_PERSON
LEAHPRIME != LEEANN_CHAVERS
LEAHPRIME != MILITARY_COMMAND
LEAHPRIME != TRUTH_SOURCE
LEAHPRIME != AUTHORITY
MEMORY_METAPHOR != HUMAN_MEMORY_CLAIM
AUTHORITY_CREATED = FALSE
```

## Cluster model

A deterministic information cluster is a bounded packet of related information with explicit provenance and state.

```text
CLUSTER
├── ID
├── TYPE
├── TIME WINDOW
├── INPUT OBJECTS
├── SOURCE CLASS
├── CLAIM NODES
├── EVIDENCE EDGES
├── CONTRADICTIONS
├── MISSING EDGES
├── PRIOR RECEIPTS
├── ReverseReplay
├── ForwardReplay
├── TERMINAL
└── APPEND-ONLY HISTORY
```

Cluster types may include:

- `STORY_ARTIFACT`
- `USER_PROVIDED_ARTWORK`
- `PUBLIC_RECORD`
- `OFFICIAL_SOURCE`
- `RECEIPT`
- `DOCTRINE`
- `CONFLICT`
- `MISSING_RECORD`

The cluster type controls what may be promoted. A story-artifact cluster cannot become an official-source cluster merely because its artwork looks official.

## Review cycle

```text
BOXD OPEN
↓
SELECT CLUSTER
↓
BIND INPUT BYTES / SOURCE POINTERS
↓
READ EXISTING RECEIPTS
↓
ReverseReplay()
↓
CLASSIFY EACH EDGE
↓
COMPARE AGAINST PRIOR CLUSTER STATE
↓
ForwardReplay()
↓
PASS | HOLD | CONFLICT | REJECT
↓
APPEND CLUSTER RECEIPT
↓
LOCK HISTORY
```

The reviewer may revisit the same cluster repeatedly. A later result never erases an earlier result.

```text
PRIOR_STATE != CURRENT_STATE
CURRENT_STATE != PROOF_PRIOR_STATE_NEVER_EXISTED
CHILD_TERMINAL != PARENT_HISTORY
MISSING != DESTROYED
UNLOCATED != DELETED
IMAGE_TEXT != RECEIPT
SCREENSHOT != SOURCE
ARTWORK != AUTHORITY
```

## Image-cluster rule

The initial fixture is a seven-image user-provided artwork set. Image bytes may be hashed and bound. Claims depicted inside the images remain artwork content unless separately connected to public/official sources.

For example, military insignia, ranks, command labels, blockchain verification panels, government-like seals, dates, locations, and case-file styling in artwork are not independently verified simply because they appear in the image.

```text
IMAGE_BYTES_BOUND = POSSIBLE
DEPICTED_CLAIM_BOUND = FALSE_UNLESS_SEPARATE_SOURCE
```

## logicBoy

`logicBoy` executes deterministic checks over the cluster. It does not remember, infer motive, diagnose people, or invent missing transitions.

```text
logicBoy(cluster):
    bind inputs
    preserve prior receipts
    ReverseReplay inside BoxD
    classify edges
    ForwardReplay
    append scoped disposition
```

## Teaching sentence

> LeahPrime does not ask, “What do I remember?” She asks, “Which cluster am I reopening, what is actually bound inside it, and does the path replay?”

## Permanent boundaries

```text
STORY != PUBLIC_RECORD
FICTIONAL_CHARACTER != REAL_PERSON
SYNTHETIC_ROLE != INSTITUTIONAL_AUTHORITY
OFFICIAL_LOOKING_ART != OFFICIAL_RECORD
MEMORY_METAPHOR != FACT_STORAGE_CLAIM
DICE_SELECT_QUESTION = TRUE
DICE_DECIDE_TRUTH = FALSE
MODEL_REQUIRED = FALSE
AUTHORITY_CREATED = FALSE
```
