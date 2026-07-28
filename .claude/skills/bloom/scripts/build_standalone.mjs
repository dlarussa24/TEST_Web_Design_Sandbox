#!/usr/bin/env node
// Embed extracted frames into the page as WebP data URIs so the HTML file is
// fully self-contained (openable from disk, no server, no folders).
// Usage: node build_standalone.mjs --frames <dir> --html <file>
//        [--width 1920] [--quality 75] [--every 2]
// Requires: npm i sharp
// Idempotent: replaces the FRAMES array whether it's the /*__FRAMES__*/[]
// marker or a previously injected array.
import sharp from 'sharp';
import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const arg = (name, dflt) => {
  const i = process.argv.indexOf('--' + name);
  return i > -1 ? process.argv[i + 1] : dflt;
};
const framesDir = arg('frames');
const htmlPath = arg('html');
const width = +arg('width', 1920);
const quality = +arg('quality', 75);
const every = +arg('every', 2);
if (!framesDir || !htmlPath) {
  console.error('usage: node build_standalone.mjs --frames <dir> --html <file> [--width N] [--quality N] [--every N]');
  process.exit(1);
}

const all = readdirSync(framesDir).filter((f) => /\.(jpe?g|png)$/i.test(f)).sort();
const picked = all.filter((_, i) => i % every === 0);
if (!picked.includes(all[all.length - 1])) picked.push(all[all.length - 1]);
console.log(`embedding ${picked.length} of ${all.length} frames @ ${width}px webp q${quality}`);

const uris = [];
for (const f of picked) {
  const buf = await sharp(join(framesDir, f)).resize({ width }).webp({ quality }).toBuffer();
  uris.push(`data:image/webp;base64,${buf.toString('base64')}`);
}

let html = readFileSync(htmlPath, 'utf8');
const re = /var FRAMES = (?:\/\*__FRAMES__\*\/)?\[[^\]]*\];/;
if (!re.test(html)) {
  console.error('FRAMES declaration not found — the page must contain `var FRAMES = /*__FRAMES__*/[];`');
  process.exit(1);
}
html = html.replace(re, `var FRAMES = ${JSON.stringify(uris)};`);
writeFileSync(htmlPath, html);
console.log(`${htmlPath} written: ${(html.length / 1024 / 1024).toFixed(1)} MB`);
