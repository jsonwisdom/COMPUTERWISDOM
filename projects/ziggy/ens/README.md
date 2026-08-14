# Ziggy ENS Layer

ENS is a **resolution and naming layer**, not automatic proof of control.

## Resolution model

Ziggy keeps these checks separate:

1. **Forward resolution** — ENS name → address / records.
2. **Reverse resolution** — address → name.
3. **Signer verification** — recovered/connected signer proves control by signature.
4. **Repository binding** — receipt explicitly names `jsonwisdom/COMPUTERWISDOM`.

A match is evidence. A mismatch is a preserved gap. Neither silently creates authority.

## Creation model

Natural-language requests may reference an ENS name as a human-readable target. Ziggy may resolve the name and read supported records, then construct a candidate creation request.

Writing ENS records or changing resolver state is a separate transaction requiring explicit human authorization.

## Address claims

See `claims.v0.1.json`.

User-supplied addresses remain `UNVERIFIED` until control is demonstrated cryptographically. Do not infer that two supplied addresses are the same wallet, replacements, aliases, or controlled by the same person unless verified.

## Receipt requirements

An ENS-aware Ziggy receipt should preserve:

- input ENS name, if supplied
- forward-resolved address
- reverse-resolved name, if checked
- connected/recovered signer address
- resolution timestamp / block context when applicable
- match or mismatch state
- source repository
- `authority_created=false`

## Sources

Protocol implementation should follow the official ENS resolver and record specifications rather than UI assumptions.
