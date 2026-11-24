# Computer Wisdom brand spec v1

Status: v1 for the public homepage. This spec describes the mark and the colors, type, and accessibility already in `index.html`, plus the header placement added with this spec. It does not approve a new drawing.

Approved raster, and the only image this spec uses:

| Field | Value |
| --- | --- |
| Path | `favicon.png` |
| Git blob | `4f3bb1115af72a4748f089689ed7672b66b5f846` |
| Size | 1769 bytes |
| Dimensions | 96×96 PNG, 4-bit colormap |
| First commit | `f660d04957025c76769e3ee62d82864d3b219c40` |
| Author date | 2026-11-24 00:17:41 -0600 |
| Author | Jay Wisdom, `jsonwisdom@yahoo.com` |
| Baseline | PR #779, merge `5571dfe46384543326c6bc1cd8580c09b744b145` |

No derived file was produced. Header, favicon, and apple-touch all reference this file. Do not recolor, redraw, crop, or substitute another image.

## Logo placement

The mark sits inside the existing header brand link (`a.brand`, href `#home`), before the wordmark `COMPUTER` / `WISDOM`. The wordmark stays. The five navigation links stay, in the same order, with the same hrefs.

Implemented rules:

- Display size in the header: 40×40 CSS pixels (`width` and `height` 40)
- Gap between the mark and the wordmark: 10px (one quarter of the 40px slot)
- Do not set a CSS width below 24px. The source is 96px; the header slot is 40px
- `alt=""`. The link text `COMPUTERWISDOM` is the accessible name, so the image is not announced a second time
- The footer remains the existing text line. A footer mark is not part of v1

Not implemented:

- A separate apple-touch or Open Graph raster. Both tags point at `favicon.png`. A 180×180 or 1200×630 file would be a new encoding. Do not upscale this 96px file to invent one
- Any placement outside the header brand link

Clear space outside the header slot is the page padding already set by `.wrap` (22px). Do not crowd the mark with a border or a second badge.

## Color

Homepage tokens are the inline custom properties in `index.html`. Hex values below are copied from that file. Favicon palette entries are the PNG `PLTE` colors, counted from the decoded 96×96 image. They are the mark's colors, not a second UI palette.

### UI tokens in `index.html`

| Hex | Role in the file |
| --- | --- |
| `#071219` | `--bg`; page background; header base |
| `#102630` | `--panel` |
| `#28464e` | `--line`; borders |
| `#72e9cf` | `--accent`; links, kickers, focus outline, primary button fill |
| `#ecfaf8` | `--ink`; primary text |
| `#abc7c9` | `--muted`; secondary text, nav links, footer |
| `#17434c` | radial highlight at the top of the page |
| `#3c756e` | gate border |
| `#0d242a` | gate fill (the stylesheet writes `#0d242acc`) |
| `#ffd08a` | `.hold` and `.gate-note` |
| `#05181b` | primary button text |
| `#142c34` | panel gradient start |
| `#0c1e25` | panel gradient end |
| `#0b1d24` | search field background |
| `#071219ed` | sticky header fill (alpha `ed` over the page) |

`color-scheme` is `dark`.

### Mark palette in `favicon.png`

Most-used `PLTE` entries: `#010101`, `#f79829`, `#191c19`, `#f8ed32`, `#e9b746`, `#1e130e`, `#f9bb34`, `#f4df3f`, `#c88a3f`, `#4f3619`. The field is near-black. The disc is gold. Do not remap these to the UI accent.

`theme-color` on the homepage is `#071219`, the existing `--bg`.

## Typography

From the inline stylesheet. No webfont is loaded.

| Use | Specification in `index.html` |
| --- | --- |
| Body | `16px/1.6 system-ui, Segoe UI, sans-serif` |
| Wordmark | weight 900, letter-spacing `0.1em` |
| Kickers, state rows, flow line | `ui-monospace, monospace` (kickers 12px, weight 700, tracking `0.13em`) |
| Heading 1 | `clamp(3.2rem, 7.8vw, 6rem)`, line-height 1.02, tracking `-0.06em` |
| Section headings | `clamp(1.9rem, 4vw, 2.6rem)`, tracking `-0.04em` |
| Footer | 13px |

Do not add a downloadable font in this version.

## Metadata

Homepage only. Values are the existing title and description, the Pages canonical host, and the approved file.

