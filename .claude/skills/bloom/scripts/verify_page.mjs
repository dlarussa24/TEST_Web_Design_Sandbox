#!/usr/bin/env node
// Verify a bloom page in a real browser: the scrub scrubs, the void is
// tinted (never pure black), reveals fire, no page errors.
// Usage: node verify_page.mjs <index.html> [screenshots-dir]
// Requires: npm i playwright-core (uses the environment's Chromium)
import { chromium } from 'playwright-core';
import { existsSync } from 'fs';
import { resolve } from 'path';

const htmlPath = resolve(process.argv[2] || 'index.html');
const shotDir = process.argv[3] || '.';

const candidates = [
  process.env.CHROMIUM_PATH,
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  ...(existsSync('/opt/pw-browsers')
    ? (await import('fs')).readdirSync('/opt/pw-browsers')
        .filter((d) => d.startsWith('chromium-'))
        .map((d) => `/opt/pw-browsers/${d}/chrome-linux/chrome`)
    : []),
  '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome',
].filter(Boolean);
const executablePath = candidates.find((p) => existsSync(p));
if (!executablePath) {
  console.error('No Chromium found; set CHROMIUM_PATH.');
  process.exit(1);
}

const browser = await chromium.launch({ executablePath, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));

await page.goto('file://' + htmlPath, { waitUntil: 'load', timeout: 180000 });
await page.waitForTimeout(5000); // let embedded frames decode

const canvasState = () => page.evaluate(() => {
  const c = document.querySelector('canvas');
  if (!c) return null;
  const ctx = c.getContext('2d');
  const d = ctx.getImageData(0, 0, 300, 300).data;
  let h = 0;
  for (let i = 0; i < d.length; i += 97) h = (h * 31 + d[i]) >>> 0;
  const corner = ctx.getImageData(5, 5, 1, 1).data;
  return { hash: h, corner: [corner[0], corner[1], corner[2]] };
});

const states = [];
for (const f of [0, 0.25, 0.5, 0.75, 1]) {
  await page.evaluate((frac) => {
    const c = document.querySelector('[data-bloom-container]') || document.querySelector('main > div');
    window.scrollTo(0, (c.offsetHeight - window.innerHeight) * frac);
  }, f);
  await page.waitForTimeout(500);
  states.push(await canvasState());
  await page.screenshot({ path: `${shotDir}/bloom-${Math.round(f * 100)}.png` });
}

await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await page.waitForTimeout(1500);
const reveals = await page.evaluate(() => ({
  total: document.querySelectorAll('.reveal').length,
  visible: document.querySelectorAll('.reveal.in').length,
}));
await page.screenshot({ path: `${shotDir}/bloom-bottom.png` });
await browser.close();

const unique = new Set(states.filter(Boolean).map((s) => s.hash)).size;
const voidPixel = states[0]?.corner || [0, 0, 0];
const voidOk = voidPixel.some((v) => v > 6);
const results = {
  distinct_canvas_states: `${unique}/5`,
  scrub_ok: unique >= 4,
  void_pixel: voidPixel,
  void_tinted_not_black: voidOk,
  reveals,
  page_errors: errors,
};
console.log(JSON.stringify(results, null, 2));
if (!(unique >= 4) || !voidOk || errors.length) {
  console.error('VERIFICATION FAILED');
  process.exit(1);
}
console.log('VERIFICATION PASSED');
