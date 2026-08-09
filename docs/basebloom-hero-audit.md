# basebloomdesign.com hero — audit and routes to 9+

## ⚠ Session handoff — read first

**The only thing to execute in the current session is committing this file to
the repo** (as `docs/basebloom-hero-audit.md`). This container is ephemeral —
`/root/.claude/plans/` is destroyed when it is reclaimed, and the next session
starts from a fresh clone. If this file is not committed, the audit is lost.

**Blocked precondition.** `basebloomdesign.com` is denied by this
environment's egress policy — the local proxy is healthy, but the policy
gateway answers `403` to `CONNECT` (`kind: connect_rejected`, host
`basebloomdesign.com:443`). This is not fixable in-session; per
`/root/.ccr/README.md`, policy denials must be reported, not routed around.

To unblock, in the **WebDesign - Sandbox** environment
(`env_01CQZGVk5hndUNGgMjDkhV8x`) on claude.ai: add `basebloomdesign.com` to
the network allowlist, then **start a new session** — proxy config is fixed at
container boot, so an existing session cannot pick up the change.
Docs: https://code.claude.com/docs/en/claude-code-on-the-web

**First three steps in the new session:**
1. Confirm access: `curl -sSI https://basebloomdesign.com/` returns 200, not
   `CONNECT tunnel failed`.
2. Pull the hero's HTML/CSS/JS and resolve the checks marked *unverified*
   below — these are what convert the three provisional scores into real ones:
   reduced-motion handling, focus visibility, `aria`/focusability on the
   decorative video, heading order, the real LCP element, and the mobile
   `<source>` selection behind the empty `src`.
3. Re-run the contrast sampler (method in **Verification**) so post-change
   scores are measured the same way as this baseline.

**Fallback if the allowlist doesn't land:** the GitHub Actions bridge works
today — runners have open internet, and it is how every measurement in this
document was captured. Documented as "route 3 — egress-locked environments" in
`.claude/skills/bloom/references/pipeline.md`.

## Context

The live BaseBloom hero scored 8.3 overall in an informal comparison. The ask
is a real audit across 8 dimensions with **distinct routes** to lift every one
to ≥9. Deliverable is a **spec only** — BaseBloom's site is a separate
codebase, so no application code in this repo changes. (The one write is
committing this document itself, per the handoff above.) Latitude: **hold the brand** (green
`#16b364`, tan `#c38d50`, the name and voice); **everything else is open** —
display face, layout, footage, scrim, motion, signature element.

### Evidence base, and its limits

Measured from two real captures (desktop 1440×900, mobile 390×844) taken in a
real Google Chrome on a GitHub runner, plus a runtime probe of the live DOM.

Contrast was sampled from the actual PNGs (8% darkest vs 8% lightest pixels
per region, WCAG relative luminance):

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

**Everything passes WCAG AA.** This corrects an earlier eyeball claim that the
eyebrow was a low-contrast weak spot — it is not.

Runtime probe: fonts are Prata 400, Inter 400/600, JetBrains Mono 400/500;
`hosts: ["basebloomdesign.com"]` — **zero third-party requests, everything
already self-hosted**. Desktop video `trades-hero-loop.mp4`, 1920×1080,
6.13 s, `readyState 4`, playing. **Mobile `<video>` has an empty `src`,
`readyState 0`, never plays**, yet imagery still renders (poster or CSS
background).

### Artifacts committed alongside this document

- `basebloom-hero-audit/baseline-desktop.webp`, `baseline-mobile.webp` — the
  captures the table above was measured from. **Visual reference only.** They
  are lossy; re-running the sampler against them returns a worst-case of
  5.09:1 versus 5.54:1 on the source PNG, because WebP shifts the luminance
  extremes the method keys on. Always re-measure from a fresh PNG capture.
- `basebloom-hero-audit/contrast-sampler.mjs` — the exact script that produced
  the table. `node contrast-sampler.mjs <image.png> [desktop|mobile]`; exits
  non-zero if any region falls below AA. Region boxes are in DPR-2 pixels and
  will need adjusting if the layout moves.

