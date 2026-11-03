# Gray Baby Series 004 - County Audit Layer - 30-Day Reverse Build v0.1

Status: `OPEN / DRAFT / UNMERGED`  
Series: `GRAY_BABY`  
Episode set: `004 / COUNTY_AUDIT_LAYER`  
Build mode: `REVERSE`  
Window: `30 DAYS`  
Authority created: `FALSE`  
Membrane intact: `TRUE`

## Purpose

Build the County Audit Layer backward from a parent-safe replay packet to the child's first observation. The architecture is designed in reverse, then learned and replayed forward.

```text
BUILD ORDER:   DAY 30 -> DAY 01
REPLAY ORDER:  DAY 01 -> DAY 30
```

No new doctrine is introduced. Series 004 inherits the Series 003 child loop exactly:

```text
LOOK -> GUESS -> SOURCE -> RECEIPT -> GAP -> HOLD -> REPLAY
```

Canonical boundaries remain:

```text
QUESTION != ACCUSATION
GAP != FRAUD
ANOMALY != MISCONDUCT
NUMBER_FOUND != MONEY_AUDITED
DPI != LOCAL_AUTHORIZATION
SOURCE_BOUND != TRAIL_CLOSED
UNKNOWN_HOLD = SUCCESSFUL_GAP_DETECTION
AUTHORITY_CREATED = FALSE
```

Mission `004-001 / WESTVIEW_HISTORY_LIVE` remains a separate applied example. This file adds thirty curriculum missions, `004-002` through `004-031`, without overwriting that example.

## Locked mission-card fields

Every day uses the Series 003 structure:

1. What did I actually see?
2. What am I guessing?
3. Who said it?
4. Where is the receipt?
5. TRUE / FALSE / HOLD
6. First Gap
7. Parent-Safe Replay
8. Takeaway

The cards below are intentionally short. A child may stop at `HOLD` on any day. Completion is not measured by reaching TRUE; finding the first unresolved edge is a successful result.

---

# Reverse Build - Day 30 down to Day 01

## Day 30 - Mission 004-031 - Parent-Safe County Replay Packet

**Mission:** Start with the finished packet we wish we could safely hand to another family.

- **LOOK:** A packet containing claims, sources, receipts, gaps, corrections, and unresolved edges.
- **GUESS:** A polished packet may look complete.
- **SOURCE:** Every conclusion must point backward to a replayable source chain.
- **RECEIPT:** Index of sources + gap ledger + correction log + audit boundary.
- **TRUE / FALSE / HOLD:** `HOLD` if any promoted claim cannot be replayed.
- **FIRST GAP:** First conclusion without a surviving receipt.
- **PARENT-SAFE REPLAY:** "Show me the trail behind this sentence."
- **TAKEAWAY:** `POLISHED != PROVEN`.

## Day 29 - Mission 004-030 - Share Gate

**Mission:** Decide whether the replay is ready to leave the family workspace.

- **LOOK:** Proposed public or community-safe summary.
- **GUESS:** Shareable may feel the same as verified.
- **SOURCE:** The replay packet, not reactions or reposts.
- **RECEIPT:** Privacy check + source check + parent/human review.
- **TRUE / FALSE / HOLD:** `HOLD` when permission, context, or sourcing is unclear.
- **FIRST GAP:** First item that cannot safely travel with its context.
- **PARENT-SAFE REPLAY:** "Can another family see both what we know and what we do not know?"
- **TAKEAWAY:** `SHARING != VERIFICATION`.

## Day 28 - Mission 004-029 - Receipt Index

**Mission:** Make every promoted statement point to a receipt.

- **LOOK:** Claims beside source references.
- **GUESS:** A long source list may look sufficient.
- **SOURCE:** Original records where available; clearly labeled secondary sources otherwise.
- **RECEIPT:** Claim-to-source index.
- **TRUE / FALSE / HOLD:** `HOLD` for orphan claims.
- **FIRST GAP:** First claim with no source pointer.
- **PARENT-SAFE REPLAY:** "Which receipt belongs to this sentence?"
- **TAKEAWAY:** `SOURCE_LIST != CLAIM_BINDING`.

## Day 27 - Mission 004-028 - Correction Log

**Mission:** Preserve what changed instead of silently rewriting history.

