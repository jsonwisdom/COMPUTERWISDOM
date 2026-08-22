# Double Onion Alabama DARVO Policy Audit v0.1

**Operator:** `jaywisdom.base.eth`  
**Parent:** Alabama Live Constitution / Civil War Dualistic Onion draft PR #496  
**Classification:** `LEGAL_POLICY_RESEARCH_NOT_LEGAL_ADVICE`  
**Authority created:** `false`  
**DARVO finding created:** `false`

## Executive disposition

As of the 2026-08-18 audit, no Alabama statute, Alabama court rule, statewide K-12 administrative rule, or Alabama Judicial System policy expressly named `DARVO` was located in the official state sources searched.

That does **not** mean DARVO-like conduct is legally irrelevant. Alabama law regulates underlying conduct and burdens through custody statutes, domestic-violence presumptions, protection-from-abuse remedies, harassment law, judicial ethics, educator standards, and child-abuse reporting duties.

```text
NAMED_ALABAMA_DARVO_STATUTE = NOT_LOCATED
NAMED_ALABAMA_FAMILY_COURT_DARVO_POLICY = NOT_LOCATED
NAMED_ALABAMA_SCHOOL_DARVO_POLICY = NOT_LOCATED
DARVO = ANALYTIC_PATTERN_LABEL
DARVO != LEGAL_FINDING
NARCISSISTIC_LABEL != LEGAL_ELEMENT
```

## Double Onion

### Onion A — Event / Record

```text
EXACT EVENT
-> ACTOR
-> EXACT WORDS / ACTION
-> DATE + PLACE
-> SOURCE / TRANSCRIPT / FILING
-> DENIAL IF ANY
-> ATTACK IF ANY
-> ROLE REVERSAL IF ANY
-> BURDEN BEFORE / AFTER
-> CONSEQUENCE
-> RECEIPT
```

### Onion B — Law / Authority

```text
CASE / INSTITUTION TYPE
-> GOVERNING LAW / RULE
-> LEGAL STANDARD
-> BURDEN OF PROOF
-> PRESUMPTION IF ANY
-> REQUIRED FINDINGS
-> ORDER / DECISION
-> REVIEW STANDARD
-> APPEAL / COMPLAINT / REMEDY
-> RECEIPT
```

The onions cross only when the event receipt can be tied to an actual legal duty, burden, prohibition, or standard.

## Alabama family-court policy map

### Initial / joint custody

Ala. Code § 30-3-152 requires the court to consider joint custody in every case and permits custody based on the child's best interest. The statute expressly includes parental cooperation, encouragement of the child's relationship with the other parent, and any history or potential for child abuse, spouse abuse, or kidnapping among the factors.

Source: https://alison.legislature.state.al.us/code-of-alabama?section=30-3-152

```text
BEST_INTEREST = LEGAL_STANDARD_COMPONENT
DARVO = NOT_STATUTORY_LABEL
```

### Domestic or family violence

Ala. Code Article 6, §§ 30-3-130 through 30-3-136, governs custody and domestic/family abuse. Section 30-3-131 provides a rebuttable presumption against custody with a perpetrator once the court determines domestic or family violence occurred. Section 30-3-132 requires consideration of safety, well-being, and the history of violence.

Sources:
- https://alison.legislature.state.al.us/code-of-alabama?section=30-3-131
- https://alison.legislature.state.al.us/code-of-alabama?section=30-3-132

```text
ALLEGATION_OF_ABUSE != COURT_DETERMINATION_OF_ABUSE
COURT_DETERMINATION -> STATUTORY_PRESUMPTION_IF_SECTION_APPLIES
```

### Custody modification — McLendon correction

The controlling case is **Ex parte McLendon, 455 So. 2d 863 (Ala. 1984), Supreme Court of Alabama** — not `455 So.2d 863 (Ala. Civ. App. 1984)`.

McLendon is not the standard for every custody dispute. It is a modification/repose doctrine used in circumstances involving an existing custody disposition; Alabama appellate decisions distinguish situations in which the best-interest standard applies instead.

Source: https://law.justia.com/cases/alabama/supreme-court/1984/455-so-2d-863-1.html

```text
MCLENDON != UNIVERSAL_CUSTODY_STANDARD
WRONG_STANDARD_APPLIED = LEGAL_ERROR_CANDIDATE
DARVO_PATTERN != SUBSTITUTE_FOR_STANDARD-OF-REVIEW_ANALYSIS
```

### Relocation burden

Ala. Code § 30-3-169.4 expressly allocates and can shift the burden of proof in relocation proceedings. Unless the statutory domestic-violence/child-abuse condition applies, there is a rebuttable presumption that relocation is not in the child's best interest; the relocating party bears the initial burden, after which the burden shifts if met.

Source: https://alison.legislature.state.al.us/code-of-alabama?section=30-3-169.4

```text
STATUTORY_BURDEN_SHIFT != DARVO
UNAUTHORIZED_BURDEN_REVERSAL = AUDIT_CANDIDATE
```

### Protection from Abuse

