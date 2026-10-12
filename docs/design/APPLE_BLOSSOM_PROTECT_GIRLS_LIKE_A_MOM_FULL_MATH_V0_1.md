# Apple Blossom Awesome — Protect Girls Like a Mom Would — Full Math v0.1

> **Purpose:** design a protection system that carries the complexity for a girl instead of making her carry the institution.
>
> **AUTHORITY = false** · **HUMAN_CHAIR = the girl's words only** · **QUESTION ≠ BURDEN**

## Mom Rule

A girl should not need legal vocabulary, perfect screenshots, technical expertise, money, social status, or institutional stamina before adults and machines preserve evidence and open a safe path to help.

**Protect the girl. Preserve the evidence. Investigate the conduct. Hold proven offenders accountable. Do not turn protection into surveillance of the girl.**

Due process remains part of the evidence system: allegation, evidence, finding, and remedy stay distinct. Protecting a girl and requiring reliable proof are not opposites.

## The six non-negotiables

### 1. Name the girl explicitly

“Children,” “minors,” “users,” and “the public” are not substitutes for examining impacts on girls.

Systems must be able to test and report girl-specific failure modes, including:
- sexual deepfakes and synthetic intimate imagery
- AI-enabled harassment and stalking
- education surveillance and disciplinary systems
- hiring and employment systems
- financial and identity systems
- health and body-related systems
- housing and benefit systems

**GIRL_NAMED = REQUIRED**

### 2. Preserve the evidence before burden-dumping

When a report arrives, preservation starts before the girl is expected to reconstruct the event.

Potential records include:
- original messages and media
- generation metadata and provenance
- platform access and moderation logs
- account and device security events
- school records
- employer records
- transaction and payment records
- law-enforcement or agency records
- chain-of-custody events

Rule:

```
WHO_CONTROLS_DATA → PRESERVES_DATA
WHO_GENERATED_LOG → EXPLAINS_LOG
GIRL_REPORTS_HARM ≠ GIRL_REBUILDS_HIDDEN_SYSTEM
```

### 3. Put explanation duties where data and power live

The girl provides what she knows. Institutions holding inaccessible evidence carry the duty to produce, preserve, explain, and identify gaps in their own records, subject to applicable law.

```
GIRL → EXPERIENCE + AVAILABLE_RECEIPTS
PLATFORM → PLATFORM_LOGS + MODEL/ACCOUNT EVENTS
SCHOOL → SCHOOL_RECORDS + DECISION_PATH
EMPLOYER → EMPLOYMENT_RECORDS + DECISION_PATH
BANK/PAYMENT_RAIL → TRANSACTION/AUTHENTICATION_RECORDS
AGENCY → OFFICIAL_RECORD + ACCESS/AUDIT_TRAIL
```

This is not automatic liability. It is an evidence-access rule: **the party controlling a record should not make the least-powerful person prove what is hidden inside that party's system.**

### 4. Independent audit must be possible

For material automated decisions or serious harm reports, the relevant decision chain should be reproducible.

Minimum audit surface:
- exact system/model/version where available
- input provenance
- material transformation steps
- access and decision logs
- human interventions
- policy/rule version
- output
- retention/deletion state
- identified conflicts or missing edges

```
COMMERCIAL_SECRET ≠ BLANK_CHECK_FOR_UNREVIEWABLE_HARM
AUDIT_ACCESS ≠ PUBLIC_DUMP_OF_PRIVATE_DATA
```

Auditors need enough access to test the system while the girl's private information stays minimized and protected.

### 5. Remedy must be fast enough to matter

A remedy arriving after the damage has become permanent is incomplete.

Possible remedy lanes, depending on facts and law:
- rapid removal or access restriction
- account/device security recovery
- evidence preservation hold
- emergency safety planning
- school accommodations or transfer protections
- employment protections
- credit/payment remediation
- legal aid
- counseling and victim services
- civil remedies
- criminal referral when evidence supports it

Every lane needs:
**OWNER + DEADLINE + STATUS + APPEAL/CORRECTION PATH + RECEIPT**

### 6. Accountability follows the proven actor

Systems should resist easy evasion through anonymity, deletion, re-uploading, account hopping, cross-platform movement, synthetic identity, or AI face/voice substitution.

But the state machine remains explicit:

```
ALLEGATION ≠ FINDING
IDENTIFIER_MATCH ≠ PERSON_PROVEN
MODEL_OUTPUT ≠ FACT
EVIDENCE → REVIEW → FINDING → REMEDY / ACCOUNTABILITY
```

Confirmed offenders should not gain immunity merely because AI, anonymity, deletion, or platform boundaries made the evidence harder to follow.

## The protection boundary

If “protection” produces more surveillance, restriction, shame, or burden for the girl than for the system or perpetrator, the design has failed.

```
PROTECT_GIRL ≠ MONITOR_GIRL
PROTECT_GIRL ≠ SILENCE_GIRL
PROTECT_GIRL ≠ LIMIT_GIRL'S_FUTURE
PROTECT_GIRL ≠ FORCE_PUBLIC_DISCLOSURE
PROTECT_GIRL ≠ MAKE_HER_REPEAT_TRAUMA_TO_EVERY_SYSTEM
```

Default posture:
- minimize collection
- restrict access
- preserve necessary evidence
- explain who can see it
- let her correct the record
- do not infer consent from silence
- do not infer credibility from social status
- do not publish her story for her

## Mom-shaped interface

A girl should be able to begin with ordinary language:

> “Something happened and I need help.”

The system can ask only what is necessary for routing and immediate safety. It should not demand a courtroom-ready narrative at intake.

### First response

1. **Are you in immediate danger?**
2. **What do you want right now?** Stop it, save evidence, secure an account, tell someone, understand what happened, or something else.
3. **What can the system preserve without making you do more work?**
4. **Who must act next?**
5. **What will happen with your information?**

### Yellow is allowed

A girl may:
- be unsure
- change her mind
- remember more later
- disagree with the helper
- decline to answer nonessential questions
- ask for another trusted adult
- correct the record

Uncertainty is a state, not a credibility failure.

## Full Math responsibility chain

```
EVENT
→ SAFETY_TRIAGE
→ PRESERVATION_TRIGGER
→ DATA_CUSTODIAN_MAP
→ EVIDENCE_COLLECTION
→ PROVENANCE_BIND
→ CONFLICT_CHECK
→ INDEPENDENT_REVIEW
→ FINDING
→ REMEDY
→ ACCOUNTABILITY
→ CORRECTION / APPEAL
→ RETENTION / DELETION REVIEW
```

Every arrow must have:
- owner
- authority
- input
- output
- timestamp
- provenance
- access policy
- failure state
- correction path

Missing edge → **HOLD**, never silent promotion.

## Minimum machine schema

```json
{
  "rights_holder": "GIRL",
  "human_chair": "HER_WORDS_ONLY",
  "immediate_safety": "UNKNOWN|SAFE|AT_RISK",
  "requested_help": [],
  "evidence": {
    "user_available": [],
    "institution_controlled": [],
    "preservation_status": "OPEN|HELD|COMPLETE|UNKNOWN"
  },
  "custodians": [],
  "claims": [],
  "conflicts": [],
  "audit_state": "NOT_STARTED|OPEN|HOLD|CLOSED",
  "finding_state": "NONE|UNRESOLVED|SUPPORTED|NOT_SUPPORTED",
  "remedies": [],
  "accountability_actions": [],
  "privacy": {
    "collection_minimized": true,
    "access_logged": true,
    "girl_can_correct_record": true
  },
  "authority_created": false
}
```

## Mom test

Before shipping a policy, platform, school system, bank workflow, AI model, or government program, ask:

**If this were my daughter, would I accept this burden allocation?**

If the answer requires her to become the investigator, archivist, cybersecurity analyst, lawyer, acoustician, banker, or database administrator merely to get an adult institution to inspect its own records, the system is unfinished.

## Closing invariant

```
FULL_MATH_FOR_GIRLS
= EVIDENCE_COMPLETENESS
+ RESPONSIBILITY_COMPLETENESS
+ AUDIT_COMPLETENESS
+ REMEDY_COMPLETENESS
+ ACCOUNTABILITY_COMPLETENESS
+ PRIVACY_BOUNDARY
+ HUMAN_CHAIR
```

**Who controls the data, preserves it.  
Who deploys the system, explains it.  
Who exercises power, carries responsibility.  
Who causes proven harm, faces accountability.  
The girl does not fight the machine for the right to remain a person.**

**AUTHORITY_CREATED = FALSE**
