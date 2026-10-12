# Jaytree Documents — Evidence Mechanics v0.1

**Identity surface:** `jaywisdom.eth`  
**Role:** public-claim laboratory notebook, not authority registry  
**Source class:** `USER_SUPPLIED`  
**Series 004 posture:** environmental layer integrated  
**Authority created:** `FALSE`

## Core distinction

`TRACEABLE_SEQUENCE != PROVEN_CAUSATION`

Sequence proves chronology. Dependency is what can support causation.

## Edge classes

### TRACE EDGE

**Claim:** B occurred after A.

Evidence may include timestamps, ordering, block height, or commit ancestry.

### DERIVATION EDGE

**Claim:** B was produced from A.

Evidence may include input hash + declared transformation + output hash.

### CAUSAL EDGE

**Claim:** A materially caused B.

This is the stronger claim. It requires measurable dependency, intervention, mechanism, or counterfactual evidence appropriate to the claim.

## Edge invariants

```text
A BEFORE B        != A CAUSED B
A HASHED WITH B   != A CAUSED B
A REFERENCED BY B != A CAUSED B
B DERIVED FROM A   = measurable transformation edge
A CAUSED B         = stronger claim requiring stronger receipt
```

## Law 5 — Replay must expose failure

```text
REPLAY(S0, T) =
  S1        reproduction succeeds
  GAP       required evidence missing
  CONFLICT  measurements disagree
  FAIL      claimed transition cannot reproduce
```

Failure is evidence too. If an independent observer cannot reproduce the edge, the system must not quietly preserve the original conclusion.

## Environmental Layer — Series 004 correction

Series 004 is not agent-only. No observation, receipt, transition, or replay occurs outside an environment.

The environment is not another agent. It is the field of boundary conditions in which states and interactions occur.

### Transition law

```text
(S_n, E_n) --I_n--> (S_(n+1), E_(n+1))
```

Where:

- `S_n` = recorded state
- `E_n` = environment at that state
- `I_n` = measured interaction

State alone is insufficient to explain a transition.

### Environmental state object v0.1

```text
E_n = {
  physical_environment,
  legal_environment,
  institutional_environment,
  network_environment,
  economic_environment,
  social_environment,
  temporal_environment,
  jurisdiction,
  available_resources,
  active_rules,
  incentives,
  constraints
}
```

Each field is a separate evidence lane, not a single undifferentiated context blob.

### Law 6 — No transition exists outside an environment

A receipt proving that A happened before B is not enough to explain the transition unless the material boundary conditions are also recorded.

```text
S_A = S_B
DOES NOT IMPLY
RESULT_A = RESULT_B
WHEN
E_A != E_B
```

### Committee-vote example

A vote is an interaction inside an environment. Material boundary conditions may include chamber rules, statute, jurisdiction, quorum, delegation, and recipient discretion.

```text
VOTE + ENVIRONMENT -> PROCEDURAL EFFECT
```

The vote alone does not determine the downstream effect.

### Platteville-policy example

Policy text is not the human outcome. Material boundary conditions may include classroom, instructor, funding, accreditation, enrollment, disability access, local population, and institutional incentives.

```text
POLICY TEXT + ENVIRONMENT -> ACTUAL HUMAN OUTCOME
```

### CrissCross upgrade

CrissCross must ask:

> What environment had to exist for this claimed transition to occur?

### Enforcement Tail Replay — environment-aware

Forward:

```text
CLAIM
-> LAW
-> AUTHORITY
-> PROCEDURE
-> ENVIRONMENT / BOUNDARY CONDITIONS
-> ACTION
-> RECEIPT
-> EFFECT
```

Reverse:

```text
EFFECT
-> RECEIPT
-> ACTION
-> ENVIRONMENT
-> PROCEDURE
-> AUTHORITY
-> LAW
-> CLAIM
```

A broken required edge produces `HOLD`, not inferred procedural force.

## Experimental membrane

```text
ENVIRONMENT contains [
  STATE
    -> OBSERVED INTERACTION
    -> MEASUREMENT
    -> EDGE CLASSIFICATION
    -> RECEIPT
    -> INDEPENDENT REPLAY
    -> PASS / GAP / CONFLICT / FAIL
]
```

Environment surrounds the apparatus; it does not become a sixth agent.

- BoxD preserves the specimen.
- BitBot verifies the bytes.
- ScrewMath tests constraints.
- GirlMath exposes gaps.
- Ziggy explains.
- LeahPrime reasons.
- Human decides.
- Environment records the forces and boundary conditions acting on all of them.

## Authority boundary

**Authority cannot repair a broken experimental edge.**

A court ruling may itself become an observable state. An agency report may itself become an observable state. An expert opinion may itself become an observable state.

But if the claim is **X caused Y**, the robe, badge, credential, model, wallet, ENS name, or institutional label cannot substitute for the missing interaction measurement or material environmental boundary conditions.

## Canonical Jaytree rule

`jaywisdom.eth` is treated here as a laboratory notebook for public claims, not an authority registry.

> Preserve the state. Measure the edge. Record the environment. Publish the receipt. Let somebody else replay it.

## Status

```text
SOURCE = USER_SUPPLIED
TRACEABLE_SEQUENCE = NOT_CAUSATION
CAUSATION_CLAIM = REQUIRES_MEASURED_DEPENDENCY
REPLAY_FAILURE = FIRST_CLASS_EVIDENCE_STATE
ENVIRONMENTAL_LAYER = INTEGRATED
ENVIRONMENT_IS_AGENT = FALSE
ENVIRONMENTAL_OBJECT = V0_1_DEFINED
SERIES_004_AGENT_ONLY = FALSE
AUTHORITY_CREATED = FALSE
```
