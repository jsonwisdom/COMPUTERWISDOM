# THE GOLDEN FLEECE — UNIVERSAL MERKLE CONSTELLATION v0.1

**PROJECT ARGO ∞ / DESIGN ONLY / CANON FALSE / HOLD**  
**Scope:** A navigable narrative-and-provenance index for voyages, research, journalism and public artifacts. This is NOT a new universally trusted root, an operational verifier, a global identity service or a rewrite of existing Merkle protocols.

## Fiction layer

ARGO ZERO carries an expanding *sky map*: every adventure is a star; every verified chain of source references a route; every missing proof appears as a dark star. Jason can fly into any constellation to ask what the captain knew, when, from which artifact, and what an independent reader can recompute.

The Golden Fleece is the **quest to make journeys inspectable**, not an assertion that cryptography makes every story true.

## Technical proposal (no actual hashes computed)

```text
Voyage events / photos / samples / research / episodes
         |     per-source consent and provenance
         v
  Evidence-classed leaves (not all public)
         |     profile-specific hashing
         v
Distinct domain Merkle trees + per-tree roots
         |     explicit bridge receipts if compatible
         v
   Optional bounded voyage manifest(s)
         |     path/type/timestamp/replay scope
         v
 CONSTELLATION VIEW: an indexed graph of root pointers
         |     NOT silently one cryptographic master root
         v
     Human Jason review of story/publication
```

### A root is not a universal truth certificate

- **Hash**: byte-integrity check against a committed digest, under declared rules.
- **Merkle inclusion proof**: membership of a particular leaf in a particular committed tree.
- **Bridge receipt**: documented relationship whose evidence and profiles must themselves replay.
- **Constellation**: an **index of separate, typed roots and dependency edges**, not a shared cryptographic root by default.
- **Forest root**: valid only for a declared, fixed ordering and hashing profile and the trees actually committed.
- **Source provenance**: separate inquiry into origin, authenticity and evidence class.
- **Truth/authority**: not conferred by any of the above.

### Existing incompatible profiles stay incompatible

JOY's AppleBlossom evidence-forest candidate uses domain separation, length-prefixing, evidence classes and an odd-node promotion policy. Existing Store Release, Lapis, AppleBlossom and JSON_MATH_MERKLE proposals may have different leaf encodings, odd-node policies, root scopes and canonicalization rules. Never merge roots into a new historic root by name alone; each must have an independently verified declared profile and bridge.

**Separation invariant:** `CONSTELLATION_VIEW != MERKLE_ROOT != CONTENT_TRUTH != AUTHORITY`.

### Candidate record shape

```json
{
  "schema": "ARGO_CONSTELLATION_REFERENCE_V0_1",
  "record_kind": "DESIGN_EXAMPLE_ONLY",
  "voyage_id": "EPISODE_001_PROPOSED",
  "source_class": "FICTION_PUBLIC",
  "artifact_uri": "PENDING_SOURCE",
  "observed_at_utc": "PENDING",
  "received_at_utc": "PENDING",
  "digest": null,
  "merkle_profile_id": null,
  "tree_id": null,
  "tree_root": null,
  "inclusion_proof": null,
  "bridge_receipt": null,
  "verification_status": "UNRUN",
  "publication_approved_by_jason": false
}
```

**No real hash placeholders masquerading as genuine hashes.**

### Domain separation

Public satire, scientific samples, private home/family, private wallet finance, navigation/safety logs, public audit material, and unpublished research are independent evidence classes with distinct access-control policies. Public-index links may show only release-approved metadata and safely bounded references. Private family/wallet events never auto-export to GitHub or public media.

### Quest mechanics

The player selects one claimed star and gathers original material. A replay classifies the star `UNRUN / HOLD / CONFLICT / VERIFIED_SCOPED`; a verified hash earns an *integrity badge*, not a truth badge. A conflicting root keeps both histories preserved and displays the missing bridge. A player can win by finding a deliberate HOLD.

### Sources and safety

- [COMPUTERWISDOM Merkle Forest Scaling V1](https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/workflows/deepseek-zora-ingestion-v1/merkle_forest_scaling_v1.md)
- [JOY public manifest root boundary](https://github.com/jsonwisdom/JOY/blob/main/README.md)
- [Receipt engine / independent replay prototype](https://github.com/jsonwisdom/receipts-engine-v1/blob/main/README.md)
- Google Drive conceptual provenance reviewed read-only: *AppleBlossomAwesome — Evidence Class Registry + Merkle Forest v0.1* (2026-08-20), maintained privately with its original visibility. No private document links or contents are republished in this GitHub draft.

`FOREST_ROOT_ADOPTED=false`
`CROSS_PROFILE_MERGE=false`
`EXISTING_CANON_MODIFIED=false`
`AUTHORITY_CREATED=false`
`APPROVAL_GATE=JASON`
