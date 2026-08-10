"""Lock BIG SIPPY to canon colour in any still or clip.

The generation models will not hold a specific hue. Across the asset library
the pouch has rendered anywhere from blue (235 deg) to pink (333 deg) against a
canon of 265.3 deg. Prompt text reduces the spread but never closes it — the
same lesson as the band typography and the ear notch: props render, exact
design does not. So the design is enforced here, deterministically, after
generation.

What it does, per frame: finds the yellow band, derives the pouch body from the
purple above and below it, then rotates hue to canon and re-centres saturation
while leaving per-pixel VALUE untouched. Keeping value is the point — the
shading, the specular roll-off and the scene's light still read as real, only
the colour identity is pinned.

Auto-detection is only safe on clean frames. In a cluttered store the set
dressing is built from the same purples and yellows as the pouch, and testing
showed it lock onto a crisp packet in one frame and flat-fill a shelf item in
another. For anything busy, pass the pouch's bounding box.

usage: python3 lock-sippy.py in.png  out.png  [--box=x0,y0,x1,y1]
       python3 lock-sippy.py in.mp4  out.mp4  [--box=x0,y0,x1,y1] [--report]
"""
import sys
import numpy as np
from scipy import ndimage

# ---- canon, measured off the approved composite docs/rufus-pouch-final.png
CANON_BODY_H = 265.3 / 360.0
CANON_BODY_S = 0.46
CANON_BAND_H = 48.2 / 360.0
CANON_BAND_S = 0.95


def rgb_to_hsv(a):
    a = a.astype(np.float32) / 255.0
    mx, mn = a.max(2), a.min(2)
    d = mx - mn
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    h = np.zeros_like(mx)
    nz = d > 1e-6
    im = (mx == r) & nz
    h[im] = ((g - b)[im] / d[im]) % 6
    im = (mx == g) & nz
    h[im] = (b - r)[im] / d[im] + 2
    im = (mx == b) & nz
    h[im] = (r - g)[im] / d[im] + 4
    h /= 6.0
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
    return np.stack([h, s, mx], 2)


def hsv_to_rgb(hsv):
    h, s, v = hsv[:, :, 0] * 6.0, hsv[:, :, 1], hsv[:, :, 2]
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, q, v, v, q])
    return (np.clip(np.stack([r, g, b], 2), 0, 1) * 255).astype(np.uint8)