- **LOOK:** Old state, new state, reason, date, source.
- **GUESS:** The newest answer may erase how we got there.
- **SOURCE:** Prior receipt + stronger correcting evidence.
- **RECEIPT:** Append-only correction entry.
- **TRUE / FALSE / HOLD:** `HOLD` if the reason for the change is missing.
- **FIRST GAP:** First changed conclusion without a documented delta.
- **PARENT-SAFE REPLAY:** "What did we believe before, and what new evidence changed it?"
- **TAKEAWAY:** `CORRECTION = PROGRESS`.

## Day 26 - Mission 004-027 - Gap + Anomaly Ledger

**Mission:** Separate missing evidence from surprising evidence.

- **LOOK:** Open gaps and observed anomalies.
- **GUESS:** A strange thing may feel suspicious.
- **SOURCE:** The record that shows the absence, conflict, or unusual difference.
- **RECEIPT:** Separate `GAP` and `ANOMALY` entries.
- **TRUE / FALSE / HOLD:** `HOLD` before assigning motive or misconduct.
- **FIRST GAP:** First unresolved dependency.
- **PARENT-SAFE REPLAY:** "What is missing, and what is merely unusual?"
- **TAKEAWAY:** `ANOMALY != MISCONDUCT`.

## Day 25 - Mission 004-026 - Finding Boundary

**Mission:** Write exactly what the evidence supports - and no more.

- **LOOK:** Draft finding and its evidence chain.
- **GUESS:** Strong wording may sound more useful.
- **SOURCE:** Receipts already replayed.
- **RECEIPT:** Supported claim + explicit non-claims.
- **TRUE / FALSE / HOLD:** `HOLD` if wording exceeds evidence.
- **FIRST GAP:** First unsupported word or implication.
- **PARENT-SAFE REPLAY:** "What can we say? What can we not say yet?"
- **TAKEAWAY:** `EVIDENCE_BOUND_LANGUAGE = SAFER_LANGUAGE`.

## Day 24 - Mission 004-025 - Audit Reconciliation

**Mission:** Ask whether the audited record reconciles the money trail being studied.

- **LOOK:** Audit report, financial statements, notes, and relevant fund information.
- **GUESS:** Having an audit PDF may feel like every transaction was checked.
- **SOURCE:** Independent audit report and audited statements.
- **RECEIPT:** Relevant page/note tied to the specific question.
- **TRUE / FALSE / HOLD:** `HOLD` if the audit does not answer the specific trail.
- **FIRST GAP:** First money edge not reconciled by the audited record.
- **PARENT-SAFE REPLAY:** "What exactly did the audit tell us about this dollar trail?"
- **TAKEAWAY:** `AUDIT_PRESENT != EVERY_TRANSACTION_PROVEN`.

## Day 23 - Mission 004-024 - Independent Audit Identity

**Mission:** Verify what document is actually an independent audit.

- **LOOK:** Auditor name, reporting period, opinion section, statements, notes.
- **GUESS:** Any finance PDF may look like an audit.
- **SOURCE:** The audit document itself and issuing entity surface.
- **RECEIPT:** Document identity + period + auditor.
- **TRUE / FALSE / HOLD:** `HOLD` if document type is unclear.
- **FIRST GAP:** Missing auditor/report-period identity.
- **PARENT-SAFE REPLAY:** "How do we know this is the audit and not just a budget report?"
- **TAKEAWAY:** `FINANCIAL_DOCUMENT != INDEPENDENT_AUDIT`.

## Day 22 - Mission 004-023 - Fund Accounting

**Mission:** Place the number in the correct fund or accounting category.

- **LOOK:** Fund name, account class, beginning balance, revenue, expenditure, ending balance when available.
- **GUESS:** All school dollars may seem interchangeable.
- **SOURCE:** Budget, ledger summary, audited statements, or official fund schedule.
- **RECEIPT:** Number + fund + period + unit.
- **TRUE / FALSE / HOLD:** `HOLD` when the fund is unknown.
- **FIRST GAP:** First number without fund/kind.
- **PARENT-SAFE REPLAY:** "Which bucket does this money belong to?"
- **TAKEAWAY:** `SAME_DOLLARS != SAME_FUND`.

