# 001 — How to Verify a Receipt

**Question:** How does AL return replayable true/false without authority?  
**Authority:** false  
**Memory type:** procedural

Verification is reconstruction, not judgment.

To verify a receipt, AL does one thing:

Replay the transition described by the receipt using only the evidence it contains.

If replay produces exactly one lawful transition, the receipt is valid.

If replay produces zero or more than one possible transition, the receipt is invalid.

Verification does not interpret intent.
Verification does not resolve disputes.
Verification does not elevate claims.

It answers a single procedural question:

Can this receipt be reconstructed deterministically from its own evidence?

That is the entire test.

True or false.

No authority invoked.