Ala. Code §§ 30-5-6 and 30-5-7 provide hearings, temporary ex parte protection, and remedies including restraints against threats, harassment, stalking, abuse, and certain contact, with custody/visitation safety relief where applicable.

Sources:
- https://alison.legislature.state.al.us/code-of-alabama?section=30-5-6
- https://alison.legislature.state.al.us/code-of-alabama?section=30-5-7

## Appeal / post-judgment correction

The earlier formulation `file Rule 59(e) before the 42-day appeal window expires` is too loose.

Alabama Rule of Civil Procedure 59(e) requires a motion to alter, amend, or vacate to be filed **not later than 30 days after entry of judgment** in the ordinary circuit-court rule. Alabama Rule of Appellate Procedure 4 generally provides 42 days for civil appeals, but final juvenile-court orders are among the matters with a 14-day appeal period. A timely Rule 50/52/55/59 post-judgment motion suspends the appellate clock under Rule 4(a)(3).

Sources:
- https://judicial.alabama.gov/docs/library/rules/cv59.pdf
- https://judicial.alabama.gov/docs/library/rules/ap4.pdf

```text
RULE_59E_DEADLINE != 42_DAYS
APPEAL_DEADLINE != ALWAYS_42_DAYS
LIVE_CASE_DEADLINE = VERIFY_CASE_TYPE + ORDER_DATE + APPLICABLE_RULE
```

## Judicial DARVO audit / JIC

Alabama judicial ethics require judges to avoid impropriety and perform duties impartially and diligently. The Judicial Inquiry Commission may investigate judicial misconduct, but it is **not an appellate court** and cannot reverse or modify a judicial decision. The JIC threshold to file charges is a majority finding that a reasonable basis exists; `clear and convincing evidence` is the burden for charges prosecuted before the Court of the Judiciary, not the threshold merely to submit a citizen complaint.

Sources:
- https://judicial.alabama.gov/library/RulesCanons
- https://judicial.alabama.gov/appellate/JIC

```text
LEGAL_ERROR -> APPELLATE_LANE
JUDICIAL_MISCONDUCT -> JIC_CANDIDATE_LANE
JIC != APPEAL
BAD_RULING_ALONE != ETHICS_VIOLATION_PROVEN
```

## Teachers / principals / parents

`Narcissistic teacher`, `narcissistic principal`, and `narcissistic parent` are not useful legal predicates without qualified clinical evidence and a reason diagnosis is legally relevant.

Audit observable conduct instead.

### Schools

Ala. Code § 16-28B-6 requires schools to develop and implement evidence-based practices aimed at an environment free of harassment, intimidation, violence, and threats of violence and to intervene when covered incidents occur.

Alabama Administrative Code Rule 290-4-3-.03 requires educators to support safe, positive learning climates, respectful communication, ethical practice, and reflection on bias. Rule 290-4-3-.04 requires school leaders to promote supportive environments, advocate for student welfare, and understand applicable laws, rights, policies, and regulations.

Sources:
- https://alison.legislature.state.al.us/code-of-alabama?section=16-28B-6
- https://admincode.legislature.state.al.us/administrative-code/290-4-3-.03
- https://admincode.legislature.state.al.us/administrative-code/290-4-3-.04

### Parents / adults generally

Where conduct crosses statutory elements, Alabama law may address domestic violence, protection orders, harassment, stalking, child abuse/neglect, interference with custody, or other specific conduct. The legal question is the elements and evidence — not whether an actor can be called a narcissist or said to have used DARVO.

## Event-level DARVO test

```text
D = exact denial + actor + proposition denied
A = exact attack + target + words/action
RVO = evidence that complainant/victim role was reversed into offender/problem role
BURDEN_SHIFT = burden before + burden after + governing legal allocation
CONTRARY_EVIDENCE = admitted / rejected / ignored / explained
DECISION = exact order / finding / action
REVIEW = appeal / administrative review / JIC / school grievance / other lawful path
```

Terminal rules:

```text
DENIAL_ONLY = HOLD
DENIAL_PLUS_ATTACK = HOLD_RVO_REQUIRED
D+A+RVO_WITH_RECEIPTS = DARVO_PATTERN_CANDIDATE
DARVO_PATTERN_CANDIDATE != LEGAL_ERROR
DARVO_PATTERN_CANDIDATE != MISCONDUCT_FINDING
LEGAL_ERROR_REQUIRES_GOVERNING_LAW_EDGE
SYSTEMIC_DARVO_REQUIRES_AGGREGATE_EVIDENCE
```

## Closing disposition

```text
ALABAMA_FAMILY_COURT_DARVO_POLICY = NOT_LOCATED
ALABAMA_DARVO_LEGISLATION = NOT_LOCATED
ALABAMA_EDUCATION_DARVO_POLICY = NOT_LOCATED
DARVO_ADJACENT_LEGAL_CONTROLS = PRESENT
EVENT_BY_EVENT_DOUBLE_ONION_AUDIT = OPEN
SYSTEMIC_DARVO_FINDING = HOLD_AGGREGATE_EVIDENCE_REQUIRED
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
DARVO_FINDING_CREATED = FALSE
```
