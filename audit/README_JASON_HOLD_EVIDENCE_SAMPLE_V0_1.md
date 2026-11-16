# JASON Denominator — scoped HOLD autopsy v0.1

**Mode:** bounded, evidence-source-linked, read-only. **Authority created:** false. **Audit verdict:** automatic from verified observations; no human approval is required for an audit verdict.

This is **14 selected cases**, not all HOLDs in JASON's multi-repo history, BNS, ENS, DNS, PowerShell, voice, or ChatGPT history. A `HOLD` workflow gate is distinct from a claim-level `PASS`, `FAIL`, or `UNKNOWN`.

## How to run (only after these files actually exist in your checkout)

```powershell
Test-Path .\scripts\jason_hold_tally.py
Test-Path .\audit\JASON_HOLD_EVIDENCE_SAMPLE_V0_1.json
python .\scripts\jason_hold_tally.py .\audit\JASON_HOLD_EVIDENCE_SAMPLE_V0_1.json
python -m unittest discover -s tests -p test_jason_hold_tally.py
```

No token, network connection, GitHub CLI, or new software dependency beyond Python is required. The script prints a tally, does not write files, and never changes Git, identity, finances, or source authority. If a path does not exist, fix the working directory before executing.

## Bounded findings from 14 selected cases

| Reason family | Selected cases |
| --- | ---: |
| Missing source/coverage | 4 |
| Environment/authentication/access | 3 |
| Identity/custody proof | 3 |
| Delivery and continuity | 2 |
| Governance process | 1 |
| Replay validation | 1 |
| **Total** | **14** |

Source labels: exactly 3 `HOLD`, 4 `BLOCKED`, 7 other statuses in the selected evidence. In this *new remediation registry* the workflow gate is HOLD for all 14 until their own test succeeds. Four are protective controls that must not be removed merely to make a dashboard green. Ten are repair candidates.

**Crucial limits:** The case facts and declared claim verdicts came from dated inspected records; executing the tally does **not** refetch those sources, certify that each case remains current, prove the origin of a missing artifact, or prove all of Jason's original research was recovered. The script calls its counts `declared_evidence_verdict_counts` to prevent a category promotion.

## Architectural diagnosis and repair order

1. **PERSON-FIRST ROOT:** The existing Supreme Seymour flywheel is a public-repository HEAD observer. It is not wired to original JASON voice/chat inputs, and the 500-date JSON does not contain 500 daily audits. Restore original records and prior-day joins before claims of recursive learning.
2. **PATH PREFLIGHT:** Never present `powershell -File` commands without checking that the file was actually downloaded and its path exists. Prefer a direct read-only inline probe.
3. **DURABLE RECEIPTS:** The September 23 workflow uploaded an artifact with configured 30-day retention; November 3 API listed none. Preserve upload PASS, retrieval UNKNOWN, and cause UNKNOWN separately. Build durable opt-in operator-facing delivery, not a success badge.
4. **AUTH / RULE MISCONFIGURATION:** Preserve distinction between a GitHub credential-precedence problem, a required-check name mismatch, and failed code. Recheck live current state before patching rules.
5. **PROTECTIVE BOUNDARIES:** Keep privacy, real asset-control/ownership, payment authorization, and primary-source hashing gates. These are not arbitrary AI obstacles.
6. **AUTO AUDIT VERDICTS:** Report source-supported PASS/FAIL/UNKNOWN without human audit-signoff. Keep deployment, payment, signing, and private publication as separately authorized actions.

**This draft repair is not a production release.** Nothing is merged or deployed by the tally; history remains untouched.
