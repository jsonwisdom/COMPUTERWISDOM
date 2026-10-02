# JSONWisdom Story Mode Building

Story Mode turns a large repository into a navigable sequence without pretending that narrative is evidence.

## Build order

1. Identity — who is speaking and within what scope?
2. Worlds — what bounded context exists?
3. Characters — who or what participates?
4. Projects — what is being built?
5. Scenes — what happened or is proposed?
6. Claims — what exactly is asserted and with which epistemic type?
7. Evidence — what replayable source supports the claim?
8. Receipts — what succeeded, failed, or remains held?
9. Replay — can another operator reproduce the digest and result?
10. Publication — what may be shared, and under whose permission?

## Commands

Run from the repository root:

    python STORY_MODE/tools/validate.py
    python STORY_MODE/tools/build.py
    python STORY_MODE/tools/replay.py

`build.py` writes a deterministic manifest to `STORY_MODE/08-replay/story-mode.manifest.json`. `replay.py` fails closed if a governed file is missing or its SHA-256 differs.

## Boundaries

- Existing repository history is not moved or rewritten.
- A path organizes an artifact; it does not prove it.
- A receipt records an event; it does not create truth or authority.
- Jason Wisdom controls Jason Wisdom's own voice and creation within voluntary, explicit scope.
- Story Mode creates no authority over another person, government, or institution.

Proposal: https://github.com/jsonwisdom/COMPUTERWISDOM/issues/459