Three limits to state plainly:
1. Contrast is measured on **one frame each** (desktop t≈2.63 s, frame mean
   luma 114.2). On a video hero, contrast is a *distribution*, not a value.
2. No source access → reduced-motion handling, focus states, `aria` on the
   video, and real LCP are **unverified**, not assumed absent.
3. Scores for Accessibility, Performance and Mobile parity are provisional
   pending the source checks listed under each.

---

## Scorecard

| # | Dimension | Now | Gap |
|---|---|---|---|
| 1 | Typography | 8.5 | 0.5 |
| 2 | Composition | 8.0 | 1.0 |
| 3 | Legibility | 8.5 | 0.5 |
| 4 | Hierarchy & conversion | 9.0 | hold |
| 5 | Distinctiveness | 7.0 | **2.0** |
| 6 | Accessibility | 7.5* | 1.5 |
| 7 | Performance / LCP | 7.0* | 2.0 |
| 8 | Mobile parity | 5.5* | **3.5** |

\* provisional — see limits above.

---

## 1 · Typography — 8.5 → 9

**Evidence.** Prata carries eyebrow, h1 and trust bullets; Inter carries
subcopy, phone, buttons, nav. The white/green h1 split is the signature move
and it works. Three defects: **Prata ships one weight (400 only)**, so there
is no bold inside the serif and all hierarchy must come from size alone;
**Prata is used at ~14–15 px for the trust bullets**, which is the worst
possible use of a Didone-adjacent face — hairlines thin out and apertures
close; **JetBrains Mono 400 + 500 is downloaded but appears nowhere in the
hero**.

**The 9 bar.** Every face earns its download, no face is used below its
optical floor, and the serif can express hierarchy without relying on size.

**Route A — Retire Prata from small sizes (surgical, lowest risk).** Keep
Prata for h1 only. Move eyebrow and trust bullets to Inter: eyebrow at
600/12px/0.16em tracking/uppercase, bullets at 400/15px. Drop JetBrains Mono
from the hero's font payload entirely (load it on the routes that use it).
Net: one serif doing one job at one size, at the size it was drawn for.

**Route B — Swap Prata for a multi-weight display serif (systemic).**
Replace with a face that has real weight range and holds up small —
Fraunces (variable, with `SOFT`/`WONK` axes), Newsreader, or Source Serif 4.
Buys a 600 for the green h1 line against a 400 white line, which strengthens
the split-color device with weight as well as hue. Costs a brand-recognition
reset on the display face.

**Route C — Variable-font consolidation (performance-flavoured).** Collapse
to two variable families: one display, one text. One woff2 per family covers
every weight, so hierarchy becomes free and the payload shrinks despite more
weights being available.

**Pick: A, then B if the display face is genuinely up for debate.** A is
half a day and removes all three defects. B raises the ceiling but resets
recognition.

**Acceptance.** No face rendered below 16 px except Inter; zero font files
downloaded that render no glyphs in the hero viewport; h1 hierarchy legible
in greyscale.

---

## 2 · Composition — 8.0 → 9

**Evidence.** Left-aligned text column (~40% width) against the roofer on the
right — genuine figure/ground. Three defects: a **large dead zone bottom-left**
below the trust bullets (roughly 20% of hero height carrying nothing); the
**subcopy→phone interval is the loosest in the stack** and breaks the vertical
rhythm; the green h1 line runs right and **collides with the roof pipe** behind
it. The centred `scroll ↓` cue is also off-axis against a left-aligned column.

**The 9 bar.** Every region of the frame is doing work, the vertical rhythm is
a deliberate scale, and no text overlaps a busy region of footage.

**Route A — Tighten the stack and fill the void.** Reduce the subcopy→phone
gap to the same interval as h1→subcopy, pull the whole block down to optical
centre, and move the trust bullets into the reclaimed bottom-left as a 2×2
grid. Left-align the scroll cue to the text column. Purely CSS.

