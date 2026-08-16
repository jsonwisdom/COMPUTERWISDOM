# Jaytree Documents — Evidence Mechanics v0.1

**Identity surface:** `jaywisdom.eth`  
**Role:** public-claim laboratory notebook, not authority registry  
**Source class:** `USER_SUPPLIED`  
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

## Experimental membrane

```text
STATE
  ↓
OBSERVED INTERACTION
  ↓
MEASUREMENT
  ↓
EDGE CLASSIFICATION
  ↓
RECEIPT
  ↓
INDEPENDENT REPLAY
  ↓
PASS / GAP / CONFLICT / FAIL
```

## Authority boundary

**Authority cannot repair a broken experimental edge.**

A court ruling may itself become an observable state. An agency report may itself become an observable state. An expert opinion may itself become an observable state.

But if the claim is **X caused Y**, the robe, badge, credential, model, wallet, ENS name, or institutional label cannot substitute for the missing interaction measurement.

## Canonical Jaytree rule

`jaywisdom.eth` is treated here as a laboratory notebook for public claims, not an authority registry.

> Preserve the state. Measure the edge. Publish the receipt. Let somebody else replay it.

## Status

```text
SOURCE = USER_SUPPLIED
TRACEABLE_SEQUENCE = NOT_CAUSATION
CAUSATION_CLAIM = REQUIRES_MEASURED_DEPENDENCY
REPLAY_FAILURE = FIRST_CLASS_EVIDENCE_STATE
AUTHORITY_CREATED = FALSE
```
