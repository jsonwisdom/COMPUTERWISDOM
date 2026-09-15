# CLAWBACK MACHINE — PROTOCOLS V1

**Class:** replay / provenance / institutional-machine audit infrastructure  
**Authority created:** false  
**Verdict created:** false  
**External action:** none  
**Default disposition:** HOLD until receipts close the edge

## Root

ClawBackMachine reverse-replays the machinery that caused an observable object to exist. It does not argue from the final document alone.

```text
WISH
→ OBSERVE
→ PRESERVE
→ ATOMIZE
→ WAYBACK
→ FULL_MATH_AUDIT
→ WIKIATOM_BOMB
→ DELTA_LAYER
→ REPLAY
→ PUBLIC_RECEIPT
→ NEXT_QUESTION
↺
```

Hard membranes:

```text
DOCUMENT != INSTITUTIONAL_CAUSE
SEARCH_RESULT != ARCHIVE
SEARCH_MISS != NONEXISTENCE
CURRENT_STATE != HISTORICAL_STATE
MIGRATION != CREATION
RELEASE_TIME != DOCUMENT_TIME != EVENT_TIME
RECEIPT != AUTHORITY
DELTA != WRONGDOING
HOLD != FALSE
SIMULATION != EVIDENCE
AUTHORITY_CREATED = FALSE
```

---

## 1. WAYBACK_MACHINE_V1

**Purpose:** reconstruct lineage backward from a present object to prior versions, migrations, source systems, actors, clocks, and authority edges.

This is an internal replay primitive. It is not an assertion of affiliation with any external archive service.

### Required lineage record

```text
object_id
object_type
current_pointer
current_hash
source_system
source_version
previous_version
supersedes
created_clock
modified_clock
published_clock
captured_clock
migration_events[]
source_receipts[]
authority_receipts[]
unknowns[]
```

### Migration receipt

Every surface change SHOULD emit:

```text
migration_id
from_surface
to_surface
source_object_id
source_version
source_hash_before
destination_hash_after
migration_clock
transformations[]
omissions[]
operator_or_process
unknowns[]
```

Rules:

```text
HASH_CHANGED -> DELTA, not automatic corruption
HASH_SAME -> byte identity only, not semantic truth
MIGRATION_RECEIPT_MISSING -> HOLD
NEW_SURFACE != NEW_FACT
OLD_VERSION != INVALID_VERSION
```

WayBack output is a version graph, not a single preferred story.

---

## 2. FULL_MATH_AUDIT_V1

Full Math is the completeness membrane for every ClawBack run.

```text
FULL_MATH =
  inputs
+ exclusions
+ clocks
+ receipts
+ contradictions
+ failed_searches
+ unresolved_edges
+ transition_authority
```

### Required audit fields

```text
question
scope
inputs[]
excluded_inputs[]
source_objects[]
clocks[]
receipts[]
contradictions[]
failed_searches[]
unknowns[]
unresolved_edges[]
transition_authority[]
assumptions[]
disposition
next_receipt_required
```

Rules:

```text
DEPTH_OF_RESEARCH != PROOF
PASS != VERIFIED
TRACEABLE_SEQUENCE != PROVEN_CAUSATION
OBJECT != VERDICT
FAILED_SEARCH != NEGATIVE_FACT
NO_PUBLIC_RECEIPT_LOCATED -> HOLD
```

A FullMATH audit is incomplete if an exclusion, failed search, unknown, clock conflict, or transition authority is silently omitted.

---

## 3. WIKIATOM_BOMB_V1

**Class:** NON_DESTRUCTIVE_GRAPH_EXPANSION

The word "Bomb" names a fan-out operation only. It performs no destructive, explosive, offensive, or external action.

### Atom input

```text
WikiAtom {
  atom_id,
  claim_or_object,
  source_pointer,
  observed_clock,
  version,
  state
}
```

### Fan-out

```text
ATOM
├─ RECORD
├─ PROVENANCE
├─ AUTHORITY
├─ CUSTODY
├─ CLOCK
├─ IDENTITY
├─ METRIC
├─ CONTRADICTION
├─ CHALLENGE
├─ MIGRATION
├─ UNKNOWN
└─ NEXT_RECEIPT
```

Each branch becomes its own atom and can recursively fan out.

### Safety / correctness controls

```text
MAX_DEPTH = CONFIGURABLE
VISITED_ATOM_SET = REQUIRED
CYCLE -> RECORD_AND_STOP_BRANCH
MISSING_EDGE -> HOLD
CONFLICT -> PRESERVE_BOTH
PROMOTION_REQUIRES_RECEIPT = TRUE
SIDE_EFFECTS = FALSE
```

