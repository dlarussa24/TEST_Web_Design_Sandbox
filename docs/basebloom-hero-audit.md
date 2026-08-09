# basebloomdesign.com hero — audit and routes to 9+

**Status: source-verified.** The domain was allowlisted mid-audit, so every
score below is measured against the live HTML, CSS and JS rather than inferred
from screenshots. Nothing here is provisional any more.

## Context

An audit of the live BaseBloom hero across 8 dimensions, with **distinct
routes** to lift each to ≥9. Deliverable is a **spec only** — BaseBloom's site
is a separate codebase, so no application code in this repo changes. Latitude:
**hold the brand** (green `#16b364`, tan `#c38d50`, the name and voice);
**everything else is open** — display face, layout, footage, scrim, motion,
signature element.

## Corrections to the first pass

Source access killed four findings from the screenshot-only version. Recording
them because a wrong finding acted on is worse than no finding:

| First-pass claim | Reality |
|---|---|
| "The eyebrow is a low-contrast weak spot" | **False.** 5.64:1 desktop, 6.13:1 mobile — passes AA. |
| "An autoplaying loop with no reduced-motion guard is the most likely violation" | **False.** Five `prefers-reduced-motion` blocks; `.hero-bg{display:none}` under reduce, and the JS gate checks it too. |
| "Add `aria-hidden` to the decorative video" | **Already done**, in the markup as shipped. |
| "The mobile video has an empty `src` — possibly a bug" | **Deliberate and well built.** Gated on `min-width:721px` **and** not-reduced-motion **and** `navigator.connection.saveData`, with retry handling for Low Power Mode `play()` rejection. Respecting Save-Data is better than most production sites manage. |
| "Make the poster the LCP element" (Perf route C) | **Actively wrong.** LCP is already the `<h1>` text at 1080 ms desktop / 428 ms throttled. Promoting a 180 KB JPEG to LCP would make it worse. |

Three scores moved up as a result: Accessibility 7.5→8.5, Performance 7.0→8.5,
Mobile parity 5.5→7.5.

## Evidence

**Contrast** — sampled from real-Chrome captures, mean of the darkest 8% of
pixels against the lightest 8% per region, WCAG relative luminance:

| Element | Desktop | Mobile |
|---|---|---|
| nav links | 14.21:1 | — |
| eyebrow | 5.64:1 | 6.13:1 |
| h1 white line | 13.61:1 | 16.19:1 |
| h1 green line | 6.13:1 | 6.81:1 |
| subcopy | 15.14:1 | 15.97:1 |
| phone | 16.66:1 | 16.01:1 |
| tan button | 5.56:1 | 5.38:1 |
| green button | 5.54:1 | 5.64:1 |
| trust bullets | 15.83:1 | 6.94:1 |

Every element passes AA on both viewports.

**Runtime** — measured on a clean network with real Google Chrome (a MITM
proxy in the path would distort timings, so the local session was the wrong
instrument):

| | desktop, unthrottled | mobile, 4G + 4× CPU |
|---|---|---|
| LCP | **1080 ms** — element is `<h1>` | **428 ms** — element is `<h1>` |
| FCP | 1080 ms | 428 ms |
| CLS | **0** | **0.0531** |
| Transfer | 2 603 KB | 551 KB |
| Video attached | yes | **no** (by design) |

Desktop paid a cold CDN miss and mobile hit a warm edge, so the two LCP figures
are not directly comparable — both are nonetheless excellent.

**Assets** — `trades-hero-loop.mp4` 1 904 269 B (the source comment says "6MB";
it is 1.9 MB), `trades-hero-poster.jpg` 184 509 B, `prata-400.woff2` 19 224 B,
`inter-400.woff2` 48 256 B, `jetbrains-mono-400.woff2` 31 432 B,
`ambient-drift.js` 9 136 B.

**Fonts fetched on load, both viewports:** prata-400, inter-400, inter-600,
jetbrains-mono-400, jetbrains-mono-500. Space Grotesk 500/600/700 are declared
but never fetched — confirming fetch-on-use, and that the JetBrains Mono pair
genuinely is pulled during initial load.

