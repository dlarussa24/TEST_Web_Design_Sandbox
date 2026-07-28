---
name: bloom
description: Generate a luxury scroll-driven "3D bloom" landing page for ANY named object using Higgsfield AI generation. The object is photographed in a studio void, deconstructed into an exploded view, animated as a cinematic 4K deconstruction video, and turned into a self-contained landing page whose hero scrubs frame-by-frame through the object opening up as the visitor scrolls — with the entire design system (colors, gradients, accents, cursor, glows) sampled from the object itself. Use this skill whenever the user invokes /bloom <object>, names an object after the word bloom, or asks for a "bloom page", "3D bloom", "scroll-driven landing page", "deconstruction page", "exploded-view site", "product landing page with AI video", or wants a Higgsfield-generated scroll experience for a product, building, vehicle, instrument, or any physical object — even if they don't say "bloom" explicitly.
---

# Bloom — object-driven scroll-deconstruction landing pages

Turn any named object into a cinematic landing page: `/bloom vintage Leica M6`,
`/bloom carbon-fiber track bike`, `/bloom luxury alpine chalet`.

The finished page has one signature move: the hero holds a photoreal render of
the object suspended in a dark void, and as the visitor scrolls, the object
**opens** — its components separate along their natural mechanical axes,
frame by frame, until it hangs in a balanced exploded arrangement. The visitor
is weaving through the object's layers. Everything else on the page (palette,
gradients, borders, glow, cursor) is derived from the object's own materials,
so every bloom page looks like it was art-directed for that object alone.

This skill blends two proven briefs (read `references/source-prompts.md` for
both originals): a luxury scroll-scrub landing page (canvas + JPEG frames, no
video element, no scroll listener) and the BaseBloom "3D bloom" concept
(scroll-to-open, drag-to-turn, jewel-dark aesthetic, interaction hints).

## Workflow at a glance

1. **Understand the object** — niche, materials, natural layers
2. **Generate assets in Higgsfield** — still → exploded still → video → 4K
3. **Extract frames** — 24 fps, 2560px, high quality
4. **Sample the design system from the frames** — scripts/sample_palette.mjs
5. **Build the page** — copy assets/template.html, fill slots, embed frames
6. **Verify in a real browser** — scripts/verify_page.mjs
7. **Deliver** — send index.html + screenshots; commit if in a repo

Work through the phases in order; each depends on the previous one's output.

## Phase 1 — Understand the object

Before generating anything, decide three things (a sentence each is enough):

- **Niche & voice**: who buys/loves this object? A watch page whispers heritage;
  a synthesizer page hums with circuitry. All copy follows this voice — never
  lorem ipsum, never generic.
- **Materials**: the 3–5 surfaces that define it (e.g. cedar, slate, copper for
  a chalet; brass, leather, glass for a camera). These predict the palette and
  make the generation prompts concrete.
- **Deconstruction layers**: 6–10 components it naturally splits into, along
  which axes. A house lifts vertically (roof → trusses → walls → foundation);
  a watch blooms radially; a bike explodes along its frame lines. Name them in
  the prompts — vague prompts produce mushy deconstructions.

## Phase 2 — Generate assets (Higgsfield MCP)

Prompt templates with the `{OBJECT}`/materials/layers slots are in
`references/source-prompts.md` §"Parameterized templates". The sequence:

1. **Hero still** — `generate_image` (nano_banana_pro or the current
   recommendation from `models_explore` for product photography). Studio-grade
   photo of {OBJECT}, three-quarter angle, **pure black background, no ground
   plane, no reflections** (the void must be uniform so the page can tint it).
   16:9.
2. **Exploded still** — `generate_image` with the hero still's job id as a
   reference image. Every named layer floats apart along its natural axis,
   uniform spacing, symmetrical, technical-illustration calm. Same black void.
3. **Hero video** — `generate_video` (kling3_0, 10s, 16:9) with
   `start_image` = hero still and `end_image` = exploded still. Camera orbits
   first, deconstruction begins mid-shot, ends suspended. The start/end anchors
   are what make the scrub feel authored instead of hallucinated.
4. **Upscale everything** — `upscale_video` (bytedance, `aigc` preset,
   4K, fps 24) and `upscale_image` (4K) on both stills. The page's "extremely
   high definition" quality comes from extracting frames from the 4K master,
   never from upscaling soft frames later.

Poll jobs with `job_display`. While generation runs, scaffold the page and
workspace — don't idle.

## Phase 3 — Extract frames

From the **4K upscaled** video:

```bash
ffmpeg -i hero.mp4 -vf "fps=24,scale=2560:-2" -q:v 2 "frames/frame_%04d.jpg"
```

Count the files — that's `FRAME_COUNT`. Keep the 4K mp4 too (SEO video asset).

**Transport problem**: the generated media lives on Higgsfield's CDN, which
sandboxed environments often can't reach. Pick the first route that works —
all three are detailed in `references/pipeline.md`:

- **Local**: `curl` the URL, run local ffmpeg (or `npm i ffmpeg-static`).
- **Higgsfield sandbox**: `sandbox_exec` has ffmpeg + open internet; process
  there, publish via `media_upload` presigned URL.
