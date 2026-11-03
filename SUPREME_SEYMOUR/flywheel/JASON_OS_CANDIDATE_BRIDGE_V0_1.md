# JASON_OS candidate bridge — CEO → GRAPH → FOLD → QUERY v0.1

**Branch-only implementation; not merged or deployed.** This is a PRIVATE, read-only *candidate projection* adjacent to the historical JASON_OS kernel. It does **not** modify/fabricate the documented frozen CEO, GRAPH, FOLD, QUERY schema hashes or assert those schemas are implemented. See `artifacts/JASON_OS_CONVERSATION_COMPILER_INGESTION_STATUS_V0_1.md`.

## Chain

1. **Original source**: A private voice transcript or original chat JSON file identified through the explicit JASON denominator manifest. Observe original bytes, hash them exactly, do not infer authorship.
2. **CEO candidate**: Parsed/extracted text, with source byte SHA-256, separate declared event time (unverified), candidate text digest, source recovery action, and `evidence_verdict=UNKNOWN`. A text parse is not a validated CEO observation.
3. **GRAPH candidate**: Each candidate references its source object using an explicit `EXTRACTED_FROM_BYTES` edge. No family, identity, historical or ownership inference. Voice transcripts optionally reference original audio bytes via `DECLARED_TRANSCRIPT_OF` with `relation_verdict=UNKNOWN`.
4. **FOLD candidate**: Per-source summary keeps `UNKNOWN`, `CONFLICT`, `SOURCE_NOT_USABLE` and `reconstruction_complete=false`; does not silently combine missing and parsed records.
5. **QUERY candidate**: Returns per-source status, digest, recovery action and `UNKNOWN` verdict. A nonexistent input returns `NOT_ENUMERATED` rather than invented evidence.
6. **Public flywheel**: Only aggregate counts and status categories. Full candidate text/IDs/hashes reside in `build/supreme-seymour-flywheel/private/jason-os-candidates.json`; current GitHub artifact workflow uploads only `flywheel-report.json` and `flywheel-summary.md`. No private manifest, originals or detailed output is committed or uploaded.

## Private input configuration

`JASON_SOURCE_ROOT` and `JASON_SOURCE_MANIFEST` are explicit local paths provided separately by operator-controlled local execution. No such paths configured in CI. Never put original source bytes in GitHub.

Supported candidate extraction is intentionally narrow: voice UTF-8 transcript `text`, and explicit chat JSON `{"messages":[{"text":"..."}]}` or a single-item export `[{"chat":{"messages":[...]}}]`. Other valid JSON formats remain parsed but **not extracted**, with `IMPLEMENT_EXPLICIT_CHAT_LAYOUT_EXTRACTOR` recovery action. A voice transcript without an original audio pointer remains an unverified transcription and asks to repair the audio reference; an original audio pointer is not identity proof.

**Original source authentication, event time, historical completeness, operator learning, and verified memory remain UNKNOWN.** This is not a ChatGPT export connector and does not capture original microphone input. The connected ChatGPT app exposes Coinbase features, not original ChatGPT chat archives.

## Test

The branch includes 16 unit tests and 3 end-to-end flywheel tests, in addition to the prior 16 source-recovery tests, for a total of **35 synthetic tests**. Check test outcomes in the GitHub Action; these statements describe test inventory, not test success.

```text
python -m unittest discover -s SUPREME_SEYMOUR/flywheel/tests -p "test_*.py" -v
```

CI is configured to use Python 3.12 on Windows and Linux, with no access to personal originals.

## Pre-merge gaps

- Exact historical JASON_OS kernel schema conformance and import manifest ABI have not been validated, since the frozen schemas are referenced by hash but the private originals and canonical kernel implementation are not present in this branch.
- The candidate graph does not establish voice authorship, ENS ownership, DNS custody, family relationships or any external truth claim.
- Private output remains local/ephemeral; durable private retention and user delivery are unimplemented.
- A source location symlink must stay confined to the declared private root; `_confined` enforces this.
- A missing or failed dependent source is HOLD only for that path; public GitHub observation and other parsed candidates continue.
