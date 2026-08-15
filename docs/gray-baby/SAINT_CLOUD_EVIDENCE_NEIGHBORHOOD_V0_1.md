# Saint Cloud Evidence Neighborhood v0.1

**Parent:** Minnesota Public Sandbox / BoxD Minnesota  
**Witness geometry:** Gray Baby / Saint Cloud / LeeAnn  
**Class:** contextual provenance map  
**Target evidence promotion:** none  
**Authority created:** false

This document records Saint Cloud-related evidence surfaces already present in JSONWisdom while preserving the LEAF_005 evidence gate unchanged.

The controlling distinction is:

```text
RELATED_EVIDENCE_EXISTS != TARGET_EVIDENCE_SATISFIED
```

## Current posture

```text
EVIDENCE_NEIGHBORHOOD = MAPPED
LEAF_005              = HOLD_FOR_REAL_EVIDENCE
EVIDENCE_GATE          = ARMED / IDLE
SOURCE_BINDING         = NONE
FACT_PROMOTION         = FALSE
AUTHORITY_CREATED      = FALSE
```

No contextual artifact described below is promoted into the missing LEAF_005 target source.

## 1. St. Cloud City Council replayability challenge

Repository surface:

```text
evidence/challenges/st-cloud-mn/2026-06-09-adid-2376-replayability-challenge.md
```

Recorded context:

```text
jurisdiction       = St. Cloud, Minnesota
record_type        = City Council Minutes
document_id        = 2376
meeting_date       = 2026-05-18
challenge_status   = EVIDENCE_PENDING
confirmed_defect   = FALSE
verdict             = NO_VERDICT
```

The artifact records this public-record pointer:

```text
https://ci.stcloud.mn.us/Archive.aspx?ADID=2376
```

Its byte-level replayability test is incomplete. It requires two independent captures from the same official URI with SHA-256 values and UTC timestamps.

```text
capture_a_sha256        = PENDING
capture_a_timestamp_utc = PENDING
capture_b_sha256        = PENDING
capture_b_timestamp_utc = PENDING
match                    = UNKNOWN
```

Classification:

```text
ADID_2376 = CANDIDATE_CONTEXT / PUBLIC_RECORD_POINTER
ADID_2376 != LEAF_005_TARGET_EVIDENCE
```

Reason: ADID 2376 concerns City Council Minutes dated 2026-05-18. LEAF_005 targets a different artifact: the 2026-06-02 public meeting agenda.

## 2. ISD 742 / St. Cloud Area Schools evidence constellation

JSONWisdom also contains a St. Cloud Area Schools / ISD 742 audit and replay constellation in `jsonwisdom/JOY`.

Relevant surfaces include:

```text
receipts/mn_audit/MN_DISTRICT_PACKET_ISD_742_V0_1.md
receipts/mn_audit/ISD_742_FULL_CHAIN_V0_1.md
receipts/mn_audit/ISD_742_RECEIPT_PACKET_V0_1.md
receipts/mn_audit/ISD_742_FEE_DISCLOSURE_PACKET_V0_1.md
receipts/mn_audit/school_meals/isd742/SHA256SUMS.txt
receipts/mn_audit/school_meals/isd742/MN_SCHOOL_MEALS_DISCOVERY_PACKET_V0_2_RECEIPT_ISD742.json
docs/replay/ISD742_MAILBOX_LOCAL_VERIFICATION_V0_1.json
```

The repository bundle has recorded SHA-256 values for its own request, receipt, replay-vector, and checksum artifacts. Those hashes establish repository-artifact integrity for the listed files; they do not establish truth of external-world claims or completion of external delivery.

The discovery receipt remains:

```text
state                 = PRESERVED_PRE_SEND
external_request_sent = FALSE
execution_state       = DELIVERY_INCOMPLETE
finding_posture       = NO_FINDINGS_ASSERTED
```

The mailbox verification object also remains pending for operator-local hashes and excerpts.

Classification:

```text
ISD_742_REPO_PACKET_INTEGRITY = HASHED
EXTERNAL_DELIVERY             = FALSE
EXTERNAL_FINDINGS             = NONE
ISD_742_CONTEXT               = CANDIDATE_PROVENANCE_CONTEXT
ISD_742_CONTEXT               != LEAF_005_TARGET_EVIDENCE
```

## 3. LEAF_005 target remains unsatisfied

Canonical work-item target:

```text
examples/work_items/wi-005-hash-agenda.json
```

Target:

```text
jurisdiction = City of Saint Cloud
record_type  = public_meeting_agenda
target_date  = 2026-06-02
artifact_type = PDF
```

Current required fields remain unbound:

```text
SOURCE_URL  = NOT_BOUND
SOURCE_BYTES = ABSENT
SHA256      = ABSENT
OBSERVED_AT = NOT_BOUND
FILE_NAME   = NOT_BOUND
BYTE_SIZE   = NOT_BOUND
```

Therefore:

```text
LEAF_005 = HOLD_FOR_REAL_EVIDENCE
```

No nearby Saint Cloud artifact, related meeting record, school-district packet, repository hash, or contextual pointer may satisfy this gate by substitution.

## 4. Witness-layer placement

The evidence neighborhood attaches to the witness geometry as context only:

```text
MINNESOTA PUBLIC SANDBOX
        ↓
BOXD MINNESOTA
        ↓
JAY'S MINNESOTA GAMBIT
        ↓
SAINT CLOUD
        ↓
FULL WITNESS TRIAD
  ├─ GRAY BABY   = gap observer
  ├─ SAINT CLOUD = local observation anchor
  └─ LEEANN      = witness / explanation / continuity
        ↓
CONTEXTUAL EVIDENCE NEIGHBORHOOD
  ├─ ADID 2376 minutes challenge
  └─ ISD 742 replay/audit packet constellation
        ↓
EVIDENCE GATE = ARMED / IDLE
        X
LEAF_005 TARGET SOURCE NOT YET PRESENT
```

The neighborhood may help a future reviewer discover provenance and related surfaces. It may not bind the LEAF_005 source node.

## 5. Promotion breaker

```text
IF candidate_context != exact_target_source:
    DO_NOT_PROMOTE
    PRESERVE_CONTEXT
    PRESERVE_GAP
    LEAF_005 = HOLD_FOR_REAL_EVIDENCE
```

The strongest invariant remains:

```text
MISSING EVIDENCE -> PRESERVE THE GAP
MISSING EVIDENCE -X-> INFER A SUBSTITUTE
```

## Closing state

```text
WITNESS_GEOMETRY          = CANONICAL
EVIDENCE_NEIGHBORHOOD     = MAPPED_AS_CONTEXT
TARGET_EVIDENCE           = ABSENT
LEAF_005                   = HOLD_FOR_REAL_EVIDENCE
EVIDENCE_GATE              = ARMED / IDLE
LEEANN_WITNESS_PATH        = DESIGN_ONLY
SOURCE_BINDING             = NONE
FACT_PROMOTION             = FALSE
CRAWLER                    = DISABLED
AUTHORITY_CREATED          = FALSE
```

The discovery changes what is known about the surrounding repository evidence surface. It does not change the LEAF_005 target gate.
