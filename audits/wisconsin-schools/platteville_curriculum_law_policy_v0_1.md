# Platteville Curriculum Audit v0.1 — Law vs Policy vs Practice

Status: REVIEW_OPEN  
Parent lane: Southwest Wisconsin School Budget BitBot v0.1 / CHAOS audit  
Authority created: false

## Core question

What is legally required, what does Platteville School District say it does, and what can be proven from the actual curriculum, assessment, staffing, access, and student-outcome records?

```text
LAW != POLICY
POLICY != PROCEDURE
PROCEDURE != PRACTICE
PRACTICE != OUTCOME
MISSION_STATEMENT != MEASUREMENT
COURSE_TITLE != CURRICULUM
RUBRIC_MISSING_FROM_PUBLIC_SEARCH != RUBRIC_DOES_NOT_EXIST
SEARCH_MISS != ABSENCE
```

## Legal floor

Federal Title IX, 20 U.S.C. § 1681, prohibits exclusion from, denial of benefits of, or discrimination under federally funded education programs on the basis of sex, subject to statutory exceptions.

Source: https://www.law.cornell.edu/uscode/text/20/1681

This legal floor does not by itself prove equal participation, equal opportunity, equal classroom treatment, equivalent assessment, or equivalent outcomes in a particular Platteville course.

## Platteville public policy/procedure surfaces observed

- District mission publicly states high levels of learning for all in a safe, inclusive learning community; every student, every day.
- District website links Essential Learning Outcomes.
- District student-services navigation links a Title IX surface.
- School board schedule identifies a Program Committee and a Community Outreach & Policy Committee.
- District publicly identifies a Director of Continuous Improvement.

These are policy/procedure surfaces. They are not automatic proof of classroom implementation.

## Current subject findings

### Mathematics

Public staff records identify multiple Platteville High School math teachers.

Current public search did not surface a publicly inspectable high-school mathematics grading rubric or assessment rubric.

```text
MATH_STAFF_PRESENT = TRUE
PUBLIC_MATH_RUBRIC_FOUND = FALSE_IN_CURRENT_SEARCH
RUBRIC_EXISTS = UNKNOWN
STATUS = HOLD
```

Questions:
- What are the Essential Learning Outcomes by high-school math course?
- What common assessments are used?
- Is there a scoring rubric?
- Is the rubric the same across sections/teachers?
- What evidence triggers reteaching or intervention?
- Can a student/parent inspect the rubric before assessment?

### Accounting / Business Education

Public staff records identify a current high-school Business Education teacher. A Platteville FBLA report identifies students competing in `Accounting I`, which is evidence that Accounting I exists as an educational/competitive subject surface.

```text
BUSINESS_EDUCATION_STAFF_PRESENT = TRUE
ACCOUNTING_I_REFERENCE_FOUND = TRUE
ACCOUNTING_CURRICULUM_PUBLICLY_REPLAYED = FALSE
ACCOUNTING_RUBRIC_PUBLICLY_REPLAYED = FALSE
STATUS = PARTIAL / HOLD
```

Questions:
- Is Accounting I a scheduled credit-bearing course, competition category, or both?
- What accounting standards/competencies are taught?
- Do students reconcile real or synthetic public financial statements?
- Are debits/credits, funds, liabilities, debt service, and public-sector accounting distinguished?
- What rubric determines mastery?

### Physics / Physical Science

Public staff records identify at least one Platteville High School science teacher, and the district publicly promotes STEM. Current public search did not surface a standalone high-school course titled `Physics` or a public high-school course catalog establishing whether Physics is offered.

```text
HS_SCIENCE_STAFF_PRESENT = TRUE
STEM_CLAIM_PRESENT = TRUE
STANDALONE_PHYSICS_COURSE_FOUND = FALSE_IN_CURRENT_SEARCH
PHYSICS_ABSENT = NOT_PROVEN
STATUS = HOLD
```

Questions:
- Is Physics offered in the current high-school master course list?
- If yes, is it offered every year or on rotation?
- If not, which physical-science course satisfies the district pathway?
- What laboratory/measurement requirements exist?
- What rubric measures experimental reasoning rather than answer recall?

## Girls / sex-equality audit

Do not infer exclusion from missing publicity, and do not infer inclusion from a nondiscrimination statement.

```text
TITLE_IX_LEGAL_FLOOR = PRESENT
DISTRICT_INCLUSIVE_POLICY_LANGUAGE = PRESENT
ACTUAL_EQUAL_ACCESS = UNKNOWN
ACTUAL_PARTICIPATION_BY_SEX = UNKNOWN
ACTUAL_COMPLETION_BY_SEX = UNKNOWN
ACTUAL_OUTCOMES_BY_SEX = UNKNOWN
GIRLS_EXCLUDED = NOT_PROVEN
GIRLS_SUBSTANTIVELY_INCLUDED = NOT_YET_PROVEN
STATUS = HOLD
```

Required evidence should focus on lawful, aggregate, privacy-safe records such as course availability, prerequisites, enrollment/participation rates where public, completion, advanced-course access, extracurricular pipelines, and published outcome data. Do not expose private student records.

## Platteville Procedure audit

The candidate procedure chain is:

```text
LAW / ADMIN CODE
→ BOARD POLICY
→ PROGRAM COMMITTEE / DISTRICT PROCEDURE
→ ESSENTIAL LEARNING OUTCOME
→ COURSE OFFERING
→ LESSON / LAB / ASSIGNMENT
→ ASSESSMENT
→ RUBRIC
→ STUDENT WORK / AGGREGATE OUTCOME
→ PLC REVIEW / RETEACH
→ BOARD / PUBLIC REPORTING
```

For each arrow, BitBot asks for the source; Gray Baby names the missing edge; Ziggy turns the question into a replayable student mission; Leah classifies law/policy/procedure/evidence; JOY tests whether the system is useful, fair, accessible, and human-safe.

## Role split

```text
BITBOT = exact source / byte / change / provenance verifier
ZIGGY  = kid-facing question, measurement, experiment, replay
LEAH   = classification: LAW | POLICY | PROCEDURE | PRACTICE | OUTCOME | HOLD
GRAY_BABY = gap watcher / contradiction card
JOY    = human inclusion, access, fairness, meaning, lived outcome
CRISSCROSS = compare forward story against reverse evidence path
```

## Promotion rule

```text
ANOMALY != FAILURE
GAP != VIOLATION
DISPARITY != DISCRIMINATION
POLICY != COMPLIANCE
COMPLIANCE != QUALITY
```

No allegation against a teacher, employee, district, student, or board member may be promoted without claim-specific evidence and human review.

AUTHORITY_CREATED = FALSE