The operation does not collapse branches back into a verdict. It expands the graph until each claim can be replayed independently.

```text
WIKIATOM_BOMB != VERDICT_ENGINE
WIKIATOM_BOMB != AUTHORITY_ENGINE
WIKIATOM_BOMB != DELETION
WIKIATOM_BOMB = AUDIT_FAN_OUT
```

---

## 4. DELTA_LAYER_AND_PROTOCOLS_V1

Delta is a first-class object. Every meaningful change is preserved with before/after state and the receipt that observed it.

### Delta object

```text
Delta {
  delta_id,
  object_id,
  base_version,
  head_version,
  base_hash,
  head_hash,
  observed_clock,
  delta_class,
  changed_fields[],
  unchanged_fields[],
  source_receipts[],
  propagation_targets[],
  unknowns[],
  disposition
}
```

### Delta classes

```text
BYTE_DELTA
TEXT_DELTA
STRUCTURE_DELTA
METRIC_DELTA
METRIC_IDENTITY_MISMATCH
CLOCK_DELTA
AUTHORITY_DELTA
CUSTODY_DELTA
SOURCE_SURFACE_DELTA
MIGRATION_DELTA
VERSION_DELTA
ABSENCE_CLAIM_DELTA
UNKNOWN_DELTA
```

### Protocol A — Detect

```text
FREEZE BASE
FREEZE HEAD
COMPARE SAME FIELD DEFINITIONS
EMIT DELTA
```

### Protocol B — Identity gate

A numeric or semantic comparison is forbidden until the objects share compatible identity:

```text
same_subject
same_metric_or_field_definition
same_scope
same_clock_window
same_unit
compatible_method
```

Failure emits `METRIC_IDENTITY_MISMATCH` or `STRUCTURE_DELTA`; it does not permit misleading arithmetic.

### Protocol C — Propagate

A delta MAY trigger dependent replays.

```text
DELTA
→ identify dependents
→ mark stale dependents
→ rerun only affected checks
→ preserve old result
→ write new version
```

Rules:

```text
CHILD_DELTA != PARENT_WRONGDOING
SOURCE_DELTA != INTENT
AUTHORITY_DELTA != ILLEGALITY
CLOCK_DELTA != CAUSATION
```

### Protocol D — HOLD propagation

```text
REQUIRED_PARENT = HOLD
→ DEPENDENT_PROMOTION = BLOCKED
→ DEPENDENT_STATE = HOLD_PARENT_MISSING
```

HOLD propagates only where the missing edge is actually required.

### Protocol E — Public replay

Public output SHOULD contain:

```text
WHAT_WE_OBSERVED
WHAT_CHANGED
WHAT_DID_NOT_CHANGE
WHAT_WE_CAN_REPLAY
WHAT_CONFLICTS
WHAT_IS_UNKNOWN
WHO_OR_WHAT_HAS_AUTHORITY
WHAT_RECEIPT_IS_MISSING
NEXT_QUESTION
```

The public report must expose the receipt path without upgrading interpretation into authority.

---

## Composite run

```text
CURRENT_OBJECT
      ↓
WAYBACK_MACHINE
      ↓
VERSION + MIGRATION GRAPH
      ↓
FULL_MATH_AUDIT
      ↓
WIKIATOM_BOMB
      ↓
INDEPENDENT EVIDENCE ATOMS
      ↓
DELTA_LAYER
      ↓
PASS | DELTA | HOLD
      ↓
PUBLIC REPLAY RECEIPT
      ↓
NEXT QUESTION
      ↺
```

## Optional Monte Carlo sidecar

Monte Carlo runs may perturb missing edges, version order, source availability, migration loss, or clock uncertainty to test **audit resilience**, not truth.

```text
SIMULATED_BRANCH != HISTORICAL_FACT
PROBABILITY_OUTPUT != EVIDENCE
MONTE_CARLO_RESULT != VERDICT
```

Useful outputs:

```text
CAN_REPLAY
CAN_RECOVER_LAST_PROVEN_STATE
CAN_IDENTIFY_MISSING_RECEIPT
CAN_SURVIVE_SOURCE_LOSS
CAN_EXPLAIN_DELTA
```

## State

```text
WAYBACK_MACHINE_V1 = DEFINED
FULL_MATH_AUDIT_V1 = DEFINED
WIKIATOM_BOMB_V1 = DEFINED
DELTA_LAYER_AND_PROTOCOLS_V1 = DEFINED
EXECUTABLE_IMPLEMENTATION = NOT_YET_BOUND
PUBLIC_REPLAY_RUN = NOT_YET_BOUND
AUTHORITY_CREATED = FALSE
NO_FAKE_GREEN = TRUE
```
