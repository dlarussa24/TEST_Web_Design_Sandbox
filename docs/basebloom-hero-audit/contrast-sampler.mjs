#!/usr/bin/env node
// Measure WCAG contrast of text regions in a page screenshot.
//
// This is the exact method that produced the baseline table in
// ../basebloom-hero-audit.md. Re-run it after each change wave so score
// movement is backed by the same measurement that set the baseline.
//
//   node contrast-sampler.mjs <image> [desktop|mobile]
//
// Method: crop each named region, sort its pixels by WCAG relative
// luminance, and treat the mean of the darkest 8% as background and the
// mean of the lightest 8% as foreground. On antialiased text over video
// this approximates the true fg/bg pair closely enough to judge AA/AAA,
// and it needs no DOM access — which matters when the page is behind an
// egress policy and all you have is a PNG.
//
// Caveat that must travel with any number this prints: a video hero's
// contrast is a DISTRIBUTION across frames, not a value. A single capture
// is one sample. To claim a floor, run this across every extracted frame
// and report the MINIMUM.

import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const FFMPEG = require('ffmpeg-static');

// name, x, y, w, h — in actual image pixels (captures were DPR 2)
const REGIONS = {
  desktop: [
    ['nav links', 1322, 50, 946, 42],
    ['logo wordmark', 330, 40, 290, 60],
    ['Free demo btn', 2320, 35, 300, 70],
    ['eyebrow', 331, 428, 700, 34],
    ['h1 line1 (white)', 331, 500, 1150, 110],
    ['h1 line2 (green)', 331, 655, 1390, 110],
    ['subcopy', 331, 828, 1020, 46],
    ['phone number', 328, 1140, 315, 50],
    ['tan button', 330, 1210, 525, 90],
    ['green button', 888, 1210, 340, 90],
    ['trust bullets', 353, 1364, 1540, 44],
  ],
  mobile: [
    ['eyebrow', 48, 196, 610, 22],
    ['h1 white', 48, 250, 520, 160],
    ['h1 green', 48, 450, 560, 170],
    ['subcopy', 48, 665, 660, 200],
    ['phone', 48, 1000, 380, 50],
    ['tan button', 48, 1120, 530, 100],
    ['green button', 48, 1258, 355, 100],
    ['trust bullets', 48, 1425, 690, 180],
  ],
};

const srgb = (v) => {
  v /= 255;
  return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
};
const luminance = (r, g, b) => 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b);
const contrast = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
const hex = (c) => '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('');

function sample(image, [name, x, y, w, h]) {
  const raw = execFileSync(
    FFMPEG,
    ['-hide_banner', '-loglevel', 'error', '-i', image,
     '-vf', `crop=${w}:${h}:${x}:${y}`, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
    { maxBuffer: 1 << 28 },
  );

  const px = [];
  for (let i = 0; i < raw.length; i += 3) px.push([raw[i], raw[i + 1], raw[i + 2]]);
  px.sort((p, q) => luminance(...p) - luminance(...q));

  const k = Math.max(1, Math.floor(px.length * 0.08));
  const mean = (arr) =>
    arr.reduce((t, c) => [t[0] + c[0], t[1] + c[1], t[2] + c[2]], [0, 0, 0])
       .map((v) => Math.round(v / arr.length));

  const bg = mean(px.slice(0, k));
  const fg = mean(px.slice(-k));
  const ratio = contrast(luminance(...bg), luminance(...fg));
  const grade = ratio >= 7 ? 'AAA' : ratio >= 4.5 ? 'AA' : ratio >= 3 ? 'large-only' : 'FAIL';

  return { name, bg: hex(bg), fg: hex(fg), ratio, grade };
}

const [image, which = 'desktop'] = process.argv.slice(2);
if (!image) {
  console.error('usage: node contrast-sampler.mjs <image> [desktop|mobile]');
  process.exit(2);
}
const regions = REGIONS[which];
if (!regions) {
  console.error(`unknown region set "${which}" — expected desktop or mobile`);
  process.exit(2);
}

let worst = Infinity;
let failures = 0;
for (const region of regions) {
  const r = sample(image, region);
  worst = Math.min(worst, r.ratio);
  if (r.ratio < 4.5) failures++;
  console.log(
    r.name.padEnd(24),
    'bg', r.bg.padEnd(9),
    'fg', r.fg.padEnd(9),
    (r.ratio.toFixed(2) + ':1').padStart(8),
    ' ' + r.grade,
  );
}
console.log(`\nworst: ${worst.toFixed(2)}:1   below AA: ${failures}/${regions.length}`);
process.exit(failures ? 1 : 0);
