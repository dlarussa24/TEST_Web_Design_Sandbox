import { useState } from 'react';

const links = [
  { label: 'Trades', href: '#trades' },
  { label: 'Concepts', href: '#concepts' },
  { label: 'Free demo', href: 'mailto:hello@basebloom.studio?subject=Free%20demo' },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <div className="absolute top-6 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center">
      <div className="bg-white rounded-full shadow-lg flex items-center gap-4 pl-5 pr-3 py-2.5">
        <span className="text-lg font-bold tracking-tight text-black">BaseBloom.</span>
        <button
          aria-label="Menu"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
          className="w-8 h-8 flex flex-col items-center justify-center gap-[5px]"
        >
          <span
            className="block w-5 h-[2px] bg-black transition-transform duration-300"
            style={{
              transitionTimingFunction: 'cubic-bezier(0.77,0,0.175,1)',
              transform: open ? 'translateY(3.5px) rotate(45deg)' : 'none',
            }}
          />
          <span
            className="block w-5 h-[2px] bg-black transition-transform duration-300"
            style={{
              transitionTimingFunction: 'cubic-bezier(0.77,0,0.175,1)',
              transform: open ? 'translateY(-3.5px) rotate(-45deg)' : 'none',
            }}
          />
        </button>
      </div>
      <div
        className={`mt-3 bg-white rounded-2xl shadow-lg py-2 px-2 min-w-[180px] transition-all duration-300 origin-top ${
          open
            ? 'opacity-100 scale-100 translate-y-0 pointer-events-auto'
            : 'opacity-0 scale-95 -translate-y-2 pointer-events-none'
        }`}
      >
        {links.map((l) => (
          <a
            key={l.label}
            href={l.href}
            onClick={() => setOpen(false)}
            className="block px-4 py-2.5 rounded-xl text-sm font-medium text-black hover:bg-black/5 transition-colors"
          >
            {l.label}
          </a>
        ))}
      </div>
    </div>
  );
}
