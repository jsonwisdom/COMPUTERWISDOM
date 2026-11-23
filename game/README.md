# JASON'S GAME 500 — Prototype v0.1
Status: DRAFT / NO PAYMENT / NO WALLET / NO SETTLEMENT.
## Mission
Turn 500 Stripe catalog SKU identifiers (JASON-001 through JASON-500) into a free educational strategy game. Stripe objects remain inactive. This prototype does not access Stripe, authenticate purchases, mint Zora collectibles, pay cash rewards, sign wallet messages, or enable x402.
## Rules
Choose five unique cards. Each contributes 100 points. Each represented role contributes 40 points, five unique roles earns an additional 100 points, and correctly answering the evidence challenge adds 100 points. Roles are synthetic assignments by SKU index modulo 5; they are NOT imported from verified live product metadata. The resulting combinatorial space is Binomial[500,5] = 255,244,687,600 possible unordered five-card teams, as calculated via Wolfram.
## Reproducibility
All rules and selections can be exported locally as a JSON receipt. Receipt is a self-reported gameplay transcript, NOT cryptographically authenticated ownership, score certification, or financial proof. The browser does not persist the team.
## Acceptance checklist
- Cards JASON-001 and JASON-500 appear and can be selected
- A sixth distinct card cannot enter a full team
- Duplicate SKU cannot be added twice
- Five cards covering all five roles score 800 before the question, 900 after correct answer
- A five-card single-role team scores 540 before question
- Filters and search preserve existing selections
- Export contains only game data; no wallet or secret material
- No network fetch, checkout, API credentials, or Stripe mutations
## Next gated iteration
Import source-of-truth SKU/name data from a sanitized public export (never secret keys or private Stripe responses); add deterministic challenge decks, replay validation, optional multiplayer, accessibility tests, abuse controls, and catalog verification. Payment, revenue, and ownership mechanics remain separately gated.
