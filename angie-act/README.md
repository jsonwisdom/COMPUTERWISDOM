# ANGIE Act Public Scorecard Starter Kit

Run commands from the repository root.

## Purpose
This starter kit provides a clean JSON schema, example scorecards, and a validator for ANGIE Act public scorecards.

ANGIE = **Alignment • Norm • Gain • Integrity • Evidence**

The goal is simple: scorecards should be reproducible, auditable, and hard to game.

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jsonschema
python angie-act/scripts/validate_scorecard.py angie-act/examples/claim_001.clean.json
python angie-act/scripts/validate_scorecard.py angie-act/tests/fixtures/
```

## Files
- `schema/angie_act.schema.json` – Official schema (v1.0)
- `examples/` – Sample scorecards with different verdicts
- `scripts/validate_scorecard.py` – Validator v1.1 with business rules
- `tests/fixtures/` – Pass/fail test cases
- `LICENSE` – CC-BY-4.0

## Notes
- Example files are fictional training examples.
- Schema v1.0 checks structure.
- Validator v1.1 checks meaning and anti-gaming rules.
- All scorecards require record-based explanations and `source_links`.

## Validator v1.1 rules
1. `clean` requires at least 1 `source_link`
2. `evidence.score == 2` requires at least 3 `source_links`
3. `influence_flagged` requires meaningful `audit_notes`
4. `amy_flag == true` requires meaningful `audit_notes`
5. All filter explanations must be non-empty
6. All `source_links[].url` values must be valid absolute URIs
7. `claim_type = minnesota_state` must cite at least one Minnesota-specific source

> If the money trail cannot survive measurement, it does not get to masquerade as proof.
