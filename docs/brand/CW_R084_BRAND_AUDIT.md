# CW-R084 brand audit

Audit date: 2026-11-24. Target: the GitHub Pages homepage in `index.html`, which `.github/workflows/static.yml` publishes from the repository root. This file records what was observed. It does not change DNS, Cloudflare, Vercel, or GitHub Pages settings.

`AUTHORITY_CREATED=false`. Nothing in this audit promotes a deployment or grants authority.

## How this was checked

Repository state is `origin/master` at `16bd292479b40a89e59d73017017bbf71a95ecda` before the homepage edit. Live HTTP was fetched with curl from this environment on 2026-11-24. GitHub Pages configuration was read with `gh api repos/jsonwisdom/COMPUTERWISDOM/pages` (read-only).

Pages API result used below:

- `cname`: `jsonwisdom.com`
- `html_url`: `https://jsonwisdom.com/`
- `source.branch`: `master`
- `source.path`: `/`
- `status`: `built`
- `https_enforced`: true

No `CNAME`, `vercel.json`, `netlify.toml`, `wrangler.toml`, `robots.txt`, or `sitemap.xml` is in the git tree.

## Header

Source: `index.html` (`<header><nav class="wrap" aria-label="Main navigation">`).

Before this change the brand was text only: `COMPUTER` plus a span `WISDOM`, linking to `#home`. Five links follow, in this order: Citizen Root (`#citizen-root`), Work (`#work`), Learning (`#learning`), Verification (`#verification`), About (`#about`).

The header is sticky, background `#071219ed`, bottom border `#28464e`. Nav links use `#abc7c9`. The wordmark uses weight 900 and `0.1em` tracking. The accent half of the wordmark uses `#72e9cf`.

There was no header image.

This branch adds one image inside the existing brand link: `favicon.png` at 40×40 CSS pixels, `alt=""`, with a 10px gap before the unchanged wordmark. The five links, their hrefs, and their order are unchanged.

## Homepage

Source: root `index.html`. Production bytes before this edit matched that file exactly.

- Live URL fetched: `https://jsonwisdom.com/`
- HTTP 200, `content-type: text/html; charset=utf-8`, `server: cloudflare`, response also carried `x-github-request-id`
- Body size 11867 bytes
- SHA-256 `df61ce2d0e58fad2b5748414943ed3ab4bb3cc24aa5511a8dc35598f318bc3fc`
- Same SHA-256 as `index.html` on `16bd2924`

The page is one document: hero, Citizen Root, work cards, learning, verification, YubiKey workdesk entry, about, then the footer. Copy, card order, and the workdesk link `./workdesk/index.html` are unchanged in this branch.

Styles for this page are inline in `index.html`. The homepage does not link `assets/style.css`.

## Footer

Source: `index.html` footer.

Text observed: `COMPUTER WISDOM · JSONWisdom · Build. Seal. Verify. Repeat. · Optional wallet-control message signatures only. No transactions or live payments.`

Color `#abc7c9`, 13px, top border `#28464e`. No logo image. This branch does not add one.

## Mobile layout

Viewport meta, present in the file and in the live body: `width=device-width,initial-scale=1`.

Breakpoints in the same inline stylesheet:

- `max-width: 900px`: hero becomes one column; card grid becomes two columns
- `max-width: 560px`: card grid becomes one column; `.links{display:none}`

At 560px and below the five section links are removed from layout and from the accessibility tree (`display: none`). There is no disclosure control. This branch does not change that rule, because the navigation structure stays as it is. A way to reach those same five links on a narrow viewport is proposed in the spec and is not implemented.

`prefers-reduced-motion: reduce` sets `scroll-behavior: auto`. That rule was already present.

## Social metadata

Before this change, `index.html` had no `og:*` tags and no `twitter:*` tags. Confirmed in the live body (search for `og:` and `twitter:` returned no hits).

This branch adds Open Graph and a Twitter summary card. The image URL is the approved favicon, not a new plate. `twitter:card` is `summary` because the only approved raster is 96×96.

## Search metadata

| Tag or file | Before | This branch |
| --- | --- | --- |
| `<title>` | `Computer Wisdom \| The Puzzle & Jason’s YubiKey Gateway` | unchanged |
| meta description | `Jay Wisdom's public research homepage: artificial intelligence, receipts, cryptographic verification and civic evidence.` | unchanged |
| viewport | present | unchanged |
| canonical | absent | `https://jsonwisdom.com/` |
| meta robots | absent | `index, follow` |
| JSON-LD | absent | one `WebSite` node using that name, URL, description, and favicon URL |
| `robots.txt` in git | absent | still absent |
| `sitemap.xml` in git | absent | still absent |

