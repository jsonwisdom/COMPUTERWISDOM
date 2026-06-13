# IPE-RECEIPT-001 Artifact Validation Protocol

## Purpose

IPE-RECEIPT-001 is the first production receipt intended to validate the deployed IPE receipt schema against a real public document.

This document defines the artifact validation procedure required before minting the receipt.

## Target Artifact

**Document:** City of St. Cloud Home Rule Charter  
**Institution:** City of St. Cloud  
**Receipt ID:** IPE-RECEIPT-001  
**Layer:** Authority  
**Document class:** charter

## Core Rule

No receipt may be minted from a placeholder URL, metadata-only hash, guessed checksum, or unverifiable portal path.

The receipt requires a specific downloadable artifact and a SHA256 hash computed from the actual retrieved bytes.

## Required Values

Before `receipts/st-cloud/IPE-RECEIPT-001.json` can be created, the following values must be known:

```json
{
  "source_url": "canonical downloadable artifact URL",
  "sha256": "64-character SHA256 hash from downloaded bytes",
  "file_size_bytes": 0,
  "retrieval_timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## Local Generation Procedure

Run these commands in a trusted local environment:

```bash
curl -L -o st-cloud-home-rule-charter.pdf "URL_TO_CHARTER_PDF"
sha256sum st-cloud-home-rule-charter.pdf
wc -c st-cloud-home-rule-charter.pdf
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

## Receipt Mapping

Map the output into the hardened schema:

| Field | Source |
|---|---|
| `source_url` | Canonical URL used for retrieval |
| `hashes.sha256` | Output from `sha256sum` |
| `file_size_bytes` | Output from `wc -c` |
| `retrieval_timestamp` | UTC timestamp from `date -u` |
| `access_method` | `public_web` if retrieved from official public website |
| `document_class` | `charter` |
| `orphaned_claims` | `0` |

## First Claim Boundary

The first claim must remain narrow.

Allowed claim:

```text
This receipt identifies the Home Rule Charter as an authority-layer document for the City of St. Cloud.
```

Disallowed claim:

```text
This proves St. Cloud complies with its charter.
```

## Invariants

- No ghost hash.
- No fake receipt.
- No metadata-only checksum.
- No portal path as binary artifact.
- No unsupported claim.
- No merge until verify is green.

## Status

IPE-RECEIPT-001 remains blocked until the real artifact URL, binary SHA256, file size, and retrieval timestamp are available.
