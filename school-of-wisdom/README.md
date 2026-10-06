# School of Wisdom — Public Update Beacon

This is the public, app-independent notification surface for the School of Wisdom.

Primary source of truth:
- `updates.jsonl` — append-only public update ledger

Derived publication surfaces:
- `latest.json` — latest public update
- `feed.json` — machine-readable JSON feed
- `feed.xml` — Atom feed
- `index.html` — human morning dashboard

The website is the notification system. Email is optional, not foundational.

## Morning loop

```text
APPEND UPDATE
-> BUILD DERIVED FEEDS
-> DEPLOY GITHUB PAGES
-> 200 OK
-> PAGE SHOWS NEW SINCE LAST VISIT
-> JASON REVIEWS
-> NEXT WORK CYCLE
```

The page stores only the last-seen update id in the local browser. It does not need ChatGPT memory or Gmail to tell Jason that something changed.

## Public boundary

Never publish:
- private keys or credentials
- bank account numbers
- raw private financial connector payloads
- non-public transaction details
- human identity joins that are not independently proven

Public recommendations are summaries with provenance state, not instructions to trade or spend.
