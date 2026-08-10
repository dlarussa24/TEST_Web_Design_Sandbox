"""Reject frames where the BIG SIPPY pouch drifts off spec.
usage: python3 check_pouch.py image.png"""
import sys, numpy as np
from PIL import Image

TARGET = np.array([150, 110, 205])          # #966ECD
im = Image.open(sys.argv[1]).convert('RGB')
a  = np.array(im).astype(int); h, w = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

yellow = (R > 170) & (G > 150) & (R - B > 90) & (G - B > 80)
if yellow.sum() < 400:
    print('FAIL  no yellow band found'); sys.exit(1)

# densest yellow block = the band
best = max(((yellow[y:y+220, x:x+220].sum(), x, y)
            for y in range(0, h, 100) for x in range(0, w, 100)))
_, cx, cy = best
x0, y0 = max(0, cx-160), max(0, cy-160)
x1, y1 = min(w, cx+300), min(h, cy+300)
reg, ry = a[y0:y1, x0:x1], yellow[y0:y1, x0:x1]

# band orientation: wider than tall = horizontal
ys, xs = np.nonzero(ry)
bw, bh = xs.max()-xs.min(), ys.max()-ys.min()
horiz = bw > bh * 1.4

# body colour: blue-dominant pixels around the band
body = (~ry) & (reg[:,:,2] - reg[:,:,1] > 30) & (reg[:,:,2] > 80)
ok = True
if body.sum() < 300:
    print('FAIL  no purple body around the band'); ok = False
else:
    med = np.median(reg[body], axis=0).astype(int)
    dist = float(np.linalg.norm(med - TARGET))
    # magenta check: red must not dominate blue
    magenta = med[0] > med[2]
    print(f'body median RGB {tuple(med)}   distance from target {dist:.0f}')
    if magenta:
        print('FAIL  body is magenta/pink, not purple'); ok = False
    elif dist > 90:
        print('WARN  body drifted far from spec'); ok = False
    else:
        print('PASS  body colour within tolerance')
print('PASS  band is horizontal' if horiz else 'FAIL  band is not horizontal')
sys.exit(0 if (ok and horiz) else 1)
