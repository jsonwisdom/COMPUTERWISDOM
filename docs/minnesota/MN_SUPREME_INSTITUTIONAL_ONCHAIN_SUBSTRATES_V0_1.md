# Minnesota Supreme Institutional Auditing — On-Chain Substrates v0.1

Status: DRAFT / REVIEWABLE / ENABLED_FOR_BUILD
Authority: AUTHORITY_CREATED = FALSE
Epoch: 2026

## Purpose

Create a Minnesota institutional-audit substrate that preserves source bytes off-chain, commits bounded hashes on-chain, and replays Record and Power onions independently.

`SUPREME` means highest-order architectural audit substrate. It does **not** mean the Minnesota Supreme Court, judicial authority, or governmental supremacy.

## Geographic Scope

```text
MINNESOTA
  -> STATE
  -> COUNTY
  -> CITY | TOWN | TOWNSHIP
  -> OFFICE | AGENCY | COURT | AUTHORITY
  -> BUDGET | FUND | PROGRAM
  -> CONTRACT | GRANT | PAYMENT
  -> BUSINESS_ENTITY
  -> AUDIT | CASE | FINDING
```

People are not primary graph nodes. `OFFICEHOLDER` and `PERSON_GAP` are temporal/resolution metadata only when a public record requires the join.

## Dual Onion

### Onion A — RECORD

```text
SOURCE
 -> FETCH
 -> RAW_BYTES
 -> CANONICALIZE
 -> SHA256
 -> RECEIPT
 -> ON_CHAIN_COMMITMENT
 -> INDEPENDENT_REPLAY
 -> DELTA
```

### Onion B — POWER

```text
INSTITUTION
 -> OFFICE
 -> CLAIMED_AUTHORITY
 -> LAW | POLICY | ORDER
 -> ACTION
 -> IMPLEMENTATION
 -> CONSEQUENCE
 -> RECEIPT
 -> REPLAY
```

Evidence in one onion cannot pay for a missing edge in the other.

## On-Chain Boundary

The chain stores commitments and replay metadata, not sensitive source records.

Allowed on-chain fields:
- artifact/content hash
- canonicalization version
- source class
- jurisdiction ID
- timestamp / block reference
- prior commitment hash
- receipt ID
- replay state

Blocked by default:
- raw court filings
- private PII
- protected health data
- private financial account data
- unredacted victim data
- allegations without source classification

```text
RAW_BYTES = OFF_CHAIN
HASH_COMMITMENT = MAY_BE_ON_CHAIN
HASH != TRUTH
CHAIN_TIMESTAMP != EVENT_PROOF
ON_CHAIN != AUTHORITY
```

## 2026 Versioning

```text
ANNUAL_ROOT: MN/2026
  -> STATE_ROOT
  -> 87 COUNTY ROOTS
  -> MUNICIPAL ROOTS
  -> INSTITUTION ROOTS
  -> DAILY RECEIPTS
  -> EVENT RECEIPTS
```

Every update is append-only:

```text
S(t+1) = S(t) + DELTA(t)
NEW_INFORMATION != REWRITE_OLD_STATE
```

Cadence:
- EVENT = source/budget/case/payment change
- DAILY = Dual Onion close receipt
- MONTHLY = budget/entity reconciliation
- ANNUAL = frozen 2026 Minnesota root

## Budget + Fraud Overlay

```text
OFFICE | AGENCY
 -> APPROPRIATION
 -> FUND | PROGRAM
 -> CONTRACT | GRANT
 -> BUSINESS_ENTITY
 -> PAYMENT
 -> PROPERTY | PROVIDER | RELATED_ENTITY
 -> AUDIT | CASE | FINDING
```

Fraud state is typed and source-scoped:

```text
NORMAL_PUBLIC_RECORD
ANOMALY
AUDIT_FINDING
CIVIL_ALLEGATION
CRIMINAL_CHARGE
PLEA
CONVICTION
SETTLEMENT
HOLD
```

Shared addresses, registered agents, Delaware formation, political office, or graph proximity do not independently establish fraud.

## Institutional Nodes

Primary nodes may include:
- Minnesota Judicial Branch / courts
- Minnesota Legislature
- constitutional offices
- state agencies
- counties
- cities/towns/townships
- school districts
- public authorities and boards

Each node is audited as an institution, not as a person.

## Imagination Attestation

Story surfaces may name symbolic interfaces such as BoxDee, LeahPrime, or other JaySpace teaching objects, but must be machine-typed:

```json
{
  "type": "IMAGINATION_ATTESTATION",
  "story_is": "INTERFACE_AND_EXPLORATION",
  "source": false,
  "receipt": false,
  "authority": false,
  "promotion_requires_independent_evidence": true
}
```

`STORY != SOURCE != RECEIPT != AUTHORITY`.

## Surface Contract

- GitHub = schemas, code, commits, PR state, tests, verifier artifacts.
- Google Drive = drafts, maps, runbooks, source packets, continuity.
- Google Calendar = milestone/review timestamps only; calendar event != proof.
- OpenAI Platform = access surface only unless independent runtime/deployment evidence is bound.
- Public chains = bounded commitment surface only.

## Terminal States

`PASS | HOLD | CONFLICT | REJECT`

## Enablement State

```json
{
  "mn_supreme_institutional_audit": "ENABLED_FOR_BUILD",
  "on_chain_commitments": "ENABLED_WITH_PRIVACY_MEMBRANE",
  "raw_bytes_on_chain": false,
  "dual_onion_required": true,
  "state_county_municipal_hierarchy": true,
  "budget_fraud_overlay": true,
  "people_primary_nodes": false,
  "authority_created": false
}
```

Closing rule: preserve bytes, commit hashes, replay independently, expose deltas, never manufacture authority.