def largest(mask, min_px=250):
    """Biggest connected blob in mask, or None if nothing meets min_px."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return None
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    k = int(np.argmax(sizes)) + 1
    if sizes[k - 1] < min_px:
        return None
    return lab == k


# the pouch has rendered anywhere in this arc — blue through purple to pink.
# Anything outside it is scenery, not a drifted BIG SIPPY.
BODY_HUE_LO, BODY_HUE_HI = 200 / 360.0, 345 / 360.0


def _body_for(band, hsv):
    """Given a candidate band, return its pouch body mask or None.

    Scoped to a box around the band and to the plausible pouch hue arc, so a
    yellow snack packet sitting next to a red display cannot pose as a pouch.
    """
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    ys, xs = np.nonzero(band)
    bw = xs.max() - xs.min()
    bh = ys.max() - ys.min()
    if bw < bh * 1.4:                      # band must read horizontal
        return None

    cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
    half_w, half_h = int(bw * 0.62), int(bw * 0.95)
    H, W = h.shape
    box = np.zeros_like(band)
    box[max(0, cy - half_h):min(H, cy + half_h),
        max(0, cx - half_w):min(W, cx + half_w)] = True

    # Exclude the band itself (dilated past its antialiased rim), NOT its
    # whole rows. Row-exclusion cut the pouch in half: everything below the
    # band stayed unlocked and the result had a hard colour seam at the
    # band's top edge. Dark lettering inside the band is safe either way —
    # it falls below the value floor.
    box &= ~ndimage.binary_dilation(band, iterations=4)

    chroma = ((s > 0.20) & (v > 0.14) & box
              & (h > BODY_HUE_LO) & (h < BODY_HUE_HI))
    # The band splits the body into disconnected regions above and below it,
    # so take every sizeable blob rather than only the largest.
    lab, n = ndimage.label(chroma)
    if n == 0:
        return None
    sizes = ndimage.sum(chroma, lab, range(1, n + 1))
    body = np.isin(lab, [k + 1 for k in range(n) if sizes[k] >= 300])
    return body if body.sum() >= 300 else None


def find_pouch(hsv, box=None):
    """Return (band_mask, body_mask), or (None, None) if no pouch is visible.

    The band anchors everything — yellow is the most stable channel in
    generation — but a store full of yellow packaging offers many decoys, so
    each yellow blob is scored by how much pouch-coloured body hangs off it.

    Scoring is not enough on its own. Tested across the library it landed on a
    crisp packet in one frame and flat-filled a shelf item in another, because
    the set dressing is made of the same purples and yellows the pouch is. Pass
    an explicit `box` (x0,y0,x1,y1) for anything cluttered — auto-detect is a
    convenience for clean frames, not a guarantee.
    """
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    yellow = (h > 0.085) & (h < 0.195) & (s > 0.45) & (v > 0.45)
    if box is not None:
        x0, y0, x1, y1 = box
        keep = np.zeros_like(yellow)
        keep[y0:y1, x0:x1] = True
        yellow &= keep
    lab, n = ndimage.label(yellow)
    if n == 0:
        return None, None

    # Only the biggest few yellow blobs are worth testing. A busy store frame
    # can label thousands of them and each test is a full-region pass.
    sizes = ndimage.sum(yellow, lab, range(1, n + 1))
    order = [k for k in np.argsort(sizes)[::-1] + 1 if sizes[k - 1] >= 400][:12]

    best = None
    for k in order:
        band = lab == k
        body = _body_for(band, hsv)
        if body is None:
            continue
        score = int(sizes[k - 1]) * min(int(body.sum()), 40000)
        if best is None or score > best[0]:
            best = (score, band, body)

    if best is None:
        return None, None
    return best[1], best[2]


def feather(mask, px=2):
    f = ndimage.gaussian_filter(mask.astype(np.float32), px)
    return np.clip(f, 0, 1)[:, :, None]


def relock(rgb, canon_h, canon_s, mask):
    """Pin hue, re-centre saturation, leave value alone."""
    hsv = rgb_to_hsv(rgb)
    med_s = float(np.median(hsv[:, :, 1][mask]))
    scale = canon_s / max(med_s, 0.05)
    out = hsv.copy()
    out[:, :, 0] = canon_h
    out[:, :, 1] = np.clip(hsv[:, :, 1] * scale, 0, 1)
    fixed = hsv_to_rgb(out)
    a = feather(mask)
    return (rgb * (1 - a) + fixed * a).astype(np.uint8)


def lock_frame(rgb, box=None):
    """Returns (locked_rgb, before_hues) — before_hues is None if no pouch."""
    hsv = rgb_to_hsv(rgb)
    band, body = find_pouch(hsv, box)
    if band is None:
        return rgb, None
    before = (
        float(np.median(hsv[:, :, 0][band]) * 360),
        float(np.median(hsv[:, :, 0][body]) * 360) if body is not None else None,
    )
    out = relock(rgb, CANON_BAND_H, CANON_BAND_S, band)
    if body is not None:
        out = relock(out, CANON_BODY_H, CANON_BODY_S, body)
    return out, before


def parse_box(argv):
    for a in argv:
        if a.startswith('--box='):
            x0, y0, x1, y1 = (int(v) for v in a.split('=', 1)[1].split(','))
            return (x0, y0, x1, y1)
    return None


def main():
    src, dst = sys.argv[1], sys.argv[2]
    report = '--report' in sys.argv
    box = parse_box(sys.argv)

    if src.lower().endswith(('.mp4', '.mov', '.webm')):
        import imageio.v2 as iio
        rd = iio.get_reader(src)
        fps = rd.get_meta_data().get('fps', 24)
        frames = [np.asarray(f) for f in rd]
        out, misses, hues = [], 0, []
        for i, f in enumerate(frames):
            locked, before = lock_frame(f, box)
            out.append(locked)
            if before is None:
                misses += 1
            else:
                hues.append(before[1])
                if report and i % 12 == 0:
                    b = 'n/a' if before[1] is None else f'{before[1]:.1f}'
                    print(f'f{i:3d}  band {before[0]:5.1f}  body {b}')
        iio.mimwrite(dst, out, fps=fps, quality=9, macro_block_size=1)
        seen = [x for x in hues if x is not None]
        print(f'\n{len(frames)} frames, pouch located in {len(frames)-misses}')
        if seen:
            print(f'body hue before lock: {min(seen):.1f} to {max(seen):.1f} '
                  f'(spread {max(seen)-min(seen):.1f} deg)')
        print(f'body hue after  lock: {CANON_BODY_H*360:.1f} on every frame')
        if misses:
            print(f'WARNING: {misses} frames had no readable pouch and were '
                  f'passed through untouched')
    else:
        from PIL import Image
        rgb = np.array(Image.open(src).convert('RGB'))
        locked, before = lock_frame(rgb, box)
        if before is None:
            print('no pouch located — nothing changed')
        else:
            b = 'n/a' if before[1] is None else f'{before[1]:.1f}'
            print(f'band {before[0]:.1f} -> {CANON_BAND_H*360:.1f}   '
                  f'body {b} -> {CANON_BODY_H*360:.1f}')
        Image.fromarray(locked).save(dst)
    print(f'wrote {dst}')


if __name__ == '__main__':
    main()
