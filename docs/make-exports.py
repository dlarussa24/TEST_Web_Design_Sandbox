"""Cut one 3:4 master into the aspect ratios each surface wants.
usage: python3 exports.py master.mp4 outprefix"""
import imageio.v2 as iio, numpy as np, sys
from PIL import Image

src, pre = sys.argv[1], sys.argv[2]
rd = iio.get_reader(src); fps = rd.get_meta_data()['fps']
frames = [np.asarray(f) for f in rd]
H0, W0 = frames[0].shape[:2]
print(f'master {W0}x{H0} @ {fps:g}fps, {len(frames)} frames')

# subject sits centre-right; bias the crop right so the ATM stays as context
# without letting Rufus drift to the frame edge
def crop_resize(im, target_w, target_h, xbias=0.54, ybias=0.5):
    h, w = im.shape[:2]
    tr = target_w / target_h
    if w / h > tr:                      # too wide -> cut sides
        nw = int(round(h * tr)); nh = h
        x0 = int(round((w - nw) * xbias)); y0 = 0
    else:                               # too tall -> cut top/bottom
        nw = w; nh = int(round(w / tr))
        x0 = 0; y0 = int(round((h - nh) * ybias))
    c = im[y0:y0+nh, x0:x0+nw]
    return np.asarray(Image.fromarray(c).resize((target_w, target_h), Image.LANCZOS))

SPECS = [
    ('reels', 1080, 1920, 0.54, 0.5),   # TikTok + IG Reels + FB Reels
    ('feed',  1080, 1350, 0.50, 0.42),  # IG feed + FB feed (4:5)
    # 1:1 deliberately omitted: it clips the pouch, which is the mode indicator
]
for name, tw, th, xb, yb in SPECS:
    out = f'{pre}-{name}.mp4'
    w = iio.get_writer(out, fps=fps, codec='libx264', bitrate='6000000',
                       macro_block_size=None,
                       ffmpeg_params=['-pix_fmt','yuv420p','-preset','slow','-profile:v','high'])
    for f in frames: w.append_data(crop_resize(f, tw, th, xb, yb))
    w.close()
    print(f'  {name}: {tw}x{th} -> {out}')
    # contact sheet frame for eyeballing the crop
    Image.fromarray(crop_resize(frames[0], tw, th, xb, yb)).save(f'{pre}-{name}-check.png')
