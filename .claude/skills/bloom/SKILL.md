---
name: bloom
description: Generate a luxury scroll-driven "3D bloom" landing page for ANY named object using Higgsfield AI generation, orchestrating the other installed design skills across its phases. A cinematic two-act 4K hero — act one awakens the object as the visitor scrolls, act two erupts into a climax and settles to rest exactly at the body handoff — while the object's "signature medium" (fire for a volcano Pokémon, flowing tequila for a reposado, dust and light for a workshop) drifts as an ambient particle field through the rest of the page. The design system is sampled from the object itself. Use whenever the user invokes /bloom followed by an object name (append --max for the full multi-skill pipeline), or asks for a "bloom page", "3D bloom", "scroll-driven landing page", "deconstruction page", "exploded-view site", or a Higgsfield-generated scroll experience for a product, drink, building, vehicle, creature, instrument, or any physical object — even if they don't say "bloom" explicitly.
---

# Bloom — object-driven scroll-story landing pages

Turn any named object into a cinematic landing page: `/bloom vintage Leica M6`,
`/bloom Casamigos Reposado`, `/bloom Typhlosion using Sacred Fire`.

The finished page tells a story in one continuous scroll: the hero holds a
photoreal render of the object in a dark void, and scrolling drives a
**two-act film**, frame by frame — Act 1 opens/awakens the object (a watch
blooms apart, a fire ignites ring by ring, a wave of tequila gathers), and
Act 2 delivers the climax and settles it to rest (the fire crashes down and
the creature lands on its feet; the liquid arcs down and fills a glass to a
standing pour). The final frame lands exactly at the hero-to-body handoff.
Below the hero, the object's **signature medium** — embers, droplets, dust —
drifts through every section as an ambient particle field, so the story never
stops. Everything (palette, gradients, borders, glow, cursor, particles) is
derived from the object's own materials.

Proven end to end on "The Meridian Estate" (house/roofing) and "Typhlosion —
The Sacred Fire Awakens" (creature/energy). Read
`references/source-prompts.md` for the parameterized prompt templates and
worked medium examples.

## Workflow at a glance

1. **Understand the object** — niche, materials, layers, **signature medium**
2. **Generate Act 1** — still → climax-state still → video → review → 4K + 9:16
3. **Generate Act 2** — continuation anchored on Act 1's true last frame
4. **Extract frames** — both acts, both orientations, 24 fps
5. **Sample the design system** — scripts/sample_palette.mjs
6. **Build the page** — assets/template.html, all slots + MEDIUM config
7. **Verify in a real browser** — scripts/verify_page.mjs + eyeball the joints
8. **Deliver** — page + screenshots; commit; deploy if a site is linked

## Orchestration — bloom conducts, the other skills play

Bloom owns the pipeline and the final page. The other installed design skills
are **consultants bound to specific phases**: invoke them where the table says,
take what serves the object, and discard advice that fights the proven
mechanics below. Bloom's rules always win a conflict — no consultant may add a
`<video>` element, a scroll event listener, a navbar, a footer, a cookie
banner, lorem ipsum, or text dimmer than `#888888` on dark.

### Two tiers

| Invocation | Consults |
|---|---|
| `/bloom <object>` | **Default.** Phases 1, 5, 7 only — direction, palette validation, compliance audit. Fast, cheap, and already produces the proven page. |
| `/bloom <object> --max` | **Full pipeline.** Everything in the default plus the phase-6 build consults (entry sequence, GSAP motion layer) and the phase-7 double audit. Use when the page is the deliverable and polish is worth the extra passes. |

If the user names a skill explicitly (`/bloom Leica M6 --max, skip gsap`),
their instruction overrides this table.

### The map

