# ANTI_DRIFT_NEWS_OPEN_SOURCE_REPLAY_CLIENT_SPEC_V1

A fully open-source, trustless verification client for Anti-Drift News.

Placement: `docs/anti_drift_news/open_source_replay_client_spec_v1.md`  
Repo: `jsonwisdom/COMPUTERWISDOM`  
Status: Ready for PR #202 merge path  
Authority: false  
Public from day one

This client enables any participant to independently reconstruct, verify, and dispute Anti-Drift News state without trusting servers, maintainers, or UI surfaces.

It operationalizes the constitutional invariants:

- `authority:false`
- `append_only`
- `replay_supremacy`
- `public_from_day_one`
- `no_hidden_state`
- `no_privileged_mutation`
- `math_over_trust`

---

## 1. Purpose

The Anti-Drift News Open-Source Replay Client is a sovereign verification tool.

It ensures that:

- No server can rewrite history
- No maintainer can override events
- No UI can misrepresent state
- No cache can drift from truth
- No authority can intervene

The client is the public's right to verify.

---

## 2. Manifest Verification

The client MUST:

1. Load the root manifest from `MANIFEST_URL`.
2. Verify the `manifest_hash` using canonical JSON serialization.
3. Verify that each segment entry includes:
   - `segment_id`
   - `storage_uri`
   - `hash`, sha256
4. Reject the manifest if:
   - Any segment hash mismatches
   - Any segment is missing
   - Any segment is reordered
   - The manifest hash does not match the canonical manifest

Outcome:

If the manifest fails verification:

```txt
HALT: MANIFEST_CORRUPTED
```

---

## 3. Segment Verification

For each segment, the client MUST:

- Stream JSONL line-by-line
- Verify the segment's SHA-256 hash
- Validate that each line is a JSON object
- Detect:
  - Truncation, missing lines
  - Insertion, extra lines
  - Reordering, line order mismatch
  - Mutation, hash mismatch

If any anomaly is detected:

```txt
HALT: SEGMENT_CORRUPTED
```

---

## 4. Event Verification

Each event MUST pass:

1. Schema validation against `EVENT_SCHEMA_V1`
2. `authority === false`
3. `event_hash` verification:
   - Canonical JSON
   - Sorted keys
   - SHA-256 match
4. Replay boundary compliance

Invalid events MUST be rejected and reported.

No invalid event may mutate state.

---

## 5. Replay Engine Integration

The client MUST embed the exact same replay engine defined in:

- `replay_engine_spec_v1.md`
- `game_state_schema_v1.md`

Replay MUST be:

- Deterministic
- Idempotent
- Canonically ordered
- Boundary-aware
- Bit-identical across machines

Replay output MUST match:

```txt
GAME_STATE_SCHEMA_V1
```

---

## 6. Snapshot Receipts

The client MUST support generating `GAME_STATE_SNAPSHOT` receipts:

```json
{
  "type": "GAME_STATE_SNAPSHOT",
  "game_id": "ADN-000001",
  "snapshot_hash": "sha256:...",
  "manifest_hash": "sha256:...",
  "segment_range": ["seg_001", "seg_014"],
  "derived_by": "adn_replay_client_v1",
  "authority": false
}
```

Snapshots are:

- Non-authoritative
- Reproducible
- Verifiable
- Public

They are not a replacement for events.

---

## 7. CLI Surface

The client MUST expose the following commands.

Verify a game:

```bash
adn verify --game-id ADN-000001
```

View leaderboard:

```bash
adn leaderboard
```

Inspect receipts for a claim:

```bash
adn receipts --claim CLAIM-001
```

Verify manifest integrity:

```bash
adn manifest verify
```

Verify a specific segment:

```bash
adn segment verify --segment-id SEG-000001
```

Generate a snapshot:

```bash
adn snapshot generate --game-id ADN-000001
```

All commands MUST:

- Produce deterministic output
- Include hashes
- Include event counts
- Include drift indicators

---

## 8. Dispute Surface

Users MUST be able to challenge:

- Missing events
- Invalid hashes
- Incorrect badge assignments
- Incorrect leaderboard rankings
- Incorrect `drift_risk` outputs
- Manifest substitution
- Segment corruption

Disputes are events.

They enter the log via:

```txt
DISPUTE_RAISED
```

There is no admin override.

The community resolves disputes by replaying the log.

---

## 9. Constitutional Invariants

The client MUST enforce:

- `authority:false`
- `append_only`
- `replay_supremacy`
- `public_from_day_one`
- `no_hidden_state`
- `no_privileged_mutation`
- `math_over_trust`

Any violation MUST trigger:

```txt
HALT: CONSTITUTIONAL_VIOLATION
```

---

## 10. Threat Model

The client MUST defend against:

- Compromised servers
- Corrupted caches
- Reordered events
- Missing segments
- Inserted events
- Forged badges
- Forged scores
- Manifest substitution
- Segment truncation
- Segment mutation
- Replay poisoning
- UI misrepresentation

The client MUST treat all servers as untrusted.

Only math is trusted.

---

## 11. Canon Phrase

This site does not ask you to trust it.  
It gives you the math to verify it.

Secondary canon:

Not anti-news.  
Anti-drift.  
Public receipts from day one.
