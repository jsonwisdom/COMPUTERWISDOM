# Leaf 005 — Manual Evidence Instructions

State: PENDING_REAL_EVIDENCE  
Target Artifact: City of Saint Cloud public meeting agenda PDF  
Authority: false  
Fraud status: UNKNOWN

Leaf 005 cannot auto-fetch the agenda due to site/security restrictions.
Jay must manually collect the evidence.

## 1. Manual Download Steps — iPhone Friendly

1. Open Safari on iPhone.
2. Navigate to the official agenda page using the real `source_url` once known.
3. Tap the agenda PDF link.
4. When the PDF opens, tap `Share`.
5. Tap `Save to Files`.
6. Choose `On My iPhone` or iCloud Drive.
7. Confirm the file is saved locally.
8. Record the file name exactly as saved.

## 2. Capture Required Evidence Fields

Jay must collect:

- `source_url` — exact URL where the PDF was downloaded
- `observed_at` — ISO8601 UTC timestamp when Jay downloaded it
- `sha256` — SHA-256 hash of the downloaded PDF
- `file_name` — local filename
- `byte_size` — file size in bytes, if available

No substitutions.  
No guesses.  
No invented values.

## 3. Hash Calculation Options

### Option A — iOS Shortcuts

1. Use or install an iOS Shortcut that computes SHA-256.
2. Run it on the saved PDF.
3. Copy the resulting 64-character hash.

### Option B — iCloud + Mac

1. Save the PDF to iCloud.
2. On a Mac, open Terminal.
3. Run:

```bash
shasum -a 256 <filename>.pdf
```

4. Copy the 64-character hex digest.

### Option C — Trusted Hashing App

- Use a reputable App Store hashing tool.
- Confirm it supports SHA-256.
- Run it on the saved PDF.
- Copy the exact output.

## 4. Receipt Fields Jay Must Fill

```json
{
  "authority": false,
  "fraud_status": "UNKNOWN",
  "source_url": "REPLACE_WITH_ACTUAL_URL",
  "observed_at": "REPLACE_WITH_ISO8601_UTC",
  "sha256": "REPLACE_WITH_SHA256_HEX",
  "file_name": "REPLACE_WITH_FILENAME",
  "byte_size": "REPLACE_WITH_INTEGER_OR_NULL"
}
```

No additional fields.  
No narrative.  
No inference.  
No fraud scoring.

## 5. JSON Template

File:

```text
public_agenda_receipt_001.json
```

Template:

```json
{
  "authority": false,
  "fraud_status": "UNKNOWN",
  "source_url": "REPLACE_WITH_ACTUAL_URL",
  "observed_at": "REPLACE_WITH_ISO8601_UTC",
  "sha256": "REPLACE_WITH_SHA256_HEX",
  "file_name": "REPLACE_WITH_FILENAME",
  "byte_size": 0
}
```

## Safety Rule

Do not invent URL.  
Do not invent hash.  
Do not invent timestamp.

If evidence is unavailable, status remains:

```text
PENDING_REAL_EVIDENCE
```

## Closing Rule

Leaf 005 becomes real only when Jay manually records real public evidence.

Authority remains false.