**Route B — Re-frame the footage, not the layout.** Regrade/reposition the
video so the subject sits further right and lower, opening a clean dark plane
under the text column; use `object-position` per breakpoint. Fixes the pipe
collision without touching the type stack.

**Route C — Split the hero into a two-column grid.** Text column left at a
fixed measure, and let the right column hold a small proof element — a live
demo thumbnail, a "5 days" counter, a mini before/after. Converts dead space
into evidence and feeds Distinctiveness too.

**Pick: A + C.** A is cheap and fixes rhythm; C converts the dead zone into
persuasion rather than just filling it. B is a good adjunct if the pipe
collision survives A.

**Acceptance.** No empty region >12% of hero area; vertical gaps drawn from a
4-step scale; h1 bounding box overlaps no footage region whose local contrast
variance exceeds a set threshold.

---

## 3 · Legibility — 8.5 → 9

**Evidence.** All AA on the sampled frames (table above). The real exposure is
**variance**: a flat-ish scrim over 147 frames means the measured 5.54:1 on the
green button is a sample, not a floor. The mobile trust bullets already read
dimmer (6.94:1 vs 15.83:1 desktop).

**The 9 bar.** The *worst* frame in the loop passes AA, and the primary
headline passes AAA.

**Route A — Bottom-weighted gradient scrim (highest value per line of CSS).**
Replace the flat tint with `linear-gradient(to bottom, rgba(8,20,12,.35) 0%,
rgba(8,20,12,.72) 55%, rgba(8,20,12,.88) 100%)`, protecting the text zone
while letting the upper footage stay bright. Costs nothing, lifts the floor
everywhere.

**Route B — Grade the source video.** Bake a slight S-curve and a −15%
luminance lift into the darker third of the footage at encode time, so the
page needs less scrim. Preserves footage vibrancy; requires a re-encode.

**Route C — Per-frame adaptive scrim.** Sample mean luma of the text region
each rAF and interpolate scrim opacity. Technically elegant, guarantees a
floor, but adds JS to the critical path — hard to justify over A.

**Pick: A, verified by Route D below.**

**Route D — the measurement that proves it (do this regardless).** Extract all
147 frames, composite the actual text colors over each at the proposed scrim,
and compute the contrast distribution. Report the **minimum**, not the mean.
This is the only way to claim a 9 honestly.

**Acceptance.** Min contrast across all frames ≥4.5:1 for every text element;
≥7:1 for the h1.

---

## 4 · Hierarchy & conversion — 9.0 → hold, harden to 9.5

**Evidence.** Already the strongest dimension: eyebrow → headline → concrete
promise → phone → two differentiated CTAs → four trust bullets → scroll cue.
`(229) 938-6924 — ask for David, the lead developer` is the best single
element on the page. **"No ranking promises"** differentiates by *refusing* a
claim competitors make — genuinely confident.

**The 9.5 bar.** The two CTAs are visually ranked, and the promise is
falsifiable on its face.

**Route A — Rank the CTAs.** Currently tan and green sit at near-equal
weight, which splits intent. Make "See a free demo of your site" the solid
primary and demote "▶ View live work" to a ghost/outline button.

**Route B — Make the promise checkable.** "Live in five days" is strong;
"live in five days — see 27 sites we've already shipped" is checkable, and
links the claim to the gallery already in the nav.

**Pick: A.** B only if the gallery count is accurate and current.

**Acceptance.** Five-second test: ≥80% of testers name the primary action
correctly, unprompted.

---

## 5 · Distinctiveness — 7.0 → 9  ← biggest gap

**Evidence.** Dark full-bleed video + letterspaced eyebrow + oversized serif +
two CTAs is a well-worn premium template. What *is* distinctive: the
split-color headline, the green, the named human, "No ranking promises".

**The strategic defect.** The hero shows **the customer's job, not
BaseBloom's craft**. It's roofing b-roll — the same footage any trades-adjacent
agency could run. The product being sold is *a website built from your photos
in five days*, and none of that transformation appears above the fold.

**The 9 bar.** A visitor who saw the hero for two seconds with the logo
removed could still name what the company does — and could not confuse it
with a roofing company or a generic agency.

