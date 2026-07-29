# P0_OPERATOR_CHECKLIST_V1

Status: FROZEN CONTROL
Authority: false
Estate advancement: none

## Purpose

This checklist binds the human operator before any P0 manifest-recovery search writes files, preserves artifacts, creates candidate entries, or requests witness attestation.

Completion of this checklist authorizes only execution of the frozen P0 runbook. It does not establish candidate admissibility, repository identity, or reconciliation authority.

## Preconditions

The operator must record:

- execution_id
- operator_id
- operator role
- UTC start timestamp
- selected P0 source class
- selected source location
- access authorization basis
- witness availability state

The operator must confirm they have read and will follow:

- `MANIFEST_RECOVERY_SEARCH_PLAN_V1.md`
- `SEARCH_EXECUTION_CHECKLIST_V1.md`
- `P0_EXECUTION_RUNBOOK_V1.md`
- `CANDIDATE_LOG_POPULATION_WORKFLOW_V1.md`
- `CHAIN_OF_CUSTODY_WITNESS_PROTOCOL_V1.md`
- `WITNESS_ATTESTATION_CHECKLIST_V1.md`

## Mandatory acknowledgements

Before execution, every item must be explicitly acknowledged:

- [ ] Historical recovery only; reconstruction is prohibited.
- [ ] Inference from present-day repositories is prohibited.
- [ ] Live GitHub enumeration cannot substitute for a historical artifact.
- [ ] Repository names must not be normalized, corrected, deduplicated, reordered, or inferred.
- [ ] Raw bytes must be preserved before content inspection.
- [ ] Recovery timestamps must not be represented as historical capture timestamps.
- [ ] `NO_RESULT` and `ACCESS_DENIED` are valid outcomes.
- [ ] A discovered artifact begins as a candidate with `admissibility.status: NOT_EVALUATED`.
- [ ] Operator action cannot self-ratify a candidate.
- [ ] Witness attestation establishes byte-preservation observations only.
- [ ] All authorization booleans remain false.
- [ ] Authority remains false.

## Search binding

Record before search begins:

- P0 source priority
- source class
- source locator
- exact approved search terms
- approved commands or UI actions
- expected preservation destination
- expected checklist entry identifier

Unapproved query expansion requires stopping the run and opening a new execution record.

## Access state

Select exactly one initial state:

- `ACCESS_CONFIRMED`
- `ACCESS_PARTIAL`
- `ACCESS_DENIED`
- `SOURCE_UNAVAILABLE`

`ACCESS_DENIED` and `SOURCE_UNAVAILABLE` must produce a completed run record with no candidate fabrication.

## Outcome

Select exactly one final outcome:

- `NO_RESULT`
- `ACCESS_DENIED`
- `SOURCE_FOUND`
- `RUN_ABORTED`

For `SOURCE_FOUND`, record:

- preserved raw artifact locator
- original source label or filename
- preservation timestamp UTC
- byte length
- SHA-256 digest
- hashing tool and command
- candidate_id
- candidate-log entry locator
- witness state

For `NO_RESULT`, record searched locations and exact terms. Do not create a candidate entry.

## Stop conditions

Stop immediately on:

- attempted live-estate substitution
- inability to preserve raw bytes before inspection
- source modification or export transformation
- digest mismatch
- unclear source ownership or access authorization
- timestamp role confusion
- identity inference or normalization attempt
- self-ratification attempt
- any instruction conflicting with a frozen control

## Completion statement

The operator must attest:

> I executed only the bounded P0 recovery action recorded here. I did not reconstruct repository identities, substitute present-day GitHub observations, normalize names, determine admissibility, authorize identity extraction, or authorize reconciliation.

Checklist completion does not establish evidence admissibility or identity.

Authority remains false.