## Day 21 - Mission 004-022 - Expenditure Evidence

**Mission:** Distinguish money authorized from money actually spent.

- **LOOK:** Expenditure record, payment register, audited expense line, or equivalent public record.
- **GUESS:** A levy or budget number may feel like proof of spending.
- **SOURCE:** Actual expenditure surface.
- **RECEIPT:** Amount + date/period + payee/category when public + source.
- **TRUE / FALSE / HOLD:** `HOLD` without expenditure evidence.
- **FIRST GAP:** Authorization-to-spending edge.
- **PARENT-SAFE REPLAY:** "We know they planned or raised it. Do we know what was spent?"
- **TAKEAWAY:** `AUTHORIZED != SPENT`.

## Day 20 - Mission 004-021 - Payment / Invoice Edge

**Mission:** Follow one permitted sample from obligation to payment when a public record exists.

- **LOOK:** Invoice, payment register, voucher, check register, or equivalent.
- **GUESS:** A contract amount may equal final payment.
- **SOURCE:** Public payment record.
- **RECEIPT:** Contract/obligation reference -> payment evidence.
- **TRUE / FALSE / HOLD:** `HOLD` when payment evidence is unavailable or exempt.
- **FIRST GAP:** Obligation-to-payment edge.
- **PARENT-SAFE REPLAY:** "What public record shows the money actually moved?"
- **TAKEAWAY:** `CONTRACT_AMOUNT != FINAL_PAYMENT`.

## Day 19 - Mission 004-020 - Contract / Purchase Edge

**Mission:** Find the public authorization that creates an obligation to buy or build.

- **LOOK:** Contract, bid award, purchase order, board approval, or procurement record.
- **GUESS:** Project announcement may look like a contract.
- **SOURCE:** Official procurement/board record.
- **RECEIPT:** Vendor/project + authorized amount/terms + approval source.
- **TRUE / FALSE / HOLD:** `HOLD` if the obligation record is absent.
- **FIRST GAP:** Approval-to-contract edge.
- **PARENT-SAFE REPLAY:** "Where did the district actually agree to buy or build this?"
- **TAKEAWAY:** `PROJECT_ANNOUNCEMENT != CONTRACT`.

## Day 18 - Mission 004-019 - Budget-to-Actual

**Mission:** Compare the plan with what later happened.

- **LOOK:** Adopted budget and actual results for the same fund/year.
- **GUESS:** Matching labels may hide different periods or units.
- **SOURCE:** Official budget + official/audited actuals.
- **RECEIPT:** Apples-to-apples comparison with year, fund, unit, and source.
- **TRUE / FALSE / HOLD:** `HOLD` if dimensions do not match.
- **FIRST GAP:** First incompatible comparison field.
- **PARENT-SAFE REPLAY:** "Are these really the same kind of number?"
- **TAKEAWAY:** `COMPARISON_REQUIRES_COMPATIBLE_DIMENSIONS`.

## Day 17 - Mission 004-018 - Certification Artifact

**Mission:** Find the record that certifies the levy or other required number.

- **LOOK:** Certification form, official submission, signed record, or equivalent public artifact.
- **GUESS:** A meeting agenda may prove certification occurred.
- **SOURCE:** Certification artifact or direct official record of certification.
- **RECEIPT:** Certified number + date + authority/source.
- **TRUE / FALSE / HOLD:** `HOLD` if certification is only proposed or indirectly reported.
- **FIRST GAP:** Vote-to-certification edge.
- **PARENT-SAFE REPLAY:** "Where is the record that says the number was officially certified?"
- **TAKEAWAY:** `VOTE != CERTIFICATION_ARTIFACT`.

## Day 16 - Mission 004-017 - Recorded Vote

**Mission:** Verify the action taken, not merely the item discussed.

- **LOOK:** Minutes or official action record with motion/result.
- **GUESS:** Presence on an agenda may feel like approval.
- **SOURCE:** Direct minutes/action record.
- **RECEIPT:** Motion + result + date + body.
- **TRUE / FALSE / HOLD:** `HOLD` if the result is not directly captured.
- **FIRST GAP:** Agenda-to-action edge.
- **PARENT-SAFE REPLAY:** "Did they talk about it, or did they vote on it?"
- **TAKEAWAY:** `AGENDA_ITEM != RECORDED_VOTE`.

