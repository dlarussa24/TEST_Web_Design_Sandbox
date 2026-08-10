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
        ys, xs = np.nonzero(ry)
        if not (xs.max()-xs.min() > (ys.max()-ys.min()) * 1.4):
            fails.append('pouch: band is not horizontal')
        body = (~ry) & (reg[:,:,2] - reg[:,:,1] > 30) & (reg[:,:,2] > 80)
        if body.sum() < 300:
            fails.append('pouch: no purple body around the band')
        else:
            med = np.median(reg[body], axis=0).astype(int)
            dist = float(np.linalg.norm(med - POUCH))
            if med[0] > med[2]:
                fails.append(f'pouch: body is magenta/pink {tuple(med)}')
            elif dist > 90:
                fails.append(f'pouch: body drifted {tuple(med)} dist {dist:.0f}')

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
