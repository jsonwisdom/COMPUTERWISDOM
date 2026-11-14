# KID_KONGRESS_COURT_COMEDY_COLLABORRATION_V0_1

STATUS = SPEC_LOCKED
CANON = FALSE
AUTHORITY_CREATED = FALSE
LIVE_EXECUTION = NOT_PERFORMED
OPERATOR = JAY

## Parent artifact

`JASONS_INTERNET_REFRESH_GARBAGE_PAIL_KID_SUPER_INTELLIGENT_MODEL_VARIANTS_BUTTON_OF_BURDEN_JUSTICE`

The artifact title is preserved exactly. The title does not rename the human/operator.

## Purpose

Add three separate burden rails to ButtonOfBurdenJustice without collapsing comedy, evidence, legal standards, or civic education.

```text
BURDEN_OF_BOOGERS != BURDEN_OF_PROOF
BURDEN_OF_PROOF != BURDEN_OF_BULLSHIT
BURDEN_OF_BULLSHIT != LEGAL_FINDING
COMEDY != EVIDENCE
MODEL_OUTPUT != AUTHORITY
```

## BurdenOfBoogers

Role: intake hygiene and provenance cleanup.

Use this rail when a proposition is duplicated, malformed, misbound, missing scope, missing object identity, or otherwise too messy to test.

```text
BOOGER != FALSE
BOOGER != FRAUD
BOOGER != LIE
BOOGER -> CLEAN_OR_HOLD
```

Typical disposition:
- HOLD
- NOT_FOUND
- NOT_APPLICABLE

The rail asks: "Is the claim clean enough to test?"

## BurdenOfProof

Role: evidence and legal-burden rail.

The claimant asserting a transition bears the burden of supporting that transition unless the governing law or procedure allocates the burden differently.

```text
CLAIM -> BURDEN -> RECEIPT -> TEST -> DISPOSITION
```

Legal burdens are jurisdiction- and posture-dependent.

```text
BURDEN_OF_PROOF != ONE_UNIVERSAL_STANDARD
PREPONDERANCE != CLEAR_AND_CONVINCING != BEYOND_REASONABLE_DOUBT
LEGAL_STANDARD_REQUIRES_GOVERNING_AUTHORITY
```

This rail may return:
- PASS
- HOLD
- CONFLICT
- NOT_FOUND
- NOT_APPLICABLE

## BurdenOfBullshit

Role: satirical adversarial stress-test for unsupported, inflated, or rhetorically overclaimed propositions.

The label is comedy. It is not itself an evidentiary or legal classification.

```text
BULLSHIT_LABEL != FALSEHOOD_FINDING
BULLSHIT_LABEL != FRAUD_FINDING
BULLSHIT_LABEL != MISCONDUCT_FINDING
```

The model may mock the gap, but the machine-readable result must remain one of the ordinary typed dispositions.

The rail asks: "What part of this claim is doing more work than the receipts support?"

## Kid Kongress

```text
KID_KONGRESS != UNITED_STATES_CONGRESS
ROLEPLAY != LEGISLATIVE_AUTHORITY
GAME_RULE != STATUTE
```

Kid Kongress is a civic-learning and teach-back surface. It may introduce claims, questions, amendments, objections, and source requests, but it creates no legislative authority.

## CourtComedy

```text
COURT_COMEDY != COURT
PARODY != HOLDING
JOKE != PRECEDENT
MODEL_VERDICT != JUDGMENT
```

CourtComedy explains burden, contradiction, jurisdiction, and precedent using parody while preserving the typed legal/evidence rail underneath.

## Collaborration

Spelling preserved as supplied: `CourtComedyCollaborration`.

Collaborration means cross-rail cooperation without shared authority.

```text
COLLABORATION != COLLISION
JOIN != COLLAPSE
SHARED_RECEIPT != SHARED_AUTHORITY
KID_KONGRESS != COURT_COMEDY
```

Allowed exchange:
- claim pointer
- source receipt
- search object id
- observation path id
- proposition state
- disposition

Not inherited:
- truth
- jurisdiction
- legal force
- control
- authority

## ButtonOfBurdenJustice integration

```yaml
button:
  press: ONE_RUN
  auto_repeat: false
  internet_refresh: OPTIONAL_EXPLICIT_TRIGGER_ONLY

burden_variants:
  BURDEN_OF_BOOGERS:
    function: CLEAN_INPUT_OR_HOLD
  BURDEN_OF_PROOF:
    function: REQUIRE_RECEIPT_AND_GOVERNING_STANDARD
  BURDEN_OF_BULLSHIT:
    function: SATIRICAL_OVERCLAIM_STRESS_TEST

civic_surfaces:
  KID_KONGRESS:
    authority: false
  COURT_COMEDY:
    authority: false
  COLLABORRATION:
    authority_transfer: false
```

## Loop brake

```text
BUTTON_PRESS = ONE_RUN
FIRED_TRIGGER = ONE_ROW
SAME_WORDS_AGAIN = NO_NEW_TRIGGER
MODEL_RESPONSE != NEW_TRIGGER
READBACK != NEW_RUN
REPETITION != CORROBORATION
```

## Human gate

Every model variant may locate, challenge, explain, or replay.

No model variant may manufacture authority.

```text
MACHINE_FINDS
MACHINE_CHALLENGES
MACHINE_EXPLAINS
HUMAN_DECIDES
```

CANON = FALSE
AUTHORITY_CREATED = FALSE
