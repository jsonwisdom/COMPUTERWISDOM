# FBI Fraud Finder — Tom Homan $50,000 Version Replay v0.1

**Class:** public-record authority/version audit  
**Workflow:** `FBIFraudFinderWorkFlow`  
**Subject:** Thomas D. Homan  
**Proposition ID:** `FBI-TOM-HOMAN-50000-001`  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Core proposition

What public records establish about the reported 2024 undercover FBI operation involving Tom Homan and a reported $50,000 cash payment, how DOJ/FBI later described and closed the matter, and how media, congressional, FOIA, and administration versions changed over time.

## Hard membrane

```text
MEDIA_REPORT != PRIMARY_BYTE
CONGRESSIONAL_QUESTION != ANSWER
INVESTIGATION != GUILT
CASH_PAYMENT != BRIBE_FINDING
CASE_CLOSED != EVENT_DID_NOT_OCCUR
DECLINATION != EXONERATION_OF_EVERY_FACT
NO_CREDIBLE_CRIMINAL_EVIDENCE != NO_EVIDENCE_EXISTED
PRIVATE_CITIZEN != GOVERNMENT_CONTRACTING_AUTHORITY
FOIA_WITHHOLDING != DELETION
RECORDING_REPORTED != RECORDING_PUBLICLY_ACQUIRED
```

## Authority clock

### T0 — 2024 reported undercover operation

Media reporting by Reuters, AP, Washington Post, ABC, and others states that an FBI undercover operation in 2024 recorded Homan receiving a bag containing approximately $50,000 from agents posing as business executives while discussing possible future government-contract assistance.

At the reported transaction date Homan was a **private citizen**, not a federal contracting officer or White House official.

```text
UNDERCOVER_OPERATION_EXISTED = BOUND_MEDIA / later acknowledged as a DOJ/FBI matter
$50K_CASH_ACCEPTANCE = BOUND_MULTI_SOURCE / HOLD_PRIMARY_BYTE
QUID_PRO_QUO = HOLD
CRIMINAL_BRIBERY_FINDING = REJECT
HOMAN_GOVERNMENT_CONTRACT_AUTHORITY_AT_T0 = FALSE
```

### T1 — September 2025 public disclosure

Major media outlets published source-based accounts of the investigation. The stories generally converge on four reported facts:

1. an undercover FBI operation existed;
2. approximately $50,000 cash was reportedly transferred;
3. the interaction was reportedly recorded;
4. investigators were considering whether later government-contract conduct would supply an additional factual/legal edge.

The published stories are **secondary-source snapshots**, not the recording, case file, close-out memo, or cash-custody record.

### T2 — September 2025 DOJ/FBI closure version

FBI Director Kash Patel and Deputy Attorney General Todd Blanche publicly stated that the matter originated under the prior administration, was reviewed by FBI agents and DOJ prosecutors, that the review found `no credible evidence of any criminal wrongdoing`, and that the investigation was closed.

```text
INVESTIGATION_ACKNOWLEDGED = PROVEN_PUBLIC_STATEMENT
INVESTIGATION_CLOSED = PROVEN_PUBLIC_STATEMENT
OFFICIAL_CLOSURE_RATIONALE = BOUND_TO_STATEMENT
CLOSE_DATE = HOLD
CLOSE_DECISION_MAKER = HOLD
DECLINATION_OR_CLOSE_MEMO_PUBLIC = FALSE
```

### T3 — White House / Homan public versions

The White House characterized the investigation as politically motivated and said Homan did nothing wrong and was not involved in White House contract-award decisions. Public Homan responses evolved from formulations centered on having done nothing illegal / there being nothing to the matter to a later categorical denial that he accepted the reported $50,000.

This is a **version delta**, not itself proof that either version is false.

```text
VERSION_DELTA_HOMAN = BOUND
MEMORY_OR_WORDING_CONFLICT = REVIEW_REQUIRED
```

### T4 — Congressional oversight 2025–2026

House and Senate members requested recordings, investigative files, close-out material, the disposition of the reported $50,000, and communications involving DOJ/FBI/White House/transition officials.

A House Judiciary Questions for the Record document asked FBI Director Patel whether the FBI possessed audio/video recordings, other records indicating cash acceptance, what became of the $50,000, and when/who closed the investigation.

