# ADR-008 — Wisdom Operator Specification

## Status

```text
DRAFT_UNFROZEN
HUMAN_AUTHORITY_REQUIRED
AI_DECISION_AUTHORITY_FALSE
AI_EXECUTION_AUTHORITY_FALSE
RUNTIME_ENFORCEMENT_NOT_PROVEN
```

## Context

COMPUTERWISDOM already separates personal, private, and public planes and requires human authorization for cross-plane movement and execution. Those controls answer where information belongs and how it may move, but they do not answer whether an action should occur.

The Wisdom Operator introduces a human-governed review layer before consequential action, publication, commercialization, identity merge, or family-memory release.

This is a governance model, not literal physics and not a claim that software can compute morality.

## Decision

Adopt the following review sequence:

```text
OBSERVE
→ VERIFY
→ UNDERSTAND
→ CARE
→ DECIDE
→ ACT
→ LEARN
→ REPLAY
```

The `CARE` stage is a required human review of foreseeable impact, dignity, consent, privacy, family meaning, and downstream consequences. It is not delegated to an AI system.

## Operator Contract

```json
{
  "operator": "APPLY_WISDOM",
  "authority": "human",
  "ai_role": ["search", "organize", "compare", "draft"],
  "ai_decision_authority": false,
  "ai_execution_authority": false
}
```

## Wisdom Index Questions

Before public release or consequential action, the human reviewer asks:

1. Is it true?
2. Is it useful?
3. Is it kind?
4. Is it replayable?
5. Will it still make sense in 50 years?

A negative or unresolved answer routes the artifact back to revision, evidence collection, consent review, or archive.

## Plane Roles

```text
ALMS                = Can we prove it?
JOY                 = Why does it matter?
COMPUTERWISDOM      = How do we teach and share it?
WISDOM              = Should we do it at all?
```

These are design questions, not grants of legal, moral, family, or technical authority.

## Family Boundary

When a proposal affects family identity, memory, dignity, privacy, commercialization, or legacy:

```text
ALMS RECEIPT
→ REPLAY
→ WISDOM REVIEW
→ FAMILY REVIEW
→ HUMAN AUTHORIZATION
→ PUBLIC DERIVATIVE
```

No family member is assigned authority, consent, or responsibility merely because the architecture names a role or symbolic axis. Actual participation must be voluntary and explicit.

## Invariants

```text
NO_MODEL_JUDGMENT_CREATES_EXECUTION_AUTHORITY
CARE_IS_NOT_AUTOMATED
VERIFICATION_DOES_NOT_EQUAL_PERMISSION
FAMILY_MEANING_DOES_NOT_EQUAL_PUBLICATION_CONSENT
IDENTITY_POINTER_DOES_NOT_CREATE_AUTHORITY
DRAFT_DOES_NOT_EQUAL_CANON
```

## Consequences

Positive:

- makes human judgment explicit;
- prevents proof from being mistaken for permission;
- creates a review point for dignity, consent, and long-term consequences;
- remains vendor-independent and portable.

Tradeoffs:

- introduces deliberation latency;
- cannot guarantee wise outcomes;
- requires named human accountability;
- cannot be reduced to a fully mechanical score without losing its purpose.

## Verification State

```text
SPECIFICATION_PRESENT = TRUE
RUNTIME_IMPLEMENTED = FALSE
INDEPENDENTLY_REPLAYED = FALSE
SIGNED = FALSE
HASH_FROZEN = FALSE
PUBLICATION_AUTHORIZED = FALSE
```
