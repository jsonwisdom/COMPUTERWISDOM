# GITHUB MIRROR — V0.1

Mirror source: observed Google Drive readback.

Transport:
`QUESTION → METADATA → DRIVE_READBACK → GITHUB_MIRROR → RECEIPT`

Rules:
1. Preserve question text across surfaces.
2. Preserve directory names across surfaces.
3. Treat Drive readback as evidence, not authority.
4. Never infer merge approval from successful mirroring.
5. Any semantic delta becomes `DELTA`, not silent normalization.
6. Missing evidence becomes `HOLD`.

`authority_created = false`
