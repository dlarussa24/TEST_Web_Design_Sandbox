'use client';

import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { FRAME_COUNT } from './frameCount';

const framePath = (index: number) =>
  `/frames/frame_${String(index + 1).padStart(4, '0')}.jpg`;

const fadeIn = {
  hidden: { opacity: 0, y: 16 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.8, delay: 0.8 + i * 0.15, ease: 'easeOut' as const },
  }),
};

export default function ScrollHero() {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const images: HTMLImageElement[] = [];
    let currentIdx = -1;
    let rafId = 0;

    const sizeCanvas = () => {
      const dpr = window.devicePixelRatio || 1;
      canvas.width = canvas.clientWidth * dpr;
      canvas.height = canvas.clientHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const draw = (index: number) => {
      const img = images[index];
      if (!img || !img.complete || img.naturalWidth === 0) return;
      const cw = canvas.clientWidth;
      const ch = canvas.clientHeight;
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;
      // Contain-fit: the whole subject stays in frame on every viewport;
      // the tinted void fills the rest so letterboxing is invisible.
      const scale = Math.min(cw / iw, ch / ih);
      const dw = iw * scale;
      const dh = ih * scale;
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = '#101012';
      ctx.fillRect(0, 0, cw, ch);
      ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
      // Lift the footage's pure-black void up to the page's warm charcoal
      // gradient so the hero never reads as flat #000.
      ctx.globalCompositeOperation = 'lighten';
      const tint = ctx.createLinearGradient(0, 0, 0, ch);
      tint.addColorStop(0, '#101012');
      tint.addColorStop(1, '#17110b');
      ctx.fillStyle = tint;
      ctx.fillRect(0, 0, cw, ch);
      ctx.globalCompositeOperation = 'source-over';
      currentIdx = index;
    };

    sizeCanvas();

    for (let i = 0; i < FRAME_COUNT; i++) {
      const img = new Image();
      img.src = framePath(i);
      if (i === 0) {
        img.onload = () => draw(0);
      }
      images.push(img);
    }

    const loop = () => {
      const top = container.getBoundingClientRect().top;
      const progress = Math.max(
        0,
        Math.min(1, -top / (container.offsetHeight - window.innerHeight))
      );
      const target = Math.round(progress * (FRAME_COUNT - 1));
      if (target !== currentIdx) {
        draw(target);
      }
      rafId = requestAnimationFrame(loop);
    };
    rafId = requestAnimationFrame(loop);

    const onResize = () => {
      sizeCanvas();
      if (currentIdx >= 0) draw(currentIdx);
    };
    window.addEventListener('resize', onResize);

    return () => {
      cancelAnimationFrame(rafId);
      window.removeEventListener('resize', onResize);
    };
  }, []);

  return (
    <div ref={containerRef} style={{ height: '300vh', position: 'relative' }}>
      <div
        style={{
          position: 'sticky',
          top: 0,
          width: '100vw',
          height: '100vh',
          overflow: 'hidden',
          background: 'linear-gradient(170deg, #101012 0%, #17110b 100%)',
        }}
      >
        <canvas
          ref={canvasRef}
          style={{ display: 'block', width: '100%', height: '100%' }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-end',
            pointerEvents: 'none',
            background:
              'linear-gradient(to top, rgba(15,12,9,0.92) 0%, rgba(16,14,12,0.35) 50%, transparent 100%)',
          }}
        >
          <div style={{ padding: 'clamp(2rem, 6vw, 5rem)', maxWidth: 900 }}>
            <motion.p
              custom={0}
              initial="hidden"
              animate="visible"
              variants={fadeIn}
              style={{
                fontFamily: 'var(--font-inter)',
                fontSize: '0.65rem',
                letterSpacing: '0.25em',
                textTransform: 'uppercase',
                color: '#C08A55',
                marginBottom: '1.2rem',
              }}
            >
              Est. 1905 · Highgate
            </motion.p>
            <motion.h1
              custom={1}
              initial="hidden"
              animate="visible"
              variants={fadeIn}
              style={{
                fontFamily: 'var(--font-playfair)',
                fontWeight: 400,
                fontSize: 'clamp(2.4rem, 6vw, 5.5rem)',
                lineHeight: 1.05,
                color: '#ffffff',
                marginBottom: '1.4rem',
              }}
            >
              The Meridian Estate
            </motion.h1>
            <motion.p
              custom={2}
              initial="hidden"
              animate="visible"
              variants={fadeIn}
              style={{
                fontFamily: 'var(--font-inter)',
                fontWeight: 300,
                fontSize: '1.05rem',
                lineHeight: 1.7,
                color: '#E5E5E5',
                maxWidth: 460,
                marginBottom: '2.2rem',
              }}
            >
              A residence assembled slate by slate, beam by beam — scroll to
              lift the roof and see a century of craft suspended in mid-air.
            </motion.p>
            <motion.a
              custom={3}
              initial="hidden"
              animate="visible"
              variants={fadeIn}
              href="#features"
              style={{
                display: 'inline-block',
                background: 'linear-gradient(135deg, #C08A55 0%, #8B5A38 100%)',
                color: '#140E08',
                fontFamily: 'var(--font-inter)',
                fontWeight: 500,
                fontSize: '0.7rem',
                letterSpacing: '0.18em',
                textTransform: 'uppercase',
                textDecoration: 'none',
                padding: '0.9rem 2.6rem',
                pointerEvents: 'auto',
              }}
            >
              Explore the Residence
            </motion.a>
          </div>
        </div>
      </div>
    </div>
  );
}
