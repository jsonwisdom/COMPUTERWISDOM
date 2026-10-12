# JAYWISDOM PUBLIC PROOF MEMBRANE — v0.1

Status: IN REVIEW
Date: 2026-07-29
Authority: false
Human release gate: required

## Purpose

Establish a receipts-first public identity and proof membrane connecting the JayWisdom public surface, project directory, source repository, release records, and durable naming pointers without converting publication, minting, repository access, or wallet references into authority.

## Added artifacts

- `jaywisdom/projects/index.json` — machine-readable public project index
- `jaywisdom/verify/index.html` — zero-dependency verifier interface

## Required fields

Each indexed public project records:

- stable project ID
- explicit classification
- verification state
- source pointer
- release-record pointer when available
- public URL when declared
- explicit statements of what is not claimed

## Invariants

1. Authority is false by default.
2. Repository activity is not automatically public publication.
3. A merged pull request does not independently prove deployment.
4. Unknown, hold, conflict, and deployment-unverified are valid states.
5. Private, personal, treasury, family, credential, and operational-control lanes are excluded.
6. Zora artifacts are distribution signals, not proof of authority.
7. Token references carry no promise of price, profit, liquidity, utility, or future value.
8. Publication remains human-gated.

## Verification boundary

This version does not validate cryptographic signatures, ENS ownership, wallet control, GitHub Pages deployment, Zora mint provenance, or third-party availability. Those checks require independent observations and separate receipts.
