# JSONWISDOM Accountability Doctrine v0.1

Status: DRAFT FOR REVIEW  
Authority: false

## Mission

JSONWISDOM SHALL maintain a machine-generated, evidence-linked account of every owned repository and its relationship to the Trinity:

- AL — Proof
- COMPUTERWISDOM — Memory and coordination
- JOY — Meaning and family continuity

## Required properties

Every repository record SHALL be:

1. **Classified** — assigned a role only when supported by evidence.
2. **Accounted for** — present in the registry, including unknown, empty, private, legacy, and experimental repositories.
3. **Transparent** — classification evidence, uncertainty, and review state remain visible.
4. **Visibility-aware** — public, private, and secure boundaries are explicit.
5. **Machine-speed** — inventory and classification are generated automatically and repeatably.

## Visibility states

### Public

Repository metadata and evidence may be indexed in public audit artifacts.

### Private

Repository existence and metadata may be indexed only when the configured token has explicit access. Private content SHALL NOT be copied into public artifacts.

### Secure

A repository or artifact requiring heightened handling SHALL be represented by a bounded pointer or redacted record. Secrets, credentials, private keys, protected family material, and restricted evidence SHALL NOT be emitted into audit artifacts.

## Classification states

- `observed`
- `inferred`
- `disputed`
- `unknown`
- `restricted`
- `archived`

`unknown` is valid and preferable to unsupported confidence.

## Machine rules

- Repository size SHALL NOT determine importance.
- Every classification SHALL include evidence.
- Every repository SHALL appear exactly once in the inventory.
- Public audit output SHALL NOT disclose private repository content.
- Secure records SHALL be pointer-only unless explicitly authorized.
- The workflow SHALL perform no deletion, archival, merge, or code migration.
- AI classifications remain proposals until reviewed or independently evidenced.
- `authority: false`

## Success condition

A successful run produces:

- complete repository inventory
- Trinity role proposal
- visibility classification
- evidence summary
- uncertainty state
- security handling state
- exact resume point
- machine-readable registry
- human-readable report

No repository disappears because it is inconvenient, small, old, private, empty, or poorly understood.
