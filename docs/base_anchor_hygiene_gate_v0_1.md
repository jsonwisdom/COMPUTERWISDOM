# BASE_ANCHOR_HYGIENE_GATE_V0_1

Status: GATE_FIRST  
Issue: #88  
Parent: #67  
Authority: false  
Membrane: HOLDS

## Purpose

BASE_ANCHOR_HYGIENE_GATE_V0_1 records a bounded review gate for public anchor references.

It prevents ghost anchors, ambiguous anchor claims, and promotion from anchor reference to authority.

## Required Anchor Fields

- chain
- tx_hash_or_eas_uid
- payload_hash
- operator_confirmation
- no_existing_anchor_conflict

## Core Rule

Receipt is not deed.

An anchor reference records that a claim or payload was referenced. It does not, by itself, prove truth, ownership, legal validity, or adjudication.

## Gate Rules

- RECEIPT_NOT_DEED
- MISSING_FIELDS_BLOCK
- ANCHOR_CONFLICT_BLOCK
- OPERATOR_CONFIRMATION_REQUIRED
- NO_ANCHOR_TO_AUTHORITY_PROMOTION

## Forbidden Promotions

- Anchor reference to verified truth
- Anchor reference to legal conclusion
- Anchor reference to ownership conclusion
- Anchor reference to ENS or Base authority
- Anchor reference to autonomous merge authority
- Anchor reference to policy authority

## Closing Rule

Anchors witness claims. Receipts preserve claims. Humans interpret. Authority remains false.
