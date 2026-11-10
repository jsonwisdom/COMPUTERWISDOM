# BLACKBARPRESS — Evidence Trail From Hell
## CI-FIRST / Wolfram evidence-graph proof, v1 (2026-11-10)

**Status: FORMAL MODEL PASS · CASE-SPECIFIC CLAIMS UNKNOWN**

This file is a reproducible logical test of how an evidence graph should treat *missing, affirmative, and contradictory* source links. It **does not** demonstrate that any real individual used an aircraft, paid a particular amount, obtained an unauthorized bed, carried cash, committed a crime, or was involved in a private relationship.

### Reproduction

Run [the Wolfram Language source](../proofs/blackbarpress_evidence_graph_v1.wl) in a Wolfram kernel:

```wolfram
Get["proofs/blackbarpress_evidence_graph_v1.wl"]
```

On 2026-11-10, the Wolfram Language evaluator returned:

```text
combinations: 27
completeTriplePassIffAllPass: True
contradictedTripleFailIffSomeFail: True
unresolvedTripleUnknownIffMissingAndNotContradicted: True
independentModelProven: True
specificCabinNotInferredFromModel: True
unrelatedMissingCabinDoesNotErasePaymentPath: True
flightNotEvidenceOfPassengerIdentity: True
graphIsAcyclic: True
hasCandidatePathTailToPayment: True
allChecksPass: True
```

**Scope:** all 3^3 possible 3-input verdict combinations, plus six structural/sample checks = nine named checks. The receipt values in the Wolfram file are **synthetic demonstration data**, not independently examined source documents. The tests prove the stated aggregation properties of this *defined model*; they do not certify accuracy of any entered verdict.

### Logical contract

For a **conjunctive claim** that requires all stated evidence predicates:

- **PASS** iff every mandatory predicate is independently established.
- **FAIL** iff evidence contradicts at least one required predicate.
- **UNKNOWN** otherwise (including missing or insufficient evidence).

These are scoped verdicts about **defined propositions**, not labels for people, credibility scores, or allegations of guilt. A missing edge changes a dependent claim to UNKNOWN; unrelated claims retain their own verdicts. Contrary evidence can defeat a conjunctive claim, but it must be tied to that specific proposition. No negative inference from the absence of a public record.

### Evidence graph (candidate join architecture; not real associations)

```text
Tail → Serial → Model
              ↘ SpecificCabin [needs aircraft-specific layout/modification documentation]
Tail → Flight → TravelApproval → Payment → CourtExhibit → Evidence
```

Graph reachability shows that a *candidate pathway* exists in the abstract schema, **not** that a record supplies each link, or that an observed journey justifies an inference about passengers, bedrooms, spending or misconduct.

Required separation:
1. FAA registration/model is not verified aircraft-specific bedroom configuration.
2. Movement data is not a passenger manifest or proof of who traveled.
3. Government procurement authority is not automatically a proof of actual payment or personal use.
4. Court dockets are not guarantees that sealed exhibits are publicly available.
5. Court evidence and redactions are case-specific, and lawful privacy protections matter.

### Proposed receipt schema (not populated)

```json
{
  "claim_id": "UNASSIGNED",
  "proposition": "Clearly defined, falsifiable assertion",
  "source_url": null,
  "issuing_authority": null,
  "document_date": null,
  "retrieval_timestamp_utc": null,
  "raw_sha256": null,
  "record_locator": null,
  "predicate": null,
  "verdict": "UNKNOWN",
  "method": "source inspection and independent corroboration",
  "limitations": ["no underlying source document yet"]
}
```

The first production audit must preserve source bytes as legally permitted, calculate SHA-256 over those original bytes, separately hash normalized metadata, record capture time, issue an append-only correction record, and recompute claim statuses when new evidence arrives. GitHub commit provenance alone is **not** proof that an external source was accurate or unchanged before capture.

### CI-FIRST boundaries

- **PASS (model):** Wolfram evaluation of all nine checks.
- **UNKNOWN (deployment):** No automated GitHub CI job or independent reviewer confirmation from this document alone.
- **UNKNOWN (real-world cases):** No Minnesota currency-transport, tribal-leader, passenger, SDNY, Epstein, DOJ redaction-authority, or government/corporate-jet person-level records were supplied to this model.
- **No authority conferred:** This branch/PR does not authorize collection of private records, unsealing, wallet signing, payments, deployment, or publication of unsubstantiated allegations.

**Verification over narrative. Preserve records. Distinguish documentary proof from graph adjacency.**
