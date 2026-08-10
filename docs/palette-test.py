from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np

SRC, WORD = 'blueB.png', 'BIG SIPPY'
YLO, YHI = 940, 1086
FP = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

base = Image.open(SRC).convert('RGB')
a0 = np.array(base).astype(int)
R,G,B = a0[:,:,0], a0[:,:,1], a0[:,:,2]
bandmask_full = (R > 110) & (R - G > 55) & (R - B > 55)
sub = bandmask_full[YLO:YHI+1]
cols = np.nonzero(sub.sum(axis=0) > 3)[0]
csp  = np.split(cols, np.nonzero(np.diff(cols) > 6)[0] + 1)
crun = max(csp, key=len); X0, X1 = int(crun[0]), int(crun[-1])

# body mask: the light-blue pouch region (blue dominant, bright)
bodymask = (B > 120) & (B - R > 20) & (B - G > 5)

def render(body, band, text):
    a = a0.copy()
    if body is not None:
        px = a[bodymask]
        lum = px.mean(axis=1, keepdims=True)
        lum = (lum - lum.min()) / max(1.0, (lum.max() - lum.min()))
        a[bodymask] = np.clip(np.array(body)[None,:] * (0.72 + 0.45*lum), 0, 255)
    reg = a[YLO:YHI+1, X0:X1+1]
    m   = sub[:, X0:X1+1]
    lum = reg.mean(axis=2, keepdims=True)
    lum = (lum - lum.min()) / max(1.0, (lum.max() - lum.min()))
    reg[m] = np.clip(np.array(band)[None,:] * (0.80 + 0.30*lum), 0, 255)[m]
    a[YLO:YHI+1, X0:X1+1] = reg
    im = Image.fromarray(a.astype('uint8')); d = ImageDraw.Draw(im)
    d.rectangle([X0+8, YLO+18, X1-8, YHI-18], fill=band)
    best = 8
    for s in range(10, 400, 2):
        f = ImageFont.truetype(FP, s); bb = d.textbbox((0,0), WORD, font=f)
        if bb[2]-bb[0] > (X1-X0)*0.82 or bb[3]-bb[1] > (YHI-YLO)*0.42: break
        best = s
    f = ImageFont.truetype(FP, best); bb = d.textbbox((0,0), WORD, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((X0+((X1-X0)-tw)//2-bb[0], YLO+((YHI-YLO)-th)//2-bb[1]), WORD, font=f, fill=text)
    return im

def sodium(im):
    """Approximate high-pressure sodium street lighting: warm cast, crushed blues, low sat."""
    a = np.array(im).astype(float)
    a[:,:,0] *= 1.18; a[:,:,1] *= 0.90; a[:,:,2] *= 0.42
    a = np.clip(a, 0, 255)
    im2 = Image.fromarray(a.astype('uint8'))
    im2 = ImageEnhance.Brightness(im2).enhance(0.55)
    return ImageEnhance.Color(im2).enhance(0.65)

BLUE  = (150, 205, 235)
CANDS = [
 ('A  blue / red / white',    None,        (176,32,64),  (255,255,255)),
 ('B  blue / red / yellow',   None,        (176,32,64),  (250,214,60)),
 ('C  blue / navy / white',   None,        (26,44,98),   (255,255,255)),
 ('D  blue / black / white',  None,        (24,22,26),   (255,255,255)),
 ('E  white / red / white',   (238,238,232),(176,32,64), (255,255,255)),
 ('F  blue / yellow / black', None,        (245,200,20), (20,18,16)),
]

tiles_day, tiles_night, labels = [], [], []
for lab, body, band, text in CANDS:
    im = render(body, band, text)
    w,h = im.size
    c = im.crop((int(w*0.28), int(h*0.40), int(w*0.72), int(h*0.56)))
    c = c.resize((300, int(300*c.height/c.width)))
    tiles_day.append(c); tiles_night.append(sodium(c)); labels.append(lab)

TW, TH = tiles_day[0].size
pad, lblh = 10, 26
grid = Image.new('RGB', (TW*3 + pad*4, (TH+lblh)*4 + pad*5), (242,240,236))
d = ImageDraw.Draw(grid)
lf = ImageFont.truetype(FP, 13)
for i,(td,tn,lab) in enumerate(zip(tiles_day,tiles_night,labels)):
    col, row = i % 3, i // 3
    x = pad + col*(TW+pad); y = pad + row*2*(TH+lblh+pad)
    d.text((x, y), lab + '   DAYLIGHT', font=lf, fill=(40,38,44)); grid.paste(td, (x, y+lblh))
    y2 = y + TH + lblh + pad
    d.text((x, y2), lab + '   NIGHT / SODIUM', font=lf, fill=(40,38,44)); grid.paste(tn, (x, y2+lblh))
grid.save('palette_grid.png'); print('grid', grid.size)

# ── refinement: which red holds white type best, day and night ──
REDS = [('current  B02040',(176,32,64)), ('deeper  8C0F28',(140,15,40)),
        ('brighter D81E2C',(216,30,44)), ('vermilion E63512',(230,53,18))]
td, tn, lb = [], [], []
for lab, rgb in REDS:
    im = render(None, rgb, (255,255,255)); w,h = im.size
    c = im.crop((int(w*0.28), int(h*0.40), int(w*0.72), int(h*0.56)))
    c = c.resize((300, int(300*c.height/c.width)))
    td.append(c); tn.append(sodium(c)); lb.append(lab)
TW,TH = td[0].size; pad,lblh = 10,26
g2 = Image.new('RGB', (TW*4+pad*5, (TH+lblh)*2+pad*3), (242,240,236))
d2 = ImageDraw.Draw(g2); lf2 = ImageFont.truetype(FP, 13)
for i,(a_,b_,l_) in enumerate(zip(td,tn,lb)):
    x = pad+i*(TW+pad)
    d2.text((x,pad), l_+'  DAY', font=lf2, fill=(40,38,44)); g2.paste(a_, (x,pad+lblh))
    y2 = pad+TH+lblh+pad
    d2.text((x,y2), l_+'  NIGHT', font=lf2, fill=(40,38,44)); g2.paste(b_, (x,y2+lblh))
g2.save('red_grid.png'); print('red grid', g2.size)
