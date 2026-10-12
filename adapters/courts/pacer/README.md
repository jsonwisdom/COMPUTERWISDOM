# PACER Court Adapter

Status: PARTIAL_IMPLEMENTATION_V0_1
Authority: false
Production ready: false

Purpose: parent namespace for PACER/CM-ECF integration inside RePlay Genesis.

Children:
- `auth/` — IMPLEMENTED_V0_1 authentication lifecycle and endpoint-specific session handling
- `cache/` — IMPLEMENTED_V0_1 persistent token/session cache with delegated secret storage
- `qa/` — SHELL_ONLY PACER QA validation fixtures and run receipts

Current implementation boundary:
- authentication + persistent cache code exists
- offline fake-transport/fake-secret-store validation exists
- real PACER QA authentication has NOT been run
- real OS-keyring persistence has NOT been independently validated here
- PACER PCL query adapter is not part of this milestone
- no successful MATCH / COMPLETE PACER receipt exists yet

Hard boundaries:
- no credentials in Git
- no assumed token TTL
- PACER/CM-ECF is an official record surface, not an authority creator by itself
- failed retrieval stays UNRESOLVED
- negative-control receipt stays off-chain
- mainnet provenance attestation requires a successful MATCH + COMPLETE receipt and independent hash/JCS replay
