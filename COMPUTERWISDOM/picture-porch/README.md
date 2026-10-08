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

## Verification status

- **PASS (local Chromium opaque-origin fallback test):** UI renders; fails closed without IndexedDB; word-picture/JOY question appears; sample phone-number prompt blocked; no JavaScript exceptions; no network requests. See `test_fallback.py` for the standalone test (uses Python Playwright + Chromium).
- **NOT RUN IN A REAL ORIGIN:** IndexedDB persistence across reload; atomic quota under concurrent tabs; download handling; complete prompt-safety/adult review. The controlled test browser blocked HTTP and file navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. The normal-origin Playwright test (`test_picture_porch.py`) is included for a developer to run in an environment permitting localhost browser access.
- **NO LIVE IMAGE PROVIDER:** No external credits are required; no claim of AI image generation.

## Role separation

- COMPUTERWISDOM: implements and reviews the technical studio.
- JOY / Game of Wisdom: provides reflective questions, not execution permission or family approval.
- Jason: retains human decision and approval authority.

No writing to JOY, no public release, no family approval inferred from this PR.