- **GitHub Actions bridge** (for egress-blocked environments where only
  github.com is reachable): commit a `workflow_dispatch` workflow that
  downloads, extracts, and commits the frames; trigger it via the GitHub MCP;
  `git pull` the result; delete the workflow afterwards. This is the proven
  route when curl returns proxy 403s — don't fight the proxy, route around it.

## Phase 4 — Sample the design system from the object

Run `scripts/sample_palette.mjs <frames-dir>` (needs `npm i sharp`). It prints
dominant warm/cool/bright clusters from an exploded-view frame. From those:

- **Accent**: the object's signature material tone, brightened until it reads
  clearly on the dark background (never dimmer than #888 equivalent). This
  colors labels, icons, spec keys, buttons, cursor glow.
- **Accent gradient**: accent → its darker sibling (e.g. cedar → copper) for
  primary buttons.
- **Secondary**: the object's cool/contrast tone, used sparingly — card
  gradients, dividers, a hint in the CTA glow.
- **Background gradient**: NOT pure black. Build a 3–4 stop, 170deg gradient
  from the object's shadow tones (e.g. `#101012 → #131114 → #17110b → #100c08`
  for a slate-and-cedar house). `background-attachment: fixed` on body;
  sections transparent.
- **Void tint**: the video frames have a #000 void — the canvas must lift it.
  The template's draw loop composites a `lighten` gradient pass after each
  frame so void pixels match the page gradient exactly. Keep it.

## Phase 5 — Build the page

Copy `assets/template.html` to the workspace as `index.html` and fill every
`{{SLOT}}`. The template already contains the proven mechanics — don't rebuild
them, restyle them:

- 300vh sticky **canvas scrub hero** (rAF + getBoundingClientRect, no scroll
  listener, no video element), devicePixelRatio-aware, cover-fit, void tint
- **Drag to turn**: horizontal drag on the hero nudges the frame index, so the
  visitor can "turn the object in their hand"; scroll remains the master
  timeline. Hint chip: "scroll to open · drag to turn".
- **Layer captions**: short labels that fade in at scrub milestones naming the
  layer currently separating ("the slate lifts", "the movement rises"). Write
  one per deconstruction layer from Phase 1 — this is the weaving-through-
  the-passes storytelling.
- **Custom cursor**: accent-colored glow dot that scales over interactive
  elements (respects `prefers-reduced-motion` and disappears on touch).
- **Scroll progress rail** along the viewport edge in the accent color.
- Sections: features grid (6 cards, object-specific), specs table (8–10
  accurate rows), 4K stills gallery (the two upscaled images), closing CTA
  with radial glow. All reveal on scroll (IntersectionObserver, y 24→0,
  staggered, once).
- Mobile: single column below 768px; hero canvas untouched.

Then embed the frames to make the file self-contained:

```bash
node scripts/build_standalone.mjs --frames <frames-dir> --html index.html \
  --width 1920 --quality 75 --every 2
```

(Every 2nd frame at 1920px WebP ≈ visually identical scrub, ~half the bytes.
If the user will host the page with a `frames/` folder instead, skip embedding
and point the loader at the folder — offer both.)

### SEO & engagement (fill these — they're template slots, not suggestions)

- `<title>` = object name + one differentiator; meta description ≤160 chars
  written like ad copy; canonical URL slot.
- Open Graph + Twitter card using the 4K hero still.
- **JSON-LD** `Product` (or `House`/`Vehicle` when truer) with name, image,
  description, brand.
- One `<h1>` only; sections use `<h2>`; every image/canvas has alt/aria text;
  the deconstruction narrative is mirrored in real text (layer captions render
  as HTML, so the page's story is crawlable, not trapped in pixels).
- `<link rel="preload">` for the first frame; lazy-load the gallery;
  `prefers-reduced-motion` swaps the scrub for the 4K still.

## Phase 6 — Verify like you mean it

Run `scripts/verify_page.mjs <path-to-index.html>` (needs `npm i
playwright-core`; use the environment's preinstalled Chromium). It opens the
page via `file://`, scrolls the hero at 0/25/50/75/100%, and asserts:

- ≥4 distinct canvas states (the scrub actually scrubs)
- void pixels are NOT pure black (tint works)
- reveal elements gain their visible class
- zero page errors

It saves screenshots — **look at them**. Check the exploded frame for detail
sharpness, and the sections for palette harmony. Then send the user the
screenshots and the final file.

## Phase 7 — Deliver

- Send `index.html` (and screenshots) to the user.
- In a git repo: commit page + frames + 4K assets, push to the working branch.
- Report what was generated (asset job ids), the sampled palette, frame count,
  and file size — and note the fonts load from Google Fonts (the only network
  dependency).

## Judgment calls

- Model choices drift: when unsure, ask `models_explore(action:'recommend')`
  rather than hardcoding yesterday's best model.
- Credits are the user's money: preflight with `get_cost` when a generation
  plan is unusual (multiple variants, long durations), and prefer one good
  10s video over three mediocre ones.
- If the user names a person, brand logo, or something that can't be
  deconstructed (a liquid, a concept), say what you can do instead — e.g.
  bloom the bottle, not the wine.
