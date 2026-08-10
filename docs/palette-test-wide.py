exec(open('palette.py').read().split('# ── refinement')[0])
from PIL import Image, ImageDraw, ImageFont

BLUE = (150,205,235)
SYS = [
 ('0 CONTROL blue/red/white',   None,          (216,30,44),  (255,255,255)),
 ('G silver/red/white',         (196,199,204), (216,30,44),  (255,255,255)),
 ('H mint/red/white',           (168,224,190), (216,30,44),  (255,255,255)),
 ('I hotpink/white/red',        (240,110,170), (250,250,250),(200,25,40)),
 ('J purple/yellow/black',      (150,110,205), (248,205,30), (18,16,20)),
 ('K blue/hotpink/white',       None,          (232,52,140), (255,255,255)),
 ('L blue/white/black',         None,          (250,250,248),(18,16,20)),
 ('M cream/red/white',          (238,226,198), (216,30,44),  (255,255,255)),
 ('N teal/white/navy',          (60,175,180),  (250,250,248),(20,40,95)),
 ('P purple/white/purple',      (150,110,205), (250,250,248),(120,70,180)),
 ('Q lime/purple/white',        (200,230,90),  (110,55,165), (255,255,255)),
 ('R blue/orange/white',        None,          (240,120,25), (255,255,255)),
]

td, tn, lb = [], [], []
for lab, body, band, text in SYS:
    im = render(body, band, text); w,h = im.size
    c = im.crop((int(w*0.28), int(h*0.40), int(w*0.72), int(h*0.56)))
    c = c.resize((286, int(286*c.height/c.width)))
    td.append(c); tn.append(sodium(c)); lb.append(lab)

TW,TH = td[0].size; pad,lh = 9,22
COLS = 4; ROWS = (len(SYS)+COLS-1)//COLS
g = Image.new('RGB', (TW*COLS+pad*(COLS+1), ROWS*(2*(TH+lh)+pad*2)+pad), (242,240,236))
d = ImageDraw.Draw(g); f = ImageFont.truetype(FP, 12)
for i,(a_,b_,l_) in enumerate(zip(td,tn,lb)):
    col, row = i%COLS, i//COLS
    x = pad+col*(TW+pad); y = pad+row*(2*(TH+lh)+pad*2)
    d.text((x,y), l_+'  DAY', font=f, fill=(40,38,44)); g.paste(a_, (x,y+lh))
    y2 = y+TH+lh
    d.text((x,y2), 'NIGHT', font=f, fill=(90,86,96)); g.paste(b_, (x,y2+lh))
g.save('palette_wide.png'); print('wide grid', g.size)