### Artifacts

- `basebloom-hero-audit/baseline-{desktop,mobile}.webp` — the captures the
  contrast table was measured from. **Visual reference only**; WebP is lossy
  and shifts the extremes the method keys on (5.09:1 vs 5.54:1 worst case).
  Always re-measure from a fresh PNG.
- `basebloom-hero-audit/contrast-sampler.mjs` — the script that produced the
  table. `node contrast-sampler.mjs <image.png> [desktop|mobile]`, exits
  non-zero if any region falls below AA.

**The one limit that remains:** contrast is measured on a single frame per
viewport. On a video hero, contrast is a *distribution* across 147 frames, not
a value. See Legibility route D.

---

## Scorecard

| # | Dimension | Now | Gap |
|---|---|---|---|
| 1 | Typography | 8.5 | 0.5 |
| 2 | Composition | 8.0 | 1.0 |
| 3 | Legibility | 8.5 | 0.5 |
| 4 | Hierarchy & conversion | 9.0 | hold |
| 5 | Distinctiveness | 7.0 | **2.0** |
| 6 | Accessibility | 8.5 | 0.5 |
| 7 | Performance / LCP | 8.5 | 0.5 |
| 8 | Mobile parity | 7.5 | 1.5 |

Overall **8.2**. The work is concentrated in two places: Distinctiveness, and
mobile's broken headline.

---

## 1 · Typography — 8.5 → 9

**Verified.** `.kicker{font-family:"Prata";font-size:.8rem}` — **12.8 px**,
dropping to `.72rem` (**11.5 px**) under 720 px. `.trust` is also Prata. This
is worse than the screenshot suggested: a Didone-adjacent face with fine
hairlines set at 11.5 px over moving footage. Prata ships **one weight (400)**,
so hierarchy inside the serif can only come from size. JetBrains Mono 400 + 500
(31 KB + ~30 KB) are fetched on load but paint only `.mcycle`, `.mstatic` and
`.gcard .gnum` — all below the fold, on both viewports.

**The 9 bar.** Every face earns its download, no face is set below its optical
floor, and the serif expresses hierarchy without relying on size alone.

- **Route A — retire Prata from small sizes.** Prata for the h1 only. Kicker
  and trust bullets to Inter (kicker 600 / 12 px / 0.16em / uppercase, bullets
  400 / 15 px). Lazy-load the JetBrains Mono pair on intersection with the
  gallery rather than at document load.
- **Route B — swap to a multi-weight display serif.** Fraunces (variable,
  `SOFT`/`WONK`), Newsreader or Source Serif 4. Buys a 600 for the green line
  against a 400 white line, strengthening the split-colour device with weight
  as well as hue. Costs recognition on the display face.
- **Route C — variable-font consolidation.** Two variable families, one woff2
  each. Hierarchy becomes free and total payload drops despite more weights.

**Pick: A.** Half a day, removes all three defects, keeps Prata's equity where
it earns its keep.

**Acceptance.** No face below 16 px except Inter. No font file fetched before
first paint that paints no glyph above the fold. H1 hierarchy legible in
greyscale.

---

## 2 · Composition — 8.0 → 9

**Evidence.** Left-aligned column at roughly 40% width against the roofer —
genuine figure/ground. Three defects: a **dead zone bottom-left** carrying
nothing across roughly 20% of hero height; the **subcopy→phone interval is the
loosest in the stack**, breaking vertical rhythm; and the green h1 line
**collides with the roof pipe** behind it. The centred `scroll ↓` cue is
off-axis against a left-aligned column.

**The 9 bar.** Every region of the frame does work, vertical rhythm follows a
deliberate scale, and no text sits over a busy region of footage.

- **Route A — tighten the stack, fill the void.** Match subcopy→phone to the
  h1→subcopy interval, pull the block to optical centre, move the trust bullets
  into the reclaimed bottom-left as a 2×2 grid, left-align the scroll cue.
  Pure CSS.
