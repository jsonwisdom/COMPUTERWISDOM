# ADR-006 — Vendor Absence and Sovereign Recovery

## Status

Proposed

## Context

A durable family and research system cannot depend on the continued existence, goodwill, compatibility, or account access of any software vendor, repository host, cloud provider, identity platform, or AI company.

The architecture must survive a world in which the current commercial tooling never existed or disappears without warning.

## Decision

1. Canonical state is stored as ordinary, documented files in an operator-controlled directory.
2. Git is permitted as a portable history format, but no hosted Git service is authoritative.
3. Hosted repositories are mirrors, publication surfaces, or collaboration copies only.
4. Core artifacts use open and documented formats: UTF-8 Markdown, JSON, JSON Lines, SVG, PNG, PDF/A where appropriate, and detached signatures.
5. Every protected plane has an encrypted offline backup and a documented recovery procedure.
6. Every public release can be reconstructed from frozen source bytes without access to a proprietary application.
7. AI-generated outputs are drafts until accepted by a human and bound to source references and receipts.
8. No cloud-specific identifier may be the sole identifier of an artifact.
9. Migration and restoration tests are governance events and produce receipts.

## Reference topology

```text
OPERATOR-CONTROLLED ROOT
├── JOY/
├── AL/
├── COMPUTERWISDOM/
├── receipts/
├── manifests/
├── keys-public/
└── recovery/

OPTIONAL MIRRORS
├── Git host A
├── Git host B
├── object store
├── content-addressed network
└── encrypted removable media
```

## Failure model

The system must tolerate:

- account suspension;
- vendor shutdown;
- domain loss;
- API removal;
- pricing changes;
- cloud-region loss;
- repository corruption;
- AI-provider replacement;
- loss of a primary device.

## Consequences

- Deployment may require more explicit backup and recovery work.
- Convenience features cannot become hidden trust dependencies.
- Public mirrors remain useful, but they can be replaced.
- A complete recovery drill becomes more valuable than a platform badge.

## Verification gate

This ADR is not operationally satisfied until an independent machine can restore a frozen release from an offline export, reproduce its hashes, replay its receipt chain, and render the public documentation without using the original hosting account.
