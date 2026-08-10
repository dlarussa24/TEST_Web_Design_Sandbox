from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys

SRC, WORD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
YLO, YHI = int(sys.argv[4]), int(sys.argv[5])   # band row range, measured

im = Image.open(SRC).convert('RGB')
a  = np.array(im).astype(int)
R,G,B = a[:,:,0], a[:,:,1], a[:,:,2]
mask = (R > 110) & (R - G > 55) & (R - B > 55)

sub = mask[YLO:YHI+1]
cols = np.nonzero(sub.sum(axis=0) > 3)[0]
csp  = np.split(cols, np.nonzero(np.diff(cols) > 6)[0] + 1)
crun = max(csp, key=len)
x0, x1 = int(crun[0]), int(crun[-1])
print(f'band x {x0}-{x1} y {YLO}-{YHI}  ({x1-x0} x {YHI-YLO})')

med = tuple(int(v) for v in np.median(a[YLO:YHI+1, x0:x1+1][sub[:, x0:x1+1]], axis=0))
print('median red', med)

d = ImageDraw.Draw(im)
inset_x = max(2, (x1-x0)//40)
inset_y = max(2, (YHI-YLO)//8)
d.rectangle([x0+inset_x, YLO+inset_y, x1-inset_x, YHI-inset_y], fill=med)

target_w = int((x1-x0) * 0.82)
target_h = int((YHI-YLO) * 0.42)
fp = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
best = 8
for size in range(10, 400, 2):
    f = ImageFont.truetype(fp, size)
    bb = d.textbbox((0,0), WORD, font=f)
    if bb[2]-bb[0] > target_w or bb[3]-bb[1] > target_h: break
    best = size
f = ImageFont.truetype(fp, best)
bb = d.textbbox((0,0), WORD, font=f)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
d.text((x0 + ((x1-x0)-tw)//2 - bb[0], YLO + ((YHI-YLO)-th)//2 - bb[1]),
       WORD, font=f, fill=(255,255,255))
im.save(OUT); print('wrote', OUT, 'font', best)