- **Route B — re-frame the footage.** Reposition so the subject sits further
  right and lower, opening a clean dark plane under the text, via
  per-breakpoint `object-position`. Fixes the pipe collision without touching
  the type stack.
- **Route C — two-column grid with a proof element.** Text left at a fixed
  measure; the right column holds a demo thumbnail, a five-day counter, or a
  mini before/after. Converts dead space into evidence and feeds
  Distinctiveness.

**Pick: A + C.** A fixes rhythm cheaply; C converts the dead zone into
persuasion rather than merely filling it.

**Acceptance.** No empty region above 12% of hero area. Gaps drawn from a
four-step scale. H1 bounding box clear of high-variance footage regions.

---

## 3 · Legibility — 8.5 → 9

**Evidence.** All AA on the sampled frames. The exposure is **variance**: the
measured 5.54:1 on the green button is one sample from 147 frames, not a floor.

**The 9 bar.** The *worst* frame in the loop passes AA, and the headline passes
AAA.

- **Route A — bottom-weighted gradient scrim.** Replace the flat tint with
  `linear-gradient(to bottom, rgba(8,20,12,.35), rgba(8,20,12,.72) 55%,
  rgba(8,20,12,.88))` — protects the text zone while the upper footage stays
  bright. Highest value per line of CSS on the page.
- **Route B — grade the source video.** Bake an S-curve and a −15% luminance
  lift into the darker third at encode time so less scrim is needed. Preserves
  vibrancy; requires a re-encode.
- **Route C — per-frame adaptive scrim.** Sample text-region luma each rAF and
  interpolate opacity. Guarantees a floor but adds JS to the critical path —
  hard to justify over A.
- **Route D — measure the distribution. Do this regardless.** Extract all 147
  frames, composite real text colours at the proposed scrim, report the
  **minimum**. Without D there is no defensible claim, only a better-looking
  guess.

**Pick: A, proven by D.**

**Acceptance.** Minimum across all frames ≥ 4.5:1 every element, ≥ 7:1 the h1.

---

## 4 · Hierarchy & conversion — 9.0 → hold, harden to 9.5

**Evidence.** The strongest dimension. Eyebrow → headline → concrete promise →
phone → two CTAs → four trust bullets → scroll cue, every element earning its
slot. `<a class="hero-tel" href="tel:+12299386924">(229) 938-6924 <small>ask
for David, the lead developer</small></a>` is the best element on the page — a
named human, correctly marked up as a `tel:` link. **"No ranking promises"**
differentiates by *refusing* a claim competitors make.

- **Route A — rank the CTAs.** Tan and green sit at near-equal weight,
  splitting intent. Make "See a free demo of your site" the solid primary and
  demote "▶ View live work" to a ghost outline.
- **Route B — make the promise checkable.** "Live in five days — see the sites
  we've already shipped", linking to the gallery already in the nav. Only if
  the count is accurate.

**Pick: A.**

**Acceptance.** Five-second test: ≥ 80% name the primary action unprompted.

---

## 5 · Distinctiveness — 7.0 → 9  ← the real work

**Evidence.** Dark full-bleed video, letterspaced eyebrow, oversized serif, two
CTAs — a well-worn premium template. What *is* distinctive: the split-colour
headline, the green, the named human, "No ranking promises".

**The strategic defect.** The hero shows **the customer's job, not BaseBloom's
craft**. It is roofing b-roll — footage any trades-adjacent agency could run.
The product is *a website built from your photos in five days*, and none of
that transformation appears above the fold.

**The 9 bar.** A visitor who saw the hero for two seconds with the logo removed
could still name what the company does, and could not mistake it for a roofing
company or a generic agency.

- **Route A — dramatize the transformation.** Make the signature element a
  Google Business listing morphing into a live site: the drab listing card
  assembling into a finished page, on scroll or as a four-second loop.
  Visualizes the promise directly, cannot be confused with a roofing company,
  and reuses demos they already own. Footage stays as a background layer.