## Day 15 - Mission 004-016 - Motion Identity

**Mission:** Identify exactly what was moved or approved.

- **LOOK:** Motion text or action summary.
- **GUESS:** Similar numbers may refer to different actions.
- **SOURCE:** Minutes/action record.
- **RECEIPT:** Motion language bound to the relevant number/item.
- **TRUE / FALSE / HOLD:** `HOLD` if action text is ambiguous.
- **FIRST GAP:** Number-to-action wording edge.
- **PARENT-SAFE REPLAY:** "What exactly did the motion say?"
- **TAKEAWAY:** `NUMBER_MATCH != ACTION_MATCH`.

## Day 14 - Mission 004-015 - Minutes Identity

**Mission:** Verify the minutes belong to the correct meeting.

- **LOOK:** Date, meeting type, body, title, approval status if stated.
- **GUESS:** A search result snippet may feel like the minutes.
- **SOURCE:** Direct official minutes endpoint/document.
- **RECEIPT:** Meeting identity + direct text/page.
- **TRUE / FALSE / HOLD:** `HOLD` when only a shell, index, or snippet is available.
- **FIRST GAP:** Endpoint-to-substantive-minutes edge.
- **PARENT-SAFE REPLAY:** "Can we read the actual minutes, not just the link?"
- **TAKEAWAY:** `MINUTES_ENDPOINT != MINUTES_BODY`.

## Day 13 - Mission 004-014 - Agenda / Resolution

**Mission:** Bind the proposed number to the meeting where action was scheduled.

- **LOOK:** Official agenda, resolution, or meeting packet.
- **GUESS:** A proposed item may feel final.
- **SOURCE:** Official local meeting surface.
- **RECEIPT:** Item/resolution + number + date + body.
- **TRUE / FALSE / HOLD:** `HOLD` for final-action claims.
- **FIRST GAP:** Proposal-to-action edge.
- **PARENT-SAFE REPLAY:** "This tells us what they planned to consider. What happened next?"
- **TAKEAWAY:** `PROPOSED != APPROVED`.

## Day 12 - Mission 004-013 - Levy Component

**Mission:** Separate operations, debt service, community service, and total where applicable.

- **LOOK:** Levy breakout.
- **GUESS:** Total levy may look like one undifferentiated number.
- **SOURCE:** Official local agenda/certification and state anchor when available.
- **RECEIPT:** Component + type + total reconciliation.
- **TRUE / FALSE / HOLD:** `HOLD` when component meaning is unclear.
- **FIRST GAP:** Number-to-type edge.
- **PARENT-SAFE REPLAY:** "What kind of levy dollar is this?"
- **TAKEAWAY:** `TOTAL != COMPONENT`.

## Day 11 - Mission 004-012 - Budget / Fund Type

**Mission:** Classify the number before comparing it.

- **LOOK:** Budget, levy, revenue, expenditure, debt, balance, rate, or other label.
- **GUESS:** Two dollar amounts may look comparable because both use `$`.
- **SOURCE:** Document label and surrounding table/text.
- **RECEIPT:** Number type + fund/kind.
- **TRUE / FALSE / HOLD:** `HOLD` until classification is stable.
- **FIRST GAP:** Missing type/fund.
- **PARENT-SAFE REPLAY:** "What kind of number is it before we compare it?"
- **TAKEAWAY:** `DOLLAR_SIGN != SAME_MEANING`.

## Day 10 - Mission 004-011 - Owner / Year / Unit

**Mission:** Bind every number to who, when, and what unit.

- **LOOK:** District/entity, fiscal year, dollars/rate/count/percent.
- **GUESS:** A familiar district name may be assumed from context.
- **SOURCE:** Header, table label, metadata, or official page context.
- **RECEIPT:** `OWNER + YEAR + UNIT`.
- **TRUE / FALSE / HOLD:** `HOLD` if any dimension is unknown.
- **FIRST GAP:** First missing dimension.
- **PARENT-SAFE REPLAY:** "Whose number is it, from what year, and measured how?"
- **TAKEAWAY:** `NUMBER_WITHOUT_DIMENSIONS = AMBIGUOUS`.

