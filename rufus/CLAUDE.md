# Rufus pipeline — standing orders

This directory is the Rufus the Raccoon / Rufus Gone Rogue production
pipeline. Routine sessions working here follow these rules without being
reminded. Full canon lives in `../docs/character-bible.html` and
`../docs/prompt-reference.html`; the strategy in
`../docs/rufus-growth-playbook.html`. (When this tree migrates to the
dedicated `rufus-media` repo, those docs move into `docs/` here.)

## Hard nevers (any violation = do not post, no exceptions)

- No children or teenagers in frame. Adults only.
- No tobacco imagery. No realistic weapons in Rufus's possession.
- Rufus is never harmed, trapped, or in distress.
- No legible third-party trademarks — the cap emblem is worn to an abstract
  smudge; acceptance test: "could a viewer name the team or brand?" If yes,
  clean with `tools/delogo.py` or reject.
- No licensed music baked into files. Video audio is generated ambience;
  platform music is added at post time from commercial-safe pickers only.
- Bystander panic is expressed with hands BELOW shoulder height. No
  cheering poses, no raised arms.

## Design locks

- Rufus: real North American raccoon, real paws (never human hands), dense
  grey-brown fur, black mask, ringed tail. Headwear optional; if worn, one
  of: battered navy cap (default), beanie, cowboy hat, bandana — lived-in,
  illegible.
- BIG SIPPY: purple body `#966ECD` (canon hue 265.3°), ONE yellow horizontal
  band, band-yellow short thick straw. Generate the pouch BLANK; the label
  is applied in post, never asked of the generator.

## The post chain (every asset, in order)

1. Generate via Higgsfield (`get_cost` preflight; image `soul_2` 3:4,
   video `flux_3_video` with `generate_audio`). Pass an approved frame as
   image reference. Local files can't upload through the proxy — route via
   the file's `raw.githubusercontent.com` URL with `media_import_url`.
2. `tools/lock-sippy.py in out --box=…` — pin pouch colour (explicit box in
   cluttered scenes).
3. `tools/sippy-artwork.py in out --box=… --straw=…` — full label layout
   (BIG on body, SIPPY in band, straw rework) when the pouch is prominent.
4. `tools/delogo.py` — only if a trademark rendered.
5. `tools/check-frame.py asset [--video]` — the gate. Non-zero exit = do not
   post; regenerate once, else log as skipped.
6. Eyes-on review happens in Slack — that is what the approval step is for.
   Identity consistency is not machine-checkable.

## Posting rules

- Captions come from `docs/caption-bank.md`, 70% Type A / 30% Type B,
  rotation tracked in `pipeline/post-log.md`. Never explain the joke.
- Label posts as AI-generated on Meta surfaces.
- Slack log channel: `#rufus-posts`. ✅ = approved, ❌ = rejected,
  no reaction = hold. Publish IG via Zapier "Instagram for Business",
  TikTok via Higgsfield `tiktok_publish`. Reply in-thread with live links.
- Update `pipeline/post-log.md` on every state change.
