# CoinBaseKidsCustimerSelfServiceConnector

Local-only Phase-1 prototype for Jason's full-math Coinbase self-service connector.

## Boundary

- Adult customer Coinbase account data only.
- Read-only account/history adapters.
- No trade, transfer, send, withdraw, portfolio mutation, signing, custody, or recommendations.
- "Kids" means the explanation layer uses simple, inspectable language. It is not a child trading product.
- Coinbase is one rail, not the whole financial identity.
- Missing data is HOLD, never zero.
- UNKNOWN transfer counterparties stay HOLD even when the transaction receipt itself is PASS.
- Event receipt, identity join, fee completeness, and history completeness are separate clocks.

## Architecture

CUSTOMER VIEW CREDENTIAL / MANUAL EXPORT
→ NORMALIZER
→ COMPUTERWISDOM SIDECAR
→ FULL-MATH STATE ENGINE
→ EXPLANATION LAYER
→ HUMAN

COMPUTERWISDOM SIDECAR responsibilities:
1. Preserve current state when a branch is blocked.
2. Keep the session alive without inventing data.
3. Route to the next safe read-only move.
4. Emit a receipt for each routing decision.

The sidecar is a routing membrane, not authority and not ReceiptOS verification.

## Status

WRITE=false
TRADE=false
TRANSFER=false
SIGN=false
AUTHORITY_CREATED=false
CANON=false
NO_FAKE_GREEN=true
