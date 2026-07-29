# MANIFEST_RECOVERY_SEARCH_PLAN_V1

Status: FROZEN PROCEDURE
Authority: false
Estate state: COUNT KNOWN → IDENTITIES UNKNOWN → RECONCILIATION PENDING

## Purpose

Define the only admissible procedure for locating a historical, name-level, capture-time-anchored list of the original 72 non-anchor repositories.

This is a forensic recovery workflow.

It is not:

- a reconstruction workflow
- an inference workflow
- a live-estate enumeration workflow
- a normalization workflow
- a memory-based recovery workflow

## Admissible evidence classes

Recovery attempts may target only:

1. Historical GitHub account-data export
2. Historical API or GitHub CLI response
3. Historical committed registry
4. Historical CI or governance artifact
5. Historical email attachment
6. Historical backup file
7. Historical screenshot
8. Historical terminal output
9. Historical chat attachment or message

Anything generated solely from the current GitHub estate is inadmissible as the original identity manifest.

## Search locations

Search may include:

- local workstations, laptops, VMs, and shell history
- Google Drive, OneDrive, Dropbox, and other cloud storage
- email inboxes, sent mail, drafts, and attachments
- GitHub commits, branches, releases, Actions artifacts, and logs
- backup systems and filesystem snapshots
- screenshot, Desktop, Documents, Downloads, and Pictures folders
- Slack, Teams, Discord, and other historical chat systems

## Search terms

Use exact and related forms of:

- 75 repositories
- 72 repositories
- repo list
- repository inventory
- manifest
- registry
- audit
- export
- backup
- snapshot
- gh repo list
- GitHub export
- GitHub backup
- repos.json
- repositories.csv
- inventory.txt
- manifest.txt
- repo-names
- repo-list

## Evidence priority

Rank candidate artifacts in this order:

1. GitHub export ZIP
2. Timestamped API or CLI response
3. Committed registry
4. CI artifact
5. Email attachment
6. Backup file
7. Screenshot
8. Terminal output
9. Chat message

Priority does not replace admissibility review. A higher-ranked artifact may still be rejected.

## Candidate capture procedure

For every candidate:

1. Preserve the original file unchanged.
2. Record discovery location and discovery timestamp.
3. Record claimed capture timestamp and source.
4. Compute SHA-256 over the preserved source bytes.
5. Record file size and media type.
6. Record whether all 75 repositories, all 72 non-anchors, or only a partial list are visible.
7. Record whether the artifact may have been generated from the current estate.
8. Append the candidate to `MANIFEST_RECOVERY_CANDIDATE_LOG_V1.json`.
9. Do not extract or normalize names until admissibility is established.

## Admissibility checks

A candidate must be evaluated for:

- capture timestamp
- capture source
- source integrity
- completeness
- non-derivation from the current estate
- readable repository identities
- preservation of original ordering, casing, formatting, duplicates, and anomalies

Reject with an explicit reason when any required property is missing or ambiguous.

## Prohibited transformations

Before manifest creation, do not:

- deduplicate names
- normalize casing
- repair spelling
- replace historical names with live names
- infer renames
- infer deletions
- merge or split entries
- fill gaps from memory
- supplement with current GitHub output

## Stop conditions

Search stops only when:

- an admissible historical artifact containing the complete original identity set is found; or
- all declared locations have been searched and no admissible artifact is found.

If no admissible artifact is found, state remains:

`COUNT KNOWN → IDENTITIES UNKNOWN → RECONCILIATION PENDING`

## Output boundary

This plan authorizes search and candidate logging only.

It does not authorize:

- `ORIGINAL_72_MANIFEST_V1`
- identity reconciliation
- repository classification
- rename, missing, added, private, archived, empty, split, or merge determinations
- portfolio completion claims

`authority: false`
