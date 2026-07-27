# JSONWisdom Knowledge Management System

Status: INITIAL CONTROL PLANE
Authority: false
Source of truth: linked evidence, commits, receipts, and reviewed records

## Mission

Preserve, connect, rank, retrieve, and replay the people, projects, places, objects, subjects, repositories, claims, and evidence discussed across Jason Wisdom's work.

This is not a monorepo and does not copy runtime code. It is an importance-weighted coordination layer across repositories.

## Two Knowledge Environments

### JSONWisdom AI Knowledge Environment

Purpose: operator-owned, AI-assisted knowledge recovery and collaboration.

Capabilities:
- register entities and concepts
- link repositories by responsibility and dependency
- score importance independently of repository size
- preserve evidence and uncertainty
- generate daily state and resume records
- route work to the correct repository
- distinguish observed, inferred, disputed, and unknown states

### USAF Knowledge Management Review Lane

Purpose: document USAF knowledge-management practices, failures, lessons, and modernization proposals without claiming official USAF authority.

This lane records:
- observed legacy practices
- operator experience
- failure modes such as siloing, CBT-only training, inaccessible institutional memory, and narrative replacing evidence
- proposed AI-enabled replacements
- evidence and review status

## Core Domains

1. Identity: Jason Wisdom, Jay Wisdom, JSONWisdom, Zero Cool
2. Zora: publishing, ContentCoins, market evidence, creator systems
3. Base: identity, contracts, attestations, transactions, ReceiptOS
4. Minnesota: civic records, fiscal audits, local infrastructure, governance
5. ReplayOS: state recovery and deterministic replay
6. ReceiptOS: evidence and execution receipts
7. USAF: training, knowledge management, digital foundations, Maxwell's Demon

## Importance Model

Importance is computed from:
- identity relevance
- recurrence across time
- dependency weight
- public or personal value
- evidence strength
- active urgency

Repository size is not an importance signal.

## Required Node Contract

Participating repositories SHOULD publish `.jsonwisdom/node.json` containing:
- repository responsibility
- canonical artifacts
- dependencies
- dependents
- importance scores
- current verified commit
- evidence status
- authority boundary

## State Rules

- Unknown is valid.
- Missing evidence is never converted into confidence.
- AI suggestions are proposals until accepted or evidenced.
- Repositories collaborate through pointers, APIs, issues, manifests, and receipts.
- Runtime code remains in its responsible repository.
- Daily work resumes from the last verified state; it does not reconstruct from conversation narrative.
