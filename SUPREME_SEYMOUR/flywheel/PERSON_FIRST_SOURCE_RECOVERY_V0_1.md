# JASON — Person-First Source Recovery v0.1

**Status:** draft candidate on the Seymour flywheel branch; not production, not a complete original ChatGPT or voice recovery.
**Denominator:** JASON original purpose, dated decisions, source context. No human gate for computational audit verdicts.

## What this repair does

The existing Supreme Seymour flywheel enumerates GitHub repository heads, which cannot establish the completeness of JASON's voice and ChatGPT history. This addition checks a separately supplied **local, private** source manifest and produces a scoped recovery state for each expected voice or chat original.

| Source state | Meaning | Action |
| --- | --- | --- |
| `PRESENT_PARSED` | Bytes exist and candidate parser accepted text/JSON; authenticity and completeness remain UNKNOWN | May enter a candidate-only evidence lane |
| `PRESENT_UNREADABLE` | Bytes exist, but parsing/transcription failed or is unavailable | Voice: re-transcribe/reparse; chat: reparse |
| `MISSING_SOURCE_FILE` | Indexed source path was checked under an existing source root but file is absent | Locate/restore the exact original |
| `MISSING_INDEX_REFERENCE` | Expected source lacks manifest index entry | Repair that source's index |
| `AMBIGUOUS_DUPLICATE_CONFLICT` | Multiple candidates, no deterministic authenticated selection | Resolve source-specific conflict |
| `EVIDENCE_UNAVAILABLE` | No available root or no candidate path | Find source or configure the local root |

**Safety:** A candidate transcript is not proof of original voice audio or speaker identity. A valid JSON object is not proof of full ChatGPT export, accuracy, consent, or authorship. Audio bytes alone are not a transcript. No source type is given authority by ingestion.

## Privacy and durability

- The existing two public GitHub Actions artifacts contain only counts and general statuses.
- The detailed source recovery report is written to `build/supreme-seymour-flywheel/private/person-first-recovery.json`, **never in the two-file GitHub artifact upload list**.
- Original private bytes, private filenames, IDs, and hashes are not placed into the public summary.
- Do NOT commit originals, private manifests, or the local private recovery output to GitHub.
- Private source manifests are an operator-controlled local-only adapter; GitHub Actions CI runs only synthetic fixtures.
- No original ChatGPT export or voice files were read in this draft. Without a local manifest, the system reports two **EVIDENCE_UNAVAILABLE** categories and original completeness **UNKNOWN**, not missing/deleted originals.

## Private manifest shape (fictional example, never a real source claim)

```json
{
  "schema": "JASON_SOURCE_INPUT_MANIFEST_V0_1",
  "denominator": "JASON",
  "expected": [{"id": "voice-a", "kind": "voice"}, {"id": "chat-a", "kind": "chat"}],
  "index": [
    {"id": "voice-a", "candidates": [{"path": "audio/voice-a.txt", "format": "text"}]},
    {"id": "chat-a", "candidates": [{"path": "chats/chat-a.json", "format": "json"}]}
  ]
}
```

Input candidate paths are relative to a separate `JASON_SOURCE_ROOT`; traversal and absolute paths are rejected. `JASON_SOURCE_MANIFEST` must be explicitly configured locally. This module makes no network calls or Drive/ChatGPT/Grok imports by itself.

## Windows / Linux regression

After checking out the exact branch, validate that the following directory exists before running any command:

`SUPREME_SEYMOUR/flywheel/tests`

Then from that repository root:

```text
python -m unittest discover -s SUPREME_SEYMOUR/flywheel/tests -p "test_*.py" -v
```

The draft GitHub workflow runs the same synthetic test suite on **Windows and Linux**. It never receives private inputs.

## What remains

1. Recover dated original voice and chat source bytes with custody and timestamps.
2. Connect their validated hashes and event-time joins into the existing JASON_OS CEO/GRAPH/FOLD/QUERY pipeline. Parsing is not a validated CEO observation.
3. Establish durable private delivery and acknowledgment receipts separately. A GitHub workflow success is not evidence of user comprehension.
4. Keep all dependent HOLDs scoped; unrelated, evidence-supported GitHub delta observations continue.
5. Preserve prior receipts, errors, contradictions, and corrections without silent rewrite.

**Verdicts:** PASS / FAIL / UNKNOWN for specific claims. HOLD applies only to the dependent workflow path. No unverified green, wallet authority, transfer, deployment, publication, or automated family action.
