# IPE-RECEIPT-001 Production Receipt Checklist

## Status

Production receipt PRs must not merge until the canonical artifact is available and replay becomes determinate.

## Required Governance References

- Base branch: `master`
- Schema: `IPE-SCHEMA-002` / merge `87b0d16cde9ee961738957788914f64656eb872b`
- Protocol: `IPE-RECEIPT-001-PROTOCOL` / merge `37de92ebebc80ffb855e4de8d3dc20daeb6a98a2`
- Tracking issue: `#295`

## Artifact Requirements

- [ ] Canonical source URL or custody path is specific and reachable
- [ ] Artifact is not a portal landing page
- [ ] Artifact bytes were downloaded or otherwise placed in custody
- [ ] SHA256 was computed from actual bytes
- [ ] File size in bytes was recorded
- [ ] Retrieval timestamp was recorded in ISO-8601 UTC

## Receipt Requirements

- [ ] `receipt_id` is `IPE-RECEIPT-001`
- [ ] `document_class` is `charter`
- [ ] `access_method` uses an approved enum value
- [ ] `hashes.sha256` is a real 64-character SHA256 value
- [ ] `file_size_bytes` is greater than zero
- [ ] At least one fragment is cited
- [ ] Every claim maps to a fragment through `evidence_mapping`
- [ ] `orphaned_claims` is `0`
- [ ] `privacy_review.private_data_detected` is `false`, or redaction is documented

## Bounded Claim Requirement

Allowed first claim:

```text
This receipt identifies the Home Rule Charter as an authority-layer document for the City of St. Cloud.
```

Disallowed claims:

- This proves St. Cloud complies with its charter.
- This proves legal validity.
- This proves institutional behavior.
- This proves current public access compliance.

## Replay Requirements

- [ ] Source artifact is declared
- [ ] Transform policy is declared or marked byte-preserving
- [ ] Canonical bytes are established
- [ ] Digest recomputes
- [ ] Receipt validates against schema
- [ ] `verify` passes

## Rejection Conditions

Reject this PR if any of the following occur:

- missing source artifact
- stale or unreachable URL
- portal path without specific artifact
- placeholder hash
- zero or missing file size
- missing retrieval timestamp
- unsupported claim
- schema validation failure
- non-deterministic replay
- private or sensitive data issue

## Final Rule

No ghost hash. No fake receipt. No unsupported claim. No merge until `verify` is green.
