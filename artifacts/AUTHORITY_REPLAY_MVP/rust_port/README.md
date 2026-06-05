# Authority Replay Rust Port

Status: BASELINE_SCAFFOLD
Authority: false

This directory is the second-implementation lane for the Authority Replay MVP.

Goal:

```text
Same receipt fixture
Different implementation
Same verdict
```

The Python engine remains the baseline implementation. The Rust port is intended to verify that replay results survive implementation diversity.

## Current Scope

- Parse the same Authority Replay receipt JSON fixtures.
- Evaluate the same authority chain fields.
- Return the same verdict shape as the Python engine.
- Treat tool safety blocks as distinct from GitHub policy denials.

## Promotion Rule

Do not promote `independent_replay_status` to `OBSERVED` until Python and Rust produce matching outputs for the same fixtures.

```json
{
  "independent_replay_status": "PENDING_CROSS_IMPLEMENTATION_REPLAY",
  "global_promotion": false
}
```
