# CLAIM_EVIDENCE_TAXONOMY_V1

**Standard:** `GBS-BOXDEE-BURDEN-V001`  
**Status:** PROPOSED / PR-BOUND  
**Authority created:** `FALSE`

## 1. Purpose

Freeze the semantic claim taxonomy used by P1 without collapsing claim meaning into artifact type, actor identity, gender, relation labels, feelings, or authority.

```text
ACTOR_IDENTITY    != QUERY_MODE
MALE / FEMALE     != LOGICAL / EMOTIONAL
RELATION_LABEL    != VERIFIED_RELATION
FUNCTION          != GENDER
CLAIM_CLASS       != ARTIFACT_CLASS
PASS              != AUTHORITY
```

The canonical caller-facing discriminator is named `claimClass`, not `evidenceClass`, because `INPUT_EVIDENCE_V1.receipts[*].class` already describes artifact class. The two axes MUST remain independent.

## 2. Claim classes

`claimClass` MUST be exactly one of:

```text
FACT_CLAIM
SELF_REPORT
RELATION_LABEL
INTENT_INFERENCE
MIXED
```

### 2.1 FACT_CLAIM

An externally checkable proposition about an actor, object, event, state, transition, count, identity binding, repository state, transaction, or other world-facing fact.

A P1 PASS means only that the bounded factual claim satisfied the verifier's evidence burden under the frozen input.

```text
FACT_PASS = BOUNDED_FACT_BURDEN_SATISFIED
FACT_PASS != GLOBAL_TRUTH
FACT_PASS != AUTHORITY
```

### 2.2 SELF_REPORT

A bounded statement by a speaker about that speaker's own feeling, preference, memory, perception, intention, or internal experience.

A P1 PASS means only that the evidence establishes the bounded report occurred as attributed.

```text
SELF_REPORT_PASS = SPEAKER_REPORTED_THIS
SELF_REPORT_PASS != EXTERNAL_CAUSE_PROVEN
SELF_REPORT_PASS != THIRD_PARTY_INTENT_PROVEN
SELF_REPORT_PASS != AUTHORITY
```

The verifier MUST NOT convert the reported internal state into proof of an external causal claim.

Example:

```text
"Dad hurt my feelings."

A: speaker reports hurt feelings
   class = SELF_REPORT

B: Dad performed action X
   class = FACT_CLAIM

C: Dad intended harm
   class = INTENT_INFERENCE
```

### 2.3 RELATION_LABEL

A label or relationship token as presented in a bounded source, for example `dad`, `sister`, `brother`, `mom`, `friend`, `boss`, or another role label.

A P1 PASS means only that the label was observed as used in the bounded evidence.

```text
RELATION_LABEL_PASS = LABEL_USAGE_OBSERVED
RELATION_LABEL_PASS != BIOLOGICAL_RELATION_PROVEN
RELATION_LABEL_PASS != LEGAL_RELATION_PROVEN
RELATION_LABEL_PASS != SEX_OR_GENDER_PROVEN
```

If the claim is that the relationship is objectively true, that proposition is a `FACT_CLAIM` and bears its own burden.

### 2.4 INTENT_INFERENCE

A proposition assigning motive, purpose, knowledge, desire, or intent to another actor beyond a direct self-report by that actor.

Intent MUST NOT be inferred merely from outcome, relation label, emotion, visualization, story, or search result.

```text
OUTCOME != INTENT
FEELING != THIRD_PARTY_INTENT
RELATION_LABEL != INTENT
```

A P1 PASS requires independently admissible evidence sufficient for the bounded intent proposition. A self-report by the actor about their own intent may support the inference but remains a separately classified receipt-bearing observation.

### 2.5 MIXED

A query or sentence containing two or more propositions that require different claim classes.

`MIXED` is a routing/classification state, not a pass-eligible atomic adjudication target in P1 V1.

```text
MIXED -> DECOMPOSE -> ATOMIC CLAIMS -> VERIFY INDEPENDENTLY
```

P1 V1 MUST derive:

```text
claimClass == MIXED
burdenSatisfied = false
derivedResult = HOLD
reason includes MIXED_REQUIRES_DECOMPOSITION
```

A later aggregate report may preserve multiple independently verified claim results. It MUST NOT average, merge, or allow one lane to overwrite another.

```text
FEELINGS NEVER OVERWRITE FACTS
FACTS NEVER ERASE REPORTED FEELINGS
```

## 3. Artifact classes remain separate

`INPUT_EVIDENCE_V1.receipts[*].class` remains:

```text
RECEIPT
VISUALIZATION
DRAFT
```

These describe supporting object type, not proposition meaning.

```text
RECEIPT != FACT_CLAIM
VISUALIZATION != SELF_REPORT
DRAFT != INTENT_INFERENCE
```

A `RECEIPT` can support any compatible bounded claim class when correctly bound. `VISUALIZATION` and `DRAFT` cannot independently satisfy burden.

## 4. Actor and identity dimensions

P1 MUST NOT infer sex, gender, legal relation, biological relation, authority, or intent from names or labels alone.

```text
NAME != SEX
NAME != GENDER
DAD_LABEL != VERIFIED_MALE_IDENTITY
SISTER_LABEL != VERIFIED_FEMALE_IDENTITY
JOY_NAME != ACTOR_BINDING
```

Identity and relation claims, when material, are separate fact burdens.

## 5. PASS semantics are class-scoped

The string `PASS` remains one verifier disposition, but its semantic meaning is bounded by `claimClass`:

```text
FACT_CLAIM PASS
  = factual burden satisfied for the bounded proposition

SELF_REPORT PASS
  = attributed self-report occurrence established

RELATION_LABEL PASS
  = bounded label usage established

INTENT_INFERENCE PASS
  = bounded intent proposition satisfied by admissible evidence

MIXED
  = never PASS in P1 V1; decompose first
```

Therefore:

```text
PASS_ON_SELF_REPORT != PASS_ON_FACT_CLAIM
PASS_ON_RELATION_LABEL != VERIFIED_RELATION
ALL_PASS_STATES != AUTHORITY
```

## 6. Precedence is unchanged

Claim classification occurs before burden derivation. It does not replace or reorder the constitutional disposition precedence:

```text
CLASSIFY CLAIM
  -> CLASSIFY / BIND ARTIFACTS
  -> DERIVE BURDEN
  -> FAIL > DELTA > HOLD > PASS
```

`MIXED` forces HOLD after higher-order FAIL/DELTA conditions are considered, because decomposition is incomplete rather than contradictory.

## 7. Memory and story boundary

```text
MEMORY != PROOF
STORY != FACT
SELF_REPORT != EXTERNAL_CAUSE
RELATION_LABEL != VERIFIED_RELATION
```

Memory, story, and subjective testimony remain admissible as correctly classified evidence of what was remembered, narrated, or reported. They do not self-promote into proof of external claims.

## 8. Current status

This taxonomy is a proposed contract layer within the open PR. It creates no authority and is not execution evidence.

```text
TAXONOMY_DEFINED   = TRUE
P1_EXECUTION       = NOT ESTABLISHED
AUTHORITY_CREATED  = FALSE
```
