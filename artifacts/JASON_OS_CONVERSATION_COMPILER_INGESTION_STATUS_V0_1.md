# JASON_OS Conversation Compiler — Ingestion Status V0.1

STATUS: HOLD on full corpus ingestion  
AUTHORITY: false  
DATE: 2026-09-21

## Kernel

The Conversation Compiler kernel is frozen as four layers:

- CEO — observation contract
  - schema sha256: 9b43f71d7dd261cf3d7854f36e9c4a86896710d68576b787fc7a80a03746823c
- GRAPH — explicit relations
  - schema sha256: d05f637f92b04ae2c57cac5308bc9f55a5c4e8f1d80012e48930f1f2c6672e8c
- FOLD — ephemeral projection
  - schema sha256: 96db1f57b6413bc9fad4f3c20d46236d1cae0a4d868ee9e20c218cabed10ed6c
- QUERY — read-only interrogation
  - schema sha256: 093c5601d23805ab9e73e36d201c8181170aabb47f7919a730f9c3091419a0e4

Pipeline:

CHAT → CEO → GRAPH → FOLD → QUERY → HUMAN REVIEW → NEW CEO

## Import / Extractor Boundary

Import Manifest V0.1 binds source bytes only.

Extractor V0.1 emits candidate objects only.

Key invariants:

- EXPORT FILE ≠ CONVERSATION
- CONVERSATION ≠ CEO
- IMPORT SUCCESS ≠ EXTRACTION SUCCESS
- SOURCE SPAN HASH ≠ DECODED OBSERVATION HASH
- EXTRACTOR MUST NOT EMIT VALIDATED CEO OBJECTS
- AUTHORITY CREATED = false

## Live-format fixture

A single-thread export candidate was observed in the ChatGPT runtime:

- file: `chat-export-1787807893313.json`
- bytes: 606734
- sha256: `a0edfee447aa4ab074cbc06e46cf4cc7f5b9cb4e442cb5d6f4c8969241027563`
- conversations observed: 1
- title: `Boundary Compliance Receipt`
- message path: `[0].chat.messages[]`
- messages observed: 70

Disposition:

- LIVE_EXPORT_BYTES = PASS
- HASH_REPLAY = PASS
- JSON_PARSE = PASS
- REAL_FORMAT_DISCOVERY = PASS
- 100_CONVERSATION_CORPUS = HOLD

This file is a live-format fixture only. It is not the full ChatGPT data export.

## Connected-source search

### GitHub

Repository checked:

`jsonwisdom/COMPUTERWISDOM`

Observed:

- no `conversations.json`
- no existing `JASON_OS_CONVERSATION...` artifact found in indexed search before this receipt

Disposition:

`FULL_EXPORT_SOURCE = HOLD`

### Google Drive

Both connected Drive accounts were checked.

Observed:

- no `conversations.json`
- no `chat-export`
- no `application/zip` export candidate
- Docs/PDFs mentioning ChatGPT or JSONWisdom exist but are NOT SOURCE BYTES

Disposition:

`FULL_EXPORT_SOURCE = HOLD`

## Current gate

```text
LIVE_SINGLE_THREAD_FIXTURE = PASS
FULL_EXPORT_SOURCE         = HOLD
100_CONVERSATION_CORPUS    = HOLD
INGESTION                  = BLOCKED ON SOURCE BYTES
```

The only valid next source event is receipt of the actual ChatGPT data-export ZIP or extracted `conversations.json`.

No Drive Doc, PDF, derived GitHub artifact, summary, or model reconstruction may enter the Import Manifest as source bytes.

## Acceptance bar for the first real run

```text
CORPUS = 100 actual conversations

manifest conversations = 100
reconciled conversations = 100
unaccounted turns = 0
unreplayable candidates = 0
hash failures = 0

CEO objects emitted by extractor = 0
authority created = false
```

No new kernel work is authorized by this receipt. Ingestion remains blocked on the missing full export.
