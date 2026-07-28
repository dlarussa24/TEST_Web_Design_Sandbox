import { Mail, Plus } from 'lucide-react';
import Logo from './Logo';

export default function AboutSection() {
  return (
    <section className="bg-[#F6E4CF] rounded-t-[25px] relative z-10 py-20 md:py-32 px-6">
      <div className="max-w-3xl mx-auto flex flex-col items-center gap-8">
        <p className="text-[#321C04] text-base md:text-lg text-center leading-relaxed max-w-lg">
          We craft websites that move with your trade, not over it. Built for
          craft, presence, and work that speaks for itself.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <a
            href="mailto:hello@basebloom.studio"
            className="flex items-center gap-3 bg-[#321C04] text-[#FFF9F2] rounded-full pl-1.5 pr-6 py-1.5 hover:bg-[#1F1003] transition-colors"
          >
            <span className="w-9 h-9 rounded-full bg-[#FFF9F2] flex items-center justify-center">
              <Mail size={16} className="text-[#321C04]" />
            </span>
            <span className="text-xs uppercase tracking-wide font-medium">Say hello</span>
          </a>
          <a
            href="mailto:hello@basebloom.studio?subject=Keep%20me%20informed"
            className="flex items-center gap-3 bg-[#D9C4AA] text-[#321C04] rounded-full pl-1.5 pr-6 py-1.5 hover:bg-[#CEBA9E] transition-colors"
          >
            <span className="w-9 h-9 rounded-full bg-white flex items-center justify-center">
              <Plus size={16} className="text-[#321C04]" />
            </span>
            <span className="text-xs uppercase tracking-wide font-medium">Stay informed</span>
          </a>
        </div>
      </div>

      <div className="flex items-center gap-2 w-full max-w-6xl mx-auto my-16 md:my-24">
        <span className="w-2 h-2 rounded-full bg-[#D9C4AA]" />
        <span className="flex-1 h-[2px] bg-[#D9C4AA]" />
        <span className="w-2 h-2 rounded-full bg-[#D9C4AA]" />
      </div>

      <div className="max-w-6xl mx-auto flex flex-col md:flex-row gap-10 md:gap-20">
        <div className="flex items-start gap-4 shrink-0">
          <Logo fill="#321C04" size={40} />
          <span className="text-xs uppercase tracking-widest font-semibold text-[#321C04] leading-relaxed">
            Base
            <br />
            Bloom
          </span>
        </div>
        <p className="text-2xl sm:text-3xl md:text-4xl lg:text-[42px] leading-[1.3] font-normal text-[#321C04]">
          We build websites for the trades. But, most importantly, we help your
          customers feel what your hands already know — when a site moves with
          your craft, not over it. We build the base that carries the weight,
          so your business can attend to what truly counts.
        </p>
      </div>
    </section>
  );
}