| Phase | Consult | For exactly this |
|---|---|---|
| 1 — Understand | `frontend-design` | The design thesis before any asset is generated: a named point of view for this object, one aesthetic risk you can justify, and the anti-default check (bloom's dark-void-plus-single-warm-accent look is itself becoming a default — make the direction specific to *this* object). |
| 1 — Understand | `ui-ux-pro-max` | Candidate font pairings and motion presets to choose the display/body voice from. Query it for options; you pick. |
| 5 — Design system | `ui-ux-pro-max` | Validate the palette `sample_palette.mjs` derived — contrast on dark, and whether the accent/secondary pair has a named precedent — and lock the display/body pair shortlisted in phase 1. The sampled hexes stay authoritative; this is a check, not a replacement. |
| 6 — Build (`--max`) | `premium-frontend-ui` | The **entry sequence** — the one real gap in the current pages: a preloader that resolves the first frames and fonts, then reveals, so the visitor never sees the blank gradient beat while WebPs decode. Also its hero-architecture patterns (split headline spans, depth layering). Ignore its navigation section — bloom has no navbar. |
| 6 — Build (`--max`) | `gsap-plugins` + `gsap-timeline` | SplitText letter-cascade on the h1 and one orchestrated reveal timeline for the hero copy, sequenced against the entry sequence. Layered *on top of* the frame scrubber, never replacing it. |
| 6 — Build (`--max`) | `gsap-utils` | `mapRange` / `clamp` for the scroll→frame-index math and the act-joint crossfade, in place of hand-rolled arithmetic. |
| 6 — Build (`--max`) | `gsap-performance` | 60fps discipline on everything added: transform/opacity only, `will-change` applied and removed, no layout reads inside the rAF loop. |
| 7 — Verify | `web-design-guidelines` | Compliance pass against the external Vercel standard — focus states, contrast, reduced motion, semantics. Fix what it reports. |
| 7 — Verify (`--max`) | `impeccable polish <page>` | **One bounded round**, invoked with the explicit sub-command on the built page. Batch desktop + mobile, fix what it surfaces, stop. Do not let it redesign the visual world bloom just derived from the object. |

### Deliberately not consulted

- `gsap-scrolltrigger` — would duplicate or replace the proven rAF +
  `getBoundingClientRect` scrubber. GSAP layers on top of the scrub; it never
  becomes the scrub.
- `gsap-react`, `gsap-frameworks` — bloom emits a standalone vanilla page.
- `gsap-core` — reached transitively through timeline/plugins; no separate
  consult needed.

## Phase 1 — Understand the object

Consult `frontend-design` for the thesis and `ui-ux-pro-max` for type/motion
candidates (see Orchestration). Then decide four things (a sentence each):

- **Niche & voice**: who loves this object? A reposado page seduces; a watch
  page whispers heritage; a Pokémon page reads like a trainer's field notes.
- **Materials**: the 3–5 surfaces that define it — they predict the palette.
- **Story layers**: 6–10 stages the scroll moves through, in order. For a
  machine these are components separating; for a creature or drink they are
  stages of the signature medium (ignition → rings → vortex; swell → arc →
  pour → fill). Name them explicitly in prompts and layer captions.
- **Signature medium** — the star of the page. The flowing/energetic element
  that carries the narrative: Sacred Fire for Typhlosion (ring of fire,
  vortex, eruption, burst-down, ember flakes); an aesthetic wave of agave-gold
  tequila for Casamigos Reposado (sea-swell, arcing pour, splash crown, a
  glass filled so invitingly the visitor wants to drink it); slate dust and
  raking light for a house. The medium drives the hero choreography, the
  Act-2 climax, the ambient particle field, the vignette, and every glow.

## Phase 2 — Act 1 (Higgsfield MCP)

Templates in `references/source-prompts.md` §"Parameterized templates".

1. **Hero still** — `generate_image` (nano_banana_pro): the object at rest,
   medium dormant/simmering, pure black void, no ground plane. 16:9.
2. **Climax-state still** — `generate_image` with the hero still as
   reference: the medium at full power around the intact object (exploded
   view / full vortex / wave at its crest above the glass). Same void.
3. **Act-1 video** — `generate_video` (kling3_0, 10s, 16:9),
   `start_image` = hero still, `end_image` = climax still. **The camera
   never parks**: it orbits the object in one slow, continuous, theatrical
   arc for the entire shot — the awakening begins mid-orbit and the
   deconstruction unfolds WHILE the camera keeps circling, so the visitor
   sees every beautiful side of the object and of its opened interior.
   Aim for roughly half a revolution in Act 1; Act 2 completes the circle.
   Keep the orbit slow — fast orbits make the model drift off-model.
4. **Review before you upscale** (this ordering saves real credits): pull
   frames from the RAW take via the extraction route and LOOK at them —
   especially the first frame, the midpoint, and the last frame. Only when
   the take passes: `upscale_video` (bytedance, `aigc`, 4K, fps 24), then
   `reframe` to 9:16 and 4K-upscale that output for the portrait master.
   All quality comes from extracting off the 4K masters.

## Phase 3 — Act 2 (the climax that lands)

The continuation is what makes the page feel authored. Three rules learned
the hard way:

- **Anchor both ends.** Act 2 takes TWO anchors, and each solves a failure
  seen in production:
  - `start_image` = the literal final extracted frame of Act 1 (imported via
    `media_import_url` — a public GitHub raw URL of the committed frame works
    when the CDN is blocked). Never a still: the model re-invents framing and
    the splice jumps. Prompt opens "The shot begins EXACTLY at the provided
    frame…".
  - `end_image` = **the original Act-1 hero still (Asset 1)** — the ring-
    composition rule. Without an end anchor the object drifts off-model by
    the finale (the N64 ended with garbled logos and a changed shell). With
    the hero still as the destination, the video's last frame IS its first
    frame: the same accurate object, at the same angle, settled. The whole
    scrub becomes one closed 360° orbit — open on the object, bloom it
    apart, and return to exactly the image you started from.
- **The camera keeps moving.** Act 2 is not camera-locked — the prompt says
  the camera "CONTINUES the same slow orbital motion without any cut, zoom,
  or speed change," completing the revolution begun in Act 1 so the arc
  arrives back at the hero still's angle exactly as the parts finish
  re-stacking. Continuity across the splice comes from the start anchor plus
  "continues the same motion" — not from freezing the camera.
- **The climax and the settling must co-occur and complete.** Spell out the
  physics: the eruption crashes down WHILE the object descends, both reaching
  ground together; the wave arcs down INTO the glass as the pour completes.
  Demand the resolved end state explicitly ("ALL FOUR FEET planted flat on a
  visible ground", "the glass full, surface stilling") and a HELD final
  second — models love to end mid-motion, which reads as floating.
- **The end of Act 2 = the hero-to-body handoff.** The last frame is what's
  on screen when the visitor exits the hero, so it must be settled, grounded,
  at rest. The ambient element field fades in right at that moment so the
  medium hands off into the body.

Then the same finishing chain as Act 1: review raw → 4K → reframe 9:16 → 4K.
(5s is usually enough for Act 2; reframe occasionally false-flags content —
retry with the other-resolution source and it passes.)

## Phase 4 — Extract frames

For each act × orientation, from the 4K masters:

```bash
ffmpeg -i act.mp4 -vf "fps=24,scale=2560:-2" -q:v 2 "frames/frame_%04d.jpg"   # landscape
ffmpeg -i act.mp4 -vf "fps=24,scale=1080:-2" -q:v 2 "frames/frame_%04d.jpg"   # portrait
```

Transport routes when the CDN is unreachable (details in
`references/pipeline.md`): local curl+ffmpeg → Higgsfield sandbox →
**GitHub Actions bridge** (commit a workflow_dispatch workflow that fetches,
extracts, commits; trigger via GitHub MCP; pull; delete after).

## Phase 5 — Sample the design system

`node scripts/sample_palette.mjs <frames-dir>` on a mid-climax frame. Derive
accent / accent-deep / secondary / bg gradient stops / borders exactly as the
script suggests, then verify by eye. Never pure #000 anywhere: the template's
draw loop lifts the footage's void to the page gradient with a `lighten`
pass — keep it, it's what makes letterboxing invisible. Run the sampled
palette and the phase-1 type shortlist past `ui-ux-pro-max` before locking
them in.

## Phase 6 — Build the page

Copy `assets/template.html` → the workspace and fill every `{{SLOT}}`. The
template carries the proven mechanics — restyle, don't rebuild. Under `--max`,
this is where `premium-frontend-ui` (entry sequence, hero architecture) and
the GSAP consults (`gsap-plugins`, `gsap-timeline`, `gsap-utils`,
`gsap-performance`) layer in on top of those mechanics:

- **Two-act scrub hero** (450vh, rAF + getBoundingClientRect, no scroll
  listener, no video element), contain-fit so the whole subject stays in
  frame on every viewport, devicePixelRatio-aware, void tint.
- **Orientation-aware frame sets**: hosted WebP sets (`land/` 1920px,
  `port/` 1080px, every 2nd frame, q75) chosen by viewport orientation and
  swapped live on rotate — phones get the 9:16 master full-screen. The
  embedded single-set mode remains for a self-contained deliverable file.
- **Drag to turn** nudges the frame index; hint chip "scroll to open · drag
  to turn".
- **Layer captions** — one per story layer including the Act-2 stages ("The
  column gathers", "The burst comes down", "The landing" — or for a spirit:
  "The sea gathers", "The pour arcs", "The glass fills"). This narration is
  crawlable text, so it's also the SEO story.
- **Ambient element field** below the hero: the `MEDIUM` JSON slot tunes the
  particle engine to the object — shard vs round particles, rise/fall ratio,
  body color ramp, glow color, speeds. Fire = rise-heavy glowing shards;
  liquid = fall-heavy translucent droplets with cool glow; dust = slow tiny
  shards, faint glow. Plus the medium vignette breathing at the viewport
  bottom, card hover lift + glow, warm heading underglow, pulsing CTA glow,
  button shimmer sweep. All respect prefers-reduced-motion.
- Sections: features (6 object-specific cards), specs (8–10 accurate rows),
  gallery of the 4K stills — **serve gallery images from paths that exist on
  the deployed site** (copy optimized WebPs into the public dir; a relative
  path that only exists in the repo will 404 in production).
- SEO pack: title, ≤160-char meta description, OG/Twitter from the 4K still,
  JSON-LD (`Product`/`CreativeWork` for fan/brand tributes), one h1,
  alt/aria text everywhere, lazy gallery, reduced-motion still fallback.

## Phase 7 — Verify like you mean it

`node scripts/verify_page.mjs <index.html>` (scrub scrubs, void tinted,
reveals fire, zero errors) — then LOOK at screenshots at the act joint
(~62–70% scroll), the climax, and 100%. Check four things by eye:
no framing jump at the splice; the medium completes its arc; the final
frame is settled; and **frame 1 vs the final frame side by side — same
object, same fidelity, same angle** (the ring-composition check; if the
finale's object wouldn't pass as the opening still's twin, reshoot Act 2
before spending on upscales). Test a portrait viewport too. Serve over
localhost when testing hosted frame sets — file:// taints the canvas and
getImageData throws.

Then run `web-design-guidelines` over the built page and fix what it reports.
Under `--max`, follow it with exactly one `impeccable polish <page>` round.

## Phase 8 — Deliver

Send the page + screenshots; commit everything; if the repo is linked to a
host (e.g. Netlify), push and live-verify the deployed URLs — including the
last frame of each orientation set and the gallery images.

## Judgment calls

- Brands (a tequila, a watch marque): build as an unmistakable concept/
  tribute page unless the user owns the brand — no purchase claims, credit
  the trademark holder in the JSON-LD/footer when it's fan work.
- Model choices drift: consult `models_explore(action:'recommend')` when
  unsure. Credits are the user's money — reframes are the expensive step
  (~30–36cr each), so review raw takes BEFORE upscaling/reframing, and
  prefer one good take to three mediocre ones.
- Generation queues stall sometimes: fire a cheap duplicate and race them,
  or go video-first with the ending controlled purely by a locked-frame
  prompt (proven to work) instead of blocking on an anchor still.
- If the object can't decompose or flow (a concept, a person), bloom the
  vessel instead — the bottle, not the wine; the stadium, not the anthem.
