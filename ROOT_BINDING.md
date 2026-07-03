# COMPUTERWISDOM Root Binding

## Status

```text
repository: jsonwisdom/COMPUTERWISDOM
classification: CORPORATE_OPERATIONS_ROOT_QUALIFIED
canonical_proof_root: false
authority: false
truth_claim: false
issued_at: 2026-07-03
```

## Binding Claim

`COMPUTERWISDOM` is qualified to serve as the corporate / operational doctrine root for Computer Wisdom work.

It is not the canonical proof root.

## Root Map

```text
                           +-------------------------------+
                           | jsonwisdom/Welcome-to-JSONWISDOM |
                           | Canonical Anchor 001 Proof Root  |
                           +---------------+---------------+
                                           |
                                           v
+----------------+        +-------------------------------+        +----------------+
| AL             | <----> | jsonwisdom/COMPUTERWISDOM     | <----> | receiptos-base |
| proof machine  |        | Corporate Operations Root      |        | replay/frame   |
+----------------+        +-------------------------------+        +----------------+
                                           |
                                           v
                                  +----------------+
                                  | EAS / ENS      |
                                  | witness/discovery |
                                  +----------------+
```

## Repository Roles

| Surface | Role | Authority |
|---|---|---:|
| `jsonwisdom/COMPUTERWISDOM` | Corporate operations root / doctrine control plane | false by default |
| `jsonwisdom/Welcome-to-JSONWISDOM` | Canonical Anchor 001 proof source | separate proof root |
| `jsonwisdom/AL` | Receipt/proof machinery | false by default |
| `jsonwisdom/receiptos-base` | ReceiptOS replay / frame / public docket rail | false by default |
| EAS | Witness layer | witness only |
| ENS | Discovery layer | discovery only |
| Zora/Base | Artifact publication / cultural receipt surface | artifact only until verified |

## Signer / Key Boundary

This repository does not claim custody of private keys.

```text
signing_power_in_repo: false
private_keys_allowed: false
service_account_json_allowed: false
wallet_exports_allowed: false
```

Known operational categories may be documented here, but live credentials must remain outside the repository:

- GCP KMS signer routing;
- Foundry deployment preparation;
- emergency revocation tooling;
- Zodiac roles policy patterns;
- workflow receipts;
- dry-run payment preparation.

## EAS / Anchor References

From `FINAL_ANCHOR_TOPOLOGY_v1.md`:

```text
anchor_sha256: 0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b
schema_uid: 0x244c84adef25091c97090e6e3f0b1bb932fc7022b913b7546406f4213a202cab
attestation_uid: 0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84
transaction_hash: 0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35
network: base-sepolia
attester: 0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
```

Frame / identity-binding UID from ReceiptOS frame issue:

```text
identity_binding_uid: 0x7ed8784f88dc16d9720dfd0a6d45a21b02f8d5d128eaf529ffeab0002e9c0af6
source_issue: jsonwisdom/receiptos-base#55
```

## Governance-Receipt Elevation Path

Authority can only be elevated by a separate governance receipt path:

```text
1. open authority-elevation issue
2. create authority-elevation PR
3. define exact capability requested
4. attach machine-readable receipt
5. attach replay instructions
6. pass verifier workflow
7. merge after review
8. bind merge commit hash to receipt
9. publish EAS or equivalent witness record
```

Until completed:

```text
authority: false
truth_claim: false
operational_root: qualified
canonical_proof_root: false
```

## Cross-Reference Table

| Artifact | Location | Status |
|---|---|---|
| COMPUTERWISDOM charter | `CHARTER.md` | proposed in hardening branch |
| Security boundary | `SECURITY_BOUNDARY.md` | existing |
| Security policy bridge | `SECURITY.md` | proposed in hardening branch |
| Anchor topology | `FINAL_ANCHOR_TOPOLOGY_v1.md` | existing |
| Frame MVP docket | `jsonwisdom/receiptos-base#55` | external issue |
| Garbage Pail Kidding Court docket | `jsonwisdom/receiptos-base#56` | external issue |

## Binding Line

```text
COMPUTERWISDOM is the corporate operations root. Welcome-to-JSONWISDOM remains the canonical proof root. AL preserves machinery. ReceiptOS preserves replay. EAS witnesses. ENS discovers. Authority remains false until separately elevated.
```
