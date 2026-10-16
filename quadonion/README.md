# QuadOnionAudit Proof Events — DESIGN / DRAFT IMPLEMENTATION

**NO SCHEDULES.** Event changes, not clock ticks, trigger this work.

State: `GATE_001_EXECUTION=HOLD`, `DEPLOYMENT_HOLD`. PR branch only; no human acceptance, publishing, external-source crawling, deployed MaryDeeBot dispatcher, bot-to-bot call, JOY activation, mint, or TriggerDeck canon.

## Triggers and loop

1. A new source receipt, source-byte change, recorded contradiction, failed check, replay mismatch or reviewer receipt is added to a **bounded repository case**. A PR/push event is a transport notification; the receipt's validity remains unverified by this harness.
2. On a matching PR change or approved master change, GitHub Actions checks the synthetic invariant tests and replays the metadata. **No GitHub schedule / cron is declared.**
3. MaryDeeBot's **purpose/coordination seat** assigns rotating analytic review seats Leanne -> LeahPrime -> BoxDee -> Supreme Seymour -> Leanne, with Boss Brenda as independent privacy/consent checkpoint.
4. Every event creates a review metadata receipt, explicit next disconfirming questions, and at most **3** numbered 3:4 **artwork concept candidates**. These are not images or TriggerDeck IDs. No woman, family member, or institutional subject is asserted guilty, identified from an image, or portrayed as verified based on metadata alone.
5. **Only new, independently sourced event input** qualifies for a new audit pass. The questions are output hypotheses, not verified evidence or permission for infinite self-triggering. Repeated event IDs with matching receipts dedupe; conflicting receipts sharing an ID produce CONFLICT/HOLD.
6. On no material new receipt, the process stops without mint, release, publication, JOY deployment or bot fan-out.

Input location: `quadonion/cases/*.json`; output: runner-local `quadonion-review.json` artifact (7-day retention). A workflow run is a **machine execution receipt for its own scoped computations**, not proof that URLs were fetched or persons independently verified.

Sample case is clearly `SYNTHETIC_WOMEN_RECORDS_001`, with **zero genuine sources and zero evidence events**. It represents the women's public-accountability audit lane only; no factual claims about women have been sourced, audited or accepted yet. Add public-source receipts and contrary-source records per factual claim after a privacy/legal review, not scraped private material or identity speculation.

**MaryDeeBot actual runtime is separate:** JOY's `.github/workflows/marydeebot-school-questions.yml` only checks school question chapters and may write a bounded status to JOY. This prototype **does not invoke or grant privileges to that bot**. The MARYDEE purpose charter sets authority/execution/verification to false.

## Zero-trust statements

- URL_COUNT != WITNESS_COUNT; SOURCE_OBSERVATION_COUNT may equal DECLARED_ORIGIN_COUNT without authenticating origin.
- HASH_MATCH != CONTENT_TRUTH; DECLARED_DIGEST != HASH_RECOMPUTED_FROM_EXTERNAL_BYTES.
- ART_CANDIDATE != ART_RENDERED; 3:4 declared dimensions != geometry proof of a rendered PNG.
- BOT_SEAT != HUMAN; REVIEWER_ROLE != REAL_BOT_INVOCATION.
- AUTO_TEST_PASS != HISTORICAL_FACT_VERIFIED != APPROVAL.
- FAIL/HOLD cannot be promoted by any machine metadata output.
- `publication_enabled=false`; `joy_deployment_enabled=false`; `authority_created=false`; `final_release_authority=Jason`.

## Not yet implemented — explicitly HOLD

Persistent durable append-only queue and acknowledged record prefix; evidence transport webhook that authenticates source bytes; independently checked cryptographic signatures and signer authorization; verified independent witness graph; Gate 001 crash/restart and retry-failure assertions; durable artifacts beyond 7 days; live bot task acknowledgment/role dispatch; ongoing external public source acquisition; source-backed women-focused case verification; safe image rendering/production QC.

A passing PR action after this branch is opened validates only the **synthetic code test harness and metadata processing**. No Gate 001 state transition.
