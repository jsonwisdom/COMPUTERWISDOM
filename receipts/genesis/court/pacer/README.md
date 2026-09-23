# PACER Receipt Surface

Status: SHELL_ONLY
Authority: false
Receipts: NONE
Attestations: NONE

Reserved for append-only PACER provenance receipt references and seal-envelope metadata.

Rules:
- runtime log != receipt
- receipt != seal
- seal != authority
- raw tokens/secrets prohibited
- failed retrieval receipts remain fail-closed
- mainnet attestation target requires validated MATCH + COMPLETE receipt