**Route A — Dramatize the transformation (strongest, on-brand).** Make the
signature element a **Google Business listing morphing into a live site**:
the drab listing card assembles into a full BaseBloom page as the user
scrolls or as a 4-second loop. Directly visualizes the promise, is impossible
to confuse with a roofing company, and reuses assets they already own (their
27 demos). Keeps footage as a background layer behind it.

**Route B — The "five days" device.** Make the number the hero. A large
typographic countdown — DAY 1 … DAY 5 — with each state showing the site
further along, driven by scroll. Owns a number instead of an image, cheap to
build, very hard to copy convincingly.

**Route C — Split-screen: their photos → your site.** Left half the trade's
own phone photos, right half the finished page, with a moving wipe between
them. Simplest to produce; the least novel of the three.

**Route D — Lean all the way into the wordmark.** The `blooms` green already
does the heavy lifting; extend it into a real botanical/growth motif that
animates on load. Pure brand expression, no product demonstration — lifts
memorability but not comprehension.

**Pick: A, with B as the fallback if demo assets aren't cleanly capturable.**
Both satisfy the logo-removed test; C and D do not, on their own.

**Acceptance.** Logo-removed test with 10 people from the target segment: ≥8
correctly describe the business. Also re-run the anti-default check — the
current hero would fail it.

---

## 6 · Accessibility — 7.5 (provisional) → 9

**Evidence.** Contrast passes AA everywhere measured. `h1` exists with correct
text. Unverified without source: reduced-motion, focus visibility, video
`aria`/focusability, heading order, touch-target sizes.

**The 9 bar.** AA everywhere with AAA on the headline, motion respected,
keyboard path clean, decorative media hidden from AT.

**Route A — The compliance sweep (do first, cheap).**
- `@media (prefers-reduced-motion: reduce)` → pause the loop, show the poster.
  An autoplaying looping video with no such guard is the single most likely
  live violation.
- `aria-hidden="true"` + `tabindex="-1"` on the decorative video.
- Visible focus ring on both CTAs, the phone link and every nav item, ≥3:1
  against its background.
- Confirm the eyebrow is not a heading element (it reads as one visually).
- Phone as `<a href="tel:...">`; verify the mobile `☎ Call` dingbat has an
  accessible name, not a symbol read aloud.

**Route B — Push the headline to AAA.** Green h1 line is 6.13:1. Lightening
the green toward `#3ddc84` on the headline only (keeping `#16b364` for
buttons and accents) clears 7:1 without touching brand usage elsewhere.

**Route C — Independent audit.** Run axe-core and the Vercel Web Interface
Guidelines pass against the live URL for the checks static screenshots cannot
reach.

**Pick: A + B + C.** They're complementary, not alternatives.

**Acceptance.** axe-core: zero violations in the hero subtree; all text AA,
h1 AAA; full keyboard traversal with visible focus at every stop; reduced-
motion honoured.

---

## 7 · Performance / LCP — 7.0 (provisional) → 9

**Evidence.** Strong start: everything same-origin, nothing third-party. Two
concrete costs: **JetBrains Mono 400 + 500 downloaded but rendering no hero
glyphs**, and a **1920×1080 autoplay video** served to every viewport.

**The 9 bar.** LCP <2.0 s on a throttled 4G mid-tier phone, zero unused bytes
on the critical path, CLS ≈ 0.

**Route A — Trim the critical path.** Drop JetBrains Mono from the hero
bundle; `<link rel="preload">` only the Prata and Inter subsets the hero
actually paints; subset the latin range; ensure `font-display: swap`.

**Route B — Right-size the video.** Serve 1280×720 below 768 px and 1080p
above via `<source media>`; add a VP9/WebM sibling ahead of the H.264 (a
tuned VP9 came out ~14% smaller than H.264 at SSIM 0.998 on comparable
footage in this repo); `preload="metadata"`, real `poster`.

**Route C — Make the poster the LCP element.** Ship a sharp, well-compressed
poster as the LCP paint and start the video only after `load`. Decouples the
perceived hero entirely from video weight — the biggest single win if LCP is
currently video-bound.

