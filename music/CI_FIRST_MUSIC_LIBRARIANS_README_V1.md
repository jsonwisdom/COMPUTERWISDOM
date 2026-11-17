# CI-FIRST Music Librarians — Feeling Shelves V1 (DRAFT)

## Purpose
Organize Chicago house music *by feeling* as a human-editable browsing aid, never as a factual diagnosis of music or a person. The 128 BPM value is a **mix target**, not a claim about any original record.

## Librarians
- Provenance: dates, official credits, sources, unresolved claims.
- Rhythm: distinguish target mix grid from source-record BPM and observed onset timestamps.
- Feeling: voluntary human multi-tags with explicit uncertainty.
- Lyrical Constitution: attribution, licensed excerpts, copyright limits; similarity cannot prove authorship or intent.
- Replay: deterministic PASS / FAIL / UNKNOWN receipts.

## Current 1984–1987 seed
Four editorial **candidate** records (Jesse Saunders, Chip E, Marshall Jefferson, Phuture). Historical release year and original tempo are **UNKNOWN** until independently cited and measured. No audio or copyrighted lyrics stored.

## Replay
Run `python3 music/CI_FIRST_MUSIC_LIBRARIANS_REPLAY_V1.py` from repository root. Replay hashes raw catalog bytes; changes alter the receipt. Proposed CI gate blocks **FAIL**, permits **UNKNOWN** in draft status and bars publication on UNKNOWN provenance. There is deliberately **no** new GitHub Actions workflow to avoid extra notification noise.

## Safety & boundaries
- No family/private JOY or AL nodes are imported. This is public music metadata only.
- No psychological inference, emotional scoring, artist-intent inference, or authority claims.
- Keep original recordings and bytes untouched.
- The source corpus and deployment are **not** validated by this draft.
- No live DNS, Worker, master-branch, wallet, or payment modification.
- Prior organizing-only rule: https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/WISDOM/computerwisdom_mirror_v0_1.md

## Next evidence requirement
For each catalog record: verified track/version ID, cited release-year source, licensed playback locator, audio-origin proof where lawful, measurement method, original BPM + uncertainty, listener-supplied feeling tags, and audit timestamp. Claims remain UNKNOWN until satisfied.
