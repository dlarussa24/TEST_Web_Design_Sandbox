from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
SRC, WORD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(SRC).convert('RGB'); a = np.array(im).astype(int)
R,G,B = a[:,:,0], a[:,:,1], a[:,:,2]
mask = (R > 150) & (G > 130) & (R - B > 85) & (G - B > 75)
rc = mask.sum(axis=1)
rows = np.nonzero(rc >= max(8, rc.max()*0.25))[0]
run  = max(np.split(rows, np.nonzero(np.diff(rows) > 4)[0]+1), key=len)
y0,y1 = int(run[0]), int(run[-1])

# close holes: for each band row, fill between its leftmost and rightmost yellow pixel
solid = np.zeros_like(mask)
for y in range(y0, y1+1):
    xs = np.nonzero(mask[y])[0]
    if xs.size < 6: continue
    solid[y, xs.min():xs.max()+1] = True
# inset a few px so the fill never reaches the band's outer edge
INS = 4
for y in range(y0, y1+1):
    xs = np.nonzero(solid[y])[0]
    if xs.size == 0: continue
    solid[y, :xs.min()+INS] = False; solid[y, xs.max()-INS+1:] = False
solid[y0:y0+INS] = False; solid[max(y0,y1-INS+1):y1+1] = False

cols = np.nonzero(solid[y0:y1+1].sum(axis=0) > 2)[0]
x0, x1 = int(cols.min()), int(cols.max())
med = tuple(int(v) for v in np.median(a[mask], axis=0))
a[solid] = med
im = Image.fromarray(a.astype('uint8')); d = ImageDraw.Draw(im)
FP='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; best=8
for s in range(10,400,2):
    f=ImageFont.truetype(FP,s); bb=d.textbbox((0,0),WORD,font=f)
    if bb[2]-bb[0] > (x1-x0)*0.86 or bb[3]-bb[1] > (y1-y0)*0.46: break
    best=s
f=ImageFont.truetype(FP,best); bb=d.textbbox((0,0),WORD,font=f)
tw,th=bb[2]-bb[0],bb[3]-bb[1]
d.text((x0+((x1-x0)-tw)//2-bb[0], y0+((y1-y0)-th)//2-bb[1]), WORD, font=f, fill=(18,16,20))
im.save(OUT); print('wrote',OUT,'band',x1-x0,'x',y1-y0,'font',best)
