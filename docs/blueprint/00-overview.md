# COMPUTERWISDOM Public Trinity Blueprint

## Status

Draft v0.1 for public review.

## Purpose

`COMPUTERWISDOM` is the public reference implementation of a governed, AI-enabled second-brain architecture bound to the identity anchors `jaywisdom.eth` and `jaywisdom.base.eth`.

The public system exposes architecture, governance, schemas, examples, and replayable decision records. It does not expose personal or confidential source material.

## Three planes

- **JOY — personal/family plane:** family legacy, inner life, memory, design stories, and protected personal material.
- **AL — private/operational plane:** confidential operations, relationships, finances, health, and authority-gated records.
- **COMPUTERWISDOM — public plane:** public philosophy, code, teachings, reference architecture, schemas, and safe examples.

Public materials may describe JOY and AL as types or governed planes. They must not publish protected values from either plane.

## Root identity

The identity anchors provide resolvable references. They do not create authority, prove truth, or replace source evidence.

Controlling rule:

> The hash proves byte identity. The source record supports the claim. The identity anchor helps people locate the record.

## Governance

1. Changes are proposed through pull requests.
2. Major architectural choices are recorded as Architecture Decision Records.
3. Governance-relevant transitions produce receipts.
4. Corrections are added as new events rather than silently rewriting history.
5. AI may propose, classify, compare, and generate drafts; AI does not create execution authority.
6. Cross-plane access or inference requires explicit authorization and a receipt.

## Public safety boundary

The public repository must contain no:

- private family records;
- medical, financial, credential, or relationship secrets;
- private keys, signing seeds, tokens, or operational credentials;
- unsupported claims presented as verified facts;
- simulated signatures presented as real signatures.

## Replay principle

Mistakes, rejected paths, and dead ends are retained as reviewable history when safe to publish. Replay is used to improve later versions without pretending the earlier state never existed.

## Initial implementation sequence

1. Publish the plane and identity definitions.
2. Add ADRs for repository separation, receipts, redaction, and perspective switching.
3. Add schemas with examples and validation tests.
4. Add an unsigned demonstration ledger clearly marked as non-production.
5. Implement the public perspective engine.
6. Add cryptographic signing only after key custody and verification procedures are operationally tested.

## Current boundary

This document is a design artifact. It does not claim that signing, append-only storage, cryptographic verification, or automated perspective enforcement is already operational.