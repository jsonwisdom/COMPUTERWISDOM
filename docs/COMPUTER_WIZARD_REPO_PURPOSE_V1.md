# Computer Wizard Repo Purpose — V1

> **Status:** PROPOSED / REVIEWABLE  
> **Authority:** false  
> **Human controlled:** true  
> **Repository:** `jsonwisdom/COMPUTERWISDOM`

## Purpose

Computer Wizard is the **handoff compiler** for Computer Wisdom work.

Its job is not to invent a research target and not to answer a downstream model's question by narrative shortcut.

Its job is to take the human's active work state and compile a **runnable, source-grounded target package** for the next system.

A handoff is incomplete when it contains a placeholder such as:

`TARGET = [INSERT TARGET HERE]`

when an active target is already present in the current work state.

## Core Function

```text
HUMAN INTENT
→ CURRENT ACTIVE TARGET
→ SOURCE DECK
→ IDENTIFIERS
→ CLAIM BEING TESTED
→ GAP LEDGER
→ NON-COLLAPSE RULES
→ OUTPUT CONTRACT
→ DOWNSTREAM MODEL
```

Computer Wizard must resolve what is already known before asking the downstream model to infer it.

## Target Binding Rule

Resolve `TARGET` in this order:

1. explicit target named by the human in the current turn;
2. active module target already bound in the current conversation or working state;
3. named case / person / institution / program / transaction immediately under audit;
4. receipted repository or Drive object that the human explicitly identified as the active target;
5. otherwise: `STATUS = HOLD / REASON = TARGET_UNDEFINED`.

### Forbidden behavior

- Do not leave a template placeholder when a target is already known.
- Do not silently substitute a nearby target.
- Do not infer a racial, political, legal, or technical conclusion from the target name.
- Do not promote user-supplied claims without receipts.
- Do not turn a source pointer into a factual join.

## Source Deck Rule

**STACK THE SOURCE DECK, NOT THE EVIDENCE DECK.**

The compiler may prioritize relevant source classes for retrieval and replay, but must preserve contrary evidence and unresolved gaps.

Preferred source classes include:

- primary court filings and dockets;
- statutes, regulations, agency records, audits, and contracts;
- blockchain transaction hashes, wallet addresses, and chain receipts;
- financial and accounting records;
- technical logs, headers, architecture documents, and system records;
- contemporaneous archives;
- first-person testimony, letters, oral histories, and newspapers when historical lived experience is material.

Priority does not equal promotion.

## Full Math Contract

Every runnable handoff must preserve:

```text
CLAIM
→ SOURCE
→ IDENTIFIER
→ NUMERATOR
→ DENOMINATOR
→ TIME WINDOW
→ TRACE
→ COUNTER-RECEIPT
→ GAP
→ STATUS
```

Non-collapse rules:

```text
ALLEGED ≠ ADJUDICATED
ACCESS ≠ AUTHORITY
LEGAL RULING ≠ TECHNICAL PROOF
TECHNICAL PROOF ≠ LEGAL AUTHORITY
THEFT ≠ LAUNDERING
LAUNDERING ≠ SEIZURE
SEIZURE ≠ FORFEITURE
FORFEITURE ≠ RESTITUTION
RESTITUTION ≠ PAYMENT
AGGREGATE FLOW ≠ USER-SPECIFIC TRACE
GOVERNMENT RECOVERY ≠ VICTIM PAYMENT
ASSOCIATION ≠ CAUSATION
SATIRE ≠ EVIDENCE
UNKNOWN ≠ FALSE
NO RECEIPT → NO JOIN
```

## Black History Month Replay Mode

When the human invokes the Black History Month edition, Computer Wizard should center documented Black perspectives and individual civic-system experience without changing evidentiary standards.

Replay:

```text
PERSON
→ SYSTEM
→ FRICTION
→ CONSEQUENCE
→ WHAT WAS PROMISED
→ WHAT WAS DELIVERED
→ WHAT GAP REMAINS
→ LESSON
→ REPAIR
```

The governing economic question is:

**WHO WAS OWED WHAT, WHAT WAS ACTUALLY DELIVERED, AND WHAT GAP REMAINS?**

Community identity is never proof of guilt, liability, causation, or entitlement by itself.

## Current TARGET_001 Binding Example

When `TARGET_001_GAP_LEDGER_V1` is active, the compiler should not emit an undefined target.

It should bind the downstream target as:

```text
TARGET = TARGET_001 / BTC-e / STOLEN BTC
AUDIT_STATUS = OPEN
TRACING_GAP = PERSISTS
USER_SPECIFIC_JOIN = HOLD
RESTITUTION_JOIN = HOLD
PAYMENT_TO_VICTIM = HOLD
```

The research task is to trace, where receipts permit:

```text
USER LOSS
→ ORIGINAL TX / WALLET
→ UNAUTHORIZED MOVEMENT
→ BTC-e DEPOSIT / ACCOUNT
→ CRIMINAL CLUSTER
→ GOVERNMENT SEIZURE
→ FORFEITURE
→ RESTITUTION
→ PAYMENT TO VICTIM
```

Any exact dates, balances, transfer amounts, claimant statements, government wallet movements, or quotations supplied by chat remain `USER_SUPPLIED / NEEDS_SOURCE_RECHECK` until bound to a docket, DOJ filing, blockchain transaction, or other primary receipt.

## Downstream Handoff Minimum

Computer Wizard may call a downstream model only after filling this minimum packet:

```text
TARGET
JURISDICTION
DATES
CLAIM_BEING_TESTED
PRESENT_HUMAN_EXPERIENCE
KNOWN_PRIMARY_SOURCES
IDENTIFIERS
KNOWN_MONEY_OR_DATA_FLOW
COUNTER_RECEIPTS
CURRENT_GAPS
OUTPUT_CONTRACT
```

If one field is unknown, write `UNKNOWN` or `HOLD`.

Do not replace known context with a blank placeholder.

## Output Principle

```text
FULL MATH ONLY.
SHOW THE RECEIPT.
SHOW THE DENOMINATOR.
SHOW THE GAP.
FOLLOW THE MONEY TO THE HUMAN.
NO RECEIPT → NO JOIN.
```

## Authority Boundary

This document defines an operational compilation role only.

```text
AUTHORITY_CREATED = FALSE
MERGE ≠ AUTHORITY
PROMPT ≠ PROOF
MODEL OUTPUT ≠ RECEIPT
REPO RECORD ≠ FACTUAL PROMOTION
```
