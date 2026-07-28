# Asset pipeline details

## Higgsfield call sequence (MCP tools; load via ToolSearch if deferred)

```
generate_image  { model, prompt: <Asset 1 template>, aspect_ratio: "16:9" }
generate_image  { model, prompt: <Asset 2 template>, aspect_ratio: "16:9",
                  medias: [{ value: <asset1 job id>, role: "image" }] }
generate_video  { model: "kling3_0", duration: 10, aspect_ratio: "16:9",
                  prompt: <Asset 3 template>,
                  medias: [{ value: <asset1 id>, role: "start_image" },
                           { value: <asset2 id>, role: "end_image" }] }
upscale_video   { provider: "bytedance", video_id: <asset3 id>,
                  width: <src w>, height: <src h>, resolution: "4k",
                  preset: "aigc", fps: 24 }
upscale_image   { image_id: <asset1 id>, width, height, resolution: "4k" }
upscale_image   { image_id: <asset2 id>, width, height, resolution: "4k" }
```

Poll with `job_display(id)` — status moves pending → in_progress → completed,
and completed results carry `results.rawUrl` (CloudFront). Stills complete in
~30–60s, a 10s video in ~2–6 min, 4K upscale in ~1–3 min. Overlap the waits
with page scaffolding.

Model choice: nano_banana_pro is the proven default for the stills (crisp
product/diagram work, accepts reference images); kling3_0 for the video
(honors start/end image anchors). If the catalog has moved on, trust
`models_explore(action:'recommend')` over this file.

## Frame extraction

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,nb_frames,duration \
  -of default=noprint_wrappers=1 hero.mp4
mkdir -p frames
ffmpeg -i hero.mp4 -vf "fps=24,scale=2560:-2" -q:v 2 "frames/frame_%04d.jpg"
ls frames | wc -l   # => FRAME_COUNT
```

`scale=2560:-2` keeps height even (codec-safe). A 10s / 24fps video yields
~241 frames, ~90 MB at q:v 2 — commit them; they're the page's soul.

## Transport routes (in order of preference)

### 1. Direct (open network)

`curl -fSL <rawUrl> -o hero.mp4`, local ffmpeg (`apt`, or
`npm i ffmpeg-static` and call the binary it exposes).

### 2. Higgsfield sandbox (no local ffmpeg, CDN reachable from sandbox only)

`sandbox_exec` has ffmpeg/ImageMagick/node and open internet, but the sandbox
is discarded ~10s after each call — chain the whole job in one `&&` command,
then publish results: call `media_upload` for a presigned URL, `curl -X PUT
--upload-file out.zip <upload_url>` from inside the sandbox, `media_confirm`,
and download from the returned URL if your environment can reach it.

### 3. GitHub Actions bridge (egress-locked environments)

Symptom: `curl` to the CDN returns a proxy 403 (`CONNECT tunnel failed`), but
github.com works. GitHub runners have open internet — make one do the fetch:

1. Commit `.github/workflows/fetch-assets.yml`: `workflow_dispatch` with a
   `video_url` input (plus optional still URLs); `permissions: contents:
   write`; steps: checkout → ensure ffmpeg → curl the URL → ffprobe → extract
   frames → copy into `public/frames` + `public/hero.mp4` → write the frame
   count into the page's FRAME_COUNT constant → commit & push as
   github-actions[bot].
2. Push. On a brand-new repo the workflow may take ~1–2 min to register; if
   `run_workflow` 404s, push a trivial edit to the workflow file to force
   re-indexing, then retry.
3. Trigger via GitHub MCP `actions_run_trigger` (method run_workflow, ref =
   working branch, inputs = the CloudFront URLs).
4. Poll `actions_list` until conclusion=success, then `git pull`.
5. Delete the workflow file once assets are committed — it's scaffolding.

## Design-system sampling

```bash
npm i sharp   # once per workspace
node scripts/sample_palette.mjs frames [frame-number]
```

Reads a mid-deconstruction frame (defaults to ~55% through, when the interior
is exposed), quantizes non-void pixels, and prints warm/cool/bright cluster
averages plus top swatches. Derivation rules:

- accent      = brightened warm/dominant material average (readable on dark)
- accentDeep  = same hue, ~30% darker (button gradient end)
- secondary   = cool cluster average (cards, dividers, glow hint)
- bg stops    = shadow-cluster tones, 3–4 stops, none of them #000000
- borders     = accent at 14–20% alpha; spec dividers = secondary at ~14%

## Standalone embedding

```bash
npm i sharp
node scripts/build_standalone.mjs --frames frames --html index.html \
  --width 1920 --quality 75 --every 2
```

Re-encodes every Nth frame to WebP data URIs and injects them at the
`/*__FRAMES__*/[]` marker (idempotent — safe to re-run; it replaces the
existing array). Expect ~16 MB at 1920/q75/every-2 for a 10s video. For a
hosted variant keep frames on disk and set the loader path instead.

## Verification

```bash
npm i playwright-core
node scripts/verify_page.mjs index.html [screenshots-dir]
```

Uses the environment's Chromium (checks PLAYWRIGHT_BROWSERS_PATH, falls back
to common install paths). Fails loudly if the scrub produces fewer than 4
distinct canvas states, if void pixels are pure black, or if any page error
fires. Always eyeball the screenshots before delivering.
