# Gray Baby — Apple Blossom Language Loop v0.1

**Date:** 2026-08-20  
**Class:** education / multilingual interface experiment  
**Authority created:** false  
**BoxD posture:** `OBSERVE → TEST → REPLAY → BOUND OR HOLD`

## Purpose

Make language learning fun, shareable, careable, collaborative, and easy to replay across languages while using emoji as a visual anchor.

## Core model

```text
EMOJI = ANCHOR / BOUND REFERENCE
PHRASE = ROTATING LANGUAGE EVIDENCE
INTENT = TEST TARGET, NOT AUTOMATIC PROOF
LEARNER CONFIRMATION = BINDING SIGNAL FOR THAT ROUND
```

Emoji meaning is often shared across cultures, but not identical everywhere. An emoji can anchor a lesson without proving a universal emotional meaning.

## Apple Blossom loop

```text
SEE EMOJI
→ HEAR PHRASE
→ SAY PHRASE
→ SWAP LANGUAGE
→ KEEP EMOJI ANCHOR
→ ASK LEARNER: “Same meaning?”
→ REPLAY OR CORRECT
```

### Example

```text
ENGLISH: “I love this.” ❤️
SPANISH: “Me encanta esto.” ❤️
FRENCH: “J’adore ça.” ❤️
```

Expected result:

```text
ANCHOR_HOLDS_FOR_ROUND = learner-confirmed
PHRASE_VARIATION       = observed
INTENT_MATCH           = tested
UNIVERSAL_MEANING      = HOLD
```

## Contrast pairs

- ❤️ LOVE ↔ 😡 HATE / ANGER
- ✅ YES ↔ 🚫 NO
- 😂 FUNNY ↔ 😴 BORING
- 👋 COME / HELLO ↔ 👉 GO / THERE
- 🤝 TRUST ↔ ⚠️ CAUTION

Do not assume one gender owns an emotion or communication style. Test the individual learner’s interpretation.

## BoxD status emoji

- ✅ = PROVEN / BOUND IN CURRENT TEST
- ❌ = NOT PROVEN / REJECTED
- ⚡ = TESTABLE / HIGH PRIORITY
- 🧅 = CONTEXT LAYER / NEEDS PEELING
- 📦 = VERSIONED / LOCKED STATE

## Test class — minimum viable round

1. Choose five emoji anchors.
2. Teach five short English phrases.
3. Rotate each phrase into one second language.
4. Ask the learner to identify the intended meaning without seeing the English phrase.
5. Record `correct / ambiguous / wrong`.
6. Replay after ten minutes.
7. Compare recall and confidence.

## Metrics

```text
COMPREHENSION  = correct intent / attempts
RECALL         = correct phrase after delay / attempts
TRANSFER       = correct intent after language swap / attempts
AMBIGUITY_RATE = disputed emoji meaning / attempts
FUN_FACTOR     = learner self-report
CARE_FACTOR    = learner willingness to continue / share / help a partner
```

## Disposition

```text
PEDAGOGICAL_PATTERN          = BOUND / PROMISING
EMOJI_AS_UNIVERSAL_RECEIPT   = HOLD
PHRASE_ROTATION              = TESTABLE
LEARNER_ACQUISITION          = HOLD UNTIL TESTED
SHAREABILITY                 = TESTABLE
```

## OpenAI implementation rail — optional

A future prototype can use realtime speech translation for the language swap and a conversational voice model for pronunciation, replay, correction, and turn-taking. An Apps SDK interface could display the emoji anchor, phrase variants, replay state, and learner-confirmed intent.

This is an implementation candidate, not a dependency of the learning method.

## Canonical invariant

```text
WORDS CHANGE.
EMOJI PERSISTS AS A VISUAL CUE.
MEANING MUST STILL BE TESTED.
LEARNER CONFIRMATION CLOSES THE ROUND.
```

🌸🍎👽  
**APPLE BLOSSOM = SEE → SAY → SWAP → CONFIRM → REPLAY**

---

## Formalization state — Apple-Blossom-0.3.1

```text
SCHEMA_STATE            = LOCKED
ROUND_RECEIPT           = CANONICAL
replay_correct          = SINGLE_DELAY_BOOLEAN
DERIVED_PREDICATES      = COMPUTED_ONLY
LEVEL_6_BOUNDARY        = ITEM_RETENTION_ONLY
SCHEMA_MUTATION         = VERSION_BUMP_REQUIRED
01_SCHEMA_LOCK          = COMPLETE
02_ASSISTANCE_MAPPING   = LOCKED_FOR_PRODUCTION
```

Canonical BoxD invariant:

```text
RECEIPT → COMPUTE → CLAIM
never
CLAIM → INFER MISSING RECEIPT
```

### 02 — Assistance-level mapping

`assistance_level` records the highest assistance actually used during the scored production attempt. Assistance merely offered or available does not count.

```text
0 = NO CUE
1 = EMOJI CUE
2 = AUDIO CUE
3 = PARTIAL PHRASE
4 = FULL PHRASE
```

Higher values represent stronger scaffolding for claim-gating purposes.

#### Claim ceiling imposed by assistance

```text
assistance_level = 4  → maximum licensable level = LEVEL_1 / RECOGNITION
assistance_level = 3  → maximum licensable level = LEVEL_2 / CUED_RECALL
assistance_level = 2  → maximum licensable level = LEVEL_2 / CUED_RECALL
assistance_level = 1  → maximum licensable level = LEVEL_2 / CUED_RECALL
assistance_level = 0  → may qualify for LEVEL_3–LEVEL_6, subject to outcome and replay gates
```

