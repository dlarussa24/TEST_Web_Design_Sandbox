---
name: bloom
description: Generate a luxury scroll-driven "3D bloom" landing page for ANY named object using Higgsfield AI generation. The object is photographed in a studio void, animated as a cinematic two-act 4K hero — act one opens or awakens the object as the visitor scrolls, act two erupts into a climax and settles to rest exactly as the visitor reaches the body — and the object's own "signature medium" (fire for a volcano Pokémon, flowing tequila for a reposado, sawdust and light for a workshop) drifts as an ambient particle field through the rest of the page. The whole design system — colors, gradients, accents, cursor, glows, particles — is sampled from the object itself. Use this skill whenever the user invokes /bloom followed by an object name, or asks for a "bloom page", "3D bloom", "scroll-driven landing page", "deconstruction page", "exploded-view site", "product landing page with AI video", or wants a Higgsfield-generated scroll experience for a product, drink, building, vehicle, creature, instrument, or any physical object — even if they don't say "bloom" explicitly.
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

## Phase 1 — Understand the object

Decide four things (a sentence each):

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
   `start_image` = hero still, `end_image` = climax still. Camera orbits,
   the awakening begins mid-shot, ends held at the climax state.
4. **Review before you upscale** (this ordering saves real credits): pull
   frames from the RAW take via the extraction route and LOOK at them —
   especially the first frame, the midpoint, and the last frame. Only when
   the take passes: `upscale_video` (bytedance, `aigc`, 4K, fps 24), then
   `reframe` to 9:16 and 4K-upscale that output for the portrait master.
   All quality comes from extracting off the 4K masters.

## Phase 3 — Act 2 (the climax that lands)

The continuation is what makes the page feel authored. Three rules learned
the hard way:

- **Anchor on the true last frame.** Never use a still as Act 2's start —
  the model will re-invent the framing and the splice will jump. Import the
  literal final extracted frame of Act 1 as media
  (`media_import_url` — a public GitHub raw URL of the committed frame works
  when the CDN is blocked) and pass it as `start_image`, with the prompt
  opening "The shot begins EXACTLY at the provided frame… camera LOCKED, no
  cut, no zoom, no reframing."
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
pass — keep it, it's what makes letterboxing invisible.

## Phase 6 — Build the page

Copy `assets/template.html` → the workspace and fill every `{{SLOT}}`. The
template carries the proven mechanics — restyle, don't rebuild:

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
(~62–70% scroll), the climax, and 100%. Check: no framing jump at the
splice, the medium completes its arc, the final frame is settled. Test a
portrait viewport too. Serve over localhost when testing hosted frame sets —
file:// taints the canvas and getImageData throws.

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
