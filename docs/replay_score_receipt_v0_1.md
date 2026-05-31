# REPLAY_SCORE_RECEIPT_V0_1

Status: SCHEMA_FIRST  
Issue: #84  
Parent: #67  
Authority: false  
Membrane: HOLDS

## Purpose

`REPLAY_SCORE_RECEIPT_V0_1` records bounded scores for replay behavior and receipt quality.

It scores artifacts, agent behavior, and replay discipline only. It does not score human worth, legal guilt, creditworthiness, employment suitability, truth finality, or merge authority.

## Allowed Score Dimensions

- `replayability`
- `receipt_integrity`
- `agent_discipline`
- `dispute_quality`
- `base_anchor_hygiene`

## Required Fields

- `score_receipt_id`
- `agent_or_player_id`
- `claim_or_artifact_ref`
- `score_dimension`
- `verdict`
- `supporting_receipts`
- `authority: false`
- `timestamp_utc`

## Core Rule

Score is evidence about replay quality. Score is not authority.

## Forbidden Promotions

- Score to truth
- Score to legal conclusion
- Score to human worth
- Score to creditworthiness
- Score to employment suitability
- Score to merge authority
- Score to autonomous execution right

## Closing Rule

Receipts replay. Scores contextualize. Humans merge. Authority remains false.
