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

## Media hosting — Cloudinary, never git

**Do not commit generated media to git.** Binaries in git are permanent
(history never shrinks) and the routines clone the repo on every firing;
at 3 posts/day that is ~6.4 GB/year of clone weight. The repo holds text,
tools, and a handful of reference frames only.

Every final asset goes to Cloudinary instead. Two upload paths — pick by
where the file currently lives.

### A. The file is already at a URL (raw Higgsfield output, unprocessed)

`mcp__Cloudinary__upload-asset` with `file` = that URL, `asset_folder:
rufus/YYYY-MM-DD`, `public_id` = the post id, `tags` = [mode, format,
platform targets], `resource_type` image or video. Cloudinary fetches it
server-side.

### B. The file is LOCAL (anything through the post chain) — the normal case

The Cloudinary MCP runs server-side and cannot read the sandbox filesystem,
so a local path will not work. Use a signed direct POST. This recipe is
tested and works:

1. `mcp__Cloudinary__sign-upload` with the signable params only —
   `public_id`, `asset_folder`, `tags`, `display_name`. Do NOT pass `file`,
   `resource_type`, `api_key` or `signature`.
2. POST multipart to
   `https://api.cloudinary.com/v1_1/<cloud_name>/<image|video>/upload`,
   echoing **every** key from the returned `upload_params` as its own `-F`
   field, plus `api_key`, `signature`, and the file.
   The response includes fields that are easy to miss — `colors`,
   `upload_preset`, `audit_context`, `overwrite` — and **dropping or
   renaming any one of them invalidates the signature**. Echo them verbatim.
3. `resource_type` goes in the URL path, never in the form fields.

### Both paths

- The returned **`secure_url`** is the canonical link — Slack card, the
  `cdn_url` column of the post log, and the Instagram publish call. Assets
  upload as `type: upload` (public delivery), so Instagram and TikTok can
  fetch them even though the repo is private.
- **Export before upload.** Save stills as JPEG quality 90 rather than
  uploading 2K PNG masters — the Cloudinary image cap is 10 MB and some
  masters exceed it. Measured: 4.74 MB PNG → 0.70 MB JPEG.
- **Deliver a derivative, not the original.** Insert `f_auto,q_auto,w_1080`
  after `/upload/` in the URL. Measured: 206 KB delivered vs a 4.74 MB
  master, generated on the fly with no extra upload.
- If a fetch fails locally, check `mcp__Cloudinary__get-asset-details` before
  concluding the asset is broken — an egress problem here says nothing about
  whether Instagram can fetch it.

## Posting rules

- Captions come from `docs/caption-bank.md`, 70% Type A / 30% Type B,
  rotation tracked in `pipeline/post-log.md`. Never explain the joke.
- Label posts as AI-generated on Meta surfaces.
- Slack log channel: `#rufus-posts`. ✅ = approved, ❌ = rejected,
  no reaction = hold. Publish IG via Zapier "Instagram for Business" using the
  Cloudinary `secure_url` as the media parameter; TikTok via Higgsfield
  `tiktok_publish`. Reply in-thread with live links.
- Update `pipeline/post-log.md` on every state change.
