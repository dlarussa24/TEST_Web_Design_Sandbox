from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys

SRC, WORD, OUT = 'blueB.png', 'BIG SIPPY', sys.argv[1]
FILL = tuple(int(x) for x in sys.argv[2].split(','))
TEXT = tuple(int(x) for x in sys.argv[3].split(','))
YLO, YHI = 940, 1086

im = Image.open(SRC).convert('RGB')
a  = np.array(im).astype(int)
R,G,B = a[:,:,0], a[:,:,1], a[:,:,2]
mask = (R > 110) & (R - G > 55) & (R - B > 55)
sub  = mask[YLO:YHI+1]
cols = np.nonzero(sub.sum(axis=0) > 3)[0]
csp  = np.split(cols, np.nonzero(np.diff(cols) > 6)[0] + 1)
crun = max(csp, key=len); x0, x1 = int(crun[0]), int(crun[-1])

# repaint the whole detected band area in the new colour, preserving the pouch's shading
band_px = a[YLO:YHI+1, x0:x1+1]
lum = band_px.mean(axis=2)
lum = (lum - lum.min()) / max(1.0, (lum.max() - lum.min()))   # 0..1 shading map
shade = 0.80 + 0.30 * lum[..., None]                           # keep some plastic modelling
newband = np.clip(np.array(FILL)[None, None, :] * shade, 0, 255)
region = a[YLO:YHI+1, x0:x1+1].copy()
region[sub[:, x0:x1+1]] = newband[sub[:, x0:x1+1]]
a[YLO:YHI+1, x0:x1+1] = region
im = Image.fromarray(a.astype('uint8'))

d = ImageDraw.Draw(im)
ix, iy = max(2,(x1-x0)//40), max(2,(YHI-YLO)//8)
d.rectangle([x0+ix, YLO+iy, x1-ix, YHI-iy], fill=FILL)
tw_target, th_target = int((x1-x0)*0.82), int((YHI-YLO)*0.42)
fp = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
best = 8
for s in range(10, 400, 2):
    f = ImageFont.truetype(fp, s); bb = d.textbbox((0,0), WORD, font=f)
    if bb[2]-bb[0] > tw_target or bb[3]-bb[1] > th_target: break
    best = s
f = ImageFont.truetype(fp, best); bb = d.textbbox((0,0), WORD, font=f)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
d.text((x0+((x1-x0)-tw)//2-bb[0], YLO+((YHI-YLO)-th)//2-bb[1]), WORD, font=f, fill=TEXT)
im.save(OUT); print('wrote', OUT)
