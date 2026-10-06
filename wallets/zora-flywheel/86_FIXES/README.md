# APPEND-ONLY FIX LEDGER

A fix never rewrites history.

```text
BAD_OR_STALE_STATE
  -> AUDIT
  -> FIX_RECORD
  -> NEW_STATE
```

The prior object remains addressable so replay can explain why the newer state exists.
