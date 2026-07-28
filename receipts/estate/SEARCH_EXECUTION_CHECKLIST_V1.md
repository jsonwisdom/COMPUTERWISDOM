# SEARCH_EXECUTION_CHECKLIST_V1

Status: FROZEN PROCEDURE
Authority: false
Estate advancement: none

## Purpose

This checklist executes `MANIFEST_RECOVERY_SEARCH_PLAN_V1` without reconstructing, inferring, normalizing, or substituting present-day repository identities.

Completion of this checklist does not establish that a source was found, that a candidate is admissible, that identities are known, or that reconciliation is authorized.

## Prohibited actions

- Do not enumerate the current GitHub estate as a substitute for historical evidence.
- Do not create repository names from memory.
- Do not normalize, merge, deduplicate, correct, or reorder historical observations.
- Do not classify rename, missing, added, archived, private, empty, split, or merged states before a frozen name-level manifest exists.
- Do not overwrite raw candidate artifacts.
- Do not self-ratify a candidate.

## Execution metadata

Record before searching:

- execution_id
- plan_version
- operator_id
- witness_id, if available
- started_at_utc
- execution_environment
- storage_location_class
- access_status
- exact search terms

## Location checklist

For each location, record `NOT_STARTED`, `IN_PROGRESS`, `NO_RESULT`, `CANDIDATE_FOUND`, `ACCESS_DENIED`, or `NOT_AVAILABLE`.

1. Historical GitHub account exports
2. Saved GitHub API or CLI output
3. Historical committed registries
4. GitHub Actions artifacts and logs
5. Local workstations, laptops, VMs, and shell history
6. Google Drive, OneDrive, Dropbox, and other cloud storage
7. Email attachments, sent mail, and drafts
8. Backup systems and filesystem snapshots
9. Screenshot folders
10. Slack, Teams, Discord, and other chat exports

## Required search terms

At minimum, record execution of the following terms where supported:

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

## Candidate handling

When a candidate is found:

1. Preserve the raw artifact without modification.
2. Assign a unique candidate ID.
3. Record the original filename, path, source class, and observed timestamp.
4. Copy the artifact to an evidence-preservation location without changing its bytes.
5. Compute SHA-256 over the preserved raw bytes.
6. Record byte length and media type.
7. Create one candidate-log entry conforming to `CANDIDATE_LOG_ENTRY_TEMPLATE_V1.json`.
8. Obtain witness attestation under `CHAIN_OF_CUSTODY_WITNESS_PROTOCOL_V1.md` when a witness is available.
9. Do not extract or publish repository identities until admissibility evaluation authorizes extraction.

## NO_RESULT handling

A search action returning no candidate must still record:

- location searched
- exact terms used
- start and completion timestamps
- access status
- result: `NO_RESULT`
- operator
- witness, if any
- notes on search limitations

`NO_RESULT` is a valid outcome and must not be converted into a reconstructed list.

## Completion conditions

The checklist is complete only when every planned location has a recorded terminal status and every discovered candidate has a candidate-log entry.

Checklist completion means only:

`SEARCH_EXECUTED`

It does not mean:

- `SOURCE_FOUND`
- `CANDIDATE_ADMISSIBLE`
- `IDENTITIES_ESTABLISHED`
- `ORIGINAL_72_MANIFEST_AUTHORIZED`
- `RECONCILIATION_AUTHORIZED`

## Stop condition

If no admissible historical source is found after all accessible P0 and P1 locations are exhausted, record:

`COUNT KNOWN → IDENTITIES UNKNOWN → RECONCILIATION PENDING`

Authority remains false.
