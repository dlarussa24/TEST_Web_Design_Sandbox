#!/usr/bin/env node
// Sample an object-derived design system from extracted video frames.
// Usage: node sample_palette.mjs <frames-dir> [frame-basename]
// Requires: npm i sharp
import sharp from 'sharp';
import { readdirSync } from 'fs';
import { join } from 'path';

const dir = process.argv[2];
if (!dir) {
  console.error('usage: node sample_palette.mjs <frames-dir> [frame-basename]');
  process.exit(1);
}
const frames = readdirSync(dir).filter((f) => /\.(jpe?g|png|webp)$/i.test(f)).sort();
if (!frames.length) {
  console.error('no frames found in', dir);
  process.exit(1);
}
// Default: ~55% through the sequence — deconstruction underway, interior exposed.
const pick = process.argv[3] || frames[Math.floor(frames.length * 0.55)];

const { data } = await sharp(join(dir, pick)).resize(200).raw().toBuffer({ resolveWithObject: true });

const sum = () => [0, 0, 0, 0];
const warm = sum(), cool = sum(), bright = sum(), shadow = sum();
const swatches = {};
for (let i = 0; i < data.length; i += 3) {
  const r = data[i], g = data[i + 1], b = data[i + 2];
  const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  if (r < 30 && g < 30 && b < 30) continue; // skip the void
  const key = [Math.round(r / 24) * 24, Math.round(g / 24) * 24, Math.round(b / 24) * 24].join(',');
  swatches[key] = (swatches[key] || 0) + 1;
  const add = (a) => { a[0] += r; a[1] += g; a[2] += b; a[3]++; };
  if (lum < 55) add(shadow);
  if (r > g && g >= b && r - b > 25) { add(warm); if (lum > 120) add(bright); }
  else if (b >= r) add(cool);
}

const hex = (a) => a[3]
  ? '#' + [0, 1, 2].map((i) => Math.round(a[i] / a[3]).toString(16).padStart(2, '0')).join('')
  : null;
const brighten = (h, f) => {
  if (!h) return null;
  const c = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  return '#' + c.map((v) => Math.min(255, Math.round(v * f)).toString(16).padStart(2, '0')).join('');
};

const warmAvg = hex(warm), brightAvg = hex(bright), coolAvg = hex(cool), shadowAvg = hex(shadow);
const accent = brighten(brightAvg || warmAvg, 1.15);

console.log(JSON.stringify({
  sampled_frame: pick,
  clusters: { warm: warmAvg, warm_bright: brightAvg, cool: coolAvg, shadow: shadowAvg },
  top_swatches: Object.entries(swatches).sort((a, b) => b[1] - a[1]).slice(0, 12)
    .map(([k, n]) => ({
      hex: '#' + k.split(',').map((v) => Math.min(255, +v).toString(16).padStart(2, '0')).join(''),
      px: n,
    })),
  suggestion: {
    accent,
    accentDeep: brighten(accent, 0.7),
    secondary: brighten(coolAvg, 1.25),
    bgStops: [brighten(shadowAvg, 0.45), brighten(shadowAvg, 0.55), brighten(shadowAvg, 0.5), brighten(shadowAvg, 0.35)],
    note: 'Verify accent contrast on the bg by eye; brighten further if it reads dimmer than #888 on dark.',
  },
}, null, 2));
