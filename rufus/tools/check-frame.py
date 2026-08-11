"""Gate a Rufus frame against the locked designs.
usage: python3 check_frame.py image.png            (single frame)
       python3 check_frame.py clip.mp4 --video     (samples 6 frames across the clip)

Checks what is measurable: BIG SIPPY body colour, band orientation, and the
presence of the navy cap. Identity itself is held by the reference chain, not
by this script — see the notes at the bottom of the output.
"""
import sys, numpy as np
from PIL import Image

POUCH  = np.array([150, 110, 205])   # #966ECD
CAP    = np.array([28,  42,  86])    # navy
CANON_HUE = 265.3                    # hue of #966ECD, the property that must hold


def rgb_hue_sat(c):
    r, g, b = (float(v) / 255 for v in c)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 1e-6:
        return 0.0, 0.0
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60.0, d / mx if mx > 0 else 0.0

def load(path):
    return np.array(Image.open(path).convert('RGB')).astype(int)

def check(a, label=''):
    h, w = a.shape[:2]
    R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
    fails = []

    # ---- BIG SIPPY: find the yellow band, then sample the body around it
    yellow = (R > 170) & (G > 150) & (R - B > 90) & (G - B > 80)
    if yellow.sum() < 400:
        fails.append('pouch: no yellow band found')
    else:
        purple_m = (B - G > 30) & (B > 80) & (R < B)
        best = None
        for y in range(0, h, 80):
            for x in range(0, w, 80):
                ys_, xs_ = slice(y, y+240), slice(x, x+240)
                yc = int(yellow[ys_, xs_].sum())
                if yc < 200: continue
                pc = int(purple_m[ys_, xs_].sum())
                score = yc * min(pc, 6000)          # band must sit near purple
                if best is None or score > best[0]:
                    best = (score, x, y)
        if best is None:
            fails.append('pouch: no yellow band adjacent to purple')
            cx = cy = None
        else:
            _, cx, cy = best
    if yellow.sum() >= 400 and cx is not None:
        x0, y0 = max(0, cx-160), max(0, cy-160)
        x1, y1 = min(w, cx+300), min(h, cy+300)
        reg, ry = a[y0:y1, x0:x1], yellow[y0:y1, x0:x1]
        # Trace the WHOLE band, not just the part inside this window: fitting
        # a slope to a clipped fragment exaggerates whatever section the
        # window happens to catch.
        from scipy import ndimage as _ndi
        lab, _n = _ndi.label(yellow)
        blk = lab[cy:cy+240, cx:cx+240]
        ids, counts = np.unique(blk[blk > 0], return_counts=True)
        full = lab == ids[np.argmax(counts)] if ids.size else ry
        ys, xs = np.nonzero(full)
        ry_full = full
        # Orientation, not shape. The bounding-box aspect test punished a band
        # that sags as the bag slumps — which is the realism the design wants,
        # and still a level band ON the pouch. Fit a line through the band's
        # per-column centreline instead: sag bends the line's residuals, but
        # only a rotated band tilts its slope.
        # Use the envelope midline (top+bottom)/2, not the yellow-pixel mean:
        # lettering printed on the band punches holes in the yellow mask and
        # drags per-column means around, which once pushed a level band to
        # the tilt threshold. The band's edges don't move when ink is on it.
        centers_x, centers_y = [], []
        for x in range(xs.min(), xs.max() + 1):
            col = np.nonzero(ry_full[:, x])[0]
            if col.size >= 4:
                centers_x.append(x)
                centers_y.append((col.min() + col.max()) / 2)
        if len(centers_x) < 20:
            fails.append('pouch: band too fragmentary to trace')
        else:
            # Fit the CENTRAL 60% of the run. At the pouch's side seams the
            # band wraps away from the camera and curls up or down — that
            # wrap read as ~20 deg of "tilt" on a band whose front face is
            # level. Rotation shows up in the middle; wrap lives at the ends.
            n_c = len(centers_x)
            lo, hi = int(n_c * 0.2), int(n_c * 0.8)
            slope = np.polyfit(centers_x[lo:hi], centers_y[lo:hi], 1)[0]
            tilt = abs(np.degrees(np.arctan(slope)))
            # Threshold calibrated on the library, not chosen a priori:
            # approved frames of a slumped bag measure 20-24 deg here (the
            # slump is real drape, and it is wanted), while the genuinely
            # diagonal defect frames measure 40+. The boundary sits between
            # the clusters.
            if tilt > 30:
                fails.append(f'pouch: band tilted {tilt:.0f} deg')
        body = (~ry) & (reg[:,:,2] - reg[:,:,1] > 30) & (reg[:,:,2] > 80)
        if body.sum() < 300:
            fails.append('pouch: no purple body around the band')
        else:
            med = np.median(reg[body], axis=0).astype(int)
            # Gate on HUE, not on distance to the swatch. Distance conflates
            # design drift with the scene's light: a correct pouch in a dim
            # shop sits 60-90 from #966ECD and fails, while the same reading
            # passes in daylight. Hue survives the lighting, which is exactly
            # the property a brand colour needs.
            hue, sat = rgb_hue_sat(med)
            dh = abs((hue - CANON_HUE + 180) % 360 - 180)
            if dh > 14:
                fails.append(f'pouch: hue {hue:.0f} is {dh:.0f} off canon '
                             f'{CANON_HUE:.0f} {tuple(med)}')
            elif sat < 0.25:
                fails.append(f'pouch: colour washed out, sat {sat:.2f}')

    # ---- RUFUS: navy cap present in the upper half
    top = a[:int(h*0.6)]
    navy = ((top[:,:,2] > top[:,:,0] + 25) & (top[:,:,2] > top[:,:,1] + 15)
            & (top[:,:,2] > 45) & (top[:,:,2] < 165) & (top.mean(axis=2) < 120))
    if navy.sum() < 900:
        fails.append(f'rufus: navy cap not detected ({int(navy.sum())} px)')

    tag = f'[{label}] ' if label else ''
    if fails:
        for f in fails: print(f'{tag}FAIL  {f}')
    else:
        print(f'{tag}PASS  pouch + cap within spec')
    return not fails

if len(sys.argv) > 2 and sys.argv[2] == '--video':
    import imageio.v2 as iio
    rd = iio.get_reader(sys.argv[1]); fr = [np.asarray(x).astype(int) for x in rd]
    n = len(fr); idx = [0, n//5, 2*n//5, 3*n//5, 4*n//5, n-1]
    results = [check(fr[i], f'f{i}') for i in idx]
    ok = all(results)
    print(f'\n{sum(results)}/{len(results)} sampled frames passed')
else:
    ok = check(load(sys.argv[1]))

print('\nNote: identity consistency (proportions, markings, no human hands) is not')
print('machine-checkable here. It is held by passing an approved frame as an')
print('image reference on every generation, plus eyes-on review before publish.')
sys.exit(0 if ok else 1)
