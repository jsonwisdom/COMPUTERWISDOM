# G-Dice Intelligence Federation v0.1

STATUS = PUBLIC_EDUCATIONAL_HYPOTHESIS_REPLAY
OFFICIAL_IC_ORGANIZATIONS = 18
LOGICAL_DICE = 20
AUTHORITY_CREATED = FALSE
INTELLIGENCE_FINDING_CREATED = FALSE
LAW_ENFORCEMENT_FINDING_CREATED = FALSE
CLASSIFIED_ACCESS = FALSE
OPERATIONAL_TASKING = FALSE

## Purpose
Model how a top-level claim can be decomposed into bounded hypotheses without pretending to reproduce any agency's actual internal analytic process.

## 20-dice topology

- D00 = G-DICE / constitutional question grammar
- D01..D18 = one public-mission-mapped local die for each official U.S. Intelligence Community organization
- D19 = CROSS-IC RECONCILIATION DIE

This is **20 logical dice, not 20 intelligence agencies**.

## G-DICE D6

1. WHO — actor / identity claim
2. WHAT — event / conduct claim
3. WHERE — geography / jurisdiction
4. WHEN — timeline / sequence
5. HOW — capability / mechanism
6. WHY — intent claim / competing explanations

## Agency-local D6 template
Each D01..D18 applies the same public evidence questions through that organization's publicly documented mission filter:

1. MISSION_FIT
2. SOURCE
3. CAPABILITY
4. JURISDICTION
5. COUNTER_HYPOTHESIS
6. VERDICT = PASS | HOLD | CONFLICT | REJECT | UNKNOWN

## D19 Cross-IC reconciliation D6

1. SOURCE_CONFLICT
2. TIMELINE_CONFLICT
3. IDENTITY_CONFLICT
4. JURISDICTION_CONFLICT
5. CONFIDENCE_OR_EVIDENCE_QUALITY_MISMATCH
6. UNKNOWN_HOLD

## Replay

CLAIM
→ G-DICE
→ 0..18 RELEVANT LOCAL DICE
→ D19 RECONCILIATION
→ EVIDENCE GATE
→ PUBLIC RECEIPT
→ OPTIONAL DOWNSTREAM COMMERCIAL_FAFO / LAWFUL_OSINT

## Membranes

RANDOMNESS MAY SELECT A QUESTION.
RANDOMNESS MUST NEVER DECIDE WHETHER EVIDENCE IS TRUE.

PUBLIC_MODEL != GOVERNMENT_SYSTEM
AGENCY_LABELED_DIE != AGENCY_ENDORSEMENT
PUBLIC_MISSION_MAPPING != INTERNAL_METHOD
HYPOTHESIS != INTELLIGENCE_FINDING
INTELLIGENCE_FINDING != CRIMINAL_FINDING
CLAIM != TARGET
SUSPICION != CRIMINAL
NATIONALITY != THREAT
IDENTITY_ATTRIBUTE != PROBABLE_CAUSE
COMMERCIAL_OSINT != LAW_ENFORCEMENT_AUTHORITY

No human or broad class becomes a target because a die selected a hypothesis. Particularized evidence must survive the evidence gate before any downstream investigative referral.

## OpenAI developer contract
A future implementation may use structured model outputs to generate questions, classify source state, surface contradictions, and propose counter-hypotheses. Model randomness or confidence must never be treated as legal authority or factual proof. No API key or agent is required at this scaffold stage.

## Source state
ODNI currently identifies 18 organizations in the U.S. Intelligence Community. Keep that count source-bound independently from this model.
