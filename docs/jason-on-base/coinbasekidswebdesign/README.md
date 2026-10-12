# CoinBaseKidsWebDesign — Jay's Satire Scratch Lab

**Status: DRAFT / DESIGN_HOLD / NOT DEPLOYED.** Independent adult-managed educational beta for exploring Jay's public Zora concepts. No Coinbase or Zora endorsement.

## Purpose / Function / Scaled

Purpose: public concept play + private-by-default personal preferences + voluntarily shared human feedback.
Function: six public concepts → unbiased free draw → scratch/reveal → original 3:4 SVG art → like locally → optional JSON export → arithmetic replay.
Scale: ONLY after reproducible source, Node tests, real-browser and accessibility QA, privacy review, and human release authority. No cash, prizes, wagers, lottery ticket sales, purchases, new tokens, or claims of future monetary value.

## Run locally (Node 20+, zero dependencies)

    cd docs/jason-on-base/coinbasekidswebdesign
    npm test
    npm run preview

Then open http://127.0.0.1:8787/

The Node preview binds to localhost and serves only six whitelisted public files. GitHub Pages runs the same static site, not a persistent Node server, and the app does not collect interaction data on a backend.

## Zora concept corridor

Profile: https://zora.co/@jaywisdom — independently fetched HTTP 200, but the public profile alone does not prove identity or wallet control.
Catalog: six links from a historical Jay Zora inventory as of 2026-09-01. It is a curated fixed snapshot, NOT live inventory sync, creator ownership proof, price feed, comprehensive history, or trading service.
The page links to public Zora objects; its SVG art is new, local, original educational parody. No auto-mint, scrape of third-party images, or issuance.

## Wallet corridor

Anonymous play always works. On explicit click only, an injected self-identified Coinbase-style EIP-1193 provider receives the eth_requestAccounts call. The page then reads eth_chainId for display and shows a masked public account. Changes to accounts and chain update the display. Wallet provider metadata is not cryptographically authenticated.

No signing, trades, approvals, transfers, balance/history retrieval, wallet storage or network switching. No wallet address is included in any game receipt. The app has no analytics, cookies, IndexedDB, localStorage, account backend, tracking service or server preference log. External hosting/wallet infrastructure may see ordinary network/origin metadata. Removing the local display does not revoke wallet-side permissions.

Preferences last in memory until the page reloads; export is a user-initiated local download and import is a local deterministic replay, not a cloud backup or authorization record. Wallet address does NOT establish a verified human identity, family membership, builder status, or right to private files. The app is adult-managed; minors do not need wallet access.

## Wolfram reproducibility

Six choices; 2^32=4,294,967,296 random words; rejection-sampling threshold=4,294,967,292; four top words rejected. For genuinely uniform Uint32 words, each concept has exact probability 1/6. Expected draws=1.000000000931...; no actual cash or prize. Browser Web Crypto supplies random numbers. Receipt includes accepted numeric word for replay, but does NOT independently attest to random-source honesty. Original SVG card output is deterministic under the archived concept schema. Node tests and a scoped PR audit verify the public logic; real-device QA stays HOLD.

## Seymour / feedback / zero-day puppy

Three reveals unlock a public Seymour toolbox hint. This is discoverability, NOT an access-control gate. Public Seymour case organizer remains accessible without a wallet. Private family storage is entirely outside public code and requires independent, actual authentication.

Builder can copy a local feedback note and choose to open GitHub issues. No review request is automatically sent to Coinbase Support, and no external team or response is guaranteed. Private security disclosures should not go into public GitHub issues. The puppy button is manual advisory only: it does not scan, identify a zero-day, notify a maintainer or act autonomously.

AI=INSTRUMENT; HUMAN=DECISION; AUTHORITY_CREATED=FALSE.

## Release gates

FREE_PLAY=TRUE; PAID_LOTTERY=FALSE; REAL_CASH_VALUE=0; WALLET_OPTIONAL=TRUE;
CENTRAL_PREFERENCE_LOG=FALSE; PRIVATE_FAMILY_RECORDS_EXCLUDED=TRUE;
FINANCIAL_EXECUTION=FALSE; AUTOMATIC_ALERTS=FALSE;
PRODUCTION_RELEASE=HOLD; REAL_DEVICE_QA=HOLD.
