# WikiAdam Nook v0.1 — JASON as Playwright

**Find the origin. Prove the path. Preserve the person.**

A **person-first provenance auditor** and a separate **Wikipedia first-link browser game**. These tools must never be confused.

## Two modes

1. **Conceptual navigation:** `wikipedia_first_link.py` runs a bounded Playwright Chromium walk through the first eligible English Wikipedia article link in the body prose. It skips parenthetical, italic, footnote, navigation, external and non-article links. It records cycle/no-link/timeout outcomes; it never assumes all paths reach Philosophy. Browser content is mutable and a DOM version change can change the chosen path. Results are **dated public navigation observations**, not proof of concept truth or a fresh estimate of a claimed 97%.
2. **JASON provenance:** `provenance.py` loads a declared, private, versioned graph and independently hashes local evidence files. Edges have exact typed relationships, evidence refs, declared review status and contradictions. It computes a policy-qualified path only if *every* contributing edge has reviewed evidence whose bytes hash-match. That is **not** independent proof that a source's historical claim is true.

## Exact grammatical boundaries

| Requested relationship | Allowed edge-type sequence |
| --- | --- |
| `AUTHORED_BY` | `authored_by` |
| `PROPOSED_BY` | `proposed_by` |
| `IMPLEMENTED_BY` | `implemented_by` |
| `DISCUSSED_BY` | `discussed_by` |
| `DERIVED_FROM_PERSON_WORK` | `derived_from → authored_by` or `derived_from → proposed_by` |

**Not allowed:** `discussed_by → AUTHORED_BY`; `derived_from → authored_by` interpreted as *new derivative authored by JASON*; `attributed_by → AUTHORED_BY`; or an UNKNOWN source being assigned a person.

## Denominator and metrics

`JASON` is the person-first research anchor, not a forced graph attractor. The metric denominator is the number of enumerated, deduplicated candidate IDs in one declared time/scope/policy. `0/0` becomes JSON `null` and `coverage_undefined=true`. A reported value of 1/1 does not show global research completeness, which stays UNKNOWN.

No human approval is required for the **computational audit verdict**. Human authorization remains relevant to private publication, account actions, deployment, payment or signing.

## Local use — read-only

Python 3.12 or newer is recommended. No repository write is needed to run the graph tool:

```powershell
# From the checked-out branch's repository root:
Test-Path .\projects\wikiadam\provenance.py
python .\projects\wikiadam\provenance.py .\private-manifest.json --source-root .\private-evidence
# Counts-only result for sharing:
python .\projects\wikiadam\provenance.py .\private-manifest.json --source-root .\private-evidence --public-summary
```

**Never commit your private manifest or source files.** A synthetic manifest needs `schema: WIKIADAM_PROVENANCE_V0_1`, `denominator: JASON`, `scope` with `id`, `snapshot`, `policy: WIKIADAM_POLICY_V0_1`, `candidate_ids`, `population_completeness: UNKNOWN`; empty `candidates`; typed `edges`; and `evidence` entries with local `relative_path`, `sha256`, `source_locator`, and `review_state`. The test file `tests/test_provenance.py` creates a synthetic manifest and source.

For public Wikipedia browsing (optional, explicit opt-in):

```powershell
python -m pip install playwright==1.56.0
python -m playwright install chromium
python .\projects\wikiadam\wikipedia_first_link.py --start "Alan Turing" --max-hops 12 --delay-seconds 2 --live
# Or: --random instead of --start
```

No login, CAPTCHA bypass, paywall bypass, rate-limit evasion, unrestricted domain traversal, or unbounded scraping. URLs are restricted to public English Wikipedia articles. Playwright documentation: https://playwright.dev/python/docs/locators

## Verification

```text
python -m unittest discover -s projects/wikiadam/tests -p "test_*.py" -v
```

The CI workflow independently runs Python-only logic tests on Windows and Linux and installs Chromium on Linux for DOM-fixture tests. **No live Wikipedia crawl, private source reads, or history claims occur in CI.** The repository is unchanged unless a human separately merges the draft PR.

## Evidence limits and recovery

- A hash authenticates *bytes against a recorded digest*, not who created them.
- An edge marked REVIEWED is a declaration supplied by the manifest; the software does not independently adjudicate the reviewer.
- If source bytes are missing, the output identifies a recovery action and the affected path remains UNKNOWN.
- If contradictory claims are recorded, the relevant claim is DISPUTED, not silently promoted.
- Source URLs and rendered HTML digests from Playwright do not establish a durable Wikipedia revision or permanent graph structure.
- The private source corpus, historic JASON_OS kernel, ENS/BNS/DNS identity bindings, original audio/chat exports, and global invention catalog remain **UNKNOWN** until replayed against their actual records.

**This is a v0.1 candidate implementation, not a theorem or a declaration of independent historical authorship.**
