# Computer Wisdom: Sovereign OS Broadcast Hub

> **Status: OPERATIONAL CONTROL PLANE**
>
> This repository contains anchor workers, signer routing, deployment tooling, revocation tooling, access-control logic, and replay-court coordination surfaces.
>
> It is the operational backbone for Computer Wisdom / Sovereign OS work, not the canonical Anchor 001 proof source.
>
> **Purpose:** See `docs/PURPOSE.md`.
>
> **Canonical Anchor 001:** `jsonwisdom/Welcome-to-JSONWISDOM`
>
> **Security:** See `SECURITY_BOUNDARY.md`. No keys belong in this repo.

## Replay Root Map

This repository is an operations lane. It can coordinate replay checks, prepare witness payloads, and preserve operational receipts, but it does not replace the canonical proof root.

```text
COMPUTERWISDOM = operational control plane
Welcome-to-JSONWISDOM = canonical Anchor 001 proof source
AL = receipt/proof machinery
EAS = witness layer
ENS = discovery layer
```

Replay law:

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

Boundary law:

```text
GitHub pointer != truth surface
EAS witness != global legitimacy
ENS discovery != authority
```

## Promotion vs Authority

Constitutional separation under the 2026-06-08 receipt stack.

This repository implements a constitutional replay system where Promotion and Authority are intentionally decoupled.

This prevents accidental governance elevation and ensures that all state transitions are evidence-driven.

### Promotion

A PR becomes Promoted when all of the following are true:

- Custody of referenced artifacts is established.
- Replay surface is complete.
- `reproduce.sh` emits a machine-generated attestation.
- CI records the attestation.
- GitHub merges the PR.

Promotion is a ledger event, not a governance event.

Promotion proves:

- Evidence was accepted.
- Replay succeeded.
- The merge is lawful under the doctrine.

Promotion does not grant authority.

### Authority

Authority is a governance capability, not a merge outcome.

Authority can only be elevated through:

- A dedicated authority-elevation PR.
- A governance-level artifact.
- Machine attestation.
- A lineage entry linking the elevation to PAS-001.
- A subsequent Promotion.

Authority is never implied by:

- Merge.
- Promotion.
- Replay success.
- CI attestation.
- Operator action.

This is enforced by:

- Invariant 007: No receipt may claim evidence not observed.
- Clause C-004: Promotion never creates evidence.
- Issue #297 precedent.

### Why Authority Stays False After Promotion

Because Promotion is mechanical.

Authority is constitutional.

```text
Promotion = evidence accepted
Authority = governance granted
```

These are separate chains.

### Tag Verification

To confirm a Promotion is valid:

1. Tag must point to the merge SHA, not the attested head.
2. The merge SHA must match the PR's merge commit.
3. The attestation receipt must reference the attested head.
4. `derivative_map.json` must include the CI receipt.
5. `manifest.json` must include all governance files.
6. `reproduce.sh` must replay cleanly against the tag.

This ensures:

- No time travel.
- No silent mutation.
- No authority leakage.
- No unverified governance.

Step-0 replay court baseline:

```text
replay/instructions/replay_instructions_v1.json
public_coordination/eas_anchor_payload.json
status/master.json
scripts/coordination/build_master_coordination_v2.py
scripts/coordination/verify_replay_step0.py
```

Step-0 scope:

```text
local files only
no network calls
no SALE_VERIFY receipt mutation
no live EAS publication
no inferred finality
```

Acceptance output:

```text
PASS_1_CLEAN_ARTIFACT: MATCH_CONFIRMED
PASS_2_MUTATED_ARTIFACT: FAIL_INVALID
```

## Constitutional Anchor Topology

Canonical Reference Frozen:

- [**FINAL_ANCHOR_TOPOLOGY_v1.md**](./FINAL_ANCHOR_TOPOLOGY_v1.md)
- Branch Pointer: `anchor-topology-v1`
- Frozen Commit: `3dbb071633cb1844d2cf1f6c4bb12a52a8ef83bf`
- Root Hash: `0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b`
- EAS Schema UID: `0x244c84adef25091c97090e6e3f0b1bb932fc7022b913b7546406f4213a202cab`
- EAS Attestation UID: `0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84`
- EAS Transaction Hash: `0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35`

This document defines the constitutional topology, Layer Law, separation of authority surfaces, and zero-drift invariants governing the COMPUTERWISDOM anchor system.

## Purpose

Computer Wisdom is the machine-verification and operations layer of the broader Jay's Wisdom / ALMS architecture.

It exists to help verified records, receipts, deployment actions, signer boundaries, and control-plane events become operational infrastructure that can be audited, repeated, revoked, and trusted without relying on narrative alone.

See `docs/PURPOSE.md` for the full purpose statement.

## Mint-Ready Assets

- [**Scroll Cover Image**](./scroll_cover.png)
- [**Proposal PDF (Stubborn)**](./sovereign_os_proposal.pdf)

## Zora Mint Instructions

