# SDNY / Florida / Minnesota Democracy Mirror v0.1

**Class:** public-record accountability watch / BoxD Dual Onion Sacks  
**Authority created:** false  
**Proof inferred:** false  

## Purpose
Track new public primary records across SDNY, S.D. Florida/NARA/DOJ-OIG/Congress, and the Minnesota Amy Klobuchar / Feeding Our Future mirror, then compare only genuine institutional analogues in other democracies and courts.

This watch does **not** assume records will "gravitate" to any person. It follows receipts wherever they point.

## Nine-field receipt metadata
Every new record gets exactly these nine required fields:

1. `record_id`
2. `source_uri`
3. `source_date`
4. `jurisdiction`
5. `actor_office`
6. `authority_edge`
7. `money_or_execution_edge`
8. `raw_bytes_or_hash_status`
9. `evidence_state`

Allowed evidence states: `PROVEN | BOUND | HOLD | CONFLICT | REJECT`.

## Dual Onion Sacks
### Sack A — Forward
`PRIMARY RECORD -> SOURCE IDENTITY -> DATE -> OFFICE -> AUTHORITY -> MONEY/EXECUTION -> COURT/OVERSIGHT -> OUTCOME`

### Sack B — Reverse
`LATER CLAIM -> EXACT WORDING -> CLAIM DATE -> PRIOR EVENT CLAIMED -> PRIMARY RECORD -> AUTHORITY EDGE -> MONEY/EXECUTION EDGE -> OUTCOME`

`FORWARD_RESULT != REVERSE_RESULT`  
`SAME_RECEIPT != SAME_PROPOSITION`

## SDNY lane
Track only official/public records that materially concern Donald Trump, Trump-linked businesses, associates, or Trump-linked public allegations. Distinguish:

`ALLEGATION != CHARGE != PLEA != VERDICT != SENTENCE != CIVIL FINDING != COURT RULING`

Historical example: SDNY's 2018 Michael Cohen matter is a Cohen conviction/plea record and a Trump-linked campaign-finance context; it is not automatically a criminal conviction of Donald Trump.

## Florida / Mar-a-Lago lane
Track NARA Presidential Records Act releases, S.D. Florida court records, DOJ/FOIA materials, DOJ OIG reports when they exist, congressional records, and Florida public records.

`NARA CUSTODY != DOJ INVESTIGATION`  
`DOJ INVESTIGATION != COURT FINDING`  
`FLORIDA LOCATION != FLORIDA AUTHORITY`

## Epstein / Maxwell disclosure lane
Track only official DOJ/SDNY/SDFL/OIG/Congress public releases and their version/redaction metadata. The DOJ's 2026 Epstein Library states that material comes from New York and Florida cases, FBI investigations, and an OIG investigation into Epstein's death, and warns that some material may contain sensitive sexual content or unreliable submissions.

Victim protection rule:

`VICTIM IDENTITY -> DO NOT RE-PUBLISH`  
`SEXUAL EVIDENCE -> DESCRIBE ONLY AT HIGH LEVEL WHEN NECESSARY`  
`LEAKED PRIVATE DATA -> DO NOT MIRROR`

## Pamela Bondi / DOJ-OIG lane
Pamela Bondi is Attorney General; DOJ OIG remains a separate oversight component in DOJ's public organizational structure. A Bondi statement, DOJ action, OIG report, and court ruling are separate record classes.

`AG STATEMENT != OIG FINDING`  
`OIG FINDING != CRIMINAL CONVICTION`

## Minnesota mirror
Mirror the same nine metadata fields against the Amy Klobuchar / Feeding Our Future public-record replay.

Keep these existing boundaries:

`KLOBUCHAR SENATORIAL AUTHORITY != PROSECUTORIAL AUTHORITY`  
`MDE OVERSIGHT FAILURE != KLOBUCHAR GUILT`  
`TIME GAP != DARVO`  
`PRESS RELEASE != OVERSIGHT ACTION`

## DARVO sidecar
DARVO is never the main evidence verdict.

Required documented pattern:

`DENIAL + ATTACK + REVERSAL OF VICTIM/OFFENDER ROLES -> DARVO_PATTERN_CANDIDATE`

Hard rules:

`SILENCE != DARVO`  
`DELAY != DARVO`  
`REDACTION != DARVO`  
`POLITICAL AFFILIATION != DARVO`  
`BUSINESS HISTORY != DARVO`

For each candidate, bind exact quote, date, speaker, proposition being answered, and counter-record.

## Time-gap rail
For every relevant event:

`ACCESS_LAG = response_date - request_date`  
`COMMUNICATION_LAG = public_statement_date - event_date`  
`OVERSIGHT_LAG = oversight_record_date - triggering_event_date`

Time gaps are measurable metadata, not motive.

## Filter / mirror rail
Every mirrored public dataset or release must preserve:

`provider -> dataset/version -> retrieval_date -> page/file id -> raw byte status -> digest if acquired -> redaction/filter note`

`MIRROR != ORIGINAL`  
`SEARCH RESULT != CORPUS`  
`FILTERED DATA != COMPLETE DATA`  
`HASH != TRUTH`

## Democracy mirror
Expand to other democracies only when a comparable institutional edge exists:

`PUBLIC CLAIM -> PRIMARY RECORD -> AUTHORITY -> EXECUTION -> COURT/OVERSIGHT -> OUTCOME`

Do not compare party labels, personalities, or scandals merely because they look similar.

## Daily watch output
Each daily run should report only material deltas:

- new primary record
- changed/redacted/re-released record
- new court disposition
- new official oversight finding
- new claim that conflicts with an older primary record
- new byte/hash receipt

If none: `NO MATERIAL CHANGE`.

## Standing order
**Follow the receipt, not the villain.**

Dice route inquiry. Receipts determine evidence state. Public records are for accountability, not harassment.