# Fixtures — STATUS=HOLD, AUTHORITY_CREATED=false

| Vector | Expected digest | Object status |
|---|---|---|
| TV-001 | sha256:4d576d03…6836 | SEARCH_MISS — placeholder only |
| TV-002 | sha256:49244546…03fe | SEARCH_MISS — placeholder only |
| SYN-001 | sha256:e9709c41…59dd | SYNTHETIC — proves JCS+SHA-256 pipeline |
| SYN-002 | sha256:14cfa76e…0eff | SYNTHETIC — proves JCS+SHA-256 pipeline |

TV-001/TV-002 digests come from the gate text. The objects that produce them (ARCHITECTURE_V1_5)
were not found in the box, transcripts searched, Drive search, or the last 50 commits of this repo
(`git log -S` / `git grep` for both hex strings: no hits). `TV-*.json` here are HOLD placeholders.

`src/vectors.js` fails closed: it returns `MATCH` only when the canonical bytes of the object hash
to the expected digest. A placeholder returns `SEARCH_MISS`; any other mismatch returns `MISMATCH`.
To close the gap, drop the recovered object into `TV-00N.json` and set `objectStatus` to `RECOVERED`.

SYN expected digests were computed by this implementation and cross-checked with an independent
Python canonicalizer for SYN-002 (see BUILD_REPORT.md). They are not external test vectors.