Title and description strings were copied from the existing elements. The title uses U+2019 in `Jason’s`. The description uses an ASCII apostrophe in `Wisdom's`.

### robots.txt

`GET https://jsonwisdom.com/robots.txt` returned HTTP 200, `text/plain; charset=utf-8`, 1248 bytes. The body is a comment-only content-signal preamble. It has no `User-agent` line and no `Content-Signal` directive. The same URL via `https://jsonwisdom.github.io/COMPUTERWISDOM/robots.txt` is a 301 to `https://jsonwisdom.com/robots.txt`.

That file is not in the git tree. This branch does not add or replace `robots.txt`, so a later Pages deploy from this change will not overwrite it.

### sitemap.xml

`GET https://jsonwisdom.com/sitemap.xml` returned HTTP 503, `text/html`, GitHub's error page, not an XML urlset. No sitemap is implemented here.

### Canonical host

`GET https://jsonwisdom.github.io/COMPUTERWISDOM/` returned HTTP 301, `location: https://jsonwisdom.com/`, `server: GitHub.com`, then HTTP 200 on `https://jsonwisdom.com/`.

`GET https://jsonwisdom.github.io/COMPUTERWISDOM/index.html` likewise 301s to `https://jsonwisdom.com/index.html`.

The canonical tag uses `https://jsonwisdom.com/` because that is the Pages `html_url` and the redirect target. The project path was requested and does resolve, by redirect, to that host.

## Icon path

Approved file: `favicon.png`.

- Git blob: `4f3bb1115af72a4748f089689ed7672b66b5f846`
- Size: 1769 bytes
- PNG 96×96, 4-bit colormap
- First commit: `f660d04957025c76769e3ee62d82864d3b219c40` (2026-11-24 00:17:41 -0600, Jay Wisdom, `jsonwisdom@yahoo.com`)
- Merged in PR #779 as `5571dfe46384543326c6bc1cd8580c09b744b145`

Live fetch of `https://jsonwisdom.com/favicon.png`: HTTP 200, `image/png`, 1769 bytes. Git blob of those bytes is `4f3bb1115af72a4748f089689ed7672b66b5f846`.

`GET https://jsonwisdom.github.io/COMPUTERWISDOM/favicon.png`: HTTP 301 to `https://jsonwisdom.com/favicon.png`, then the same 200 body.

`GET https://jsonwisdom.github.io/favicon.png`: HTTP 404, GitHub Pages "Site not found". The root-absolute `href="/favicon.png"` resolves to that URL only when the document is on the `github.io` host. The live document is not parsed there: GitHub redirects `/COMPUTERWISDOM/` to `https://jsonwisdom.com/` before the HTML is used. On `https://jsonwisdom.com/` the absolute href resolves to the file that returned 200.

This branch still changes the icon href from `/favicon.png` to `favicon.png`. A relative URL resolves to the same file when the homepage is served at the custom-domain root and when it is served under `/COMPUTERWISDOM/`. It does not point at `jsonwisdom.github.io/favicon.png`. No new image bytes were written. The apple-touch icon link uses the same relative file. A 180×180 export was not made.

## Connected surfaces

Read from the repo and, where noted, from one public HTTP request. No settings were changed.

| Surface | Where it appears | Observed HTTP |
| --- | --- | --- |
| `jsonwisdom.com` | Pages `cname` and `html_url`; homepage is served here | 200 homepage and favicon, as above. `server: cloudflare` with a GitHub request id |
| `jsonwisdom.github.io/COMPUTERWISDOM/` | Pages project path; linked from repo docs | 301 to `https://jsonwisdom.com/` |
| `citizen.jsonwisdom.com` | linked from `index.html`; discussed in `docs/CITIZEN_ROOT_AUDIT_2026-11-05.md` | HEAD 200, `text/html`, `server: cloudflare` |
| `wallet.jsonwisdom.com` | `flywheel-connect/base-wallet-policy.v2.json` and Confucius batch docs | HEAD 200, `text/html`, `server: cloudflare` |
| `auth.jsonwisdom.com` | `workdesk/index.html` (`const API`) | HEAD `/` returned 404, `application/json`, `server: cloudflare`. Other paths were not probed |
| `emergency.jsonwisdom.com` | `docs/ooda-emergency/PURPOSE_FUNCTION_JOY_MONITOR_V0_2.md` and the 2026-11-14 reachability receipt | GET `/api/v1/health` 200, JSON, `server: cloudflare` |
| `emergency.jsonwisdom.io` | same docs | GET `/api/v1/health` 200, JSON, `server: cloudflare` |
| `matrix.jsonwisdom.com` | named in `receipts/cloudflare/CW_OODA_EMERGENCY_50STATE_PUBLIC_REACHABILITY_2026-11-14.md` | HEAD `/` 200, `text/html`, `server: cloudflare` |
| `jsonwisdom.io` | named in the Citizen Root audit and in `docs/classes-with-glasses/golden-fleece/index.html` | DNS resolution failed in this environment (`curl` exit 6). UNKNOWN from here |