**Pick: A + B + C.** A is free, B halves mobile bytes, C fixes LCP at the
root.

**Acceptance.** Lighthouse mobile ≥95 performance; LCP <2.0 s throttled; zero
unused font bytes; CLS <0.02.

---

## 8 · Mobile parity — 5.5 (provisional) → 9  ← largest gap after Distinctiveness

**Evidence.** Three defects, one of them possibly a bug:
1. **The `<video>` has an empty `src` and never plays** (`readyState 0`,
   `duration 0`). Imagery still renders, so a poster or CSS background is
   filling in. Deliberate data-saving or a broken source selection — **this
   must be established first**; the two have opposite fixes.
2. **The h1 wraps to four lines** — "We build the / base." / "Your business /
   blooms." — stranding `base.` alone and destroying the two-line white/green
   rhythm that is the hero's signature device.
3. Trust bullets wrap awkwardly in their 2-col grid ("Live in 5 days from
   your / photos", "You own the site & / domain"); CTA buttons are unequal
   widths; no scroll cue.

**The 9 bar.** Mobile is a first-class composition, not a reflow — the
signature device survives, and any motion difference is a stated choice.

**Route A — Fix the wrap with a mobile-specific measure.** Set an explicit
`max-width` in `ch` and use `text-wrap: balance` (or explicit `<br>` at the
chosen breakpoint) so it lands 2+2. Fix bullets with
`grid-template-columns: 1fr` below 480 px and equalise CTA widths to 100%.

**Route B — Author a distinct mobile hero.** Shorter headline for small
screens ("Your business blooms." alone), poster instead of video by design,
single CTA with the phone promoted. Treats mobile as its own composition
rather than a squeeze.

**Route C — Resolve the video question explicitly.** If deliberate: keep it,
document it, ship a high-quality poster and drop the empty `<video>` element
entirely so it isn't dead weight in the DOM. If a bug: add a `<source
media="(max-width: 768px)">` pointing at a 720p encode.

**Pick: C first (it's possibly a defect), then A.** B if mobile is the
majority of traffic — likely for a local-trades audience arriving from Google
Business listings, which is worth checking in analytics before deciding.

**Acceptance.** h1 renders exactly two visual lines at 320/390/430 px; no
orphaned words in bullets; motion behaviour identical across viewports or
documented as an explicit choice; the mobile hero passes the same
logo-removed test as desktop.

---

## Sequencing

Cheap and high-certainty first, creative swing once the base is solid.

1. **Wave 1 — free wins, no design risk.** Typography A, Composition A,
   Legibility A, Hierarchy A, Performance A, Mobile A+C. Mostly CSS and
   build config; should land ~1–2 days.
2. **Wave 2 — verification.** Legibility D (per-frame contrast
   distribution), Accessibility A+B+C, Performance B+C. This is what converts
   "looks fine" into a defensible 9.
3. **Wave 3 — the swing.** Distinctiveness A (or B), plus Composition C,
   which shares the same surface. Scope separately; it's a redesign of the
   hero's central idea, not a tweak.

## Verification

No change is claimed as a 9 without a measurement:

- **Contrast** — extract all 147 frames, composite the real text colors at the
  proposed scrim, report the **minimum** ratio per element (not the mean).
- **Accessibility** — axe-core over the hero subtree; keyboard traversal
  recorded; reduced-motion toggled and confirmed.
- **Performance** — Lighthouse mobile, throttled 4G, three runs, median
  reported; verify zero unused font bytes in the coverage panel.
- **Mobile** — screenshot at 320 / 390 / 430 px and confirm the h1 wraps to
  exactly two lines at each.
- **Distinctiveness** — logo-removed comprehension test, 10 people in the
  target segment, ≥8 correct.
- **Hierarchy** — five-second test for primary-action recall.

Re-capture desktop and mobile through a real Chrome after each wave (the
Actions-bridge approach used to produce this audit's evidence) and re-run the
contrast sampler, so each score movement is backed by the same measurement
that established the baseline.
