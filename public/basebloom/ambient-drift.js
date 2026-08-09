// ambient-drift.js — the element field behind every BaseBloom surface.
// Each niche breathes its own material: rain over the roofing film, embers
// through the HVAC dark, bubbles up the plumbing page, shavings falling on
// the carpentry bench — and the landing page carries a medley of all of them.
// Mechanics adapted from the Typhlosion charcoal-ember study: a mixed
// rising/falling field with sinusoidal sway, flicker, scroll parallax and
// edge respawn, drawn on one fixed canvas.
//
//   <script src="../ambient-drift.js" data-drift="rain" data-z="45" defer></script>
//
// data-drift: medley | rain | embers | bubbles | dust | motes | pigment | shavings
// data-z:     z-index for the canvas (default 30)
// data-n:     desktop particle count (default 60; small screens run half)
// Never mounts under prefers-reduced-motion; halves density on small screens;
// skips work while the tab is hidden. pointer-events: none throughout.
(() => {
  const me = document.currentScript;
  const themeName = me?.dataset.drift || 'medley';
  const zIndex = +(me?.dataset.z || 30);
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // ---- species: how each material draws itself -------------------------------
  // Every particle: {x,y,vy,rise,s,amp,freq,ph,rot,rotV,flick,c,sp,glow}
  const rnd = (a, b) => a + Math.random() * (b - a);
  const SPECIES = {
    // soft round mote; flickers; optional additive glow (embers, glints)
    mote(ctx, p, a) {
      ctx.fillStyle = p.c + a + ')';
      ctx.beginPath(); ctx.arc(0, 0, p.s, 0, 6.283); ctx.fill();
      if (p.glow) {
        ctx.globalCompositeOperation = 'lighter';
        const g = ctx.createRadialGradient(0, 0, 0, 0, 0, p.s * 3);
        g.addColorStop(0, p.c + a * 0.55 + ')'); g.addColorStop(1, p.c + '0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, p.s * 3, 0, 6.283); ctx.fill();
        ctx.globalCompositeOperation = 'source-over';
      }
    },
    // thin falling streak (rain); drawn along its travel, slight slant
    streak(ctx, p, a) {
      ctx.strokeStyle = p.c + a + ')'; ctx.lineWidth = Math.max(0.7, p.s * 0.22);
      ctx.beginPath(); ctx.moveTo(0, -p.s * 2.6); ctx.lineTo(p.s * 0.5, p.s * 2.6); ctx.stroke();
    },
    // hollow circle with a highlight arc (water bubble / suds)
    bubble(ctx, p, a) {
      ctx.strokeStyle = p.c + a + ')'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(0, 0, p.s, 0, 6.283); ctx.stroke();
      ctx.strokeStyle = p.c + Math.min(1, a * 1.8) + ')'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(0, 0, p.s * 0.62, -2.2, -1.1); ctx.stroke();
    },
    // slim grass blade: a gently curved sliver
    blade(ctx, p, a) {
      ctx.strokeStyle = p.c + a + ')'; ctx.lineWidth = Math.max(0.8, p.s * 0.28);
      ctx.beginPath(); ctx.moveTo(0, p.s * 1.6);
      ctx.quadraticCurveTo(p.s * 0.9, 0, 0.2 * p.s, -p.s * 1.6); ctx.stroke();
    },
    // rotating paint fleck: a tiny irregular quad
    fleck(ctx, p, a) {
      ctx.fillStyle = p.c + a + ')';
      ctx.beginPath(); ctx.moveTo(-p.s, -p.s * 0.5); ctx.lineTo(p.s * 0.8, -p.s * 0.9);
      ctx.lineTo(p.s, p.s * 0.6); ctx.lineTo(-p.s * 0.6, p.s * 0.9); ctx.closePath(); ctx.fill();
    },
    // wood shaving: a curled partial-circle stroke
    shaving(ctx, p, a) {
      ctx.strokeStyle = p.c + a + ')'; ctx.lineWidth = Math.max(0.9, p.s * 0.3);
      ctx.beginPath(); ctx.arc(0, 0, p.s, 0.4, 4.4); ctx.stroke();
    },
  };

  // ---- themes: which materials, in which colors, at what balance --------------
  // Entry: [species, rgbaPrefix, share, rise?, sizeLo, sizeHi, alpha, speedLo, speedHi, glow?]
  const T = {
    rain: [
      ['streak', 'rgba(195,204,214,', 0.62, false, 3, 7, 0.34, 120, 210],
      ['mote',   'rgba(195,204,214,', 0.30, true,  0.8, 1.8, 0.22, 12, 26],
      ['mote',   'rgba(224,164,88,',  0.08, true,  1, 1.8, 0.3, 10, 20, true],
    ],
    embers: [
      ['mote', 'rgba(232,120,74,',  0.55, true,  1.2, 3, 0.5, 18, 55, true],
      ['mote', 'rgba(255,190,140,', 0.13, true,  0.8, 1.6, 0.5, 24, 60, true],
      ['mote', 'rgba(127,180,216,', 0.32, false, 1, 2.4, 0.3, 10, 30],
    ],
    bubbles: [
      ['bubble', 'rgba(63,184,168,',  0.52, true,  2, 6, 0.4, 16, 44],
      ['mote',   'rgba(111,208,195,', 0.28, true,  0.8, 1.6, 0.32, 20, 46],
      ['mote',   'rgba(184,115,51,',  0.20, false, 1, 2, 0.3, 10, 26, true],
    ],
    dust: [
      ['mote',  'rgba(245,166,35,',  0.44, true,  0.9, 2.2, 0.32, 8, 22, true],
      ['mote',  'rgba(170,178,186,', 0.38, false, 1, 2.6, 0.26, 8, 20],
      ['fleck', 'rgba(198,204,210,', 0.18, false, 1.4, 2.6, 0.22, 12, 26],
    ],
    motes: [
      ['mote',   'rgba(95,179,212,', 0.46, true, 1, 2.4, 0.36, 10, 26, true],
      ['mote',   'rgba(217,196,143,',0.34, true, 0.9, 2, 0.3, 8, 22],
      ['bubble', 'rgba(230,216,178,',0.20, true, 2, 4.5, 0.3, 14, 32],
    ],
    pigment: [
      ['fleck', 'rgba(217,166,43,', 0.46, false, 1.4, 3.2, 0.38, 14, 34],
      ['fleck', 'rgba(244,239,230,',0.32, false, 1.2, 2.6, 0.3, 12, 30],
      ['fleck', 'rgba(138,90,116,', 0.22, false, 1.2, 2.6, 0.32, 12, 30],
    ],
    shavings: [
      ['shaving', 'rgba(200,155,102,', 0.5, false, 2.4, 5.5, 0.4, 16, 38],
      ['mote',    'rgba(221,211,194,', 0.3, true,  0.8, 1.8, 0.28, 10, 24],
      ['mote',    'rgba(90,125,90,',   0.2, true,  1, 2, 0.26, 8, 20],
    ],
    // Grass and rain lead the medley three-to-one over every other material:
    // shares are tuned against the homepage's data-n="90" so blades and streaks
    // run at triple their original absolute counts while the rest hold steady.
    medley: [
      ['blade',   'rgba(34,178,76,',   0.27, false, 2.4, 4.6, 0.34, 14, 30],
      ['streak',  'rgba(107,127,148,', 0.22, false, 2.6, 5, 0.24, 90, 150],
      ['mote',    'rgba(232,120,74,',  0.08, true,  1, 2.2, 0.4, 14, 40, true],
      ['bubble',  'rgba(63,184,168,',  0.07, true,  2, 4.6, 0.32, 14, 34],
      ['mote',    'rgba(245,166,35,',  0.07, true,  0.9, 2, 0.3, 8, 22],
      ['mote',    'rgba(95,179,212,',  0.07, true,  1, 2.2, 0.32, 10, 26, true],
      ['fleck',   'rgba(217,166,43,',  0.06, false, 1.2, 2.6, 0.3, 12, 28],
      ['shaving', 'rgba(200,155,102,', 0.06, false, 2.2, 4.6, 0.32, 14, 32],
      ['mote',    'rgba(22,179,100,',  0.10, true,  1, 2.4, 0.34, 10, 26, true],
    ],
  };
  const theme = T[themeName] || T.medley;

  // ---- canvas ----------------------------------------------------------------
  const cv = document.createElement('canvas');
  cv.id = 'drift'; cv.setAttribute('aria-hidden', 'true');
  cv.style.cssText = `position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:${zIndex}`;
  const mount = () => document.body.appendChild(cv);
  document.body ? mount() : addEventListener('DOMContentLoaded', mount);
  const ctx = cv.getContext('2d');
  let W = 0, H = 0;
  function size() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = innerWidth; H = innerHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  size(); addEventListener('resize', size);

  // ---- field -----------------------------------------------------------------
  const baseN = +(me?.dataset.n || 0) || 60;
  const N = Math.round(innerWidth < 768 ? baseN / 2 : baseN);
  function pick() {
    let r = Math.random(), acc = 0;
    for (const e of theme) { acc += e[2]; if (r <= acc) return e; }
    return theme[theme.length - 1];
  }
  function mk(initial) {
    const [sp, c, , rise, lo, hi, alpha, vLo, vHi, glow] = pick();
    const s = rnd(lo, hi);
    return {
      sp, c, glow: !!glow, rise, s,
      x: rnd(-20, W + 20),
      y: initial ? rnd(0, H) : (rise ? H + rnd(10, 50) : -rnd(10, 50)),
      vy: (rise ? -1 : 1) * rnd(vLo, vHi),
      amp: rnd(5, 22), freq: rnd(0.3, 1.1), ph: rnd(0, 6.283),
      rot: rnd(0, 6.283), rotV: rnd(-0.9, 0.9),
      a: alpha, flick: rnd(2, 6),
    };
  }
  const ps = [];
  for (let i = 0; i < N; i++) ps.push(mk(true));
  window.__driftCount = N;

  let last = performance.now(), lastScroll = scrollY;
  function frame(now) {
    requestAnimationFrame(frame);
    if (document.hidden) { last = now; lastScroll = scrollY; return; }
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    const ds = scrollY - lastScroll; lastScroll = scrollY;
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < ps.length; i++) {
      const p = ps[i];
      p.y += p.vy * dt - ds * (p.s / 7) * 0.5;
      p.x += Math.sin((now / 1000) * p.freq + p.ph) * p.amp * dt;
      p.rot += p.rotV * dt;
      if (p.y < -70 || p.y > H + 70 || p.x < -50 || p.x > W + 50) { ps[i] = mk(false); continue; }
      const a = Math.max(0.05, p.a + Math.sin((now / 1000) * p.flick + p.ph) * p.a * 0.45);
      ctx.save(); ctx.translate(p.x, p.y);
      // streaks keep their fall angle; everything else tumbles
      if (p.sp !== 'streak' && p.sp !== 'blade') ctx.rotate(p.rot);
      else if (p.sp === 'blade') ctx.rotate(Math.sin((now / 1000) * p.freq + p.ph) * 0.5);
      SPECIES[p.sp](ctx, p, +a.toFixed(3));
      ctx.restore();
    }
  }
  requestAnimationFrame(frame);
})();
