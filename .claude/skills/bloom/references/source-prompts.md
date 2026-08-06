# Source prompts

The bloom skill blends two briefs. Originals first (for fidelity), then the
parameterized templates actually used by the skill.

## Original A — Luxury scroll-driven landing page (Higgsfield video)

The essential mechanics, proven in production:

- Three Higgsfield assets in sequence: studio still on pure black → exploded
  reference using the still → hero video using both as start/end anchors.
- Frames extracted with `ffmpeg -vf "fps=24,scale=<W>:-2" -q:v 2`.
- Hero: outer 300vh container, inner sticky 100vh, `<canvas>`, overlay column
  justified flex-end with a to-top gradient. **No video element. No scroll
  event listener** — a requestAnimationFrame loop reads
  `containerRef.getBoundingClientRect().top`, maps progress 0→1, rounds to a
  frame index, redraws only on change. Cover-fit draw with
  `scale = Math.max(cw/iw, ch/ih)`, devicePixelRatio scaling, resize handler.
- Overlay: small uppercase letter-spaced label in accent, display-serif h1
  (clamp sizing), one-sentence brand line, solid accent button.
- Sections: features grid (6 cards, icon + label + sentence), specs table
  (8–10 label/value rows), closing CTA with radial glow — all scroll-reveal
  (y 24→0, opacity 0→1, ~100ms stagger, ease [0.25,0,0,1], once).
- Rules: no lorem ipsum, no navbar/footer/cookie banner, single column below
  768px, no text dimmer than #888 on dark.

(Superseded in the current template: cover-fit `Math.max` crops the subject
on non-16:9 viewports — production now uses contain-fit `Math.min` with the
void tint filling the letterbox, and 450vh for the two-act scrub.)

## Original B — BaseBloom "3D bloom" concept (Concept 02 · Depth & Material)

Reverse-engineered from https://basebloom-concepts.netlify.app/site-2/:

- Thesis: prove depth by making the centerpiece OPEN as you scroll and TURN
  in your hand as you drag. Hint chip: "drag to turn · scroll to bloom".
