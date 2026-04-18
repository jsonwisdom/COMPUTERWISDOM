# HF4122 Escalation Ladder Comparison (v1.1)

This file shows the **minimal changes** that escalate the same real bill (HF4122 — Thermal energy network plan requirements) across tiers. All files validate cleanly under the current schema + validator.

## Teaching Point
v1.1 is intentionally minimal: it blocks gaming (bad URLs, weak `amy_flag` notes, missing sources) but leaves final `overall_verdict` to human judgment. The system rewards receipts.

## Side-by-Side Minimal Diffs

| File | overall_verdict | Evidence | Gain | Integrity | amy_flag | audit_notes length (stripped) | Key Addition |
|---|---|---:|---:|---:|---|---:|---|
| `hf4122_kraft_xcel.watch.json` | `watch` | 1 | 2 | 1 | false | n/a | Baseline alignment only |
| `hf4122_kraft_xcel_whatif.plausible_not_proven.json` | `plausible_not_proven` | 2 | 2 | 1 | true | >20 | Hypothetical dated contribution before bill activity |
| `hf4122_kraft_xcel_influence_flagged.json` | `influence_flagged` | 2 | 2 | 0 | true | >20 | Specific timing + procedural concern + material benefit mapping |

**Note:** Higher tiers are teaching demos with realistic timing. In production audits, replace hypothetical dates and amounts with direct links to Minnesota Campaign Finance Board CSV exports and actual amendment text diffs from revisor.mn.gov.

## Run the Proof

```bash
python angie-act/scripts/validate_scorecard.py angie-act/
```

Expected shape:
- Valid: `claim_001.clean.json`, `claim_002.plausible_not_proven.json`, `hf4122_kraft_xcel.watch.json`, `hf4122_kraft_xcel_whatif.plausible_not_proven.json`, `hf4122_kraft_xcel_influence_flagged.json`
- Invalid: `invalid_bad_url.json`, `invalid_missing_audit.json`

This is receipts-only influence forensics — no vibes, no auto-judgment.
