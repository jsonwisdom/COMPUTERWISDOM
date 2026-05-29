# BRANCH_INTERACTION_MANIFEST_V1

Constitutional computing layer — evidence-only, no authority.

This manifest describes the standard flow of a proposal through constitutional computing branches.

No branch possesses sovereign authority.

## 1. Proposal Initiation

Legislative creates:

- bills
- schema proposals
- mission amendments
- policy drafts

Legislative publishes structured proposals.

## 2. Review Request (Optional)

If constitutional-consistency review is required, Legislative may forward proposals to Judicial.

Judicial may issue advisory review outcomes:

```text
CONSISTENT
INCONSISTENT
```

The advisory is evidence, not veto authority.

## 3. Executive Acceptance

Executive checks:

- proposal integrity
- review presence when required
- structural validity

If conditions are met, Executive:

- translates proposal into execution sequence
- dispatches runtime
- records execution traces

## 4. Judicial Replay

Executive sends execution traces to Judicial.

Judicial replays and issues:

```text
VALID
INVALID
INCOMPLETE
```

If VALID:

Executive may prepare artifacts for AL admission.

If INVALID or INCOMPLETE:

Executive must not proceed to admission.

## 5. Admission (AL)

AL is the authoritative log surface.

Executive submits:

- resulting artifact
- Judicial replay evidence
- lineage references

AL admits only if:

- replay verdict is VALID
- lineage checks pass
- admission policy passes

AL is not a branch.

It is the constitutional admission surface.

## 6. Sealing

After admission, replay-seal operations finalize artifacts into immutable lineage.

Sealing follows admission.

Sealing does not create sovereignty.

## 7. Inter-Branch Communication Rules

All inter-branch communication must be:

- structured
- signed
- hashed
- versioned
- logged
- replayable
- evidence-only

Messages carry requests or reports.

They do not carry sovereign authority.

## 8. Invariant Preservation

At no point may any branch:

- legislate and execute
- execute and adjudicate
- adjudicate and legislate
- self-seal legitimacy

The constitutional stack remains separated:

```text
Legislative proposes.
Executive coordinates.
Judicial reviews.
AL admits.
Replay seals.
```

## 9. Evidence-Only Doctrine

This manifest is evidence of intended interaction patterns.

It claims no sovereignty.

Political facts require external confirmation.
