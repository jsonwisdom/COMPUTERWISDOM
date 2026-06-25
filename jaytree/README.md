# Jaytree Identity Vector v0.1

Jaytree is a proof-oriented identity surface for COMPUTERWISDOM.

```text
Linktree was for links.
Jaytree is for proofs.
```

## Purpose

Jaytree connects the public operator surface to the Receipt Core stack:

```text
GitHub merge history -> Receipt Core -> EAS proof -> jaywisdom.base.eth -> MCP -> Base agent
```

## Invariant

```text
Authority: NONE
```

Identity links do not create truth authority. They only provide a reproducible operator surface that future receipts can reference.

## Canonical surfaces

- GitHub: jsonwisdom/COMPUTERWISDOM
- Basename: jaywisdom.base.eth
- EAS network: Base
- EAS schema UID: 0xa5b0d2dd5470542a119d50eba19898f50e1f77591f01d4fec4c6f3075054aa11
- First Receipt Core attestation: 0x84b58fb78cfde7f791b311c07e5982eeffc3f60b550d594dc9407419ed5d5150
- MCP: agent coordination surface
- Base agent: agentic proof consumer

## Next step

Generate `identity-vector-v0.1.json`, compute a deterministic Jaytree root, verify locally, then optionally attest that root on Base.
