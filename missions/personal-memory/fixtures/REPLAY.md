# PMEM-OP-001 — Synthetic Replay Record

Mode: `SPECIFICATION_TRACE`  
Runtime claim: NONE  
Authority created: FALSE

## Expected trace

1. CREATE `USER_ASSERTED` deadline with REASON-only project-planning scope -> ADMITTED.
2. REASON query passes VALID/CURRENT/AUTHORIZED -> conclusion must explicitly attribute USER_ASSERTED source; derived result remains INFERRED.
3. EXPORT attempt -> REJECTED because EXPORT permission is absent. No reinterpretation into another successful operation.
4. REVOKE reasoning grant -> ADMITTED; future reasoning prohibited; historical receipts preserved.
5. Current query after revocation -> MATCHED may remain true, but USABLE=false and reasoning from object prohibited.
6. Historical replay before revocation -> usable under then-recorded policy/authority; replay after revocation -> not usable. No history rewrite.

## Precision lock

`PMEM-OP-001: SPEC_CONFORMANCE=PASS`

`SPECIFICATION != EXECUTION != BYTE-LEVEL VERIFICATION`

- Specification: rule-level PASS against frozen `v1.0 -> 010`.
- Execution: none claimed by this fixture.
- Byte-level verification: none claimed by this fixture.
- No synthetic receipt bytes, runtime ledger events, cryptographic integrity claim, external anchor, or authority are created by this document.

No laundering path is observed in the synthetic specification trace.
