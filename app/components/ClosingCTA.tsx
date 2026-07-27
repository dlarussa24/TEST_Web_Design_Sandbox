'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const ACCENT = '#C8A96E';
const ease = [0.25, 0, 0, 1] as const;

export default function ClosingCTA() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section
      style={{
        background: '#000',
        padding: 'clamp(5rem, 12vw, 10rem) clamp(1.5rem, 6vw, 5rem)',
        textAlign: 'center',
      }}
    >
      <div ref={ref} style={{ maxWidth: 800, margin: '0 auto' }}>
        <motion.p
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, ease }}
          style={{
            fontFamily: 'var(--font-inter)',
            fontSize: '0.65rem',
            letterSpacing: '0.25em',
            textTransform: 'uppercase',
            color: ACCENT,
            marginBottom: '1.4rem',
          }}
        >
          Yours to Command
        </motion.p>
        <motion.h2
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.1, ease }}
          style={{
            fontFamily: 'var(--font-playfair)',
            fontWeight: 400,
            fontSize: 'clamp(2.2rem, 5vw, 4.5rem)',
            color: '#ffffff',
            lineHeight: 1.15,
            marginBottom: '1.6rem',
          }}
        >
          A century of mastery.
          <br />
          <em style={{ color: '#E5E5E5' }}>One address of it.</em>
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.2, ease }}
          style={{
            fontFamily: 'var(--font-inter)',
            fontWeight: 300,
            fontSize: '1rem',
            lineHeight: 1.7,
            color: '#E5E5E5',
            maxWidth: 480,
            margin: '0 auto 3rem',
          }}
        >
          Each Meridian residence is commissioned, never repeated. Speak with
          our builders about raising the next one on your land.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.3, ease }}
          style={{ position: 'relative', display: 'inline-block' }}
        >
          <div
            style={{
              position: 'absolute',
              inset: '-60px -120px',
              background:
                'radial-gradient(ellipse, rgba(200,169,110,0.10) 0%, transparent 70%)',
              pointerEvents: 'none',
            }}
          />
          <motion.a
            href="#"
            whileHover={{ backgroundColor: '#000000', color: ACCENT }}
            transition={{ duration: 0.25 }}
            style={{
              position: 'relative',
              display: 'inline-block',
              background: ACCENT,
              color: '#000',
              border: `1px solid ${ACCENT}`,
              fontFamily: 'var(--font-inter)',
              fontWeight: 500,
              fontSize: '0.7rem',
              letterSpacing: '0.18em',
              textTransform: 'uppercase',
              textDecoration: 'none',
              padding: '0.9rem 2.6rem',
            }}
          >
            Find an Authorised Builder
          </motion.a>
        </motion.div>
      </div>
    </section>
  );
}
