---
lineage_root: 808f2b1c6c339eb46e68a2161da3cca22f7b0eeb
version: 0.1
status: PROPOSED
authority: false
admission_manifest: 236
parent_baseline: COMPUTER_WISDOM_CONSTITUTIONAL_BASELINE_V1
---

# Admission Protocol V0.1

**Status:** PROPOSED  
**Authority:** false  
**Lineage Root:** `808f2b1c6c339eb46e68a2161da3cca22f7b0eeb`  
**Admission Manifest:** Issue #236  
**Parent Baseline:** `COMPUTER_WISDOM_CONSTITUTIONAL_BASELINE_V1`

---

## Purpose

This protocol defines the gates for institutional ingress into the Computer Wisdom repository.

Admission determines whether an artifact is eligible to enter the archive.

Admission does not determine truth.

---

## Core Invariant

> Every conclusion must carry its replayable lineage.

---

## Drift Rule

> If lineage is hidden, authority is invalid.

---

## Gate Specifications

### G0: Origin Traceability

Every artifact must declare a `LINEAGE_ROOT` pointing to a known admitted artifact or to the Constitutional Baseline V1 merge commit.

For this protocol, the lineage root is:

```text
808f2b1c6c339eb46e68a2161da3cca22f7b0eeb
```

### G1: Schema Conformance

Every artifact must conform to its declared schema before admission.

Schema conformance establishes structural eligibility only.

It does not establish truth.

### G2: Witness Validation

Every admitted artifact requires a paired witness path:

- Admission Manifest = Issue
- Admission Object = Pull Request
- Adjudication Event = Merge

An issue may document intent, scope, and lineage.

A pull request is the admission object because it is the governed mechanism capable of modifying repository state.

A merge is the adjudication event because it records the final repository transition.

### G3: Neutrality Constraint

Admission confirms eligibility, not truth.

Artifacts must not silently promote observations, allegations, interpretations, or conclusions into authoritative facts.

Truth-claims require an explicit adjudication path.

### G4: Adjudication Requirement

No artifact is admitted without merge through the governed repository path.

Human-authorized merge is required.

`authority: false` remains enforced unless authority is explicitly established by replayable lineage.

### G5: Revision Gate

Protocol changes must version forward.

Prior versions must remain preserved as replayable history.

No expiry gate is used.

Revision preserves lineage.

Expiry risks deletion of context.

---

## Required Admission Path

1. Create an Admission Manifest issue.
2. Create an implementation branch.
3. Commit the artifact with lineage metadata.
4. Open a pull request into `master`.
5. Reference the Admission Manifest.
6. Allow required repository verification to run.
7. Merge only after repository requirements pass.

---

## Non-Claims

This protocol does not claim that admitted artifacts are true.

This protocol does not adjudicate disputes.

This protocol does not grant implicit authority.

This protocol only defines eligibility for repository ingress.

---

## Anti-Drift Boundary

No event, dispute, transformation, adjudication, protocol, or conclusion may become authoritative unless its lineage can be independently replayed from preserved artifacts.

---

## Final Rule

> Admission decides eligibility. Replay decides computation. Adjudication decides resolution. Observation decides visibility.

**Authority:** false
