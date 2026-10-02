# Minnesota Law Monitor — Charter v0.1

**Authority:** false  
**Status:** OPERATING_CHARTER_DRAFT  
**Repo:** jsonwisdom/COMPUTERWISDOM  
**Path:** `mn/law-monitor/`

## Mission

Provide a machine-auditable, receipt-first surface for Minnesota legislative and statutory status events, sourced exclusively from official public records.

## Non-Goals

- Legal advice
- Political advocacy
- Enforcement claims
- Fraud adjudication
- Predictive modeling of bill outcomes
- Scraping behind auth or CAPTCHA without explicit policy PR

## Authority Boundary

```text
authority: false
truth_claim: false
fraud_status: UNKNOWN
```

Promotion of an event into the public docket does not create law, legitimacy, or official interpretation.

## Intake Rules

1. **Official source only** — URL hostname must match an allowed root (see README).
2. **One atomic event per entry** — one bill/action + one phase + one observed_at.
3. **No invented fields** — missing data stays null or omitted; never guessed.
4. **Replayable** — entry must be reconstructible from source_url + observed snapshot metadata.
5. **Human-witnessed first** — automated crawlers remain DISABLED until a separate governance PR enables them.

## Event Identity

Canonical key form:

```text
{session_year}-{chamber}{number}-{phase}-{observed_date}
```

Example:

```text
2025-HF12-PASSED_HOUSE-2025-05-20
```

## Mutation Policy

- Append-only preferred for docket history.
- Corrections are new events with `corrects: <prior_id>`, never silent overwrite.
- Every mutation gets a COMPUTERWISDOM-style receipt when promoted beyond draft.

## Security

No private keys, no credentials, no non-public legislative materials in this path.

See root `SECURITY.md` and `SECURITY_BOUNDARY.md`.

## Promotion Path

```text
manual observation
  → draft JSON (authority: false)
  → schema validation
  → operator receipt
  → docket append
  → optional public surface render
```

No merge or CI green alone creates authority.
