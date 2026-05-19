# Secret Scan → Zora Flywheel Image Adapter Candidate

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Zora profile pointer: https://zora.co/@jaywisdom
Related repos: jsonwisdom/AL and jsonwisdom/COMPUTERWISDOM
Portal mutation: none.
Public badge: none.
Backend claim: none.
Onchain claim: none.
Image output claim: candidate only.

## Purpose

This adapter defines how a Secret Scan Receipt may unlock a Zora image output lane for Jay's repo chain.

The image can be selected in two modes:

1. RANDOM_ZORA_ARTIFACT
   - select a random eligible Zora artifact from Jay's Zora profile or an approved artifact list
   - use when the scan passes and no specific artifact is requested

2. PURPOSE_BOUND_ZORA_ARTIFACT
   - select an artifact that matches the scan purpose, audit result, epoch, repo, or receipt chain
   - use when a specific story, proof, or visual reward is being expressed

## Core Rule

The image is not the proof.
The secret scan receipt is the proof boundary.
The Zora image is a visual reward, signal, or flywheel surface.

## Required Gate

A Zora image output may be created only after:

- secret scan command is documented
- scan result is recorded
- findings are classified as PASS / WARN / FAIL
- receipt file is committed
- image mode is declared: RANDOM or PURPOSE_BOUND
- source URL or artifact ID is recorded
- no secret, token, key, or credential appears in the image or metadata

## Allowed Inputs

- Zora profile pointer: `https://zora.co/@jaywisdom`
- approved Zora artifact URL
- approved local image already owned/created by Jay
- repo audit receipt
- Epoch 004 move-validation receipt
- AL repo receipt pointer
- COMPUTERWISDOM repo receipt pointer

## Forbidden Claims

- Do not claim Zora image = secret scan proof.
- Do not claim public badge grant.
- Do not claim portal integration.
- Do not claim onchain attestation unless transaction/attestation receipt exists.
- Do not copy third-party art without permission.
- Do not expose secrets in image metadata.
- Do not publish private repo data through the image.

## Output Schema

```json
{
  "adapter_id": "SECRET_SCAN_ZORA_IMAGE_ADAPTER_V1",
  "scan_receipt": "PENDING",
  "repo_chain": ["jsonwisdom/AL", "jsonwisdom/COMPUTERWISDOM"],
  "zora_profile": "https://zora.co/@jaywisdom",
  "selection_mode": "RANDOM_ZORA_ARTIFACT | PURPOSE_BOUND_ZORA_ARTIFACT",
  "selected_artifact": {
    "source_url": "PENDING",
    "artifact_id": "PENDING",
    "reason": "PENDING"
  },
  "output_type": "IMAGE_POINTER | REWARD_CARD | FLYWHEEL_POST",
  "secret_scan_status": "PENDING",
  "public_badge_granted": false,
  "portal_html_mutated": false,
  "onchain_claimed_live": false
}
```

## Repo Chain Rule

AL may provide constitutional/replay discipline.
COMPUTERWISDOM may provide audit, receipt, and visual reward surfaces.
Zora may provide cultural distribution and flywheel surface.

None of these layers replaces the others.

## Canon

Secret scan first.
Receipt second.
Zora image third.
Public claim last, if ever.

A Zora image can celebrate a clean board.
It cannot clean the board.
