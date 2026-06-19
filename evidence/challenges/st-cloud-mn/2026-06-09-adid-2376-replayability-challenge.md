# Replayability Challenge: St. Cloud City Council Minutes ADID=2376

## Repository Status

`TEMPORARY_HOME_NOT_CANONICAL`

This file is stored in `jsonwisdom/COMPUTERWISDOM` only because no canonical `ClarityAct` or `MinutesHunter` repository was found in the connected GitHub installation at filing time.

This file does not create final authority. It preserves an audit trail until a canonical repository exists.

## Status

`EVIDENCE_PENDING`

## Verdict

No verdict entered.

## Summary

This record documents a replayability challenge for the St. Cloud, Minnesota City Council minutes artifact served through:

`https://ci.stcloud.mn.us/Archive.aspx?ADID=2376`

The challenge concerns whether the public record endpoint serves a byte-stable PDF artifact or a dynamically generated view/PDF whose bytes may mutate across requests.

At this stage, no finding of divergence has been made.

## Record

```json
{
  "project": "ClarityAct.MinutesHunter",
  "jurisdiction": "St. Cloud, Minnesota",
  "record_type": "City Council Minutes",
  "document_id": "2376",
  "public_record_uri": "https://ci.stcloud.mn.us/Archive.aspx?ADID=2376",
  "meeting_date": "2026-05-18",
  "challenge_status": "EVIDENCE_PENDING",
  "suspected_defect": "POSSIBLE_DYNAMIC_PDF_OR_VIEW_GENERATED_ARTIFACT",
  "confirmed_defect": false,
  "required_evidence": [
    "capture_a_sha256",
    "capture_a_timestamp_utc",
    "capture_b_sha256",
    "capture_b_timestamp_utc",
    "headers_if_available"
  ],
  "attestation_status": "STAGED_NOT_SIGNED",
  "authority": false
}
```

## Required Evidence Before Any Verdict

A divergence finding requires at least two independent byte captures from the same official URI.

Required comparison:

```json
{
  "same_uri": true,
  "capture_a_sha256": "PENDING",
  "capture_a_timestamp_utc": "PENDING",
  "capture_b_sha256": "PENDING",
  "capture_b_timestamp_utc": "PENDING",
  "match": null
}
```

## Constitutional Rule

Suspicion is not attestation.

No claim of `DIVERGED`, `FAILED`, or `NON_REPLAYABLE` may be entered until byte-level evidence proves mismatch across independent captures.

## Current Posture

```json
{
  "posture": "CHALLENGE_INITIATED",
  "evidence": "BYTE_CAPTURE_PAIR_REQUIRED",
  "classification": "EVIDENCE_PENDING",
  "verdict": "NO_VERDICT",
  "authority": false
}
```
