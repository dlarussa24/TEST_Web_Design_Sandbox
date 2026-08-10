"""BIG SIPPY pouch artwork — the two-word smile layout, applied in post.

Layout (from the approved character grid):
  - BIG sits large on the purple body above the band, in BAND YELLOW so it
    reads against the purple. B and G ride high, I dips — a shallow arc.
  - SIPPY sits INSIDE the yellow band as a smile: S and Y at the top of the
    curve, the middle P at the bottom. The I of BIG stacks directly over the
    middle P — both words centred on the pouch's centre column.
  - The body is unified to ONE purple: generators like to panel the pouch in
    two tones, so each body region's value is renormalised to the shared
    median while local texture stays.
  - The straw is shortened (75% less protrusion), thickened, and recoloured
    band-yellow, lit by its own luminance so the highlight survives.

Type is Liberation Sans Bold with a blur-and-threshold pass that rounds the
terminals — closer to the rounded grotesques juice brands actually print than
a raw DejaVu stamp. Every mark is lit by the surface underneath it
(multiply by local luminance), feathered, and grained into the photo.

usage: python3 sippy-artwork.py in.png out.png [--box=x0,y0,x1,y1]
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import importlib.util
import pathlib

_here = pathlib.Path(__file__).parent
_spec = importlib.util.spec_from_file_location('locksippy', _here / 'lock-sippy.py')
locksippy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(locksippy)

FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
NAVY_INK = np.array([24, 22, 30], dtype=np.float32)


# ---------------------------------------------------------------- glyphs

def glyph(ch, px, rot=0.0):
    """Rounded-terminal glyph alpha, rotated by `rot` degrees."""
    pad = px // 2
    f = ImageFont.truetype(FONT, px)
    im = Image.new('L', (px * 2 + pad, px * 2 + pad), 0)
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), ch, font=f)
    d.text((pad - bb[0], pad - bb[1]), ch, font=f, fill=255)
    a = np.array(im, dtype=np.float32) / 255.0
    # blur + threshold rounds the corners; radius scales with size
    a = ndimage.gaussian_filter(a, px * 0.03)
    a = np.clip((a - 0.42) * 6, 0, 1)
    if rot:
        a = ndimage.rotate(a, rot, reshape=True, order=1, prefilter=False)
    ys, xs = np.nonzero(a > 0.05)
    if ys.size == 0:
        return np.zeros((1, 1), np.float32)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def stamp(canvas_alpha, g, cx, cy):
    """Add glyph alpha g centred at (cx, cy) onto canvas_alpha."""
    h, w = g.shape
    y0, x0 = int(cy - h / 2), int(cx - w / 2)
    H, W = canvas_alpha.shape
    ya, yb = max(0, y0), min(H, y0 + h)
    xa, xb = max(0, x0), min(W, x0 + w)
    if ya >= yb or xa >= xb:
        return
    canvas_alpha[ya:yb, xa:xb] = np.maximum(
        canvas_alpha[ya:yb, xa:xb], g[ya - y0:yb - y0, xa - x0:xb - x0])


def word_arc(word, px, dip, rots, gap_frac=0.14):
    """Per-letter glyphs, x offsets, y offsets for an arc layout.

    dip: max downward offset (middle letters). rots: per-letter degrees.
    Returns list of (glyph, dx_center, dy_center) with dx relative to the
    word's centre.
    """
    n = len(word)
    mid = (n - 1) / 2
    gs = []
    for i, ch in enumerate(word):
        # arc profile: 0 at the ends, 1 in the middle
        t = 1 - abs(i - mid) / mid if mid > 0 else 1
        gs.append((glyph(ch, px, rots[i]), t))
    gap = px * gap_frac
    widths = [g.shape[1] for g, _ in gs]
    total = sum(widths) + gap * (n - 1)
    out, x = [], -total / 2
    for (g, t), w in zip(gs, widths):
        out.append((g, x + w / 2, t * dip))
        x += w + gap
    return out


# ---------------------------------------------------------------- surface ops

def lit_ink(rgb, hsv, alpha, ink, ref_lum, strength=0.94):
    """Blend ink onto rgb through alpha, lit by local luminance."""
    shade = np.clip(hsv[:, :, 2] / max(ref_lum, 0.05), 0.35, 1.55)
    rng = np.random.default_rng(23)
    grain = rng.normal(0, 2.0, rgb.shape[:2])
    layer = ink[None, None, :] * shade[:, :, None] + grain[:, :, None]
    a = ndimage.gaussian_filter(alpha, 1.0)[:, :, None] * strength
    return rgb * (1 - a) + layer * a


def unify_body(rgb, hsv, body):
    """One purple: renormalise each body region's value to the shared median."""
    v = hsv[:, :, 2]
    target = float(np.median(v[body]))
    lab, n = ndimage.label(body)
    out = rgb.astype(np.float32).copy()
    for k in range(1, n + 1):
        m = lab == k
        if m.sum() < 300:
            continue
        med = float(np.median(v[m]))
        scale = target / max(med, 0.05)
        if abs(scale - 1) < 0.06:
            continue
        # scale the region toward the shared tone, feathered at its edge
        a = ndimage.gaussian_filter(m.astype(np.float32), 3)[:, :, None]
        out = out * (1 - a) + (out * scale) * a
    return np.clip(out, 0, 255)