No Vercel, Netlify, or Cloudflare config file is in this repo. The only Pages workflow is `.github/workflows/static.yml`. It was not edited. CW-R081 artifact naming in that file stays as it is on `16bd2924`.

## Local render of this branch

The branch was served at `http://127.0.0.1:8765/COMPUTERWISDOM/` (repository root mapped under that prefix). This is a local render, not production.

- `GET /COMPUTERWISDOM/` returned 200, 13612 bytes
- `GET /COMPUTERWISDOM/favicon.png` returned 200, 1769 bytes, git blob `4f3bb1115af72a4748f089689ed7672b66b5f846`
- `GET /favicon.png` on that same server returned 404
- The served HTML contains `src="favicon.png"`, `href="favicon.png"`, and `rel="canonical" href="https://jsonwisdom.com/"`, and does not contain `href="/favicon.png"`

Headless Chrome screenshots of that local URL:

- Desktop viewport 1280×900: header shows the favicon mark beside `COMPUTER WISDOM`, and the five existing links (Citizen Root, Work, Learning, Verification, About)
- Mobile viewport 390×844: header shows the same mark and wordmark. The five links are not shown, which matches the existing `max-width: 560px` rule. The hero stacks in one column

Screenshot files are outside the repository: `cw_r084_desktop_1280.png` and `cw_r084_mobile_390.png`.

## What this branch does not change

Navigation labels and hrefs, page copy, workdesk authentication, security-boundary files, workflow files, and deployment config are untouched.

## Acceptance matrix

`IMPLEMENTED` means the branch contains it. `PROPOSED` means the spec states it and this branch does not build it. `PRODUCTION_VERIFIED` means it was fetched live on 2026-11-24. Unmerged edits stay HOLD on production.

| Item | IMPLEMENTED | PROPOSED | PRODUCTION_VERIFIED |
| --- | --- | --- | --- |
| Approved mark `favicon.png` blob `4f3bb1115af72a4748f089689ed7672b66b5f846` | Present, bytes unchanged. No derived file | A larger apple-touch or Open Graph plate, only if produced from these bytes without a redraw | PASS. `https://jsonwisdom.com/favicon.png` is 200 and the git blob matches |
| Header mark | 40×40 image in the existing brand link, wordmark kept | Footer mark | HOLD. Live header is still text only |
| Icon href | Relative `favicon.png` plus apple-touch to the same file | none | Current live tag is `href="/favicon.png"`. That URL 404s on `https://jsonwisdom.github.io/favicon.png` and 200s on `https://jsonwisdom.com/favicon.png`. The new relative href is HOLD until merge |
| Title and description | Unchanged existing strings | none | PASS on the pre-change homepage (hash match). This branch's extra tags are HOLD |
| Viewport | Already present | none | PASS. Live HTML contains `width=device-width,initial-scale=1` |
| Canonical | `https://jsonwisdom.com/` | none | HOLD as a tag. The host relationship is observed: project URL 301s there |
| Meta robots | `index, follow` | Do not replace the live comment-only `robots.txt` | HOLD as a tag. Live `robots.txt` is 200 and is not in git |
| Sitemap | Not added | A sitemap that lists only URLs that already exist | `GET https://jsonwisdom.com/sitemap.xml` returned 503 HTML, not a urlset |
| Open Graph and Twitter | Summary card and `og:*` using the favicon URL | `summary_large_image` when a real large plate exists | HOLD. Live HTML has neither |
| JSON-LD | One `WebSite` node | none | HOLD. Live HTML has none |
| Text contrast | Colors unchanged. Ratios are in the spec; text pairs that were computed pass AA | Raise non-text separation of `#28464e` and `#102630` against `#071219` | Arithmetic only. Not measured with a colorimeter on the live page |
| Focus and reduced motion | Existing `:focus-visible` and `prefers-reduced-motion` rules kept | none | PASS that those rules are in the live stylesheet bytes. Keyboard travel was not filmed |
| Mobile nav links | Still `display: none` at `max-width: 560px` | A disclosure that exposes the same five links | PASS that the live CSS hides `.links` at 560px. Those links are not reachable at 390px. That gap is unchanged |
| Subdomains and deploy files | No config edits | none | See the table above. `jsonwisdom.io` is UNKNOWN here |
| `.github/workflows/static.yml` | Not modified | none | Not redeployed by this unmerged branch |
