import { useEffect, useRef, useState } from 'react';
import Logo from './Logo';

const BASE = 'https://basebloom-concepts.netlify.app';

type Trade = {
  kicker: string;
  title: string;
  desc: string;
  accent: string;
  href: string;
};

const trades: Trade[] = [
  { kicker: 'Lawn & Landscaping', title: 'Landscapes composed like architecture', desc: 'An estate that unfolds as you scroll — planting plans, stonework, and seasons choreographed like a title sequence.', accent: '#22B24C', href: 'https://verdant-and-stone.netlify.app/' },
  { kicker: 'Roofing', title: 'Built for the hundred-year storm', desc: 'A ridgeline flight as the sky clears — slate, seam, and flashing shot like aerial cinema.', accent: '#6B7F94', href: `${BASE}/slate-and-storm/` },
  { kicker: 'HVAC · Heating & Cooling', title: 'Comfort engineered to be forgotten', desc: 'The seasons turn, the room holds — airflow made visible, then made invisible again.', accent: '#E8784A', href: `${BASE}/ember-and-air/` },
  { kicker: 'Plumbing', title: 'Water, carried like it matters', desc: 'Workshop to clawfoot in one take — copper bends and pressure lines told as a single moving shot.', accent: '#B87333', href: `${BASE}/copper-and-spring/` },
  { kicker: 'Electrical', title: 'The current follows your hand', desc: 'Move your cursor — the current follows and arcs to your hand. A live-wire demo of cursor-reactive craft.', accent: '#FFC93C', href: `${BASE}/site-1-classic/` },
  { kicker: 'Construction', title: 'Built plumb, built to outlive us', desc: 'A crane-up through steel at dawn — beams, welds, and bedrock sequenced like a build timelapse.', accent: '#F5A623', href: `${BASE}/beam-and-bedrock/` },
  { kicker: 'House Cleaning', title: 'Rooms returned to the light', desc: 'A drawing room comes to order in one take — dust lifts, linen settles, light comes back.', accent: '#5FB3D4', href: `${BASE}/linen-and-light/` },
  { kicker: 'Painting', title: 'Color, cut clean at the line', desc: 'A wall takes its coat as you scroll — masking, rolling, and the reveal, edge-perfect.', accent: '#D9A62B', href: `${BASE}/ochre-and-ivory/` },
  { kicker: 'Carpentry', title: 'Wood, joined to outlast trends', desc: 'One plane stroke, told as cinema — grain, joinery, and finish in close-up.', accent: '#C89B66', href: `${BASE}/grain-and-grove/` },
];

export default function FeaturesSection() {
  const [active, setActive] = useState(0);
  const [revealed, setRevealed] = useState<boolean[]>(() => trades.map(() => false));
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    const activeObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            const idx = Number((en.target as HTMLElement).dataset.idx);
            setActive(idx);
          }
        });
      },
      { threshold: 0.6 }
    );
    const revealObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            const idx = Number((en.target as HTMLElement).dataset.idx);
            setRevealed((r) => (r[idx] ? r : r.map((v, i) => (i === idx ? true : v))));
            revealObs.unobserve(en.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    cardRefs.current.forEach((el) => {
      if (el) {
        activeObs.observe(el);
        revealObs.observe(el);
      }
    });
    return () => {
      activeObs.disconnect();
      revealObs.disconnect();
    };
  }, []);

  const scrollToCard = (i: number) => {
    cardRefs.current[i]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  return (
    <section
      id="trades"
      className="relative px-5 md:px-10 lg:px-16 py-20 md:py-40 lg:py-48"
      style={{ background: 'linear-gradient(175deg, #241505 0%, #17110B 45%, #100D0A 100%)' }}
    >
      <div className="lg:grid lg:grid-cols-[400px_1fr] xl:grid-cols-[460px_1fr] lg:gap-24 xl:gap-48 max-w-[1500px] mx-auto">
        <div className="lg:sticky lg:top-0 lg:h-screen lg:flex lg:flex-col lg:justify-between lg:py-32">
          <div>
            <h2 className="text-white text-2xl sm:text-3xl lg:text-[46px] leading-[1.2] font-normal">
              Nine trades. Nine live demos. Open yours.
            </h2>
            <div className="hidden lg:flex flex-col items-start gap-2 mt-10">
              {trades.map((t, i) => (
                <button
                  key={t.kicker}
                  onClick={() => scrollToCard(i)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors bg-black/20 ${
                    active === i ? 'text-white' : 'text-white/40 hover:text-white/70'
                  }`}
                >
                  {t.kicker}
                </button>
              ))}
            </div>
          </div>
          <div className="hidden lg:block">
            <p className="text-white/70 text-sm font-medium mb-4 max-w-[300px]">
              No templates. No stock sites. Just your trade, built to move.
            </p>
            <a
              href="mailto:hello@basebloom.studio?subject=Free%20demo"
              className="inline-block bg-white text-black text-sm font-medium px-5 py-2.5 rounded-xl hover:bg-white/90 transition-colors"
            >
              Get a free demo
            </a>
          </div>
        </div>

        <div className="flex flex-col gap-10 md:gap-16 mt-12 lg:mt-0">
          {trades.map((t, i) => (
            <div
              key={t.kicker}
              ref={(el) => { cardRefs.current[i] = el; }}
              data-idx={i}
              className={`bg-black/20 backdrop-blur-sm rounded-3xl p-6 md:p-10 transition-all duration-700 ease-out ${
                revealed[i] ? 'translate-x-0 opacity-100' : 'translate-x-16 opacity-0'
              }`}
            >
              <div className="flex items-center gap-4 mb-6">
                <Logo fill="rgba(255,255,255,0.8)" size={40} />
                <h3 className="text-white text-xl md:text-2xl font-medium">{t.title}</h3>
              </div>
              <a href={t.href} target="_blank" rel="noopener" className="block group">
                <div
                  className="aspect-video rounded-2xl overflow-hidden relative flex items-end p-6 transition-transform duration-500 group-hover:scale-[1.01]"
                  style={{
                    background: `linear-gradient(140deg, ${t.accent}33 0%, ${t.accent}14 45%, rgba(0,0,0,0.35) 100%)`,
                    border: `1px solid ${t.accent}44`,
                  }}
                >
                  <div
                    className="absolute inset-0 opacity-40"
                    style={{ background: `radial-gradient(80% 90% at 85% 10%, ${t.accent}55, transparent 60%)` }}
                  />
                  <div className="relative">
                    <p className="text-[11px] uppercase tracking-[0.25em] font-semibold mb-1" style={{ color: t.accent }}>
                      {t.kicker}
                    </p>
                    <p className="text-white/90 text-sm font-medium">
                      Open the live demo <span aria-hidden>→</span>
                    </p>
                  </div>
                </div>
              </a>
              <p className="text-white/60 font-medium text-sm md:text-base leading-relaxed mt-6">{t.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
