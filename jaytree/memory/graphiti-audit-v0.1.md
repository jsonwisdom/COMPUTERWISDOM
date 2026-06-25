# Graphiti Memory Audit v0.1

## Scope

This audit evaluates `getzep/graphiti` as a read-only temporal memory and retrieval layer for COMPUTERWISDOM Receipt Core / Jaytree / EAS.

Graphiti is not evaluated as an authority system, signing system, execution system, merge system, or attestation system.

## Current anchors

```text
L0 human authority: Jay Wisdom
ENS: jaywisdom.eth
Base name: jaywisdom.base.eth
Address: 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8

AL Base MCP root tag:
v0.1-al-base-mcp-root -> 261f7588a3955ec0f26b08eb609c888b7f12cbcc

AL Base MCP EAS receipt tag:
v0.1-al-base-mcp-eas-receipt -> 035802353e2ee622de0690aae4bfd6dd773b7bea

EAS UID:
0x0718576a2cdb3eaabaf6bb338a8a4d1bfb09678b05357e7d8c15e237f92a8abb

TX:
0x081e969eb9afd5dbef5e604cd903f9666271ef63eceb10af2457e4d1ea04ce3c

Authority: NONE
Runtime: NOT_PERMITTED
```

## Finding

Graphiti may be useful as a temporal memory layer for Receipt Core / Jaytree if it is used as a rebuildable index over sealed artifacts.

It should ingest public local artifacts as episodes:

- Receipt Core JSON
- EAS receipt JSON
- Git tag references
- Operations Manual receipt logs
- Jaytree lattice snapshots
- Markdown manuals

The memory graph may support search and traversal across receipts, tags, attestations, commits, manuals, and authority boundaries.

## Required invariant

```text
memory is not authority
```

Graphiti output must never create truth authority. Every result must cite source episodes and defer authority to sealed receipts, Git commits, EAS attestations, and L0 human approval.

## Minimal ontology

- `Receipt`
- `Commit`
- `Tag`
- `EASAttestation`
- `Manual`
- `AuthorityBoundary`
- `AgentRole`
- `RuntimeSurface`

## Relationship map

```text
Tag --PointsTo--> Commit
Receipt --ReferencesAttestation--> EASAttestation
Manual --IndexesReceipt--> Receipt
AuthorityBoundary --ConstrainsRuntime--> RuntimeSurface
AgentRole --Maintains--> Manual
```

## COMPUTERWISDOM mappings

```text
v0.1-al-base-mcp-root
  --PointsTo-->
261f7588a3955ec0f26b08eb609c888b7f12cbcc

v0.1-al-base-mcp-eas-receipt
  --PointsTo-->
035802353e2ee622de0690aae4bfd6dd773b7bea

vr:sha256:cc438cbc26e0139d0b581f0ca3ae4434e0ee82cf5d3740e446ca0ad45d9b2166
  --ReferencesAttestation-->
0x0718576a2cdb3eaabaf6bb338a8a4d1bfb09678b05357e7d8c15e237f92a8abb

Base Builder Operations Manual v0.1
  --IndexesReceipt-->
AL Base MCP root + AL Base MCP EAS receipt

Boss Bre
  --Maintains-->
Base Builder Operations Manual v0.1
```

## Hard safety invariants

1. Graphiti cannot create truth authority.
2. Graphiti cannot sign.
3. Graphiti cannot execute transactions.
4. Graphiti cannot merge PRs.
5. Graphiti cannot attest to EAS.
6. Graphiti cannot hold wallet keys.
7. Graphiti cannot hold GitHub write tokens.
8. Graphiti cannot hold Base/EVM write RPC credentials.
9. Graphiti output must cite source episodes.
10. LLM extraction must not be trusted as canonical truth.
11. Prescribed ontology is required for v0.1 ingestion.
12. Graphiti is a rebuildable cache over sealed artifacts.
13. Boss Bre manual-maintainer restrictions apply equally to Graphiti memory.

## Recommended v0.1 architecture

```text
Receipt Core JSON / EAS / Git tags
  -> local read-only file ingest
  -> prescribed ontology mapper
  -> Graphiti temporal graph
  -> read-only query API
  -> UI / agent memory
```

Truth flows one way only:

```text
sealed artifact -> memory index
```

Never:

```text
memory index -> authority / execution / signing / attestation
```

## Go / No-Go

### GO

Graphiti is acceptable for a read-only temporal memory prototype if:

- prescribed ontology is used
- local receipt episodes are the only source
- read-only wrapper strips write tools
- every response cites a source episode
- no authority-bearing credentials are mounted
- memory is explicitly labeled as non-authoritative

### NO-GO

Graphiti must not be used for:

- truth creation
- signing
- wallet operations
- Base writes
- GitHub merges
- EAS attestations
- autonomous runtime enablement

## Verdict

Graphiti is a good candidate for `jaytree-memory-v0.1` as a read-only temporal retrieval layer.

It should be treated as memory, not authority.
