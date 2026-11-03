# COMPUTERWISDOM Base/EVM bootstrap

A guarded, repository-bound Base/EVM operator for Base (`8453`) and Base Sepolia (`84532`). Reads and simulations are the default. CI uses an isolated Anvil chain and never signs or broadcasts.

## Boundaries

- No raw private-key or seed input.
- No unattended signing or sending.
- `send` requires an explicit flag and typed chain confirmation.
- CI never invokes `send` and contains no wallet secret.
- Receipts record bounded observations; they do not create authority or chain truth.

## Local check

Copy `.env.example` to `.env`, select a chain, and set its RPC URL. Then run:

```powershell
.\ComputerWisdom-Base.ps1 -Action check
```

```bash
./computerwisdom-base.sh check
```

## Deterministic receipt

Receipts require a stable ID, an explicit UTC observation time, and an output path. Repeating the same inputs produces the same bytes.

```powershell
.\ComputerWisdom-Base.ps1 -Action receipt -ReceiptId replay-001 -ObservedAtUtc 2026-08-21T00:00:00Z -ReceiptOut receipt.json
python verify_receipt.py receipt.json
```

```bash
./computerwisdom-base.sh receipt --receipt-id replay-001 --observed-at-utc 2026-08-21T00:00:00Z --receipt-out receipt.json
python3 verify_receipt.py receipt.json
```

## GitHub operation

`.github/workflows/base-evm-bootstrap.yml` performs syntax checks, boots Anvil twice with Base chain IDs, executes both entry points, compares deterministic receipts byte-for-byte, verifies the receipt, and uploads the receipt plus SHA-256 report. It uses no public RPC and performs no transaction.


