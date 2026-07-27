'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const ACCENT = '#C08A55';
const ease = [0.25, 0, 0, 1] as const;

const specs: [string, string][] = [
  ['Estate No.', 'MR-1905-40'],
  ['Interior Area', '744 m² across three storeys'],
  ['Facade Material', 'Dressed limestone with quarter-sawn oak'],
  ['Structural Frame', 'Pegged oak post-and-beam, steel-free'],
  ['Roof System', 'Welsh slate on double-battened copper-lined deck'],
  ['Build Tolerance', '±2 mm across every structural junction'],
  ['Glazing', 'Low-iron triple glazing, flush stone reveals'],
  ['Weather Resistance', 'Storm-rated envelope, tested to 200 km/h winds'],
  ['Energy Autonomy', '72 hours off-grid on integrated reserve'],
  ['Foundation', 'Reinforced raft on engineered bedrock piles'],
];

export default function SpecsSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section
      style={{
        background: 'transparent',
        padding: 'clamp(4rem, 10vw, 8rem) clamp(1.5rem, 6vw, 5rem)',
      }}
    >
      <div ref={ref} style={{ maxWidth: 900, margin: '0 auto' }}>
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
            marginBottom: '1.2rem',
          }}
        >
          Technical Specifications
        </motion.p>
        <motion.h2
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.1, ease }}
          style={{
            fontFamily: 'var(--font-playfair)',
            fontWeight: 400,
            fontSize: 'clamp(2rem, 4vw, 3.5rem)',
            color: '#ffffff',
            marginBottom: 'clamp(2.5rem, 6vw, 4rem)',
            lineHeight: 1.15,
          }}
        >
          The architecture of precision.
        </motion.h2>
        <div>
          {specs.map(([label, value], i) => (
            <motion.div
              key={label}
              initial={{ opacity: 0, y: 24 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.7, delay: 0.2 + i * 0.1, ease }}
              className="spec-row"
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 2fr',
                gap: '1rem',
                padding: '1.1rem 0',
                borderBottom: '1px solid rgba(158,163,174,0.14)',
              }}
            >
              <span
                style={{
                  fontFamily: 'var(--font-inter)',
                  fontWeight: 500,
                  fontSize: '0.75rem',
                  letterSpacing: '0.12em',
                  textTransform: 'uppercase',
                  color: ACCENT,
                  alignSelf: 'center',
                }}
              >
                {label}
              </span>
              <span
                style={{
                  fontFamily: 'var(--font-inter)',
                  fontWeight: 300,
                  fontSize: '0.95rem',
                  lineHeight: 1.6,
                  color: '#E5E5E5',
                }}
              >
                {value}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
      <style>{`
        @media (max-width: 768px) {
          .spec-row {
            grid-template-columns: 1fr !important;
            gap: 0.35rem !important;
          }
        }
      `}</style>
    </section>
  );
}
