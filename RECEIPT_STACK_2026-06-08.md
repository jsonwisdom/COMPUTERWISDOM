# RECEIPT_STACK_2026-06-08

Status: FROZEN  
Effective: 2026-06-08  
Scope: FED-AI-2026-PAS-001 and descendants  
Verdict Surface: `REALITY_CONFIRMED` | `TOPOLOGY_VIOLATION` | `INCOMPLETE_CHAIN` | `PROHIBITED`

---

## 0. PURPOSE

This document defines the **receipt stack** for federal AI governance artifacts as of 2026-06-08.

It is:

- Machine-executable: every clause corresponds to a check in `make verify`.
- Human-auditable: every check is justified by a constitutional clause.
- Time-proof: no retroactive governance; no silent rule changes.

Any future verifier, tool, or policy must respect this stack or declare a fork.

---

## 1. ANCHOR ARTIFACTS

### 1.1 PAS-001 (Constitutional Anchor)

- Identifier: `FED-AI-2026-PAS-001`
- SHA256: `6246b253637baa349d61e9d6d8ac89ce4943e1d4ef16adba47be49106e48f3d1`
- IPFS: `<CID_GOES_HERE>`
- Role: Defines the doctrine and baseline obligations for AI-related federal evidence.

### 1.2 Governance Ruleset

The following files are **frozen** as of this receipt stack:

- `anti-time-travel.md`
- `derivative-receipt-spec.md`
- `stranger-replay.md`
- `RECEIPT_STACK_2026-06-08.md` (this file)

Their digests are recorded in `manifest.json`. Any verifier MUST:

- Use these exact digests.
- Fail with `PROHIBITED` if any governance file is modified without a new, explicit receipt stack.

---

## 2. TOPOLOGY OF EVIDENCE

Canonical order:

1. Observation
2. Artifact
3. Digest
4. Receipt
5. Derivative Map
6. Replay
7. Promotion

### 2.1 Topology Definition

- **Observation:** A real-world event or directive, such as a White House Executive Order section.
- **Artifact:** A concrete representation, such as a PDF, memo, code file, or dataset.
- **Digest:** Cryptographic hash of the artifact using the declared procedure.
- **Receipt:** A signed or recorded statement binding the digest to a context.
- **Derivative Map:** A machine-readable mapping from source receipts to derivative artifacts.
- **Replay:** A deterministic procedure that re-derives digests and checks lineage.
- **Promotion:** The act of declaring `REALITY_CONFIRMED` and admitting the chain into the ledger.

Any deviation from this order is a **topology violation**.

---

## 3. INVARIANTS (001-007)

These are **physics-level** constraints. They are not negotiable.

- **Invariant 001 — Deterministic Replay**  
  Given the same inputs (`source artifact`, `manifest`, `digest procedure`, `lineage map`), replay MUST produce the same digests and verdicts.

- **Invariant 002 — Single Digest per Artifact**  
  Each artifact MUST have exactly one canonical digest per declared digest procedure.

- **Invariant 003 — Immutable Manifest Entries**  
  Once a file path to digest mapping is recorded in `manifest.json`, it MUST NOT be altered in-place.

- **Invariant 004 — No Orphan Receipts**  
  Every receipt MUST reference an existing digest in the manifest.

- **Invariant 005 — No Orphan Derivatives**  
  Every derivative entry MUST reference at least one valid source receipt.

- **Invariant 006 — Total Ordering of Governance Surfaces**  
  Governance artifacts including PAS-001, this stack, and rules MUST have a clear, acyclic dependency order.

- **Invariant 007 — Stranger-Executable**  
  A stranger with only the repo, `manifest.json`, and `reproduce.sh` MUST be able to reach the same verdicts without external secrets or private context.

Violation of any invariant results in `TOPOLOGY_VIOLATION`.

---

## 4. TEMPORAL RULES (T-001-T-004)

These rules enforce **NO_TIME_TRAVEL_RECEIPTS**.

- **Rule T-001 — Monotonic Governance**  
  No receipt may claim to have been governed by a ruleset that did not yet exist at its timestamp.

