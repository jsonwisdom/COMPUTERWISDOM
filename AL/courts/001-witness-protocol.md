# 001 — Witness Protocol

**Question:** How does AL handle disputes when two replays diverge?  
**Authority:** false  
**Memory type:** procedural

A court in AL does not decide who is right.

A court in AL determines which replay survives.

When two replays diverge, the system invokes the Witness Protocol:

1. Collect the receipts from each replay.
2. Reconstruct each replay deterministically using AL replay rules.
3. Compare the resulting transitions.

If one replay reconstructs and the other does not, the reconstructable one stands.

If both reconstruct but diverge, both are preserved as branches.

If neither reconstructs, both are rejected.

The court does not interpret intent.
The court does not elevate claims.
The court does not resolve narratives.

It performs one function only:

Determine which replay is procedurally admissible.

Witnesses are not people.

Witnesses are receipts.