In July 2026 Senate Judiciary Questions for the Record, Deputy Attorney General Blanche declined to disclose the non-public close date, decision-makers, internal deliberations, White House communications, or the disposition of the reported $50,000. He repeated the official public position that the matter was reviewed and closed after no credible evidence of criminal wrongdoing was found.

```text
CONGRESSIONAL_QUESTIONS_EXIST = PROVEN
PUBLIC_ANSWER_CLOSE_DATE = HOLD
PUBLIC_ANSWER_DECISION_MAKER = HOLD
PUBLIC_ANSWER_$50K_DISPOSITION = HOLD
PUBLIC_ANSWER_WHITE_HOUSE_COMMUNICATIONS = HOLD
```

### T5 — FOIA / access layer

Multiple organizations sought the recording and related investigative records through FOIA. Litigation followed in D.D.C. and additional 2026 suits sought FBI/DOJ/DHS records. Public requester materials state that at least one FBI request was denied in full in January 2026.

```text
FOIA_REQUESTS = PROVEN
FOIA_LITIGATION = PROVEN
RECORDING_PUBLICLY_ACQUIRED_BY_THIS_REPLAY = FALSE
RECORDING_DELETED = NOT_INFERRED
```

## Byte-by-byte authority ladder

```text
REPORTED EVENT
→ FBI undercover operation
→ FBI/DOJ investigative file
→ W.D. Texas / Public Integrity participation reported
→ DOJ/FBI executive review
→ investigation closed
→ congressional oversight questions
→ FOIA requests
→ D.D.C. access litigation
→ later DOJ QFR responses
```

Each arrow requires its own receipt. No downstream official statement rewrites the earlier event; no earlier media report overrides a later official procedural disposition.

## Media-vs-public-record version table

| Version | What it can establish | What it cannot establish |
|---|---|---|
| Reuters/AP/WaPo/ABC Sept. 2025 | Multi-source reporting of operation, reported cash transfer, reported recording, reported contract discussion | Primary recording contents; complete investigative file; criminal liability |
| Patel/Blanche Sept. 2025 | DOJ/FBI acknowledge review and closure; state no credible criminal evidence | Whether cash changed hands; close memo; disposition of money; all investigative facts |
| White House/Homan 2025–2026 | Administration/subject position and denials | Independent factual adjudication |
| House/Senate oversight | Questions asked; documents demanded; oversight chronology | Truth of factual premise merely because a member states it |
| Blanche QFR July 2026 | Current public DOJ refusal/limits plus repeated closure rationale | Close date, decision-maker, White House communications, money disposition |
| FOIA litigation | Existence of live access dispute and requested record categories | Merits of underlying bribery allegation |

## Current evidence state

```text
INVESTIGATION_EXISTED                = PROVEN
INVESTIGATION_CLOSED                 = PROVEN
OFFICIAL_REASON                      = BOUND
REPORTED_$50K_TRANSFER               = BOUND_MULTI_SOURCE / HOLD_PRIMARY
REPORTED_AUDIO_VIDEO                 = BOUND_MULTI_SOURCE / HOLD_PRIMARY
QUID_PRO_QUO                         = HOLD
CRIMINAL_BRIBERY_FINDING             = REJECT
CLOSE_DATE_PUBLIC                    = HOLD
CLOSE_DECISION_MAKER_PUBLIC          = HOLD
$50K_DISPOSITION_PUBLIC              = HOLD
WHITE_HOUSE_COMMUNICATIONS_PUBLIC    = HOLD
PRIMARY_RECORDING_PUBLICLY_ACQUIRED  = FALSE
OVERALL                              = HOLD
```

## Restart rule

Media stories are immutable historical snapshots. The workflow is not.

Every run begins again from the source registry and asks:

1. Did an official source change?
2. Did a previously withheld primary byte become public?
3. Did Congress receive an answer?
4. Did a FOIA court order production or uphold withholding?
5. Did DOJ publish a close-out/declination record?
6. Did the reported money acquire a documented custody/disposition edge?
7. Did any later contract action create a source-bound execution edge?

A run that finds no new receipt emits `NO_MATERIAL_PUBLIC_DELTA`; it never converts silence into proof.

> **The media version stops at publication. The replay restarts at the receipts.**
