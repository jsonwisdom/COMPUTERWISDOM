# Picture Porch — Browser Acceptance Receipt · 2026-10-08 V0.1

**Provenance:** This is a repository mirror of observed GitHub Actions results, not the runner's immutable artifact itself. It reports synthetic browser tests only; it is **not family, legal, privacy or consent approval**.

## Directory-first binding

- Repository: `jsonwisdom/COMPUTERWISDOM`
- Directory: `COMPUTERWISDOM/picture-porch/`
- PR: [#645](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/645), **draft / unmerged** when this receipt was prepared
- Tested exact head SHA: `61019571dc16222c6394c390eed4c94352cb7c5b`
- Workflow: `.github/workflows/picture-porch-acceptance.yml`
- Actual workflow run: [37771984179](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/37771984179)
- Actual job: [113293536181](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/37771984179/job/113293536181)
- Synthetic logs and receipt artifact: [11547517859](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/37771984179/artifacts/11547517859)
- Observed receipt time (UTC): `2026-10-08T11:44:30.525846+00:00`
- Status: GitHub Actions job **success**; both browser test steps **success**

## Exact-source evidence

| Object | Algorithm | Value |
|---|---|---|
| `index.html` committed bytes | SHA-256 | `853da020c2f4befa1674f37234b81c9ba3fa316884bc083d759a97aa0700a087` |
| `index.html` Git blob | Git SHA-1 blob identifier | `8f89e5a605522abda190838f6772bd53e133487d` |
| `test_fallback.py` | SHA-256 | `d3cf0eda3757a06da9bc1f6231cfbb9e50551c5ba31f8f9fcf44a7302db12292` |
| `test_picture_porch.py` | SHA-256 | `a61444a3a0bb2acdd042bbbef3a8b5c5944873e64c6edda3a6aecbedf5a95da2` |

The original local HTML export with terminal LF has a different SHA-256; it is **not** this tested file. The source code itself was not modified during the CI/receipt stages.

## Observable browser results (synthetic prompts only)

```text
PASS: exact committed HTML bytes
PASS: renders UI in opaque-origin browser
PASS: fails closed when IndexedDB unavailable
PASS: word-picture fallback + JOY question works unsaved
PASS: basic contact-details guard blocks sample
PASS: no JS errors, no network requests in fallback
INIT: 0 of 8; local store ready
WORD: word picture stored; TXT download content verified; no count used
RELOAD: shelf persists; counter still 0 of 8
PAINT: painting saved; PNG download content verified; count 1
GUARD: contact-details prompt blocked
CAP: seven paintings saved, one slot remains
MULTI_TAB: both attempted at 7/8; one succeeded; one denied; total 8
RELOAD: count and shelf persist; no JS errors; no external requests
```

Runner JSON: `technical_acceptance=PASS`, `family_review=HOLD`, `merge=HOLD`, `deployment=HOLD`, `authority_created=false`. Prior CI runs `37771322345` and `37771665594` failed on test defects; **they are preserved as failures** and were not rewritten into a PASS.

## Limits and human decision

- This result proves only the assertions exercised in this Chromium run. It is not an exhaustive privacy audit, age-appropriate content moderation check, independent security audit, consent receipt, or assurance across all browsers/devices.
- The current regex guard is incomplete, IndexedDB is browser-profile-local and not encrypted, and the device clock/storage can bypass the painting cap; the cap is **not security-grade**.
- No child-produced prompts, personal child data or family communications are in this receipt.
- The independent adult/family review checklist is `FAMILY_PRIVACY_CONSENT_REVIEW_V0_1.md`; it is not approved.
- **MERGE = HOLD; DEPLOY = HOLD; FAMILY/PRIVACY/CONSENT = HOLD.** Jason retains separate human release authority.
- This mirror is added after the tested head; it does **not** retroactively claim the later documentation-only commit was the exact tested commit. The Actions workflow should run again on the final branch head.

**COMPUTERWISDOM builds. JOY teaches. Jason decides.**
