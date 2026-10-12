# RAW_CAPTURE_v0

**Status:** FROZEN  
**Version:** 0.1.0  
**Purpose:** Byte-preserving bridge between live retrieval/manual upload and Meridian normalization.

## Hard gate

```text
NO capture_id -> NO normalize
NO stored bytes -> NO capture_id
EMPTY body -> CAPTURE_FAILURE
HASH mismatch -> CAPTURE_FAILURE
```

## Success object

```yaml
raw_capture:
  schema_version: "0.1.0"
  kind: raw_capture
  id: "sha256:<hash-of-exact-bytes>"
  capture_method: http | manual_upload

  # Origin preservation
  url: null                  # requested/source URL; never replaced by redirect destination
  final_url: null            # terminal URL after redirects, if any
  redirects: []              # ordered [{status, location}]
  
  captured_at: "ISO8601"
  bytes_ref: "storage://..." # immutable/WORM byte object
  byte_length: 0
  content_hash: "sha256:..."

  response:
    http_status: null
    headers_ref: null

  manual_attestation:
    provided_by: null
    local_hash_before_upload: null
    attested_at: null
```

## Identity

For a successful capture:

```text
raw_capture.id = sha256(exact stored bytes)
raw_capture.content_hash = raw_capture.id
```

The same bytes MUST yield the same capture id regardless of capture method.

## HTTP WORM write

1. Accept the requested URL as supplied.
2. Fetch without normalizing, summarizing, or parsing content.
3. Record redirects separately and preserve the original requested URL in `raw_capture.url`.
4. Refuse an empty response body.
5. Compute SHA-256 over the exact response bytes.
6. Write exact bytes to immutable/WORM storage.
7. Re-read stored bytes and recompute SHA-256.
8. If pre-write and post-write hashes differ, emit `capture_failure(stage=integrity)`; emit no `raw_capture`.
9. If hashes match, set `id` and `content_hash` to that digest.
10. Only then may normalization receive the `capture_id`.

## Manual upload

Manual upload is a capture method, not a second evidentiary schema.

1. Operator supplies bytes.
2. Optional attestation records context only.
3. If supplied, `local_hash_before_upload` is compared with the hash recomputed from received bytes.
4. Bytes are written to WORM storage and re-read.
5. A mismatch at either comparison emits `capture_failure(stage=integrity)`.
6. Attestation never substitutes for bytes and never becomes the source.

## Event source rule

A later Meridian event copies its source URL from `raw_capture.url` (the requested/source URL), never from `final_url`. Redirects remain explicit capture metadata.

## Authority

`RAW_CAPTURE_v0` establishes byte identity and transport provenance only. It does not verify the truth, legality, meaning, authorship, or authority of the captured content.
