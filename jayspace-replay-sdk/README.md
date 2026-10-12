# JAYSPACE_REPLAY_SDK_v0.1

A reusable deterministic replay kernel extracted from JaySpace/ReceiptOS evidence mechanics without importing real-person, family, military, governmental, or fictional-character identity data.

## Product purpose

Turn evidence objects into typed receipts instead of asking an AI system to declare truth.

```text
CLAIM
-> SOURCE
-> AUTHORITY
-> ACTION
-> RECEIPT
-> REPLAY
-> PASS | HOLD | CONFLICT | REJECT
```

## Seven-node membrane

The SDK supports seven abstract node classes that may coexist in one case without collapsing into one another:

0. HISTORICAL_IDENTITY
1. RELATIONSHIP_ROLE
2. ALTERNATE_IDENTITY_RECORD
3. PUBLIC_PERSON_RECORD
4. CONTEXT_SPECIFIC_DERIVATION
5. GENERAL_SYNTHETIC_EXPLAINER
6. GENERATED_VARIANT

These are type labels, not declarations that any real-world identity or relationship exists.

## Non-collapse laws

```text
REAL_PERSON_RECORD != FICTIONAL_DERIVATION
FICTIONAL_DERIVATION != AUTHORITY
RELATIONSHIP_ROLE != IDENTITY_EQUIVALENCE
PUBLIC_RECORD != COMPLETE_BIOGRAPHY
SOURCE_FACT != SYNTHETIC_AUTHORITY
NARRATIVE_SIMILARITY != IDENTITY_MATCH
MODEL_OUTPUT != RECEIPT
REPLAY_RESULT != LEGAL_FINDING
AUTHORITY_CREATED = FALSE
```

## Deterministic terminal states

Precedence is fail-closed:

```text
REJECT > CONFLICT > HOLD > PASS
```

- PASS: required evidence edges are present and internally consistent.
- HOLD: a required edge is missing or unbound.
- CONFLICT: independently admissible records disagree.
- REJECT: a proposed promotion/equivalence contradicts an explicit boundary or bound evidence.

## Commercial surfaces

- Free: public claim / receipt verifier
- Pro: replay workspace + evidence ledger
- Team: collaborative CrissCross audits
- Enterprise: compliance / HR / legal / government replay workflows
- API: claim -> source -> authority -> action -> receipt
- Certification: replay-method training and audit standards

## Security and authority boundary

The deterministic core requires no network and no model. No API key belongs in this repository. Optional model integrations may explain a deterministic receipt but cannot modify the receipt, create authority, infer genealogy/relationships, or promote an identity equivalence.

`authority_created=false`
