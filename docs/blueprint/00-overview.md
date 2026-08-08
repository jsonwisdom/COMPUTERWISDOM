# COMPUTERWISDOM Public Trinity Blueprint

## Status

Draft v0.2 for public review.

## Purpose

`COMPUTERWISDOM` is the public reference implementation of a governed, AI-enabled second-brain architecture bound to the identity pointers `jaywisdom.eth` and `jaywisdom.base.eth`.

The architecture is designed as though no commercial code host, desktop vendor, cloud provider, or proprietary office suite exists. No single company is part of the trust root.

## Sovereign source rule

The canonical system is a directory tree of ordinary files on storage controlled by the operator.

```text
LOCAL CANONICAL DIRECTORY
        ↓
BYTE FREEZE + HASH + RECEIPT
        ↓
OPTIONAL DISTRIBUTED COPIES
├── public Git remote
├── object storage
├── content-addressed storage
├── removable encrypted backup
└── printed or offline recovery packet
```

A hosted repository is a distribution mirror and collaboration surface. It is never the sole source of truth.

## Three planes

- **JOY — personal/family plane:** family legacy, inner life, memory, design stories, and protected personal material.
- **AL — private/operational plane:** confidential operations, relationships, finances, health, and authority-gated records.
- **COMPUTERWISDOM — public plane:** public philosophy, code, teachings, reference architecture, schemas, and safe examples.

The planes are logical namespaces, not vendor accounts. They may be stored, mirrored, or migrated independently.

## Root identity

Identity pointers help locate records. They do not create authority, prove truth, or replace source evidence.

> The hash proves byte identity. The source record supports the claim. The identity pointer helps people locate the record.

## Minimum technology assumptions

The design assumes only:

1. a filesystem capable of preserving bytes;
2. UTF-8 text and documented binary formats;
3. SHA-256 or a declared successor hash;
4. a portable signature format;
5. a command-line or small local program capable of replaying receipts;
6. exportable backups readable without a vendor account.

## Governance

1. Changes begin as local proposals or patches.
2. Major decisions are recorded as Architecture Decision Records.
3. Governance-relevant transitions produce receipts.
4. Corrections append rather than silently rewriting history.
5. AI may propose, classify, compare, and generate drafts; AI does not create execution authority.
6. Cross-plane access or inference requires explicit authorization and a receipt.
7. Publication to any host is optional and reproducible from canonical bytes.

## Public safety boundary

The public plane must contain no private family records, medical or financial secrets, credentials, private keys, unsupported claims presented as verified facts, or simulated signatures presented as real.

## Replay principle

Mistakes, rejected paths, and dead ends remain reviewable history when safe to preserve. Replay improves later versions without pretending earlier states never existed.

## Recovery invariant

The system must remain recoverable after loss of any one vendor, account, domain, repository host, cloud region, application, or AI provider.

## Current boundary

This document is a design artifact. It does not claim that signing, append-only storage, cryptographic verification, replication, or automated perspective enforcement is already operational.