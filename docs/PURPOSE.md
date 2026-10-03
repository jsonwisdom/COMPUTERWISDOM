# Computer Wisdom — Purpose

## Core Purpose

`COMPUTERWISDOM` is the operational control plane for the Computer Wisdom / Sovereign OS architecture.

Its purpose is to turn verified records, receipts, deployment actions, signer boundaries, and control-plane events into operational infrastructure that can be audited, repeated, revoked, and trusted without relying on narrative alone.

## Role in the System

Computer Wisdom is not the canonical Anchor 001 proof source.

Computer Wisdom is the operating layer around proof systems.

It may contain or coordinate:

- anchor workers
- finality observers
- signer routing
- GCP KMS integrations
- Foundry deployment scripts
- emergency revocation tooling
- role / access-control policy
- operational mirrors for Sovereign OS assets
- control-plane state transitions

## Relationship to Jay's Wisdom

Jay's Wisdom is the philosophy and operator layer.

Computer Wisdom is the machine-verification and operations layer.

ALMS is the receipt / ledger memory layer.

Together:

```text
Jay's Wisdom → defines the verification ethic
Computer Wisdom → operates the verification machinery
ALMS → preserves receipt memory
```

## Relationship to Anchor 001

Anchor 001 remains canonical in `jsonwisdom/Welcome-to-JSONWISDOM`.

Computer Wisdom may operate around artifacts, signers, workers, and deployments, but it does not replace the canonical proof path.

Current Anchor 001 trust path:

```text
GitHub commit → JCS canonical bytes → SHA-256 → Keccak-256 → EAS attestation on Base
```

ENS remains deferred for Anchor 001.

## What Computer Wisdom Is

Computer Wisdom is:

- an operational control plane
- a signer and deployment boundary
- a machine-auditable infrastructure layer
- a place for control-plane logic that must remain falsifiable
- a bridge between verified records and executable systems

## What Computer Wisdom Is Not

Computer Wisdom is not:

- a private-key storage repo
- a replacement for Anchor 001
- a source of ghost anchors
- a production deployment claim without receipts
- a substitute for revocation, attestation, or byte-level verification

## Computer Wizard Handoff Compiler

The repository also defines **Computer Wizard** as a handoff compiler for source-grounded research and replay work.

Computer Wizard must bind an already-known active target before sending work to a downstream model. It must not replace known context with placeholders such as `TARGET = [INSERT TARGET HERE]`.

The detailed contract lives in:

- [`docs/COMPUTER_WIZARD_REPO_PURPOSE_V1.md`](./COMPUTER_WIZARD_REPO_PURPOSE_V1.md)

Its controlling rule is:

```text
HUMAN INTENT
→ ACTIVE TARGET
→ SOURCE DECK
→ IDENTIFIERS
→ CLAIM
→ GAP LEDGER
→ OUTPUT CONTRACT
→ DOWNSTREAM MODEL

NO RECEIPT → NO JOIN
```

If the target is genuinely undefined, the compiler must stop at `HOLD`; it must not invent one.

## Operating Principle

Verification must survive the operator.

The machine must be able to prove what happened, what signed, what anchored, what failed, and what was revoked.

Rule: receipts over vibes.
