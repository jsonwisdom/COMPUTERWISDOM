# Canonical serializer v1 fixture manifest

Status: DELTA / test-only.

| Fixture | Class | Required result |
|---|---|---|
| equivalent-key-order | positive | reordered keys emit identical bytes |
| unicode-preservation | positive | Unicode preserved without normalization |
| numeric-boundaries | positive | signed int53 limits accepted |
| absent-vs-null | positive | missing and null remain distinct |
| ordered-arrays | positive | array order changes bytes |
| version-envelope | positive | complete version labels accepted |
| forbidden-wall-clock | negative | WALL_CLOCK_IN_SNAPSHOT |
| unknown-field-rejection | negative | UNKNOWN_FIELD |
| duplicate-keys | negative | DUPLICATE_KEY |
| lone-surrogates | negative | LONE_SURROGATE |
| illegal-numbers | negative | ILLEGAL_NUMBER |

Run:

```sh
sh evals/canonical-serializer-v1/run_evals.sh
```

Success requires both independent runtimes to agree on every result, raw byte
string, and SHA-256 digest. Any mismatch exits nonzero.
