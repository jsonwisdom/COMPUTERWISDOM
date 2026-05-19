# Base Batches Purpose Candidate

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Service family: Confucius Compute Wisdom
Purpose rail: Base Batches
Portal mutation: none.
Onchain claim: none.
Backend claim: none.
Public badge: none.

## Purpose

Base Batches is a candidate purpose rail for turning many small Wisdom Reports, code reviews, builder checks, and receipt events into grouped verification batches.

The goal is utility at scale:

- one builder can submit an artifact
- many artifacts can be grouped into batches
- each batch can produce a Merkle root
- each root can be reviewed, anchored, challenged, or referenced later
- every claim remains tied to evidence instead of narrative

## Relationship to Confucius Compute Wisdom

Confucius Compute Wisdom is the builder-facing guide.

Base Batches is the settlement-facing batching layer.

DeepSeek or another model may help analyze inputs, but the batch only counts if the outputs are structured into receipts and reviewable roots.

## Candidate Flow

1. Builder submits code, spec, receipt, or workflow.
2. Confucius Compute Wisdom produces a candidate Wisdom Report.
3. Each report receives a receipt hash.
4. Multiple receipt hashes are grouped into a Base Batch.
5. The batch creates a Merkle root.
6. The root may later be anchored to Base, EAS, ENS, IPFS, or GitHub commit history after explicit approval.
7. Auditors can compare the batch root against the included leaves.

## Utility Surfaces

Base Batches can support:

- utility auditing
- public verification
- transparent builder review
- reusable receipt bundles
- skill evidence batches
- candidate badge evidence
- civic audit bundles
- code review proof trails

## Verifier Role

A verifier may check:

- every leaf exists
- every file path resolves
- every claim tag is bounded
- every receipt hash recomputes
- Merkle root matches the leaves
- no portal mutation occurred
- no live badge or backend claim was created without receipt

## Guardrails

- Do not call this onchain until an actual Base transaction, EAS attestation, ENS record, or other onchain receipt exists.
- Do not imply production settlement.
- Do not grant public badges from batch membership alone.
- Do not treat AI output as verified without receipt review.
- Do not ask builders to submit secrets, private keys, credentials, or sensitive personal data.

## Canon

Confucius gives builders Wisdom.
Base Batches give receipts scale.
Merkle roots make the purpose portable.
Verification makes it legitimate.