| Tag | Value |
| --- | --- |
| canonical | `https://jsonwisdom.com/` |
| robots | `index, follow` |
| Open Graph type | `website` |
| `og:url` | `https://jsonwisdom.com/` |
| `og:image` | `https://jsonwisdom.com/favicon.png` (96×96, `image/png`, alt `Computer Wisdom`) |
| Twitter card | `summary` |
| JSON-LD | `WebSite` with name `Computer Wisdom`, that URL, the existing description, and that image |
| icon | relative `favicon.png` |
| apple-touch-icon | relative `favicon.png` |

`https://jsonwisdom.github.io/COMPUTERWISDOM/` redirects to `https://jsonwisdom.com/`. The tags use the redirect target. Absolute project-path URLs were fetched and recorded in `docs/brand/CW_R084_BRAND_AUDIT.md`.

`summary_large_image` is not used. The 96px mark is the only approved image.

## Accessibility

Contrast uses the WCAG 2 relative-luminance formula. Channel `c` in 0–255 becomes `c/255`, then `c/12.92` when that is at or below 0.04045, otherwise `((c+0.055)/1.055)^2.4`. Luminance is `0.2126 R + 0.7152 G + 0.0722 B`. The ratio is `(Lighter + 0.05) / (Darker + 0.05)`.

AA thresholds used: 4.5:1 for normal text, 3:1 for large text and for non-text UI boundaries. Ratios are rounded to two decimals. These are calculations on the hex values, not camera readings of a display.

### Text pairs

| Pair | Ratio | Normal text |
| --- | --- | --- |
| `#ecfaf8` on `#071219` | 17.66 | pass |
| `#abc7c9` on `#071219` | 10.58 | pass |
| `#72e9cf` on `#071219` | 12.86 | pass |
| `#72e9cf` on `#102630` | 10.64 | pass |
| `#abc7c9` on `#102630` | 8.75 | pass |
| `#abc7c9` on `#0c1e25` | 9.56 | pass |
| `#abc7c9` on `#142c34` | 8.16 | pass |
| `#ecfaf8` on `#102630` | 14.60 | pass |
| `#05181b` on `#72e9cf` | 12.38 | pass |
| `#ffd08a` on `#071219` | 13.20 | pass |
| `#ffd08a` on `#102630` | 10.91 | pass |
| `#ffd08a` on `#0d242a` | 11.24 | pass |
| `#72e9cf` on `#0d242a` | 10.95 | pass |
| `#abc7c9` on `#0d242a` | 9.01 | pass |
| `#ecfaf8` on `#0b1d24` | 16.12 | pass |
| `#ecfaf8` on header blend `#08151d` | 17.26 | pass |
| `#abc7c9` on `#08151d` | 10.34 | pass |
| `#72e9cf` on `#08151d` | 12.57 | pass |

`#08151d` is `#071219` at alpha `ed` (237/255) composited over the radial `#17434c`. Over the page background the header composite stays `#071219`.

Mark gold on the icon field, not used as UI text: `#f8ed32` on `#010101` is 17.05; `#f79829` on `#010101` is 9.42.

### Non-text

| Pair | Ratio | 3:1 boundary |
| --- | --- | --- |
| `#72e9cf` focus outline on `#071219` | 12.86 | pass |
| `#3c756e` on `#0d242a` | 3.04 | pass |
| `#28464e` on `#071219` | 1.87 | fail |
| `#102630` on `#071219` | 1.21 | fail |
| `#142c34` on `#071219` | 1.30 | fail |
| `#0c1e25` on `#071219` | 1.11 | fail |
| `#17434c` on `#071219` | 1.75 | fail |

The failing rows are borders and panel fills against the page background. Text on those surfaces passes. This version does not change the hex values. A later change can darken the page or lighten `--line` if a 3:1 edge is required. That adjustment is not in this branch.

### Other rules already in the page

- Visible keyboard focus: `a:focus-visible` and `input:focus-visible` use a 3px `#72e9cf` outline with 3px offset
- `prefers-reduced-motion: reduce` turns off smooth scrolling. The mark has no animation
- The project search field has `aria-label="Filter projects"`
- The header nav has `aria-label="Main navigation"`
- The logo image has an empty alt, as specified above

### Not changed, and why

At `max-width: 560px` the stylesheet sets `.links{display:none}`. The five section links are not available on a 390px-wide layout. Restoring them needs a disclosure that shows the same links. That is not in this branch, because the navigation structure stays as published.

## Out of scope for v1

Workflow files, including `.github/workflows/static.yml`. Authentication and the workdesk. Page copy. DNS, Cloudflare, and other hosts. A second logo file.
