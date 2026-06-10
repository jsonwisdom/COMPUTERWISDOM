# Compute Wisdom Direct · Manifest Candidate

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Source output: `receipts/deep_seek_epoch_004_output.md`
Output receipt: `receipts/epochs/deep_seek_epoch_004_output_receipt.json`
Portal mutation: none.
Public badge: none.
Backend claim: none.
Onchain claim: none.
Official authority claim: none.

## Purpose

Compute Wisdom Direct turns the COMPUTERWISDOM repo into a receipt machine.

It is repo-native: prompts, outputs, audits, Zora drops, Meme Court cases, manifests, and receipts are captured as files, hashed, reviewed, and promoted only by explicit receipt.

## Core Pipeline

```text
CAPTURE -> PARSE -> TAG -> HASH -> RECEIPT -> REVIEW -> MERKLE -> REWARD
```

## Directory Role Map

| Directory | Role |
|---|---|
| `candidates/` | incoming proposals |
| `sessions/` | session purpose and vernacular cases |
| `services/` | reusable service/candidate surfaces |
| `services/zora-flywheel/` | Zora Factory, crawler specs, image adapters |
| `services/meme-court/` | Meme Court to Zora/Base candidate path |
| `receipts/` | session, reward, factory, audit, and epoch receipts |
| `receipts/zora_factory/` | factory drop receipts |
| `receipts/epochs/` | epoch receipts and output receipts |
| `receipts/merkle/` | Merkle purpose keys |
| `audits/` | targeted repo-chain audits |
| `epochs/` | operating epochs such as 5D Chinese Checkers |
| `MANIFEST.md` | main map / lock-state index |
| `portal.html` | protected public surface |

## Current Active Inputs

- Deep Seek Epoch 004 prompt: `receipts/deep_seek_epoch_004_prompt_exact.txt`
- Deep Seek Epoch 004 output: `receipts/deep_seek_epoch_004_output.md`
- Zora Factory schema: `services/zora-flywheel/factory_receipt_schema_candidate.json`
- Zora Factory crawler spec: `services/zora-flywheel/factory_crawler_spec_candidate.md`
- Example factory receipt: `receipts/zora_factory/example_mint_receipt_candidate.json`
- Meme Court open candidate: `services/meme-court/open_court_zora_base_candidate.md`
- Secret scan template: `receipts/secret_scan_epoch_004_receipt.json`

## Gate Rules

- No public badge without a promotion receipt.
- No portal mutation without a promotion receipt.
- No onchain/Base/Zora proof claim without a transaction or attestation receipt.
- No official authority claim without public evidence.
- No Zora image before secret scan PASS or reviewed WARN.
- No Merkle growth without a committed receipt leaf.

## Next Required Artifacts

1. `governance/move_validation_rules_candidate.json`
2. `receipts/secret_scan_epoch_004_receipt.json` updated with PASS / WARN / FAIL
3. `receipts/deep_seek_session_003_verdict.json`
4. first real `receipts/zora_factory/drop_<id>_receipt.json`
5. Merkle update receipt for Compute Wisdom Direct leaves

## Canon

Compute Wisdom Direct is direct because receipts are the path.

Deep Seek proposes.
Computer Wisdom validates.
Jay's Wisdom promotes.
No piece moves without a receipt.
