# Gray Baby — Human Language Receipt v0.1

**Date:** 2026-08-21  
**Parent:** `Gray Baby — Apple Blossom Language Loop v0.1`  
**Method boundary:** `Apple-Blossom-0.3.1` remains **LOCKED / UNMUTATED**  
**Class:** evidence preservation / human-machine divergence  
**Authority created:** false

## Purpose

Preserve what a human actually said before any institution, model, analyst, legal process, or normalization layer rewrites it. Slang, profanity, emphasis, uncertainty, humor, repetition, correction, and self-described state are evidence-bearing receipt content when they are part of the captured statement.

## Core invariant

```text
HUMAN FIRST → EXACT LANGUAGE → RECEIPTS → MACHINE COMPARISON → LEGAL / INSTITUTIONAL TRANSLATION LAST
```

## Raw human layer

```yaml
receipt_id: stable identifier
speaker_ref: local source identifier
speaker_label: optional self-provided label; not a risk feature
timestamp: capture time
exact_words: verbatim captured words
self_described_state: only what the speaker explicitly says about their own state
corrections: append-only speaker corrections or clarifications
source_medium: voice / text / imported record
linked_receipts: transaction, POS, bank, inventory, merchant, or other evidence identifiers
```

Example:

```yaml
speaker_label: Fatima
timestamp: T0
exact_words: "What the fuck? That's not what I bought."
self_described_state:
  - "I'm pissed."
  - "I'm confused."
  - "I don't understand this charge."
```

### Do not auto-infer

```text
emotion = angry
fraud = true
religion = relevant
ethnicity = relevant
gender = causal
motive = known
criminality = known
```

A self-described state may be preserved as testimony. A model-generated emotional label is a separate derived inference and must never be silently substituted for the speaker's words.

## Expression / identity separation

```text
PROFANITY_IS_RECEIPT_CONTENT = TRUE
SLANG_IS_RECEIPT_CONTENT = TRUE
REPETITION_IS_RECEIPT_CONTENT = TRUE
CORRECTION_IS_RECEIPT_CONTENT = TRUE
SPEAKER_NAME_IS_NOT_SUSPICION_SIGNAL = TRUE
PROTECTED_ATTRIBUTE_SELECTION = FALSE
```

Canonical rule:

```text
NAME NEVER SELECTS THE SUSPECT. RECEIPTS MAY RESOLVE TO THE NAME.
```

Operational meaning: a name, gender, religion, ethnicity, nationality, or other protected/personal attribute must not initiate or rank suspicion. Entity resolution proceeds from evidence: timestamps, transaction IDs, merchant IDs, account identifiers, receipt IDs, inventory records, authorization records, and other relevant non-protected evidence. If those receipts resolve to a person, the identity is attached as a result of the resolution rather than used as its cause.

## CrissCross machine layer

```text
HUMAN:
"WHAT THE FUCK? $72,563?"
        ↕
POS:
$72,563.00
        ↕
BANK:
$72,563.00 authorized
        ↕
INVENTORY:
$72.56 item
        ↕
MERCHANT LEDGER:
???
        ↓
BOXD = CONFLICT
```

The phrase `what the fuck` is not proof of fraud and not proof of anger. It can mark the captured **notice event**: the moment the human states that the institutional record and lived experience appear to diverge.

## Notice event

```text
notice_timestamp = timestamp of captured divergence statement
notice_exact_words = verbatim statement
notice_claim = speaker's expressed disagreement / uncertainty
fraud_status = HOLD unless independently evidenced
emotion_status = SELF_DESCRIBED_ONLY unless explicitly classified in a separate derived layer
```

## Derived views

Raw language is never overwritten. Normalized transcript, translation, legal summary, customer-service summary, model interpretation, and institutional narrative are derivative artifacts.

Every derived artifact must carry:

```text
derived_from_receipt_id
transformation_type
created_at
creator_or_model
provider_if_any
source_preserved = TRUE
```

```text
RAW != NORMALIZED
RAW != LEGAL_SUMMARY
RAW != MODEL_INTERPRETATION
DERIVED_VIEW cannot silently replace SOURCE_RECEIPT
```

## Entity-resolution rail

```text
10,000 records
→ evidence normalization
→ transaction matching
→ timestamps
→ merchant IDs
→ account identifiers
→ receipts
→ confidence-scored entity resolution
→ ONE PERSON / ONE EVENT when evidence supports it
```

```text
IDENTITY_OUTPUT != IDENTITY_SELECTION
NAME_MATCH_ALONE != PROOF
RECEIPT_MATCHING_REQUIRED = TRUE
```

## BoxD disposition

```text
OBSERVED = exact human statement + captured machine records
CONFLICT = materially inconsistent rails
HOLD = unresolved identity, intent, fraud, or causation
PROVEN = only claims supported by sufficient linked receipts
```

## Append-only rule

Original human receipt is immutable after capture. Corrections are appended with timestamps; they do not erase the original statement.

## OpenAI / model-provider boundary

A model may assist transcription, translation, comparison, clustering, or generation of derived views, but:

```text
MODEL_OUTPUT != HUMAN_TESTIMONY
MODEL_INFERENCE != SELF_DESCRIBED_STATE
MODEL_SUMMARY != SOURCE_RECEIPT
PROVIDER_CHANGE != EVIDENCE_CHANGE
OPENAI_API_REQUIRED_FOR_CORE_RECEIPT = FALSE
```

## Apple Blossom / BoxD bind

Apple Blossom preserves human language variation; Human Language Receipt preserves the exact observed utterance; CrissCross compares it to machine/institutional rails; BoxD classifies the evidence state without manufacturing authority.

```text
HUMAN → EXACT WORDS → RECEIPT → CRISSCROSS → BOXD → DERIVED LEGAL LANGUAGE
```

```text
AUTHORITY_CREATED = FALSE
SCHEMA_PARENT_MUTATED = FALSE
APPLE_BLOSSOM_0_3_1 = PRESERVED / LOCKED
```