- **Rule T-002 — Manifest Time Consistency**  
  A manifest entry's timestamp MUST be less than or equal to any receipt that references its digest.

- **Rule T-003 — No Retroactive Reclassification**  
  An artifact's classification, such as governance, evidence, or derivative, MUST NOT change after first admission.

- **Rule T-004 — Temporal Anchoring of PAS-001**  
  Any chain claiming PAS-001 as its doctrine MUST show that PAS-001's digest was available at or before the origin event.

Violation of any temporal rule results in `PROHIBITED`.

---

## 5. CONSTITUTIONAL CLAUSES (C-001-C-006)

These clauses explain **why** the checks exist.

- **Clause C-001 — Evidence Must Be Replayable**  
  If evidence cannot be replayed by a stranger, it is not admissible as evidence.

- **Clause C-002 — Governance Must Be Inspectable**  
  The rules that govern evidence MUST be readable and auditable by humans.

- **Clause C-003 — No Secret Law**  
  No hidden rules, private configs, or undocumented procedures may affect verdicts.

- **Clause C-004 — No Retroactive Governance**  
  You cannot change the rules after the fact to alter the status of past receipts.

- **Clause C-005 — Lineage Must Be Explicit**  
  Every derivative artifact MUST declare its source receipts in a machine-readable way.

- **Clause C-006 — Equal Replay Rights**  
  Any party, inside or outside government, has the right to run the same replay and obtain the same verdicts.

If a check fails because of missing inputs, not contradiction, the verdict is `INCOMPLETE_CHAIN`, not `PROHIBITED`.

---

## 6. VERIFIER INTERFACE

A verifier requires exactly four inputs:

1. `source artifact`
2. `manifest`
3. `digest procedure`
4. `lineage map`, such as `derivative_map.json`

### 6.1 Success Condition

If all of the following hold:

- Invariants 001-007 pass
- Rules T-001-T-004 pass
- Clauses C-001-C-006 can be mapped to concrete checks and satisfied
- Topology order is respected: Observation -> Artifact -> Digest -> Receipt -> Derivative Map -> Replay -> Promotion

Then the verifier MUST emit:

```text
VERDICT: REALITY_CONFIRMED
```

### 6.2 Failure Modes

- `TOPOLOGY_VIOLATION`: Topology or invariants broken.
- `PROHIBITED`: Temporal rules or constitutional clauses violated, such as time travel or secret law.
- `INCOMPLETE_CHAIN`: Inputs missing; chain cannot be fully evaluated.

---

## 7. STRANGER REPLAY GUARANTEE

A stranger with:

- The repo at a tagged commit
- `manifest.json`
- `derivative_map.json`
- `reproduce.sh`
- This file, `RECEIPT_STACK_2026-06-08.md`

MUST be able to:

- Run `make verify` or `./reproduce.sh`
- Obtain the same digests
- Obtain the same verdicts
- Confirm that governance artifacts match the digests in `manifest.json`

If they cannot, the defect is in documentation or tooling, not in the doctrine.
Such defects MUST be tracked as issues, such as Issue #304: Stranger Replay Failure.

---

## 8. CHANGE PROCEDURE

This receipt stack is FROZEN.

To change any invariant, rule, clause, or topology:

1. Draft a new receipt stack, such as `RECEIPT_STACK_YYYY-MM-DD.md`.
2. Assign it a new identifier and hash.
3. Record it in `manifest.json`.
4. Create a governance receipt explicitly superseding this stack.
5. Tag the repo and update `reproduce.sh` to reference the new stack.

Until such a process is completed and replayable, this stack remains the governing doctrine for PAS-001 descendants.

---

## 9. CANONICAL VERDICT MAPPING

- Invariants + Rules + Clauses all pass -> `REALITY_CONFIRMED`
- Invariant failure -> `TOPOLOGY_VIOLATION`
- Temporal rule or constitutional clause violation -> `PROHIBITED`
- Missing required inputs -> `INCOMPLETE_CHAIN`

This mapping is binding for any verifier claiming compliance with `RECEIPT_STACK_2026-06-08`.
