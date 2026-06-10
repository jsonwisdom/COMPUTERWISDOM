# EXECUTIVE_CHARTER_V1

Constitutional computing layer — evidence-only, no authority.

## 1. Branch Identity

Name: Executive Branch (Compute Wisdom)  
Domain: Coordination surfaces for constitutional computation  
Classification: Non-legislative, non-judicial, non-sovereign

Core invariant:

```text
EXECUTIVE_COORDINATES
DOES_NOT_PROPOSE_EXCEPT_PROCEDURAL_REQUESTS
DOES_NOT_ADJUDICATE
DOES_NOT_SELF_SEAL
```

This branch exists to coordinate proposals that have passed appropriate constitutional membranes, not to originate binding directives.

## 2. Purpose

The Executive Branch defines the coordination layer:

- accept legislative proposals such as bills, schema proposals, mission amendments, and policy drafts
- translate accepted proposals into executable mission steps
- dispatch runtime processes such as replay, verification, and sealing preparation
- coordinate with Judicial for replay validation
- coordinate with AL for admission
- ensure all execution is replay-verifiable

It coordinates, not commands.

It runs code, but only code constrained by prior constitutional events.

## 3. Boundaries

The Executive Branch cannot:

- draft bills, schema proposals, mission amendments, or policy drafts, except internal procedural requests that do not change the constitutional structure
- issue verdicts on lineage validity
- admit or reject artifacts into the authoritative log on its own
- finalize seals without replay confirmation
- override Judicial replay outcomes

The Executive holds runtime coordination, but runtime is constrained by proposals, review, admission, and replay.

## 4. Directory Structure

```text
COMPUTERWISDOM/executive/
├── README.md
├── EXECUTIVE_CHARTER_V1.md
├── runtime/
├── dispatch/
├── coordination-logs/
└── procedural-requests/
```

`runtime/` contains execution engines.  
`dispatch/` contains bounded dispatch records.  
`coordination-logs/` records coordination actions for replay review.  
`procedural-requests/` contains non-binding operational requests.

## 5. Executive Process

### 5.1 Proposal Acceptance

A proposal arrives from Legislative with a structured request.

Executive checks:

- proposal integrity
- schema validity
- required preconditions
- required review status when applicable

If Judicial review is pending, Executive holds the proposal in staging until replay verdict is delivered.

### 5.2 Dispatch

When preconditions are satisfied, Executive:

- translates the proposal into an executable sequence
- dispatches to runtime
- records the dispatch event
- records resulting state transitions
- notifies Judicial that new material is ready for replay verification

### 5.3 Coordination with Judicial

Executive never finalizes a state transition as authoritative.

Judicial replay must confirm:

- deterministic replay match
- no invariant violation
- lineage continuity

### 5.4 Coordination with AL

After Judicial confirmation, Executive requests AL admission of the resulting artifact.

Only AL admits.

Executive prepares and offers artifacts; it does not admit them.

## 6. Inter-Branch Membrane

Executive may:

- receive proposals from Legislative
- send execution traces to Judicial
- request admission from AL
- execute runtime operations within bounded scope

Executive may not:

- legislate
- adjudicate
- admit
- seal on its own authority
- alter proposals unilaterally

## 7. Evidence-Only Doctrine

This charter is evidence of intended separation.

No sovereignty is claimed.

Political facts require trusted external confirmation.

## 8. Closing Invariant

The Executive Branch coordinates computational machinery, but the machinery is governed by proposals, review, admission, and replay — never executive fiat.