- **Route B — the "five days" device.** Make the number the hero. A typographic
  DAY 1 … DAY 5 progression, each state showing the site further along, driven
  by scroll. Owns a number rather than an image; hard to copy convincingly.
- **Route C — split-screen: their photos → your site.** Simplest to produce,
  least novel.
- **Route D — lean into the wordmark.** Extend the green "blooms" into a
  botanical growth motif. Lifts memorability but not comprehension.

**Pick: A**, with B as fallback if demo assets aren't cleanly capturable. Both
satisfy the logo-removed test; C and D do not, on their own.

**Acceptance.** Logo-removed test, 10 people in the target segment, ≥ 8
correctly describe the business.

---

## 6 · Accessibility — 8.5 → 9

**Verified as strong.** `prefers-reduced-motion` handled in five places
including `.hero-bg{display:none}`; the video carries `aria-hidden="true"`,
`muted`, `playsinline`, `preload="none"` and a real poster; heading order is
clean (1×h1, 5×h2, 14×h3, no skips); the eyebrow is a `<span>`, not a fake
heading; the phone is a proper `tel:` link; all text passes AA.

**The one real gap: focus visibility.** The stylesheet contains
`:focus-visible` **zero times** and exactly one `:focus` rule —
`.capture input:focus, .capture select:focus` on a form below the fold. The
hero's phone link, both CTAs, every nav item and all ten gallery cards fall
back to the UA default ring, which on custom-filled buttons over video is
frequently invisible.

- **Route A — add a focus system.** One rule:
  `:where(a,button,summary,[tabindex]):focus-visible{outline:2px solid
  var(--bloom);outline-offset:3px;border-radius:6px}`. Use `:where()` so it
  carries zero specificity and cannot fight component styles. Verify the ring
  clears 3:1 against both the dark nav and the tan button.
- **Route B — push the headline to AAA.** The green h1 line is 6.13:1.
  Lightening toward `#3ddc84` **on the headline only**, keeping `#16b364` for
  buttons and accents, clears 7:1 without disturbing brand usage.
- **Route C — independent audit.** axe-core plus a Web Interface Guidelines
  pass for what neither screenshots nor source reading reach.

**Pick: A + B.** A is the actual defect; B is what converts a strong pass into
a 9. C confirms.

**Acceptance.** axe-core zero violations in the hero subtree. Every focusable
element shows a ≥3:1 ring. H1 at AAA.

---

## 7 · Performance / LCP — 8.5 → 9

**Verified as strong, and better than the first pass assumed.** LCP is the
`<h1>` — **1080 ms** desktop cold, **428 ms** on throttled 4G with 4× CPU.
Desktop CLS is **0**. Everything is same-origin; `preload="none"` on the video;
Prata 400 and Inter 400 preloaded; `font-display: swap` throughout.

Three real costs remain:

1. **Desktop transfer 2 603 KB**, almost all of it the 1.9 MB H.264 loop.
2. **JetBrains Mono 400 + 500 fetched on load on both viewports**, painting
   only below-fold content — worst on mobile, where the loop is deliberately
   skipped to save bytes and then ~60 KB of mono is fetched anyway.
3. **Mobile CLS 0.0531** against 0 on desktop. Under the 0.1 "good" threshold,
   but it is a mobile-only shift and worth finding — most likely the Prata/Inter
   swap reflowing a headline that is already wrapping to four lines.

- **Route A — stop fetching mono before the fold.** Load the JetBrains Mono
  pair on IntersectionObserver against the gallery. Removes ~60 KB from every
  initial load, mobile especially.
- **Route B — right-size the video.** A VP9/WebM sibling ahead of the H.264
  (a tuned VP9 came out 14% smaller at SSIM 0.998 on this exact file), and a
  720p encode for the 721–1024 px band that currently gets full 1080p.
- **Route C — chase the mobile CLS to zero.** Reserve the headline's box with
  `min-height` at the mobile breakpoint, or add `size-adjust`/`ascent-override`
  to the Prata `@font-face` so the fallback metrics match. Fixing the four-line
  wrap (Mobile route A) may resolve it outright — measure after that lands.

