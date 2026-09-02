# Grok Output Gate V0.1

This folder bounds Grok to nonbinding review output. The gate reads one JSON object from stdin and emits one JSON object to stdout. It does not write files, use the network, mutate Git, merge, sign, spend, promote facts, or create authority.

Rules:

- `REVIEW_FINDINGS` and `NONBINDING_RECOMMENDATION` may pass through.
- A missing or blank `batch_receipt_id` produces `HOLD_REVIEW_ONLY`; this is not a build hold.
- `FINAL_VERDICT` is removed at any nesting depth and under punctuation/case aliases.
- A receipt changes the routing state to `REVIEW_READY_FOR_HUMAN`; it never makes Grok the final verifier.
- Unknown top-level fields are dropped.

Run:

```sh
python bots/grok/grok_output_gate.py < candidate.json
python -m unittest discover -s bots/grok/tests -v
```

The process exit code is `0` for gated review output and `2` for malformed or non-object JSON.
