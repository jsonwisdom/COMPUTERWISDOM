# Computer Wisdom: Sovereign OS Broadcast Hub

> **Status:** OPERATIONAL CONTROL PLANE  
> **Classification:** CORPORATE_OPERATIONS_ROOT_QUALIFIED  
> **Authority:** false by default  
> **Canonical proof root:** `jsonwisdom/Welcome-to-JSONWISDOM`

`COMPUTERWISDOM` is the qualified corporate operations root for Computer Wisdom / Sovereign OS work. It coordinates operational records, replay receipts, signer boundaries, deployment surfaces, workflow gates, revocation tooling, and machine-auditable control-plane events.

It is **not** the canonical Anchor 001 proof source.

## Quick Start

| Need | Start Here |
|---|---|
| Formal operating charter | [`CHARTER.md`](./CHARTER.md) |
| Root topology / binding map | [`ROOT_BINDING.md`](./ROOT_BINDING.md) |
| Purpose statement | [`docs/PURPOSE.md`](./docs/PURPOSE.md) |
| Security policy | [`SECURITY.md`](./SECURITY.md) |
| Security boundary | [`SECURITY_BOUNDARY.md`](./SECURITY_BOUNDARY.md) |
| Anchor topology | [`FINAL_ANCHOR_TOPOLOGY_v1.md`](./FINAL_ANCHOR_TOPOLOGY_v1.md) |
| Rebase lineage archive | [`ARCHIVE/README_REBASE_NOTES_2026-07-03.md`](./ARCHIVE/README_REBASE_NOTES_2026-07-03.md) |

## Root Map

```text
COMPUTERWISDOM         = corporate / operational doctrine root
Welcome-to-JSONWISDOM = canonical Anchor 001 proof source
AL                     = receipt / proof machinery
receiptos-base         = replay / frame / receipt rail
EAS                    = witness layer
ENS                    = discovery layer
```

## Replay Law

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

## Boundary Law

```text
GitHub pointer != truth surface
EAS witness != global legitimacy
ENS discovery != authority
Promotion != authority
Merge != authority
```

## Authority Boundary

The default posture is:

```text
authority: false
truth_claim: false
```

Authority is never implied by:

- issue creation;
- merge;
- CI success;
- replay success;
- EAS witness;
- ENS discovery;
- operator action.

Authority can only be elevated through a separate governance path with a dedicated authority-elevation PR, machine-readable receipt, replay instructions, review, merge commit, and follow-up witness record.

## Security Boundary

No private keys, seed phrases, wallet exports, service-account JSON files, or live signing material belong in this repository.

See:

- [`SECURITY.md`](./SECURITY.md)
- [`SECURITY_BOUNDARY.md`](./SECURITY_BOUNDARY.md)

## Current Anchor References

From `FINAL_ANCHOR_TOPOLOGY_v1.md`:

```text
anchor_sha256: 0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b
schema_uid: 0x244c84adef25091c97090e6e3f0b1bb932fc7022b913b7546406f4213a202cab
attestation_uid: 0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84
transaction_hash: 0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35
network: base-sepolia
```

Frame / identity-binding UID captured in ReceiptOS frame work:

```text
identity_binding_uid: 0x7ed8784f88dc16d9720dfd0a6d45a21b02f8d5d128eaf529ffeab0002e9c0af6
source_issue: jsonwisdom/receiptos-base#55
```

## Operational Principle

```text
No receipt, no authority.
No replay, no promotion.
No secret in repo.
No fake green.
```

## Author

Jason Wisdom / Jay Wisdom  
`jaywisdom.base.eth`
