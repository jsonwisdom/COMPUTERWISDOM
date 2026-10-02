# WLFI Quad Onion Contract Authority Audit v0.1

**Class:** public-source smart-contract authority audit  
**Authority created:** FALSE  
**Proof inferred:** FALSE  
**Legal violation inferred:** FALSE

## Purpose

Test the deployed WLFI smart-contract authority topology separately from token price, political narrative, bank-charter review, and reserve attestations. Holder governance does not imply administrator immutability or absence of privileged control.

## O1 — Record / Code

Canonical WLFI proxy: `0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6`.

Observed architecture:

```text
TRANSPARENT / ERC1967 UPGRADEABLE PROXY
        ↓
WorldLibertyFinancialV3
        ↓
REGISTRY + VESTER
```

State:

```text
SOURCE_VERIFIED                  = YES
UPGRADEABLE                      = YES
V3_IMPLEMENTATION                = BOUND
MULTIPLE_IMPLEMENTATION_STATES   = BOUND
IMMUTABLE_ERC20                  = FALSE
```

Cyfrin's May 2026 WLFI unlock/V3 audit identified medium- and low-severity vesting/registry issues, including a path allowing finalized categories to bypass the intended 10% election burn. The audit records that the cited medium findings were fixed in commit `1430e245349795921bebe275f6bd1d835d9f8fa3` and verified by Cyfrin.

```text
AUDIT_FOUND_BUG                  = PROVEN
AUDITOR_SAYS_FIXED               = PROVEN
DEPLOYED_BYTECODE_FIX_MATCH      = HOLD_PENDING_BYTE_COMPARE
```

## O2 — Authority / Control

WLFI owner Safe observed at:

`0x5be9a4959308A0D0c7bC0870E319314d8D957dBB`

Privileged contract surface includes owner/guardian functions for pause, blacklist, account activation, balance reallocation, signer/guardian management, vesting/governance controls, and upgrade-dependent behavior.

```text
OWNER_SAFE                       = BOUND
ADMIN_CONTROL_SURFACE            = HIGH
BLACKLIST_CAPABILITY             = BOUND
BALANCE_REALLOCATION_CAPABILITY  = BOUND
PAUSE_CAPABILITY                 = BOUND
GOVERNANCE_ADMIN_CONTROLS        = BOUND
CURRENT_SAFE_OWNERS              = HOLD
CURRENT_SAFE_THRESHOLD           = HOLD
CURRENT_GUARDIAN_HUMAN_IDENTITY  = HOLD
TIMELOCK / DELAY                 = HOLD
ENABLED_SAFE_MODULES             = HIGH_PRIORITY_HOLD
```

Original Safe setup was observed as 2-of-3; subsequent owner/threshold mutations exist. Current signer set and threshold require a live `getOwners()` / `getThreshold()` replay.

## O3 — Execution / Use of Power

A September 4, 2025 on-chain transaction exercised `guardianSetBlacklistStatus(..., true)` against an address publicly associated with Justin Sun.

```text
BLACKLIST_FUNCTION_EXISTS        = PROVEN
GUARDIAN_AUTHORITY_EXISTS        = PROVEN
BLACKLIST_AUTHORITY_EXERCISED    = PROVEN
TARGET_BLACKLIST_STATE_CHANGED   = PROVEN_ONCHAIN
```

Membrane:

```text
FREEZE_OCCURRED                  != FREEZE_WAS_ILLEGAL
ADMIN_KEY                        != TRUMP_FAMILY_MEMBER
CENTRALIZED_CONTROL              != BACKDOOR_EXPLOIT
```

Historical reallocation, pause and full upgrade-event replays remain open.

## O4 — Oversight / Coverage Gap

Financial oversight and smart-contract authority review are separate surfaces.

```text
BANK_CHARTER_REVIEW              != WLFI_CONTRACT_SAFETY_CERTIFICATION
RESERVE_ATTESTATION              != ADMIN_KEY_AUDIT
TOKEN_VALUE / LIQUIDITY          != HOLDER_CONTROL_RIGHTS
GOVERNANCE_TOKEN                 != TRUSTLESS_TOKEN
```

The OCC World Liberty Trust / USD1 charter process does not, by itself, certify WLFI proxy-admin, guardian, blacklist, reallocation, Safe-module or upgrade behavior.

## Current BoxD ruling

```text
SOURCE_VERIFIED                  = YES
UPGRADEABLE                      = YES
OWNER_SAFE                       = PROVEN / BOUND
ADMIN_CONTROL_SURFACE            = HIGH
BLACKLIST_POWER                  = PROVEN
BLACKLIST_POWER_USED             = PROVEN
BALANCE_REALLOCATION_CAPABILITY  = BOUND
PAUSE_CAPABILITY                 = BOUND
GOVERNANCE_ADMIN_CONTROLS        = BOUND
CURRENT_SAFE_OWNERS              = HOLD
CURRENT_SAFE_THRESHOLD           = HOLD
CURRENT_GUARDIAN_IDENTITY        = HOLD
TIMELOCK / DELAY                 = NOT_YET_BOUND
ENABLED_SAFE_MODULE_AUTHORITY    = HIGH_PRIORITY_HOLD
DEPLOYED_CYFRIN_FIXES            = HOLD_PENDING_BYTE_COMPARE
TRUMP_PERSONAL_KEY_CONTROL       = NOT_PROVEN
UNLAWFUL_SEIZURE                 = NOT_PROVEN
REGULATORY_NEGLIGENCE            = NOT_PROVEN
```

## Next executable replay

```text
WLFI PROXY
→ PROXY ADMIN / UPGRADE AUTHORITY
→ OWNER SAFE
→ CURRENT OWNERS + THRESHOLD
→ ENABLED MODULES
→ GUARDIAN
→ AUTHORIZED SIGNER
→ BLACKLIST HISTORY
→ REALLOCATION HISTORY
→ PAUSE HISTORY
→ UPGRADE HISTORY
→ DEPLOYED V3 BYTECODE ↔ CYFRIN FIXED COMMIT
```

## Source pointers

- Etherscan: WLFI proxy `0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6`
- Etherscan: World Liberty Safe `0x5be9a4959308A0D0c7bC0870E319314d8D957dBB`
- Etherscan: September 4, 2025 blacklist transaction / `SetBlacklistStatus`
- Cyfrin audit report: `2026-05-06-cyfrin-wlfi-unlock-v2.0.md`
- Cyfrin-recorded fixed commit: `1430e245349795921bebe275f6bd1d835d9f8fa3`
- OCC World Liberty Trust charter materials for the separate USD1 / banking rail

## Hard membrane

```text
HOLDER_GOVERNANCE                != ADMIN_IMMUTABILITY
CENTRALIZED_AUTHORITY            != ILLEGALITY
CONTROL_CAPABILITY               != CONTROL_EXERCISED
CONTROL_EXERCISED                != IMPROPER_CONTROL
ONCHAIN_RECEIPT                  != HUMAN_IDENTITY
FINANCIAL_OVERSIGHT              != CONTRACT_AUTHORITY_AUDIT
AUTHORITY_CREATED                = FALSE
PROOF_INFERRED                   = FALSE
```
