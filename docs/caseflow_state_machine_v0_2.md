# CASEFLOW_STATE_MACHINE_V0_2

Status: BOUNDED_IMPLEMENTATION  
Parent Issue: #67  
Child Issue: #68  
Authority: false  
Membrane: HOLDS

## Purpose

`CASEFLOW_STATE_MACHINE_V0_2` defines the bounded transition kernel for constitutional caseflow. It makes state movement explicit, receipt-shaped, replayable, and blocked from unauthorized authority promotion.

This artifact defines transition discipline only. It does not adjudicate truth, grant legal authority, automate wallet signing, modify ENS/Base records, or assign reputation authority.

## States

- `DRAFT` — initial proposal or artifact state
- `UNDER_REVIEW` — review by human, agent, or witness surface is active
- `GOVERNANCE_CHECK` — membrane and rule validation state
- `APPROVED` — approved for bounded implementation
- `IN_PROGRESS` — implementation or execution is active
- `MERGED` — successfully landed by human merge authority
- `REJECTED` — blocked or declined with reason
- `REPLAY` — historical audit or replay state
- `DISPUTED` — invalid transition, ghost bypass, or disputed promotion detected

## Core Invariant

`NO_SILENT_CATEGORY_PROMOTION`

No caseflow may move into a higher governance or evidence posture without an explicit transition record.

## Valid Transition Pattern

A lawful transition must record:

- `schema_version`
- `authority: false`
- `from_state`
- `to_state`
- `transition_reason`
- receipt with `emitted: true`
- invariant value `NO_SILENT_CATEGORY_PROMOTION`

## Forbidden Promotions

- Claim directly to receipt
- Claim directly to merge
- Witness output to verified truth
- Score to authority
- Chain anchor to adjudication
- Agent action to human approval

## Boundary Rules

Observers surface. Witnesses report. Agents play. Verifiers gate. Courts translate. Receipts replay. Humans merge. Authority remains false.

## Non-Goals

- No ENS changes
- No Base anchoring
- No wallet signing automation
- No witness automation expansion
- No reputation scoring implementation
- No autonomous merge authority
- No truth-finality claim

## Court Posture

Goblin Court: ADMISSIBLE  
Meme Court: RULES_PHASE_BOUND  
Clown Court: NO_AUTHORITY_UPGRADE
