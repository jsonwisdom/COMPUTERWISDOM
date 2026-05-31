# CANONICAL_CASEFLOW_V0_2

Status: CANONICAL_INDEX  
Issue: #80  
Parent: #67  
Authority: false  
Membrane: HOLDS  
Mode: CONSOLIDATION_ONLY

## Purpose

This file resolves the caseflow v0.2 artifact-path overlap introduced across PR #69, PR #70, and PR #79.

It does not introduce new runtime behavior. It defines the canonical relationship between already-landed artifacts.

## Canonical Layering

### 1. Canonical state-object schema

Path:

`caseflow/state_machine/schema_v0_2.json`

Role:

Defines the case-level state machine object, including case identity, current state, transitions, and caseflow metadata.

Source:

PR #69

### 2. Canonical transition-rules artifact

Paths:

`caseflow/state_machine/transition_rules_v0_2.md`  
`caseflow/state_machine/transition_rules_v0_2.json`

Role:

Defines allowed transitions, actors, required checks, and membrane behavior for v0.2.

Source:

PR #70

### 3. Canonical transition-receipt schema companion

Path:

`schemas/caseflow_state_machine.v0_2.schema.json`

Role:

Defines the bounded transition receipt shape for explicit from-state / to-state movement. This supplements the case-level schema and does not replace `caseflow/state_machine/schema_v0_2.json`.

Source:

PR #79

### 4. Canonical explanatory companion

Path:

`docs/caseflow_state_machine_v0_2.md`

Role:

Explains the bounded kernel, invariant posture, forbidden promotions, and non-goals.

Source:

PR #79

### 5. Canonical test companion

Path:

`tests/test_caseflow_state_machine_v0_2.py`

Role:

Provides minimal transition fixtures proving valid movement, invalid transition blocking, DISPUTED routing, and authority-false preservation.

Source:

PR #79

## Resolution

PR #79 supplements PR #69 and PR #70. It does not replace them.

The canonical relationship is layered:

1. State-object schema: `caseflow/state_machine/schema_v0_2.json`
2. Transition rules: `caseflow/state_machine/transition_rules_v0_2.md` and `.json`
3. Transition-receipt companion schema: `schemas/caseflow_state_machine.v0_2.schema.json`
4. Documentation companion: `docs/caseflow_state_machine_v0_2.md`
5. Test companion: `tests/test_caseflow_state_machine_v0_2.py`

## Invariant

`NO_SILENT_CATEGORY_PROMOTION`

No artifact in this family grants adjudicative, legal, wallet, ENS, Base, witness, score, or autonomous merge authority.

## Boundary Posture

Authority remains false.  
Observers surface. Witnesses report. Agents play. Verifiers gate. Courts translate. Receipts replay. Humans merge.
