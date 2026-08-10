"""Embed the BIG SIPPY wordmark INTO the pouch surface, not over it.

The flat composite failed on realism: repainting the band with one solid
yellow and stamping straight text threw away every wrinkle, highlight and
shadow the generator had rendered, so the label read as a sticker pasted on
the photo. This does the opposite — the original band pixels are kept, and
the type is warped and lit by the surface it sits on:

  1. The band is located and its top/bottom edge traced per column, so the
     text baseline FOLLOWS the band as it wraps and dips with the pouch.
  2. The type is rendered straight, then resampled through that curve —
     each column of text bends with the fabric under it.
  3. Ink is applied multiplicatively, modulated by the band's own luminance:
     where the band falls into shadow the letters darken with it, where a
     specular highlight crosses the band it crosses the letters too.
  4. Edges are feathered and grained to sit in the photo's noise floor.

The purple body is expected to be hue-locked first (lock-sippy.py). This
script only touches pixels inside the located band.

usage: python3 embed-sippy.py in.png out.png "BIG SIPPY" [--box=x0,y0,x1,y1]
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

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
INK = np.array([24, 22, 30], dtype=np.float32)   # near-black navy, matches canon type


def trace_band(band):
    """Per-column smoothed top/bottom edge of the band. Returns (cols, top, bot)."""
    h, w = band.shape
    cols, top, bot = [], [], []
    for x in range(w):
        ys = np.nonzero(band[:, x])[0]
        if ys.size >= 8:
            cols.append(x)
            top.append(ys.min())
            bot.append(ys.max())
    cols = np.array(cols)
    top = ndimage.gaussian_filter1d(np.array(top, dtype=float), 9)
    bot = ndimage.gaussian_filter1d(np.array(bot, dtype=float), 9)
    return cols, top, bot


def render_type(word, wt=1600, ht=400):
    """Straight high-res alpha strip of the wordmark, centred with padding."""
    im = Image.new('L', (wt, ht), 0)
    d = ImageDraw.Draw(im)
    size = 8
    for s in range(10, ht, 2):
        f = ImageFont.truetype(FONT, s)
        bb = d.textbbox((0, 0), word, font=f)
        if bb[2] - bb[0] > wt * 0.92 or bb[3] - bb[1] > ht * 0.62:
            break
        size = s
    f = ImageFont.truetype(FONT, size)
    bb = d.textbbox((0, 0), word, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((wt - tw) // 2 - bb[0], (ht - th) // 2 - bb[1]), word, font=f, fill=255)
    return np.array(im, dtype=np.float32) / 255.0


def embed(rgb, word, box=None, span_frac=(0.08, 0.92)):
    hsv = locksippy.rgb_to_hsv(rgb)
    band, _ = locksippy.find_pouch(hsv, box)
    if band is None:
        raise SystemExit('no band located — pass --box')

    cols, top, bot = trace_band(band)
    # type spans the middle of the band's run, inset from the pouch edges.
    # Tighten the span when the band dips steeply near an edge — glyphs
    # resampled through a steep trace shear into kinks.
    n = len(cols)
    span = cols[int(n * span_frac[0]):int(n * span_frac[1])]
    x0, x1 = int(span[0]), int(span[-1])
    col_ix = {int(c): i for i, c in enumerate(cols)}

    strip = render_type(word)
    ht_s, wt_s = strip.shape

    out = rgb.astype(np.float32).copy()
    lum = hsv[:, :, 2]
    band_lum = float(np.median(lum[band]))

    alpha = np.zeros(rgb.shape[:2], dtype=np.float32)
    for x in range(x0, x1 + 1):
        i = col_ix.get(x)
        if i is None:
            continue
        yt, yb = top[i], bot[i]
        th = yb - yt
        if th < 6:
            continue
        # inset the type from the band edges so it never kisses the seam
        yt2, yb2 = yt + th * 0.16, yb - th * 0.16
        u = (x - x0) / max(1, x1 - x0)
        ys = np.arange(int(np.ceil(yt2)), int(np.floor(yb2)) + 1)
        if ys.size == 0:
            continue
        v = (ys - yt2) / max(1e-6, yb2 - yt2)
        su = min(wt_s - 1, int(u * (wt_s - 1)))
        sv = np.clip((v * (ht_s - 1)).astype(int), 0, ht_s - 1)
        a = strip[sv, su]
        keep = band[ys, x]           # never let ink leave the band
        alpha[ys, x] = a * keep

    # soften the resampled edges into the photo
    alpha = ndimage.gaussian_filter(alpha, 1.1)

    # ink lit by the surface: shadow and highlight pass through the letters
    shade = np.clip(lum / max(band_lum, 0.05), 0.35, 1.55)
    rng = np.random.default_rng(11)
    grain = rng.normal(0, 2.0, rgb.shape[:2])
    ink = INK[None, None, :] * shade[:, :, None] + grain[:, :, None]

    a3 = alpha[:, :, None]
    out = out * (1 - a3 * 0.92) + ink * (a3 * 0.92)
    return np.clip(out, 0, 255).astype(np.uint8), (x0, x1)


def main():
    src, dst, word = sys.argv[1], sys.argv[2], sys.argv[3]
    box, span_frac = None, (0.08, 0.92)
    for a in sys.argv:
        if a.startswith('--box='):
            box = tuple(int(v) for v in a.split('=', 1)[1].split(','))
        if a.startswith('--span='):
            span_frac = tuple(float(v) for v in a.split('=', 1)[1].split(','))
    rgb = np.array(Image.open(src).convert('RGB'))
    out, span = embed(rgb, word, box, span_frac)
    Image.fromarray(out).save(dst)
    print(f'embedded "{word}" across x {span[0]}-{span[1]}, wrote {dst}')


if __name__ == '__main__':
    main()
