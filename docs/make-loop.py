"""Ping-pong a generated clip so any camera drift loops seamlessly.
usage: python3 make-loop.py in.mp4 out.mp4"""
import imageio.v2 as iio, numpy as np, sys
src, dst = sys.argv[1], sys.argv[2]
rd = iio.get_reader(src); fps = rd.get_meta_data()['fps']
frames = [np.asarray(f) for f in rd]
seq = frames + frames[-2:0:-1]          # forward, then back, no duplicated ends
w = iio.get_writer(dst, fps=fps, codec='libx264', bitrate='4000000',
                   macro_block_size=None, ffmpeg_params=['-pix_fmt','yuv420p','-preset','slow'])
for f in seq: w.append_data(f)
w.close()
a, b = seq[0].astype(np.int16), seq[-1].astype(np.int16)
print(f'{len(seq)} frames, {len(seq)/fps:.2f}s, seam {float(np.abs(b-a).mean())/255*100:.3f}%')