## Day 09 - Mission 004-010 - State Anchor vs Local Authority

**Mission:** Use statewide data as an anchor without turning it into local authorization.

- **LOOK:** DPI or other state-reported figure beside local records.
- **GUESS:** State publication may feel like proof of the local vote.
- **SOURCE:** State dataset + local authorization surfaces separately.
- **RECEIPT:** Independent anchor clearly labeled as such.
- **TRUE / FALSE / HOLD:** `HOLD` for local-action claims until local evidence is found.
- **FIRST GAP:** State-anchor-to-local-authority edge.
- **PARENT-SAFE REPLAY:** "The state reports the number. Where did the local body authorize it?"
- **TAKEAWAY:** `DPI != LOCAL_AUTHORIZATION`.

## Day 08 - Mission 004-009 - Source Origin

**Mission:** Determine where the document actually came from.

- **LOOK:** Domain, publisher, organization, document path, and context.
- **GUESS:** A copied PDF or screenshot may look official.
- **SOURCE:** Publisher's own surface when available.
- **RECEIPT:** Original URL/path or preserved source reference.
- **TRUE / FALSE / HOLD:** `HOLD` if origin is unknown.
- **FIRST GAP:** Copy-to-original edge.
- **PARENT-SAFE REPLAY:** "Can we find where this originally lived?"
- **TAKEAWAY:** `COPY != ORIGINAL_SOURCE`.

## Day 07 - Mission 004-008 - Version / Date

**Mission:** Confirm that the record belongs to the time being studied.

- **LOOK:** Publication date, meeting date, fiscal year, revision/version.
- **GUESS:** A current webpage may contain an older file or vice versa.
- **SOURCE:** Document metadata and visible date fields.
- **RECEIPT:** Date/version binding.
- **TRUE / FALSE / HOLD:** `HOLD` if timing is uncertain.
- **FIRST GAP:** Source-to-time edge.
- **PARENT-SAFE REPLAY:** "Is this the right record for the right year?"
- **TAKEAWAY:** `CURRENT_PAGE != CURRENT_RECORD`.

## Day 06 - Mission 004-007 - Institution / Jurisdiction Identity

**Mission:** Verify what organization the record belongs to and what role it has.

- **LOOK:** District, school, municipality, county, state agency, auditor, vendor, or other entity.
- **GUESS:** Geographic overlap may feel like shared authority.
- **SOURCE:** Official organizational identity and record context.
- **RECEIPT:** Entity + role + boundary.
- **TRUE / FALSE / HOLD:** `HOLD` if jurisdiction is being inferred.
- **FIRST GAP:** Place-to-authority edge.
- **PARENT-SAFE REPLAY:** "Who is this organization, and what can it actually decide?"
- **TAKEAWAY:** `GEOGRAPHY != JURISDICTION`.

## Day 05 - Mission 004-006 - First Gap

**Mission:** Name the first thing that must be known before the claim can move forward.

- **LOOK:** The replay chain up to the first missing edge.
- **GUESS:** We may want to jump ahead to the most dramatic missing record.
- **SOURCE:** Everything already established before the break.
- **RECEIPT:** `PUBLIC_TRAIL_GAP = FIRST_UNRESOLVED_POSITION`.
- **TRUE / FALSE / HOLD:** `HOLD`.
- **FIRST GAP:** The first unresolved dependency - no skipping.
- **PARENT-SAFE REPLAY:** "Where exactly did our trail stop?"
- **TAKEAWAY:** `FIRST_GAP > BIGGEST_GUESS`.

## Day 04 - Mission 004-005 - TRUE / FALSE / HOLD

**Mission:** Classify the current state without forcing an answer.

- **LOOK:** Evidence collected so far.
- **GUESS:** A question may feel like it requires TRUE or FALSE immediately.
- **SOURCE:** Current receipts only.
- **RECEIPT:** State classification with reason.
- **TRUE / FALSE / HOLD:** `TRUE`, `FALSE`, or `HOLD`; `HOLD` is valid.
- **FIRST GAP:** Evidence needed to leave HOLD.
- **PARENT-SAFE REPLAY:** "What would we need to know before changing HOLD?"
- **TAKEAWAY:** `UNKNOWN != FAILURE`.

## Day 03 - Mission 004-004 - Where Is the Receipt?

