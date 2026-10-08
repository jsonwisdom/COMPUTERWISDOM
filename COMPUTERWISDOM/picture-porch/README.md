# Picture Porch v0.1 — COMPUTERWISDOM × JOY

**Status: DRAFT / not deployed / not family-approved.** This is a standalone, local-first **procedural cartoon studio**, not an AI image generator and not the previously claimed (unlocated) builder source. It is a **new implementation** under COMPUTERWISDOM. The JOY placeholder `joyspace/jayspace-pictures.html` remains unchanged.

## Why this exists

Picture Porch is a private creative experience: imagine something kind and funny → paint an on-device cartoon or make a word picture → keep it in the browser's local Shelf → get one JOY/Game of Wisdom question. No accounts, wallets, public posting, analytics, or image-provider credits.

## Use it

Open `index.html` in a modern browser. For reliable storage behavior, **serve it from localhost** instead of relying on how the browser treats `file://` origins:

```sh
cd COMPUTERWISDOM/picture-porch
python -m http.server 8765 --bind 127.0.0.1
# open http://127.0.0.1:8765/
```

The local web server serves the file to this device only; no cloud host is needed. The project is **not automatically deployed** by this PR. It also needs an independent family/privacy review before use by children.

## Boundaries and limitations

- Art uses the local Canvas 2D API (cartoon-like shapes). It **does not** synthesize arbitrary images using a remote AI. The prompt influences subject and props, but not every detail.
- The Shelf and daily quota share one IndexedDB transaction. Up to eight **saved paintings per local-calendar day**; word pictures are not counted. Deleting a painting does not refund the day's painting count. The device clock or clearing local browser data can reset the quota, so this is not a robust child-access security control.
- If IndexedDB is unavailable, paintings are disabled rather than claiming they are safely saved. Word pictures are still usable and downloadable, but are **explicitly marked unsaved**.
- The word check catches **some** harmful language and some identifiers, but is incomplete; parent/guardian supervision is required. The app intentionally does not store JOY reflection answers.
- The HTML has a restrictive CSP (`connect-src 'none'`) and no external script, image, font, API, wallet, analytics, or publish action. The *code* can be public; children should not put private details into it. Browser-local data is not encrypted or password-protected, and is visible to anyone using that browser profile.
- Source code is not deployment, test output is not child-safety certification, and a Git blob SHA is not a SHA-256 content digest. Preserve no-fake-green.

## Running the verification suite

Install Playwright and its managed Chromium once (portable across Linux, macOS, and Windows):

```sh
pip install playwright
python -m playwright install chromium
```

Then, from `COMPUTERWISDOM/picture-porch/`:

```sh
# Opaque-origin / storage-unavailable smoke test (no local server required)
python test_fallback.py

# Normal-origin acceptance suite (local HTTP server started by the script)
python test_picture_porch.py
```

Both scripts use Playwright-managed Chromium. There is no hard-coded OS browser path.

### What the normal-origin suite checks

- Shelf persistence after page reload
- Daily painting cap (8 saved paintings; word pictures do not count)
- Two-tab last-slot contention: both tabs observe **7 of 8**, both issue an attempted eighth painting, exactly one succeeds, the other receives quota rejection; each tab reloads with **8 of 8** and the expected Shelf size. This test is not verified until actually run.
- PNG download content (valid PNG signature + non-trivial size)
- TXT download content (word-picture text present)
- Contact-details guard sample
- No external network requests; no uncaught JavaScript errors

### Observed results (after Option D test correction)

| Check | Result |
|-------|--------|
| Fallback (opaque-origin) browser test | **PASS** (re-run confirmed) |
| Normal-origin suite | **HOLD** — a local earlier-suite attempt using system Chromium reached localhost navigation and was blocked by `ERR_BLOCKED_BY_ADMINISTRATOR`; this newly corrected test version was not executed |
| Committed `index.html` byte SHA-256 | **VERIFIED:** `853da020c2f4befa1674f37234b81c9ba3fa316884bc083d759a97aa0700a087` |
| Local HTML export vs committed `index.html` | **DIFFERENT BY ONE FINAL LF:** export `ba6c71cd7172165e63e3e3203da896e1c3c06dba2bd2078eb80c043be9d104d1` (with LF); committed file has no final LF |
| JOY placeholder | **UNCHANGED** |

A code change or successful CI workflow that does **not** execute the browser suite does **not** convert a blocked or un-run check into PASS.

## Option D test correction and family-review gate (2026-10-08)

- Corrected `test_picture_porch.py` to prepare **seven** saved paintings, open two tabs while both buttons are enabled, schedule competing save attempts for the last slot, assert **exactly one success and one quota-denial**, then reload both tabs to prove **eight total**. No disabled-button click masquerades as a race.
- Static review and independent adult/family decision checklist: [FAMILY_PRIVACY_CONSENT_REVIEW_V0_1.md](FAMILY_PRIVACY_CONSENT_REVIEW_V0_1.md). A prepared checklist is **not** parental consent or family approval.
- Environment preflight: Python Playwright and system Chromium present; Playwright-managed Chromium missing at `/home/oai/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome`. An older normal-origin attempt using system Chromium failed at `page.goto` with `net::ERR_BLOCKED_BY_ADMINISTRATOR` before the app loaded.
- **DO NOT** promote: this corrected concurrency test has not produced a runtime receipt. Storage persistence, quota, download acceptance, and child/family safety remain **HOLD**. Run the corrected suite with managed Chromium from an environment permitting localhost navigation and attach full stdout/stderr with test source commit and timestamp. GitHub CI for unrelated workflows is not acceptance evidence.
- No wallet, child-generated content, private family details, or child consent claims are added to this source-only draft PR. No JOY mutation, merge or deployment.

## Exact-byte provenance correction (2026-10-08)

The earlier PR receipt incorrectly labeled the local exported HTML SHA-256 as the SHA-256 of the committed `index.html`. The text matched but the bytes did not: GitHub's `index.html` has **no terminal LF**. The unchanged Git blob is `8f89e5a605522abda190838f6772bd53e133487d`, and its content SHA-256 is `853da020c2f4befa1674f37234b81c9ba3fa316884bc083d759a97aa0700a087`. The local exported HTML includes one terminal LF, producing `ba6c71cd7172165e63e3e3203da896e1c3c06dba2bd2078eb80c043be9d104d1`. The earlier **MATCH to committed bytes** claim is withdrawn. Neither `index.html` nor child-facing behavior was changed by this documentation correction.

## Verification status

- **PASS (local Chromium opaque-origin fallback test):** UI renders; fails closed without IndexedDB; word-picture/JOY question appears; sample phone-number prompt blocked; no JavaScript exceptions; no network requests. See `test_fallback.py`.
- **HOLD (normal-origin runtime):** IndexedDB persistence across reload, concurrent-tab quota, download handling, and full eighth/ninth-paint behaviour require a real-origin browser run. The controlled test environment previously blocked HTTP/file navigation. The suite in `test_picture_porch.py` is ready for any developer environment that permits localhost browser access.
- **HOLD (family / privacy / consent review):** Independent adult review is required before any child-facing use. The text guard is incomplete and is not a safety certification.
- **NO LIVE IMAGE PROVIDER:** No external credits are required; no claim of AI image generation.

## Role separation

- COMPUTERWISDOM: implements and reviews the technical studio.
- JOY / Game of Wisdom: provides reflective questions, not execution permission or family approval.
- Jason: retains human decision and approval authority.

No writing to JOY, no public release, no family approval inferred from this PR.
