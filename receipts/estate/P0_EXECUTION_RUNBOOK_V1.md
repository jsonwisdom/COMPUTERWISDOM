# P0_EXECUTION_RUNBOOK_V1

Status: FROZEN PROCEDURE
Bundle: P0_EXECUTION_HARNESS_V1
Authority: false
Estate advancement: none

## Purpose

This runbook defines the deterministic operating sequence for executing P0 manifest-recovery searches under `MANIFEST_RECOVERY_SEARCH_PLAN_V1`. It governs search activity only. It does not create repository identity, establish admissibility, authorize reconciliation, or permit reconstruction.

## Preconditions

Before execution begins, confirm:

1. `MANIFEST_RECOVERY_SEARCH_PLAN_V1.md` is present and unchanged.
2. `SEARCH_EXECUTION_CHECKLIST_V1.md` is present and unchanged.
3. `CANDIDATE_LOG_ENTRY_TEMPLATE_V1.json` is available.
4. `CHAIN_OF_CUSTODY_WITNESS_PROTOCOL_V1.md` is available.
5. `MANIFEST_RECOVERY_CANDIDATE_LOG_V1.json` exists.
6. The operator has a stable identifier.
7. UTC time is available.
8. A preservation directory exists outside any live-enumeration output path.
9. No present-day GitHub repository list will be used as a substitute source.

If any prerequisite fails, record `PRECONDITION_FAILED` and stop.

## P0 source order

Search the following historical source classes in order:

1. Historical GitHub account-data export ZIP or JSON.
2. Saved historical API or CLI response with timestamp.
3. Historical committed registry containing repository names.
4. Historical CI artifact containing repository names.

Do not proceed to a lower-priority source solely to bypass an access problem at a higher-priority source. Record the access outcome first.

## Approved search terms

Use the exact terms authorized by the frozen search plan, including:

- `75 repositories`
- `72 repositories`
- `repo list`
- `repository inventory`
- `manifest`
- `registry`
- `audit`
- `export`
- `backup`
- `snapshot`
- `gh repo list`
- `GitHub export`
- `GitHub backup`
- `repos.json`
- `repositories.csv`
- `inventory.txt`
- `manifest.txt`
- `repo-names`
- `repo-list`

Additional terms require a new version of the search plan or an explicitly logged deviation. Terms derived from current repository names are prohibited.

## Execution sequence

For each P0 location:

1. Create an execution record with `execution_id`, operator ID, location class, source locator, and UTC start time.
2. Confirm whether access is available.
3. Record one access state: `ACCESS_AVAILABLE`, `ACCESS_DENIED`, `LOCATION_NOT_PRESENT`, or `ACCESS_AMBIGUOUS`.
4. If access is unavailable, record the outcome and continue only as allowed by the search plan.
5. Execute every approved search term applicable to that location.
6. Record the exact query or UI action used and its timestamp.
7. Do not extract repository names during search.
8. When no candidate is found, record `NO_RESULT` with the completed terms and UTC completion time.
9. When a possible historical artifact is found, stop interpretation immediately and preserve the raw artifact before opening, parsing, converting, normalizing, or transcribing it.
10. Assign a `candidate_id`.
11. Preserve the original bytes or an exact export of the source surface as `raw.bin` or the original filename plus an immutable raw suffix.
12. Record byte length.
13. Compute SHA-256 over the preserved raw bytes.
14. Create a candidate-log entry using `CANDIDATE_LOG_POPULATION_WORKFLOW_V1`.
15. Invoke `WITNESS_ATTESTATION_CHECKLIST_V1`.
16. Record `SOURCE_FOUND` only as a search outcome. Do not mark the candidate admissible in this runbook.
17. Stop the location search after preservation if further interaction risks modifying or replacing the source.

## Preservation convention

Use:

`receipts/estate/recovery/<execution_id>/<candidate_id>/`

Minimum preserved files:

- `raw.bin` or original raw filename
- `raw.sha256`
- `capture-metadata.json`
- `operator-notes.txt`

The preservation directory is evidence storage. It must not contain a newly generated live GitHub inventory.

## Outcome codes

Every location execution must terminate in exactly one primary outcome:

- `NO_RESULT`
- `ACCESS_DENIED`
- `LOCATION_NOT_PRESENT`
- `ACCESS_AMBIGUOUS`
- `SOURCE_FOUND`
- `PRECONDITION_FAILED`
- `PROCEDURE_DEVIATION`
- `SEARCH_SUSPENDED`

`SOURCE_FOUND` does not mean `ADMISSIBLE`.

## Stop conditions

Stop the execution immediately when:

- raw preservation cannot be guaranteed
- hashing cannot be completed
- the source would be modified by continued access
- the artifact is discovered to be generated from the present-day estate
- an operator attempts to infer names from memory
- a current GitHub enumeration is introduced as historical evidence
- the candidate cannot be linked to a checklist entry
- self-ratification is attempted
- required provenance fields are intentionally replaced with assumptions

Record the stop reason without repairing the missing evidence through inference.

## Prohibited actions

- No reconstruction.
- No normalization.
- No deduplication.
- No inferred renames.
- No present-day enumeration substitution.
- No memory-supplied names.
- No identity extraction before preservation and candidate logging.
- No admissibility declaration by the operator alone.
- No reconciliation authorization.

## Postconditions

A completed run may establish only that:

- specified locations were searched under the frozen procedure
- access states and queries were recorded
- zero or more candidate byte artifacts were preserved and hashed
- candidate and witness records were created where applicable

It cannot establish repository identity or portfolio completion.

## Constitutional boundary

`SEARCH EXECUTED` is not `CANDIDATE FOUND`.

`CANDIDATE FOUND` is not `CANDIDATE ADMISSIBLE`.

`CANDIDATE ADMISSIBLE` is not `IDENTITIES ESTABLISHED`.

Authority remains false.