**Mission:** Ask what evidence could let another person check the claim.

- **LOOK:** The claim and candidate sources.
- **GUESS:** A confident explanation may feel like a receipt.
- **SOURCE:** The person/page making the claim is not automatically the supporting evidence.
- **RECEIPT:** A replayable record, measurement, calculation, or direct observation.
- **TRUE / FALSE / HOLD:** `HOLD` if no receipt exists yet.
- **FIRST GAP:** Claim-to-evidence edge.
- **PARENT-SAFE REPLAY:** "What could we show another person so they can check too?"
- **TAKEAWAY:** `EXPLANATION != RECEIPT`.

## Day 02 - Mission 004-003 - Who Said It?

**Mission:** Identify the source of the claim without deciding whether it is right.

- **LOOK:** Speaker, poster, website, document, image, meeting, or dataset.
- **GUESS:** A trusted or official-looking source may feel automatically correct.
- **SOURCE:** Name the source exactly.
- **RECEIPT:** Source identity only - not yet proof of the claim.
- **TRUE / FALSE / HOLD:** `HOLD` while evidence is still being tested.
- **FIRST GAP:** Source-to-support edge.
- **PARENT-SAFE REPLAY:** "Who told us this, and what did they use to know?"
- **TAKEAWAY:** `SOURCE_IDENTITY != CLAIM_PROOF`.

## Day 01 - Mission 004-002 - Look Before Story

**Mission:** Begin with the smallest observation a child can safely make.

- **LOOK:** "What did I actually see, hear, read, count, or measure?"
- **GUESS:** Keep every added meaning in a separate sentence.
- **SOURCE:** The direct observation itself.
- **RECEIPT:** A note, photo where appropriate, copied public text, measurement, or other safe observation record.
- **TRUE / FALSE / HOLD:** `HOLD` for everything beyond the observation.
- **FIRST GAP:** First place the story adds something not directly observed.
- **PARENT-SAFE REPLAY:** "Tell me what you saw before we decide what it means."
- **TAKEAWAY:** `OBSERVATION_FIRST`.

---

# Forward Learning Replay

Although the architecture was built backward, the child learns it forward:

```text
DAY 01  LOOK
  -> DAY 02 SOURCE IDENTITY
  -> DAY 03 RECEIPT
  -> DAY 04 TRUE / FALSE / HOLD
  -> DAY 05 FIRST GAP
  -> DAY 06-13 CONTEXT + NUMBER + LOCAL SOURCE
  -> DAY 14-17 MEETING ACTION + CERTIFICATION
  -> DAY 18-24 BUDGET -> CONTRACT -> SPENDING -> AUDIT
  -> DAY 25-28 FINDING + GAPS + CORRECTIONS + RECEIPTS
  -> DAY 29 SHARE GATE
  -> DAY 30 PARENT-SAFE REPLAY PACKET
```

## Kid / family protection

- Any child may be the asker, measurer, reader, mapper, recorder, or replay leader.
- No private student records are required.
- No student profiling is required.
- No public posting is required.
- A parent or guardian may stop the replay at any point.
- `HOLD` remains a respectful pause, not a punishment or failure state.

## Series 004 completion rule

Thirty days does not mean thirty forced conclusions.

```text
DAY_COMPLETED = QUESTION_REPLAYED_TO_FIRST_GAP
DAY_COMPLETED != CLAIM_PROVEN
```

A day is successful when the child can distinguish observation, guess, source, receipt, and first unresolved edge.

## Current state

```text
SERIES_004 = OPEN
REVERSE_BUILD_30_DAY = BUILT
MISSIONS_ADDED = 004-002..004-031
MISSION_004-001 = PRESERVED_SEPARATELY
BUILD_ORDER = 30_TO_01
LEARNING_REPLAY = 01_TO_30
NO_NEW_DOCTRINE = TRUE
NO_INTENSITY_INCREASE = TRUE
PARENT_SAFE = TRUE
PUBLIC_SAFE_FRAME = TRUE
WATCH_MODE = OFF
FUTURE_POLLING = OFF
AUDIT_LIVE_COMPATIBLE = TRUE
FREEZE_DECLARED = FALSE
AUTHORITY_CREATED = FALSE
```