def rework_straw(rgb, hsv, body, band, yellow_med, straw_box,
                 keep_frac=0.25, widen=8):
    """Shorten the straw's protrusion, thicken it, recolour it band-yellow.

    The straw cannot be auto-detected: in the store frames it is optically
    merged with the white shelf trim and blown-out packaging highlights into
    one huge bright blob — two detection attempts recoloured the foil zip and
    a pouch-edge highlight before this was accepted. Same conclusion as the
    pouch itself in cluttered scenes: explicit geometry beats detection, so
    the caller passes the straw's bounding box and the tube is TRACKED
    through it row by row, each row keeping the bright run nearest the run
    above it.
    """
    if straw_box is None:
        return rgb, False
    sx0, sy0, sx1, sy1 = straw_box
    s, v = hsv[:, :, 1], hsv[:, :, 2]
    ys_b, _ = np.nonzero(body | band)
    top_p = ys_b.min()

    # track the tube row by row, then interpolate the centres over the full
    # run — gaps in the raw tracking left un-erased white fragments and
    # un-recoloured stripes on the first pass
    hits = []
    prev_c = (sx0 + sx1) / 2
    for y in range(sy0, min(sy1, s.shape[0])):
        row = (s[y, sx0:sx1] < 0.38) & (v[y, sx0:sx1] > 0.5)
        if not row.any():
            continue
        idx = np.nonzero(row)[0]
        splits = np.split(idx, np.nonzero(np.diff(idx) > 3)[0] + 1)
        runs = [r for r in splits if 4 <= r.size <= 60]
        if not runs:
            continue
        best_run = min(runs, key=lambda r: abs(r.mean() - (prev_c - sx0)))
        if abs(best_run.mean() - (prev_c - sx0)) > 45:
            continue
        hits.append((y, sx0 + best_run.mean(), best_run.size))
        prev_c = sx0 + best_run.mean()
    if len(hits) < 30:
        return rgb, False
    ys_h = np.array([h[0] for h in hits])
    cs_h = np.array([h[1] for h in hits])
    w_med = float(np.median([h[2] for h in hits]))
    y_all = np.arange(ys_h.min(), ys_h.max() + 1)
    c_all = np.interp(y_all, ys_h, cs_h)
    c_all = ndimage.gaussian_filter1d(c_all, 5)
    straw = np.zeros(s.shape, bool)
    for y, c in zip(y_all, c_all):
        straw[y, int(c - w_med / 2):int(c + w_med / 2) + 1] = True

    ys, xs = np.nonzero(straw)
    prot_rows = np.unique(ys[ys < top_p])
    out = rgb.astype(np.float32).copy()
    if prot_rows.size > 4:
        cut = int(top_p - prot_rows.size * keep_frac)
        # erase the straw above the cut, filling each row from the pixels
        # flanking the straw so the shelf blur behind it continues through.
        # The erase mask is dilated past the tube's antialiased halo — the
        # first pass filled only the tube core and left a pale ghost.
        erase = ndimage.binary_dilation(straw, np.ones((1, 9), bool))
        rng = np.random.default_rng(31)
        filled = np.zeros(out.shape[:2], bool)
        for y in prot_rows[prot_rows < cut]:
            row = np.nonzero(erase[y])[0]
            if row.size == 0:
                continue
            xl, xr = row.min(), row.max()
            w_r = xr - xl + 1
            # copy the texture strip beside the tube rather than blending a
            # gradient across it — the gradient version smeared a flat column
            # through the shelf detail behind the straw
            src0 = xl - w_r - 4
            if src0 >= 0:
                patch = out[y, src0:src0 + w_r]
            else:
                patch = out[y, xr + 4:xr + 4 + w_r]
                if patch.shape[0] < w_r:
                    patch = np.repeat(out[y, xr + 4:xr + 5], w_r, 0)
            out[y, xl:xl + patch.shape[0]] = patch + rng.normal(0, 2, patch.shape)
            filled[y, xl:xr + 1] = True
        # settle the seam: soften the filled area slightly so row-by-row
        # copies read as continuous out-of-focus background
        if filled.any():
            soft = np.stack([ndimage.gaussian_filter(out[:, :, c], 1.6)
                             for c in range(3)], 2)
            af = ndimage.gaussian_filter(filled.astype(np.float32), 2)[:, :, None]
            out = out * (1 - af) + soft * af
        straw = straw.copy()
        straw[:cut] = False

    # thicken what remains, taper the cut end into a rounded cap, then
    # recolour lit by the straw's own luminance so the tube highlight stays
    thick = ndimage.binary_dilation(straw, np.ones((1, widen * 2 + 1), bool))
    ys2 = np.nonzero(thick.any(1))[0]
    cap = 12
    for i, y in enumerate(range(ys2.min(), min(ys2.min() + cap, ys2.max()))):
        row = np.nonzero(thick[y])[0]
        if row.size == 0:
            continue
        c = (row.min() + row.max()) / 2
        half = (row.max() - row.min()) / 2 * np.sqrt(max(0.0, i / cap))
        keep = np.zeros_like(thick[y])
        keep[int(c - half):int(c + half) + 1] = True
        thick[y] &= keep
    lum = hsv[:, :, 2]
    med = float(np.median(lum[straw]))
    # floor at 0.7: segments of the tube that ran through shadow otherwise
    # recolour to near-black and read as dirt on the straw
    shade = np.clip(lum / max(med, 0.05), 0.7, 1.5)
    a = ndimage.gaussian_filter(thick.astype(np.float32), 1.2)[:, :, None]
    layer = yellow_med[None, None, :] * shade[:, :, None]
    out = out * (1 - a) + layer * a
    return np.clip(out, 0, 255), True


