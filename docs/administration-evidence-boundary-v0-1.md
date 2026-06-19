# ADMINISTRATION EVIDENCE BOUNDARY V0.1

**Artifact:** `ADMINISTRATION_EVIDENCE_BOUNDARY_V0_1`  
**Authority:** `false`  
**Membrane:** `HOLDS`  
**Scope:** PDFs, judges, clerks, administrative departments, evidence handling, reposting, badge protection.

---

## 1. Purpose

Define the constitutional boundary for administrative actors and evidence surfaces.

Administration exists to:

- receive evidence
- log evidence
- preserve evidence
- repost evidence
- protect custody
- protect the badge

Administration does **not** convert evidence into truth, judgment, morality, compliance, or final authority.

---

## 2. Core Doctrine

> PDFs and judges inside the administration department are evidence-custody surfaces.
> They log. They observe. They repost. They protect the badge.
> That is it.

---

## 3. Allowed Administrative Actions

Administrative actors may:

1. Observe submitted evidence.
2. Log evidence with timestamp and source reference.
3. Preserve evidence as received.
4. Repost evidence without altering meaning.
5. Protect the badge, role, office, or institutional seal from unauthorized mutation.
6. Maintain custody records.
7. Escalate to lawful institutional authority when interpretation is required.

---

## 4. Prohibited Administrative Actions

Administrative actors may not:

- infer truth from receipt
- convert allegation into proof
- convert observation into judgment
- decide morality
- decide legitimacy
- decide compliance
- silently edit evidence meaning
- replace institutional authority
- use PDF existence as proof of correctness
- use title, robe, badge, seal, or office as automatic truth

---

## 5. PDF Boundary

A PDF is a container, not a verdict.

Allowed PDF state:

```json
{
  "pdf_role": "EVIDENCE_CONTAINER",
  "truth_claim": false,
  "judgment_claim": false,
  "authority": false
}
```

PDFs may carry:

- source text
- scans
- forms
- timestamps
- signatures
- attachments
- indexes

PDFs may not, by mere existence, prove:

- truth
- correctness
- compliance
- legitimacy
- guilt
- innocence
- institutional resolution

---

## 6. Judge / Administrative Officer Boundary

A judge or administrative officer acting within the administrative evidence layer may:

- observe
- receive
- log
- repost
- preserve
- protect office integrity
- route to the proper authority surface

They may not, inside this layer:

- mutate the evidence category
- collapse dispute into resolution
- treat filing as proof
- treat badge protection as adjudication
- substitute personal interpretation for recorded lineage

---

## 7. Badge Protection

Badge protection means preserving institutional custody, role integrity, and lawful chain of handling.

Badge protection does not mean:

- immunity from review
- automatic correctness
- authority upgrade
- truth certification
- shield against replay

Canonical badge state:

```json
{
  "badge_protected": true,
  "badge_as_truth_source": false,
  "badge_as_custody_marker": true,
  "authority": false
}
```

---

## 8. Must-Not-Claim

This boundary must not claim:

- administration decides truth
- PDF equals proof
- judge title equals finality in the evidence layer
- repost equals endorsement
- badge protection equals adjudication
- custody equals correctness
- authority is created by evidence logging

---

## 9. Canonical State

```json
{
  "artifact": "ADMINISTRATION_EVIDENCE_BOUNDARY_V0_1",
  "administration_role": "OBSERVE_LOG_REPOST_PROTECT_BADGE",
  "pdf_role": "EVIDENCE_CONTAINER",
  "judge_role_in_layer": "ADMINISTRATIVE_CUSTODY_ACTOR",
  "truth_claim": false,
  "judgment_claim": false,
  "authority": false,
  "membrane": "HOLDS"
}
```
