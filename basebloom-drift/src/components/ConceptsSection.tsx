import Logo from './Logo';

const BASE = 'https://basebloom-concepts.netlify.app';

const concepts = [
  { n: '01', name: 'Living dust', tag: 'Cursor-reactive', href: `${BASE}/site-1-classic/` },
  { n: '02', name: 'Depth & material', tag: 'Real-time 3D', href: `${BASE}/site-2/` },
  { n: '03', name: 'Type as art', tag: 'Editorial', href: `${BASE}/site-3/` },
  { n: '04', name: 'Motion & narrative', tag: 'Scrollytelling', href: `${BASE}/site-4/` },
  { n: '05', name: 'The generative engine', tag: 'Creative code', href: `${BASE}/site-5/` },
  { n: '06', name: 'Tactile physics', tag: 'Playable', href: `${BASE}/site-6/` },
  { n: '07', name: 'Data as art', tag: 'Choreographed data', href: `${BASE}/site-7/` },
  { n: '08', name: 'The details department', tag: 'Micro-interactions', href: `${BASE}/site-8/` },
  { n: '09', name: 'The studio that talks back', tag: 'Conversational', href: `${BASE}/site-9/` },
];

const crafts = [
  { kicker: 'Landscaping', name: 'The Meadow', href: `${BASE}/craft-landscaping/` },
  { kicker: 'Roofing', name: 'The Dry Line', href: `${BASE}/craft-roofing/` },
  { kicker: 'Plumbing', name: 'Flow Finds a Way', href: `${BASE}/craft-plumbing/` },
  { kicker: 'Construction', name: 'Raise the Frame', href: `${BASE}/craft-construction/` },
  { kicker: 'Cleaning', name: 'The Gleam', href: `${BASE}/craft-cleaning/` },
  { kicker: 'HVAC', name: 'Visible Air', href: `${BASE}/craft-hvac/` },
  { kicker: 'Painting', name: 'Loaded Brush', href: `${BASE}/craft-painting/` },
  { kicker: 'Carpentry', name: 'True Grain', href: `${BASE}/craft-carpentry/` },
  { kicker: 'Real Estate', name: 'From Line to Life', href: `${BASE}/craft-realty/` },
];

const assemblies = [
  { kicker: 'Landscaping', name: 'A Yard, Grown', href: `${BASE}/assembly-landscaping/` },
  { kicker: 'Roofing', name: 'The Roof, Raised', href: `${BASE}/assembly-roofing/` },
  { kicker: 'Plumbing', name: 'Behind the Walls', href: `${BASE}/assembly-plumbing/` },
  { kicker: 'Construction', name: 'Steel, Sequenced', href: `${BASE}/assembly-construction/` },
  { kicker: 'Cleaning', name: 'The Room, Returned', href: `${BASE}/assembly-cleaning/` },
  { kicker: 'HVAC', name: 'The Breathing House', href: `${BASE}/assembly-hvac/` },
  { kicker: 'Painting', name: 'The Room, Recolored', href: `${BASE}/assembly-painting/` },
  { kicker: 'Carpentry', name: 'The Table, Joined', href: `${BASE}/assembly-carpentry/` },
  { kicker: 'Real Estate', name: 'The Street, Composed', href: `${BASE}/assembly-realty/` },
];

export default function ConceptsSection() {
  return (
    <section id="concepts" className="bg-[#F6E4CF] py-20 md:py-32 px-6">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-[#321C04] text-2xl sm:text-3xl md:text-4xl leading-[1.2] font-normal mb-10 md:mb-16">
          Nine ways a website can move.
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {concepts.map((c) => (
            <a
              key={c.n}
              href={c.href}
              target="_blank"
              rel="noopener"
              className="group bg-[#FFF9F2] rounded-2xl p-6 flex flex-col gap-3 hover:bg-white transition-colors"
            >
              <span className="text-xs font-semibold tracking-widest text-[#321C04]/40">{c.n}</span>
              <span className="text-lg font-medium text-[#321C04]">{c.name}</span>
              <span className="text-xs uppercase tracking-wide font-medium text-[#321C04]/60">
                {c.tag} · <span className="group-hover:underline">Open →</span>
              </span>
            </a>
          ))}
        </div>

        <div className="flex items-center gap-2 w-full my-16 md:my-24">
          <span className="w-2 h-2 rounded-full bg-[#D9C4AA]" />
          <span className="flex-1 h-[2px] bg-[#D9C4AA]" />
          <span className="w-2 h-2 rounded-full bg-[#D9C4AA]" />
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          <div>
            <h3 className="text-[#321C04] text-xl md:text-2xl font-medium mb-6">The craft series</h3>
            <ul className="flex flex-col divide-y divide-[#D9C4AA]/60">
              {crafts.map((c) => (
                <li key={c.href}>
                  <a href={c.href} target="_blank" rel="noopener" className="group flex items-baseline justify-between py-3">
                    <span>
                      <span className="text-xs uppercase tracking-widest font-semibold text-[#321C04]/50 mr-3">{c.kicker}</span>
                      <span className="text-[#321C04] font-medium group-hover:underline">{c.name}</span>
                    </span>
                    <span className="text-[#321C04]/50 text-sm">Enter →</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="text-[#321C04] text-xl md:text-2xl font-medium mb-6">The assembly series</h3>
            <ul className="flex flex-col divide-y divide-[#D9C4AA]/60">
              {assemblies.map((c) => (
                <li key={c.href}>
                  <a href={c.href} target="_blank" rel="noopener" className="group flex items-baseline justify-between py-3">
                    <span>
                      <span className="text-xs uppercase tracking-widest font-semibold text-[#321C04]/50 mr-3">{c.kicker}</span>
                      <span className="text-[#321C04] font-medium group-hover:underline">{c.name}</span>
                    </span>
                    <span className="text-[#321C04]/50 text-sm">Enter →</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="flex items-center justify-center gap-4 mt-16 md:mt-24">
          <Logo fill="#321C04" size={32} />
          <span className="text-xs uppercase tracking-widest font-semibold text-[#321C04]">
            BaseBloom · We build the base. Your business blooms.
          </span>
        </div>
      </div>
    </section>
  );
}
