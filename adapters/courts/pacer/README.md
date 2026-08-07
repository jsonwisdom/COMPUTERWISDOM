# PACER Court Adapter

Status: SHELL_ONLY
Authority: false
Production ready: false

Purpose: parent namespace for PACER/CM-ECF integration inside RePlay Genesis.

Planned children:
- auth/ — authentication lifecycle and endpoint-specific session handling
- cache/ — persistent token/session cache with no secret-derived receipts
- qa/ — PACER QA validation fixtures and run receipts

Hard boundaries:
- no credentials in Git
- no assumed token TTL
- PACER/CM-ECF is an official record surface, not an authority creator by itself
- failed retrieval stays UNRESOLVED
- no EAS transaction is emitted from directory presence