# ---------------------------------------------------------------- main

def main():
    src, dst = sys.argv[1], sys.argv[2]
    box = straw_box = None
    for arg in sys.argv:
        if arg.startswith('--box='):
            box = tuple(int(v) for v in arg.split('=', 1)[1].split(','))
        if arg.startswith('--straw='):
            straw_box = tuple(int(v) for v in arg.split('=', 1)[1].split(','))

    rgb = np.array(Image.open(src).convert('RGB')).astype(np.float32)
    hsv = locksippy.rgb_to_hsv(rgb.astype(np.uint8))
    band, body = locksippy.find_pouch(hsv, box)
    if band is None or body is None:
        raise SystemExit('pouch not located — pass --box')

    yellow_med = np.median(rgb[band], axis=0).astype(np.float32)

    # ---- the top fold renders pinker than the lock's hue arc reaches, so it
    # escapes every body pass and survives as a second colour. Catch it by
    # its own hue range, but only a blob wide enough to be the fold — the
    # shelf packets behind the pouch are pink too, and small.
    h_ch, s_ch, v_ch = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    ys_bd0, xs_bd0 = np.nonzero(band)
    bw0 = xs_bd0.max() - xs_bd0.min()
    ys_b0 = np.nonzero(body.any(1))[0]
    zone_f = np.zeros_like(body)
    if box is not None:
        zone_f[box[1]:ys_b0.min() + 200, box[0]:box[2]] = True
    else:
        zone_f[:ys_b0.min() + 200, :] = True
    pinkish = (h_ch > 290 / 360) & (s_ch > 0.2) & (v_ch > 0.14) & zone_f
    lab_f, n_f = ndimage.label(pinkish)
    fold = np.zeros_like(body)
    for k in range(1, n_f + 1):
        m = lab_f == k
        xs_f = np.nonzero(m.any(0))[0]
        if m.sum() > 2000 and xs_f.size > bw0 * 0.5:
            fold |= m
    if fold.any():
        rgb = locksippy.relock(rgb.astype(np.uint8),
                               locksippy.CANON_BODY_H, locksippy.CANON_BODY_S,
                               fold).astype(np.float32)
        hsv = locksippy.rgb_to_hsv(rgb.astype(np.uint8))
        body = body | fold

    # ---- one purple
    rgb = unify_body(rgb, hsv, body)
    hsv = locksippy.rgb_to_hsv(rgb.astype(np.uint8))

    # ---- geometry
    ys_bd, xs_bd = np.nonzero(band)
    rows = {}
    for y in range(ys_bd.min(), ys_bd.max() + 1):
        r = np.nonzero(band[y])[0]
        if r.size >= 6:
            rows[y] = (int(r.min()), int(r.max()))
    yk = sorted(rows)
    band_top, band_bot = yk[0], yk[-1]
    bh = band_bot - band_top
    core = yk[int(len(yk) * 0.25):int(len(yk) * 0.75)]
    cx = int(np.median([(rows[y][0] + rows[y][1]) / 2 for y in core]))

    # band centreline as a function of x, for anchoring SIPPY
    col_c = {}
    for y in yk:
        x0r, x1r = rows[y]
        for x in range(x0r, x1r + 1):
            col_c.setdefault(x, []).append(y)
    cxs = sorted(col_c)
    cline = {x: float(np.mean(col_c[x])) for x in cxs}

    # ---- BIG on the MAIN PANEL, band-yellow, shallow arc (I dips)
    # The panel is found by ROW COVERAGE, not connectivity: walking up from
    # the band, keep rows where the body still spans most of the band's
    # width. The walk stops at the foil zip, whose rows have almost no body
    # in them. (A connectivity version failed twice — the body is usually one
    # blob, and the fallback centred the word on the zip.)
    xs_bd0 = np.nonzero(band.any(0))[0]
    bx0, bx1 = xs_bd0.min(), xs_bd0.max()
    need = (bx1 - bx0) * 0.55
    panel_top = band_top - 10
    for y in range(band_top - 10, 0, -1):
        if body[y, bx0:bx1].sum() < need:
            break
        panel_top = y
    panel = body.copy()
    panel[:panel_top] = False
    panel[band_top:] = False

    avail = band_top - panel_top
    big_px = int(avail * 0.40)
    big_dip = big_px * 0.30
    big = word_arc('BIG', big_px, big_dip, rots=[-8, 0, 8], gap_frac=0.16)
    a_big = np.zeros(rgb.shape[:2], np.float32)
    big_cy = panel_top + avail * 0.48
    for g, dx, dy in big:
        stamp(a_big, g, cx + dx, big_cy + dy - big_dip / 2)
    a_big *= ndimage.binary_erosion(panel, iterations=2)  # stay on the panel
    hsv_now = locksippy.rgb_to_hsv(rgb.astype(np.uint8))
    body_lum = float(np.median(hsv_now[:, :, 2][body]))
    rgb = lit_ink(rgb, hsv_now, a_big, yellow_med, body_lum)

    # ---- SIPPY in the band, navy ink, riding the band's own curve
    # The band already sags — that sag IS the smile. Adding a second dip on
    # top of it pushed the middle letters out the bottom of the band. The
    # letters sit ON the centreline, sized from the band's thickness, each
    # rotated to the centreline's local slope so they lean into the curve.
    thick = {x: len(col_c[x]) for x in cxs}
    th_med = float(np.median(list(thick.values())))
    sip_px = int(th_med * 0.46)

    def local_rot(x):
        xa, xb = int(np.clip(x - 60, cxs[0], cxs[-1])), int(np.clip(x + 60, cxs[0], cxs[-1]))
        ya = cline.get(xa) or cline[min(cline, key=lambda k: abs(k - xa))]
        yb = cline.get(xb) or cline[min(cline, key=lambda k: abs(k - xb))]
        if xb == xa:
            return 0.0
        return -float(np.degrees(np.arctan2(yb - ya, xb - xa)))

    # lay letters flat first to learn their x offsets, then re-render each
    # with its local rotation
    flat = word_arc('SIPPY', sip_px, 0, rots=[0] * 5, gap_frac=0.12)
    a_sip = np.zeros(rgb.shape[:2], np.float32)
    for ch, (g0, dx, _) in zip('SIPPY', flat):
        x_here = int(np.clip(cx + dx, cxs[0], cxs[-1]))
        # size each letter from the band's LOCAL thickness — the band thins
        # toward its ends, and a uniform size clipped the Y where the band
        # curves away
        th_here = float(np.median([thick.get(int(np.clip(x_here + o, cxs[0], cxs[-1])), th_med)
                                   for o in range(-40, 41, 10)]))
        g = glyph(ch, max(24, int(th_here * 0.46)), local_rot(cx + dx))
        y_here = cline.get(x_here, (band_top + band_bot) / 2)
        stamp(a_sip, g, cx + dx, y_here)
    band_solid = np.zeros_like(band)
    for x in cxs:
        ys_c = col_c[x]
        band_solid[min(ys_c):max(ys_c) + 1, x] = True
    a_sip *= ndimage.binary_erosion(band_solid, iterations=2)  # never leave the band
    band_lum = float(np.median(hsv_now[:, :, 2][band]))
    rgb = lit_ink(rgb, hsv_now, a_sip, NAVY_INK, band_lum)

    # ---- straw
    hsv_now = locksippy.rgb_to_hsv(rgb.astype(np.uint8))
    rgb, straw_ok = rework_straw(rgb, hsv_now, body, band, yellow_med, straw_box)

    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(dst)
    print(f'wrote {dst}  (straw {"reworked" if straw_ok else "NOT FOUND"})')
    print(f'pouch centre x={cx}  band {band_top}-{band_bot}  BIG {big_px}px  SIPPY {sip_px}px')


if __name__ == '__main__':
    main()