1. Visit https://zora.co/create (once online access is restored).
2. Upload `scroll_cover.png` as the NFT's media cover.
3. Paste contents of `sovereign_os_proposal.pdf` as the description.
4. Set royalties to `10%`, mint price `0 ETH`, and edition size as you wish.

This repository is the on-chain mirror for the Sovereign OS proposal, preserved in case Zora, GitHub, or centralized AI systems fail.

## Anchor 001 Boundary

Anchor 001 lives in `jsonwisdom/Welcome-to-JSONWISDOM`.

See `docs/ANCHOR_001_BOUNDARY.md` for the boundary between this operational control-plane repo and the canonical Anchor 001 proof path.

## Author

**Jason Wisdom (Zero Cool)**  
**Sovereign Protocol Architect**  
**TriggerDeck Operator**
Status: Gate 4 Execution (Awaiting CI Receipt)

---

## PR_202_ANTI_DRIFT_NEWS_REPLAY_ENGINE_V1

**Merge note:** This section preserves PR #202 Anti-Drift News replay engine README additions during rebase onto current master.  
**Authority:** false  
**No Fake Green:** active  
**Conflict resolution:** master README preserved; PR #202 README additions appended rather than erased.

---

# Computer Wisdom: Sovereign OS Broadcast Hub

> **Status: OPERATIONAL CONTROL PLANE**
>
> This repository contains anchor workers, signer routing, deployment tooling, revocation tooling, access-control logic, and replay-court coordination surfaces.
>
> It is the operational backbone for Computer Wisdom / Sovereign OS work, not the canonical Anchor 001 proof source.
>
> **Purpose:** See `docs/PURPOSE.md`.
>
> **Canonical Anchor 001:** `jsonwisdom/Welcome-to-JSONWISDOM`
>
> **Security:** See `SECURITY_BOUNDARY.md`. No keys belong in this repo.

## Constitutional Discovery Entry

This repository now includes a constitutional discovery path for Anti-Drift News and the wider Jay Wisdom replay stack.

Quick start:

| Need | Start Here |
|---|---|
| Full constitutional map | [`docs/constitutional_index_v1.md`](./docs/constitutional_index_v1.md) |
| Cross-repo graph | [`docs/repo_constitutional_graph_v1.md`](./docs/repo_constitutional_graph_v1.md) |
| Anti-Drift constitution | [`docs/anti_drift_news/consistency_constitutional_build_v1.md`](./docs/anti_drift_news/consistency_constitutional_build_v1.md) |
| Replay engine spec | [`docs/anti_drift_news/replay_engine_spec_v1.md`](./docs/anti_drift_news/replay_engine_spec_v1.md) |
| Open-source replay client | [`docs/anti_drift_news/open_source_replay_client_spec_v1.md`](./docs/anti_drift_news/open_source_replay_client_spec_v1.md) |
| Replay anomaly schema | [`schemas/replay_anomaly.v1.schema.json`](./schemas/replay_anomaly.v1.schema.json) |

Lineage:

```text
AL -> COMPUTERWISDOM -> JOY -> ENS -> ALMS
```

Invariant:

```text
authority:false
invalid events never change state
valid events always produce deterministic state
server is convenience
client is verification
```

Canon:

```text
This site does not ask you to trust it.
It gives you the math to verify it.

Not anti-news.
Anti-drift.
Public receipts from day one.
```

## Replay Root Map

This repository is an operations lane. It can coordinate replay checks, prepare witness payloads, and preserve operational receipts, but it does not replace the canonical proof root.

```text
COMPUTERWISDOM = operational control plane
Welcome-to-JSONWISDOM = canonical Anchor 001 proof source
AL = receipt/proof machinery
EAS = witness layer
ENS = discovery layer
```

Replay law:

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

Boundary law:

```text
GitHub pointer != truth surface
EAS witness != global legitimacy
ENS discovery != authority
```

Step-0 replay court baseline:

```text
replay/instructions/replay_instructions_v1.json
public_coordination/eas_anchor_payload.json
status/master.json
scripts/coordination/build_master_coordination_v2.py
scripts/coordination/verify_replay_step0.py
```

Step-0 scope:

```text
local files only
no network calls
no SALE_VERIFY receipt mutation
no live EAS publication
no inferred finality
```

Acceptance output:

```text
PASS_1_CLEAN_ARTIFACT: MATCH_CONFIRMED
PASS_2_MUTATED_ARTIFACT: FAIL_INVALID
```

## Constitutional Anchor Topology

Canonical Reference Frozen:

- [**FINAL_ANCHOR_TOPOLOGY_v1.md**](./FINAL_ANCHOR_TOPOLOGY_v1.md)
- Branch Pointer: `anchor-topology-v1`
- Frozen Commit: `3dbb071633cb1844d2cf1f6c4bb12a52a8ef83bf`
- Root Hash: `0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b`
- EAS Schema UID: `0x244c84adef25091c97090e6e3f0b1bb932fc7022b913b7546406f4213a202cab`
- EAS Attestation UID: `0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84`