- Fixed atmospheric background video ("flux" — liquid metal river, Kling 3.0)
  behind everything; soft haze overlay; jewel-dark mood (#060D1A navy,
  #FF4FAE magenta, #5EE6FF ice, dichroic gold).
- Centerpiece treated as *craft*: the page brags about its own construction
  ("nineteen parametric petals in three whorls", "~24k triangles", "0 model
  files") in a stats list. Adaptive resolution, framerate first. Graceful
  fallback without WebGL.
- Four full-viewport panels, text blocks alternating sides so the centerpiece
  stays visible: HERO → WHAT WE DO → PROOF (stats) → CONTACT.
- Fonts Marcellus + Jost; confident studio voice.

What bloom borrows from B: scroll-to-open as the page's one signature move,
drag-to-turn, the interaction hint, layer-by-layer storytelling ("look down
into the work"), a proof/stats section that flaunts the object's construction,
and the discipline of alternating text placement around the centerpiece.

## Parameterized templates

Fill `{OBJECT}`, `{MATERIALS}` (comma list), `{LAYERS}` (ordered component
list), `{AXIS_STORY}` (how it comes apart: vertically / radially / along the
frame), `{NICHE_VOICE}` (one line describing the buyer and tone).

### Asset 1 — hero still

> A studio-grade product photograph of {OBJECT}, shown at a three-quarter
> angle revealing its most characterful faces. Pure black background with
> zero ambient light bleed — the object floats in a black void, no ground
> plane, no environment, no reflections, no surface shadows. Fully assembled,
> every component intact: {MATERIALS} rendered with true material texture.
> Shot as if for a high-end print campaign — clinical precision, no
> stylization.

### Asset 2 — exploded still (reference: Asset 1's job id)

> Using the provided reference image: deconstruct {OBJECT} into a precise
> exploded-view diagram. Each component — {LAYERS} — floats apart from its
> assembled position along its natural mechanical axis ({AXIS_STORY}), with
> uniform spacing between parts. The arrangement is deliberate and
> symmetrical, like a technical illustration or a luxury brand's campaign
> visual. Pure black background, no ground plane. All parts retain their
> {MATERIALS} finish and material texture. No labels, no lines, no graphic
> overlays.

### Asset 3 — Act-1 video (start_image: Asset 1, end_image: Asset 2; kling3_0, 10s, 16:9)

The camera NEVER parks: it orbits for the entire shot, and the
deconstruction happens while it circles — the visitor should see every
beautiful side of the object and of its opened interior. Act 1 covers about
half a revolution; Act 2 completes the circle back to the starting angle.

> {OBJECT} floats in a pure black void, fully assembled, with no environment,
> no ground plane, no ambient reflections. The camera begins at a
> three-quarter angle and orbits {OBJECT} in one slow, smooth, theatrical,
> uninterrupted arc that CONTINUES for the entire shot — it never stops
> moving, revealing every side of the object in turn. As the orbit passes the
> direct front-facing position — approximately halfway through the shot —
> {OBJECT} begins a seamless mechanical deconstruction WHILE the camera keeps
> circling: each component separates along its natural axis with deliberate,
> weighted momentum — {LAYERS}, in that order — so the still-moving camera
> sweeps around and between the floating parts, showing their faces, edges
> and inner surfaces from changing angles. Parts float apart in perfect
> symmetry as if gravity has been selectively reversed, revealing the inner
> construction. The orbit stays slow and constant — no speed changes, no
> cuts, no zooms. By the end of the shot, all parts are suspended in a
> balanced exploded arrangement with the camera roughly half a revolution
> from where it began, still gliding, against the black void.

### Copy skeleton (adapt, never paste verbatim across objects)

- Label: "Est. {YEAR} · {PLACE}" or an equivalent provenance line
- H1: the object's given name (invent a tasteful model/estate/edition name)
- Brand line: one sentence inviting the scroll ("scroll to open it…")
- Features: 6 cards named after real construction virtues of {OBJECT}
- Specs: 8–10 accurate rows for {OBJECT}'s category
- Proof stats (from B): 3–4 measured brags about the page/object build
- CTA: "A {timespan} of mastery. / One expression of it." + niche-correct
  button ("Find an Authorised …" retailer/builder/dealer)

## Act 2 — continuation template (climax → settle → ring closure)

TWO anchors, both mandatory. kling3_0, 5s, 16:9:
- `start_image` = the TRUE last extracted frame of Act 1, imported via
  `media_import_url` (a public GitHub raw URL of the committed frame works
  when the CDN is blocked locally) — kills the splice jump.
- `end_image` = **the original Asset-1 hero still** — the ring-composition
  rule. It forces the video's final frame to be the same accurate object,
  at the same angle, as its first frame. Without it the object drifts
  off-model by the finale (production example: the N64's last frame had
  garbled logos and a changed shell; its first frame was perfect).

> The shot begins EXACTLY at the provided first frame — {OBJECT} held at
> {CLIMAX_STATE} in a dark void — and the camera CONTINUES the same slow,
> smooth orbital motion it already has: no cut, no zoom, no speed change,
> no reframing, just the unbroken continuation of the circling arc. As the
> camera completes the revolution: {ERUPTION — the medium gathers/rises for
> one breath}. Then {CRASH — it comes down/resolves in a single continuous
> motion} — and {OBJECT} {SETTLES WITH IT — every component re-stacking and
> seating home as the two complete together; NOTHING remains floating}.
> {EXPLICIT RESOLVED END STATE — e.g. "ALL FOUR FEET planted flat on a
> visible floor" / "the glass filled, the surface stilling"}. The orbit
> arrives back at its starting angle exactly as everything settles, and the
> final second HOLDS on this ending: {OBJECT} whole, at rest, identical to
> how it appeared at the very beginning of the story — the provided final
> frame. Weighted, cinematic, precise — never chaotic; the object intact.

Why each clause exists: the exact-first-frame opener + "continues the same
motion" kill the splice jump without freezing the camera; the "co-occur"
phrasing forces the climax and the settling to be simultaneous; "NOTHING
remains floating" prevents stray parts (the N64 badge); the end anchor +
"identical to the very beginning" close the ring so first and last frames
match; the held final second prevents ending mid-motion.

## Worked medium mappings

The signature medium is what "lifts and shifts" between objects — same
mechanics, different matter. Examples:

| Object | Medium | Act 1 (awakening) | Act 2 (climax → settle) | Element field | Palette family |
|---|---|---|---|---|---|
| Typhlosion using Sacred Fire | Sacred Fire | eyes → collar ignites → fire runs the ridge → rings lift → full vortex | column erupts from vortex apex → crashes down as it lands → all four feet on scorched stone | rising ember shards + falling charcoal flakes, warm glow | flame gold on crimson-charcoal, teal fur secondary |
| Casamigos Reposado | agave-gold tequila | bottle at rest → a sea of liquid swells beneath → waves climb and wrap the bottle → a crest arcs overhead | the wave arcs down in one pour-stream → splash crown → the glass fills as the wave subsides → bottle and full glass at rest, surface stilling, irresistible | falling amber droplets + rising bubbles, round, honeyed glow | reposado amber on deep agave-brown, blue-weber green secondary |
| Meridian Estate (house) | slate & timber, dust & light | roof lifts → membrane → trusses → walls → foundation | beams settle home, dust cascades and clears, light rakes the finished facade | drifting sawdust motes + falling slate dust, faint warm glow | cedar amber on charcoal, slate secondary |
| Vintage Leica M6 | glinting brass & light | top plate lifts → lens elements fan out → shutter curtain unfurls | elements spiral back together as a shutter-click flash resolves to the assembled camera on a leather mat | floating silver dust + bokeh discs, cool glow | brass on black-chrome, leather secondary |

MEDIUM JSON starting points:

- fire: `{"shape":"shard","riseRatio":0.6,"bodyLow":[26,13,8],"bodyHigh":[146,83,28],"glow":[255,140,50],"riseSpeed":[18,55],"fallSpeed":[10,32]}`
- liquid: `{"shape":"round","riseRatio":0.35,"bodyLow":[40,24,8],"bodyHigh":[220,160,60],"glow":[255,200,90],"riseSpeed":[10,26],"fallSpeed":[16,44]}`
- dust: `{"shape":"shard","riseRatio":0.5,"bodyLow":[30,26,22],"bodyHigh":[120,104,84],"glow":[200,180,140],"riseSpeed":[6,16],"fallSpeed":[4,12]}`