A full supplied phrase is exposure/recognition evidence, not recall or independent production evidence.

#### Progression gates

```text
LEVEL_0 = EXPOSURE
LEVEL_1 = recognition_correct == true
LEVEL_2 = recall_correct == true AND assistance_level IN {1,2,3}
LEVEL_3 = recall_correct == true AND assistance_level == 0
LEVEL_4 = production_correct == true AND assistance_level == 0
LEVEL_5 = delayed replay gate executed after delay_seconds > 0
LEVEL_6 = TARGET ITEM RETAINED / REPLAYABLE only when the delayed replay is independently evidenced
```

`INDEPENDENT_SUCCESS` remains valid under v0.3.1:

```text
INDEPENDENT_SUCCESS =
  production_correct == true
  AND assistance_level == 0
```

### BoxD conflict discovered during Step 02

The locked v0.3.1 schema describes `assistance_level` at production time. It does not separately record assistance actually used during the delayed replay check.

Therefore:

```text
replay_correct == true
DOES NOT BY ITSELF PROVE
replay_assistance == 0
```

A delayed replay can be correct while still being cued. Under the receipt-first invariant, independent Level-6 retention cannot be promoted from v0.3.1 unless zero replay assistance is independently guaranteed by the protocol and evidenced.

```text
RETENTION_SUCCESS_v0.3.1              = DELAYED_REPLAY_SUCCESS
INDEPENDENT_RETENTION_SUCCESS_v0.3.1  = HOLD / INSUFFICIENT_REPLAY_ASSISTANCE_RECEIPT
```

No v0.3.1 field is renamed or mutated.

### Proposed migration gate — Apple-Blossom-0.3.2

A future schema version may add:

```text
replay_assistance_level: INTEGER  # 0–4; highest assistance actually used during delayed replay
```

Then independent retention becomes fully recomputable:

```text
INDEPENDENT_RETENTION_SUCCESS =
  production_correct == true
  AND assistance_level == 0
  AND delay_seconds > 0
  AND replay_correct == true
  AND replay_assistance_level == 0
```

Until that migration is explicitly accepted and versioned, v0.3.1 remains frozen.

```text
02_ASSISTANCE_LEVEL_MAPPING       = LOCKED
PRODUCTION_INDEPENDENCE           = COMPUTABLE
REPLAY_INDEPENDENCE               = HOLD
LEVEL_6_INDEPENDENT_RETENTION     = HOLD_PENDING_REPLAY_ASSISTANCE_RECEIPT
NEXT_GATE                         = 03_RETENTION_CURVE / BOUNDED_BY_RECEIPT_QUALITY
AUTHORITY_CREATED                 = FALSE
```

---

## Directories-first responsive-language correction — 2026-08-21

AppleBlossom does not invent a new semantic or authority layer merely because a familiar word appears again.

Jason/Jay's repeated vocabulary is treated as a local navigation grammar:

```text
RULE_01 = DIRECTORIES_FIRST
WORD = PATH_TOKEN
REPEATED_WORD = INCREASE_LOOKUP_DEPTH
VARIANT = CHECK_LINEAGE_BEFORE_NEW_NODE
KNOWN_TERM = REPLAY_EXISTING_SEMANTICS_THEN_APPLY_DELTA
```

Traversal contract:

```text
TOKEN
→ PLATFORM / ROOT
→ LEVEL_1
→ LEVEL_2
→ LEVEL_3
→ ...
→ STOP_AT_USER_LANGUAGE_DEPTH
→ ANSWER_FROM_OBSERVED_STATE
```

Examples:

```text
APPLEBLOSSOM
→ method
→ receipt schema
→ implementation
→ family integration
→ provider boundary

PARENT
→ JOY family graph / parental-role variants
→ existing parental switchboard / approval membranes
→ AppleBlossom consumer binding
```

The system must not create `NEW_PARENT_LAYER` when JOY already exposes the relevant family/parental lineage.

```text
REPETITION != REDUNDANCY
VARIANT != NEW_IDENTITY_BY_DEFAULT
DIRECTORY_EXISTS_BEFORE_ABSTRACTION = REQUIRED_CHECK
```

This correction changes navigation/interpretation behavior only. It does not mutate Apple-Blossom-0.3.1 fields or learner claims.

## Existing JOY parental lineage — consume, do not replace

The AppleBlossom family implementation is downstream of JOY's already-existing parental/family semantics. At minimum, current project history includes parental-role variants such as `DADDY_JAY`, `DAD`, `DADDY_WISDOM`, `MR_WISDOM`, and `MRS_WISDOM`, plus a parental switchboard integration rail.

Those variants are context-specific surfaces and must be replayed before inventing any replacement abstraction.

```text
JOY_PARENTAL_LINEAGE
→ PARENTAL_SWITCHBOARD
→ APPLEBLOSSOM_ROUND
→ HEIDEE_EXPERIENCE
→ OPTIONAL_PROVIDER
```

Provider rule:

```text
OPENAI != PARENTAL_AUTHORITY
APPLE_MODEL != PARENTAL_AUTHORITY
MODEL_OUTPUT != FAMILY_SEMANTICS
PROVIDER_CHANGE != FAMILY_ROLE_CHANGE
```

`AUTHORITY_CREATED = FALSE`
