# APPLE_BLOSSOM_REVISION_TEXT_CANONICALIZATION_SPEC_V0_1

Status: DRAFT_UNSEALED  
Authority created: false  
No hashing ghosts: true

## Purpose

Define deterministic UTF-8 evidence bytes from retrieved Google Drive revision text without claiming identity with native Google Docs storage bytes or DOCX export bytes.

## Specification

```json
{
  "artifact_id": "APPLE_BLOSSOM_REVISION_TEXT_CANONICALIZATION_SPEC_V0_1",
  "artifact_type": "canonical_text_representation_spec",
  "purpose": "Define deterministic UTF-8 evidence bytes from retrieved Google Drive revision text without claiming identity with native Google Docs or DOCX bytes.",
  "input": {
    "source_type": "GOOGLE_DRIVE_REVISION_TEXT",
    "required_fields": [
      "file_id",
      "revision_id",
      "revision_modified_time",
      "retrieved_text"
    ],
    "raw_native_document_bytes_available": false
  },
  "transform": {
    "step_1_input": "retrieved_text exactly as returned by the revision-reading surface",
    "step_2_bom": "remove exactly one leading U+FEFF if present",
    "step_3_newlines": "normalize CRLF and lone CR to LF",
    "step_4_unicode": "NO_UNICODE_NORMALIZATION",
    "step_5_whitespace": "PRESERVE",
    "step_6_trailing_whitespace": "PRESERVE",
    "step_7_trailing_newline": "require exactly one LF",
    "step_8_encoding": "UTF-8 without BOM"
  },
  "forbidden_transforms": [
    "trim lines",
    "collapse whitespace",
    "sort lines",
    "normalize quotation marks",
    "Unicode NFC normalization",
    "Unicode NFD normalization",
    "HTML decoding beyond what the source reader already performed",
    "DOCX reconstruction",
    "semantic rewriting"
  ],
  "canonicalization_pseudocode": [
    "text = retrieved_text",
    "if text begins with U+FEFF: remove first U+FEFF",
    "text = text.replace(CRLF, LF)",
    "text = text.replace(CR, LF)",
    "remove all terminal LF characters",
    "text = text + LF",
    "canonical_bytes = UTF8(text)"
  ],
  "hashing": {
    "algorithm": "SHA-256",
    "rev2_hash_label": "REV2_CANONICAL_TEXT_SHA256",
    "rev3_hash_label": "REV3_CANONICAL_TEXT_SHA256",
    "native_byte_hash_claim": false,
    "docx_byte_hash_claim": false
  },
  "required_properties": {
    "deterministic": true,
    "idempotent": true,
    "same_transform_all_revisions": true,
    "content_preserving_except_declared_normalizations": true
  },
  "fixtures_required": [
    "leading_BOM",
    "no_BOM",
    "LF",
    "CRLF",
    "lone_CR",
    "multiple_trailing_LF",
    "no_trailing_LF",
    "interior_blank_lines",
    "trailing_spaces",
    "non_ASCII_text",
    "combining_unicode_sequence",
    "curly_quotes",
    "empty_string"
  ],
  "invariants": {
    "CANONICAL_TEXT_BYTES_NOT_EQUAL_NATIVE_GOOGLE_DOC_BYTES": true,
    "CANONICAL_TEXT_BYTES_NOT_EQUAL_DOCX_EXPORT_BYTES": true,
    "CANONICALIZATION_DOES_NOT_ESTABLISH_SEMANTIC_EQUIVALENCE": true,
    "REV2_SEMANTICS_INFERRED": false,
    "NO_SILENT_REWRITE": true,
    "NO_HASHING_GHOSTS": true
  },
  "authority": false,
  "status": "DRAFT_UNSEALED"
}
```

## Core law

```text
C(C(x)) = C(x)

same retrieved text
→ same canonical bytes
→ same SHA-256
```

## Naming boundary

```text
REV2_CANONICAL_TEXT_SHA256
REV3_CANONICAL_TEXT_SHA256

!= native Google Doc hash
!= DOCX export hash
!= proof that Drive stored those exact bytes
```

## Gate

```text
TEXT_CANONICALIZATION_SPEC = DRAFTED
FIXTURES_EXECUTED = FALSE
IDEMPOTENCE_PROVEN = FALSE
REPRESENTATION_SELECTED = FALSE
HASHING_AUTHORIZED = FALSE
REV2_HASH_BOUND = FALSE
REV3_HASH_BOUND = FALSE
V2_SCHEMA_DRAFT = BLOCKED
NO_HASHING_GHOSTS = TRUE
AUTHORITY_CREATED = FALSE
```
