# Packet 002 — Pan Park Template

**Packet:** 002_pan_park  
**Surface:** Mirror Mint MN  
**Observer:** JOY  
**Verifier:** AL  
**Renderer:** COMPUTERWISDOM  
**Identity Anchor:** jaywisdom.eth / jaywisdom.base.eth  
**Authority:** false

## Purpose

Bind the Mirror Mint Minnesota first-use-case to a witnessed civic event without pre-filling any hash or source claim.

## Current Status

```json
{
  "packet": "002_pan_park",
  "status": "TEMPLATE_COMMITTED",
  "observer": "JOY",
  "verifier": "AL",
  "renderer": "COMPUTERWISDOM",
  "hash_status": "PENDING_EXACT_RECEIPT_BYTES",
  "source_url": "PENDING_LIVE_CAPTURE",
  "captured_at_utc": null,
  "sha256": null,
  "render": "+1 Glow to COMPUTERWISDOM once sealed",
  "authority": false
}
```

## Required Before Seal

1. JOY re-observes the live source.
2. Raw bytes are captured.
3. SHA-256 is computed from those bytes.
4. Source URL, UTC timestamp, and hash are recorded.
5. Packet is updated from `TEMPLATE_COMMITTED` to `SEALED_RECEIPT`.

## Doctrine

No bytes → no hash.  
No source → no claim.  
No receipt → no promotion.

This packet is a template until the live observation exists.
