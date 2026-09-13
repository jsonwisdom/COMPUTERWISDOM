# CONGRESSIONAL PURPOSE v0.1

**Artifact class:** Public-source oversight / replay architecture  
**Parent state:** PR #512 — BoxD + LeahPrime Royale  
**Authority created:** FALSE  
**Proof inferred:** FALSE

## Purpose

The Congressional purpose of the BoxD / Onion Sack replay system is to provide legislators, committees, inspectors, auditors, journalists, and the public with a repeatable method for testing institutional claims against preserved public records.

The system does not determine guilt, issue legal findings, replace congressional judgment, or manufacture governmental authority.

Its function is narrower:

**Preserve the record, identify the lawful authority, reconstruct execution, test oversight, and make every transition replayable.**

## Congressional Use

The architecture supports oversight questions such as:

1. **RECORD — What happened?**  
   Identify the public document, statement, transaction, proceeding, rule, or event being examined.
2. **AUTHORITY — Who was legally empowered to act?**  
   Bind the actor → office → delegated power → statute, rule, order, appropriation, or other authority source.
3. **EXECUTION — What was actually done?**  
   Compare authorized action with observable implementation, expenditure, disclosure, enforcement, or administrative result.
4. **OVERSIGHT / RECOVERY — What happened when the system failed or disagreed?**  
   Trace audits, hearings, appeals, inspectors general, courts, corrective actions, reimbursements, sanctions, or unresolved gaps.

## Evidence Membrane

Congressional replay must preserve this distinction:

```text
SOURCE POINTER ≠ MIRROR ≠ PROOF
```

A durable mirror requires:

```text
raw_bytes + retrieved_at + SHA-256 + previous_mirror_hash
```

Until those elements exist, a Congress.gov, Justice.gov, NATO, court, or state-government URL remains an official-source pointer, not frozen replay evidence.

## Legislative Value

This enables Congress to compare:

```text
claim → authority → appropriation → execution → result → oversight → correction
```

across agencies, administrations, fiscal years, jurisdictions, and versions without allowing later narrative changes to silently overwrite the historical record.

It also exposes two critical failure modes:

### THE VERSION GHOST

Material changes without a bound version delta → **CONFLICT**

### THE GREEN LIGHT

A system reports success without supporting receipts → **REJECT**

## Constitutional Boundary

The architecture is an evidence-navigation and verification instrument.

It may assist Congress in investigation, legislation, appropriations oversight, hearings, record preservation, and institutional accountability.

It does not:

- decide guilt;
- create subpoena power;
- establish facts merely because data is on-chain;
- convert automation into governmental authority;
- treat satire, inference, dice, AI output, or publication as evidence of wrongdoing.

## Congressional Objective

**Make institutional memory independently replayable.**

A future Congress should be able to ask:

> What did government know, what authority existed, what action followed, what changed afterward, and can another observer reproduce that conclusion from the same preserved bytes?

Until the first frozen mirror receipt exists:

```text
SYSTEM_STATE = OVERSIGHT_MAP
```

After receipt-bound source preservation begins:

```text
SYSTEM_STATE = REPLAYABLE_EVIDENCE_INFRASTRUCTURE_CANDIDATE
```

```text
No receipt → no promotion.
No authority → no invented power.
No replay → no durable institutional claim.
```

## Identity / Attestation Boundary

```text
OVERSIGHT_IDENTITY_LABEL = jaywisdom.eth
ATTESTATION_IDENTITY_LABEL = jaywisdom.base.eth
ONCHAIN_ATTESTATION = HOLD / NOT_EXECUTED
IDENTITY_OWNERSHIP_VERIFIED = FALSE
AUTHORITY_CREATED = FALSE
PROOF_INFERRED = FALSE
```

The identity labels above are user-designated publication / attestation labels. They do not, by themselves, establish legal identity, ownership, governmental status, or on-chain attestation.
