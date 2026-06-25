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

## Registration intent

- Resolver: none
- Revocable: false
- Versioned: yes
- Future versions require new schema UIDs

## Operator warning

Admission Controller status is determined by the most granular failure. A Policy Fail (1) prevents pipeline completion just as effectively as a Schema/Receipt Fail (2). Always check exit codes before automated downstream deployments.

## Registration command placeholder

Use EAS SDK or EAS CLI against the target chain and register the schema string above with no resolver and revocable=false.

After registration, record:

```text
network:
schema_uid:
transaction_hash:
explorer_url:
```

## Next rail

After schema registration, v0.4 can add optional attestation checks to `verify_chain.py` without changing receipt semantics.
