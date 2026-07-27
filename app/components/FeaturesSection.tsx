'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const ACCENT = '#C8A96E';

type Feature = {
  label: string;
  copy: string;
  icon: React.ReactNode;
};

const iconProps = {
  width: 32,
  height: 32,
  viewBox: '0 0 32 32',
  fill: 'none',
  stroke: ACCENT,
  strokeWidth: 1.2,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
};

const features: Feature[] = [
  {
    label: 'Century Slate Roof',
    copy: 'Hand-split Welsh slate, graded and laid in diminishing courses, engineered to shelter the residence for more than a hundred years.',
    icon: (
      <svg {...iconProps}>
        <path d="M4 16 L16 5 L28 16" />
        <path d="M8 13 L8 20 M16 8 L16 20 M24 13 L24 20" />
        <path d="M6 20 L26 20" />
      </svg>
    ),
  },
  {
    label: 'Copper Ridgework',
    copy: 'Standing-seam copper ridges, valleys and gutters, folded by hand and left to earn their patina season after season.',
    icon: (
      <svg {...iconProps}>
        <path d="M4 20 C10 12, 22 12, 28 20" />
        <path d="M4 24 C10 16, 22 16, 28 24" />
        <circle cx="16" cy="9" r="2.5" />
      </svg>
    ),
  },
  {
    label: 'Envelope Waterproofing',
    copy: 'A triple-membrane building envelope seals every junction from ridge to footing, tested against wind-driven rain at storm pressure.',
    icon: (
      <svg {...iconProps}>
        <path d="M16 4 C16 4, 25 9, 25 17 C25 23 21 27 16 27 C11 27 7 23 7 17 C7 9 16 4 16 4 Z" />
        <path d="M12 17 C12 20 14 22 16 22" />
      </svg>
    ),
  },
  {
    label: 'Heritage Timber Frame',
    copy: 'A post-and-beam skeleton of quarter-sawn oak, joined with pegged mortise and tenon exactly as the first Meridian houses were.',
    icon: (
      <svg {...iconProps}>
        <path d="M6 27 L6 10 L16 4 L26 10 L26 27" />
        <path d="M6 27 L26 27" />
        <path d="M6 10 L26 27 M26 10 L6 27" />
      </svg>
    ),
  },
  {
    label: 'Certified Craftsmanship',
    copy: 'Every structural assembly is inspected twice — once by the master builder, once by an independent surveyor — before it is ever concealed.',
    icon: (
      <svg {...iconProps}>
        <circle cx="16" cy="14" r="8" />
        <path d="M12.5 14 L15 16.5 L20 11.5" />
        <path d="M12 21 L10 28 L16 25 L22 28 L20 21" />
      </svg>
    ),
  },
  {
    label: 'Panoramic Glazing',
    copy: 'Floor-to-ceiling low-iron glass, set flush into the stone facade, frames the landscape with the clarity of open air.',
    icon: (
      <svg {...iconProps}>
        <rect x="5" y="6" width="22" height="20" />
        <path d="M16 6 L16 26 M5 16 L27 16" />
      </svg>
    ),
  },
];

const ease = [0.25, 0, 0, 1] as const;

export default function FeaturesSection() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section
      id="features"
      style={{
        background: '#000',
        padding: 'clamp(4rem, 10vw, 8rem) clamp(1.5rem, 6vw, 5rem)',
      }}
    >
      <div ref={ref} style={{ maxWidth: 1200, margin: '0 auto' }}>
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
          Crafted Without Compromise
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
            marginBottom: 'clamp(2.5rem, 6vw, 4.5rem)',
            maxWidth: 700,
            lineHeight: 1.15,
          }}
        >
          Every layer of this house earns its place.
        </motion.h2>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: 'clamp(1.5rem, 3vw, 2.5rem)',
          }}
        >
          {features.map((feature, i) => (
            <motion.div
              key={feature.label}
              initial={{ opacity: 0, y: 24 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.7, delay: 0.2 + i * 0.1, ease }}
              style={{
                borderTop: '1px solid rgba(200,169,110,0.2)',
                paddingTop: '1.8rem',
              }}
            >
              <div style={{ marginBottom: '1.2rem' }}>{feature.icon}</div>
              <h3
                style={{
                  fontFamily: 'var(--font-inter)',
                  fontWeight: 500,
                  fontSize: '0.95rem',
                  letterSpacing: '0.06em',
                  color: '#ffffff',
                  marginBottom: '0.7rem',
                }}
              >
                {feature.label}
              </h3>
              <p
                style={{
                  fontFamily: 'var(--font-inter)',
                  fontWeight: 300,
                  fontSize: '0.9rem',
                  lineHeight: 1.7,
                  color: '#E5E5E5',
                }}
              >
                {feature.copy}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
