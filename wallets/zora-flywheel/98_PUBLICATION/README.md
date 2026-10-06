# PUBLICATION GATE

The School of Wisdom public surface is generated from append-only public updates.

Required publication checks:
- append-only update ledger parses
- ids are unique
- timestamps do not regress
- derived latest/feed artifacts build
- GitHub Pages deploy completes
- School of Wisdom page returns HTTP 200
- latest.json returns HTTP 200
- no raw private financial connector payload is published

```text
200_OK = SITE_REACHABLE
200_OK != CLAIM_TRUE
PUBLICATION != SIGNATURE
```
