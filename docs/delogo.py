"""Paint out a rendered trademark, leaving plain fabric behind.

Why this exists: "navy baseball cap" is a near-synonym for one specific team's
cap in the training data. Across a five-frame test round the interlocking NY
mark rendered in three of them, twice on Rufus and once on a bystander, in
spite of "plain navy baseball cap with NO logo and NO lettering". Negatives do
not suppress it — the same lesson as the ear notch, in the other direction:
the model volunteers detail it has strongly associated, and prompt text will
not talk it out of it.

Two responses, and both are needed. Long term the canon should stop asking for
the cap that summons the mark. Short term any frame already generated can be
cleaned here: inside a given box this finds the pixels markedly lighter than
the surrounding fabric, fills them from that fabric, and re-lays grain so the
patch does not read as a smooth blot on a noisy photo.

usage: python3 delogo.py in.png out.png --box=x0,y0,x1,y1 [--box=...]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage


def delogo(rgb, box, lift=28):
    """Remove light-on-dark marking inside box. Returns (rgb, pixels_filled)."""
    x0, y0, x1, y1 = box
    reg = rgb[y0:y1, x0:x1].astype(np.float32)
    lum = reg.mean(2)

    # The fabric is the dark majority; the mark is the light minority. Taking
    # the 45th percentile as "fabric" keeps the estimate away from both the
    # mark and any specular highlight on the crown.
    fabric_lum = np.percentile(lum, 45)
    mark = lum > fabric_lum + lift
    if mark.sum() < 20:
        return rgb, 0

    # Keep only the mark itself. A box drawn slightly wide will also catch the
    # bright wall behind the cap, and filling that leaves a dark rectangle
    # hanging in mid-air — so drop blobs that touch the box edge, which is what
    # spill looks like, and keep the compact ones.
    lab, n = ndimage.label(mark)
    if n:
        edge = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
        keep = np.zeros_like(mark)
        for k in range(1, n + 1):
            if k in edge:
                continue
            keep |= lab == k
        mark = keep
    if mark.sum() < 20:
        return rgb, 0

    # grow slightly so the mark's antialiased rim goes too
    mark = ndimage.binary_dilation(mark, iterations=3)

    fabric_px = reg[~mark]
    if len(fabric_px) < 50:
        return rgb, 0
    base = np.median(fabric_px, 0)
    # Photographic grain is close to monochrome. Drawing it per channel tints
    # the patch and it reads as coloured speckle against flat fabric.
    noise_sd = float(fabric_px.std(0).mean()) * 0.5

    # Fill with the local fabric colour rather than one flat value, so the
    # crown's shading gradient survives across the patch.
    filled = reg.copy()
    filled[mark] = base
    smooth = np.stack([ndimage.gaussian_filter(filled[:, :, c], 9)
                       for c in range(3)], 2)

    rng = np.random.default_rng(7)
    grain = rng.normal(0, max(noise_sd, 1.5), reg.shape[:2])[:, :, None]
    patch = smooth + grain

    alpha = ndimage.gaussian_filter(mark.astype(np.float32), 2)[:, :, None]
    out = reg * (1 - alpha) + patch * alpha
    rgb = rgb.copy()
    rgb[y0:y1, x0:x1] = np.clip(out, 0, 255).astype(np.uint8)
    return rgb, int(mark.sum())


def main():
    src, dst = sys.argv[1], sys.argv[2]
    boxes = [tuple(int(v) for v in a.split('=', 1)[1].split(','))
             for a in sys.argv if a.startswith('--box=')]
    if not boxes:
        sys.exit('need at least one --box=x0,y0,x1,y1')

    rgb = np.array(Image.open(src).convert('RGB'))
    for b in boxes:
        rgb, n = delogo(rgb, b)
        print(f'box {b}: filled {n} px' if n else f'box {b}: nothing to remove')
    Image.fromarray(rgb).save(dst)
    print(f'wrote {dst}')


if __name__ == '__main__':
    main()
