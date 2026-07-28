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

### Asset 3 — hero video (start_image: Asset 1, end_image: Asset 2; kling3_0, 10s, 16:9)

> {OBJECT} floats in a pure black void, fully assembled, with no environment,
> no ground plane, no ambient reflections. The camera begins at a
> three-quarter angle and slowly orbits in a smooth, uninterrupted arc. As the
> camera arrives at the direct front-facing position — approximately halfway
> through the shot — {OBJECT} begins a seamless mechanical deconstruction.
> Each component separates along its natural axis with deliberate, weighted
> momentum: {LAYERS}, in that order. Parts float apart in perfect symmetry as
> if gravity has been selectively reversed, revealing the inner construction.
> The movement is slow, cinematic, and precise — never chaotic. By the end of
> the shot, all parts are suspended in a balanced exploded arrangement, still
> against the black void.

### Copy skeleton (adapt, never paste verbatim across objects)

- Label: "Est. {YEAR} · {PLACE}" or an equivalent provenance line
- H1: the object's given name (invent a tasteful model/estate/edition name)
- Brand line: one sentence inviting the scroll ("scroll to open it…")
- Features: 6 cards named after real construction virtues of {OBJECT}
- Specs: 8–10 accurate rows for {OBJECT}'s category
- Proof stats (from B): 3–4 measured brags about the page/object build
- CTA: "A {timespan} of mastery. / One expression of it." + niche-correct
  button ("Find an Authorised …" retailer/builder/dealer)
