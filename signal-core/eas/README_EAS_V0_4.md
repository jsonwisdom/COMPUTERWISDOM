# Receipt Core v0.4: EAS Schema Anchor

Receipt Core v0.4 adds an optional public EAS schema anchor for receipts and receipt bundles.

This does not change local verification semantics.

## Invariant

```text
Authority: NONE
```

The EAS schema is a public coordination point, not an authority grant.

## Schema string

```text
string receiptId,string artifactHash,string claimGraphHash,uint256 claimsCount,string receiptCoreHash,bool authorityNone,string policyHash,string bundleRoot,string version
```

## Registration

```text
network: Base
schema_number: 1618
schema_uid: 0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11
creator: 0xC345B26094c63C69222Ee775189a3d3eaead5a84
transaction_hash: 0x60f9ac0a4d23b112743cc902f4d3f8f06f239664f9b9cc0c3c2909ef682ea7bf
```

## First attestation

```text
attestation_uid: 0x84b58fb78cfde7f791b311c07e5982eeffc3f60b550d594dc9407419ed5d5150
transaction_hash: 0x539c087bb2987bfa3eae4099b0a37765d1ec824e7c6174169745fc440004cab5
receiptId: vr:sha256:fb83118511079eca8bb21adc5b24a7c26971f055c061ddcd4a7d7f532b2b759c
receiptCoreHash: sha256:b2bb199d65e2d4f66cf093fd0d4218341046d892ce3c17cc881c2bda4d66868e
authorityNone: true
version: v0.4
```

## Registration intent

- Resolver: none
- Revocable: false
- Versioned: yes
- Future versions require new schema UIDs

## Operator warning

Admission Controller status is determined by the most granular failure. A Policy Fail (1) prevents pipeline completion just as effectively as a Schema/Receipt Fail (2). Always check exit codes before automated downstream deployments.

## Next rail

After schema registration, v0.4 can add optional attestation checks to verify_chain.py without changing receipt semantics.
