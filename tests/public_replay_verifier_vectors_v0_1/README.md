# Public Replay Verifier Vectors V0.1

These fixtures define the golden inputs and expected verifier outputs for the Computer Wisdom public replay verifier.

If an implementation accepts the same packet fixture and observable evidence conditions, it must emit the same `COMPUTERWISDOM_REPLAY_VERIFIER_V0_2` classification state.

## Invariants

- Hash mismatch is a hard floor at `MAINTAIN`.
- Evidence-layer failure caps output at `PARTIAL_REPLAY_READY`.
- Routing-layer failure is non-fatal.
- Authority remains `false`.

## Vector Set

- `perfect_packet.input.json`
- `perfect_packet.expected.json`
- `hash_mismatch.input.json`
- `hash_mismatch.expected.json`
- `github_invalid.input.json`
- `github_invalid.expected.json`
- `base_eas_invalid.input.json`
- `base_eas_invalid.expected.json`
- `ipfs_invalid.input.json`
- `ipfs_invalid.expected.json`
- `routing_only_failure.input.json`
- `routing_only_failure.expected.json`