**Pick: A + C**, with B when the encode is convenient. Note that **route C from
the first pass — "make the poster the LCP element" — is withdrawn**: LCP is
already text, and promoting a 180 KB JPEG would regress it.

**Acceptance.** LCP under 2.0 s throttled (already met — hold it). CLS under
0.02 on both viewports. Zero font bytes fetched before first paint that paint
nothing above the fold.

---

## 8 · Mobile parity — 7.5 → 9

**The video is not a defect.** Source comment: *"The source is attached by JS
on wide viewports only. A phone on cell data gets the poster and never requests
the loop."* Gated on `min-width:721px` **and** not-reduced-motion **and**
`navigator.connection.saveData`, with `canplay` / `pointerdown` /
`visibilitychange` retries for Low Power Mode rejection. This is careful work;
the only nit is that the comment says 6 MB where the file is 1.9 MB.

**The real defect is the headline.** `.hero h1{font-size:clamp(2.6rem, 5.5vw,
4.1rem)}`, and the `max-width:720px` block adjusts the kicker and trust bullets
but **never touches the h1**. So at 390 px it floors at **41.6 px** inside a
342 px column. Measured character widths: "We build the base." needs ≤ ~38 px
and "Your business blooms." ≤ ~32.6 px to hold one line each. The result is a
four-line wrap that strands `base.` alone and destroys the two-line white/green
split that *is* the hero's signature device.

Secondary: trust bullets wrap awkwardly in their `1fr 1fr` grid, CTA widths are
unequal, and there is no scroll cue.

- **Route A — fix the clamp at the mobile breakpoint.** Inside
  `@media(max-width:720px)`, set `.hero h1{font-size:clamp(2rem, 8.2vw,
  2.6rem)}` — 32 px at 390 px, 26 px at 320 px, 35 px at 430 px, all inside the
  measured budget. Add `text-wrap: balance`. Bullets to
  `grid-template-columns:1fr` below 480 px; CTAs to `width:100%`.
- **Route B — author a distinct mobile hero.** Shorter headline for small
  screens ("Your business blooms." alone), poster by design, single CTA with
  the phone promoted. Treats mobile as its own composition rather than a
  squeeze.
- **Route C — keep and document the video gate.** It is correct; add it to the
  design notes so a future refactor does not "fix" it. Optionally drop the
  stated 6 MB to the real 1.9 MB.

**Pick: A**, then C for the record. B only if analytics show mobile is the
majority — likely for a local-trades audience arriving from Google Business
listings, so worth checking before deciding.

**Acceptance.** H1 renders exactly two visual lines at 320, 390 and 430 px. No
orphaned words in bullets. Mobile CLS under 0.02. The video gate documented.

---

## Sequencing

1. **Wave 1 — cheap, no design risk.** Typography A, Composition A, Legibility
   A, Hierarchy A, Accessibility A+B, Performance A, Mobile A+C. Mostly CSS;
   roughly one to two days. This alone takes six of eight dimensions to 9.
2. **Wave 2 — verification.** Legibility D (per-frame contrast distribution),
   Accessibility C, Performance C re-measured after the Mobile A fix.
3. **Wave 3 — the swing.** Distinctiveness A (or B) with Composition C, which
   shares the same surface. Scope separately: it is a redesign of the hero's
   central idea, not a tweak.

## Verification

No score is claimed without a measurement:

- **Contrast** — all 147 frames, real text colours at the proposed scrim,
  report the **minimum** per element, never the mean.
- **Accessibility** — axe-core over the hero subtree; keyboard traversal
  recorded; reduced-motion toggled and confirmed.
- **Performance** — real Chrome on a clean network (not through the agent
  proxy, which distorts timings); 4G + 4× CPU; three runs, median reported.
- **Mobile** — capture at 320, 390 and 430 px; the h1 must be exactly two
  visual lines at each.
- **Distinctiveness** — logo-removed comprehension test, 10 people, ≥ 8 correct.
- **Hierarchy** — five-second test for primary-action recall.
