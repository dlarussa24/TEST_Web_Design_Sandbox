import Navbar from './components/Navbar';
import AboutSection from './components/AboutSection';
import FeaturesSection from './components/FeaturesSection';
import ConceptsSection from './components/ConceptsSection';

const HERO_VIDEO = '/basebloom/basebloom-hero-web-loop.mp4';

export default function App() {
  return (
    <>
      <section className="relative h-screen overflow-hidden mb-[-25px]">
        <video
          className="absolute inset-0 w-full h-full object-cover"
          src={HERO_VIDEO}
          autoPlay
          muted
          loop
          playsInline
        />
        <div className="absolute inset-0 bg-black/20" />
        <Navbar />
        <div className="relative z-10 h-full flex flex-col justify-end items-center pb-12 md:pb-16 px-6">
          <h1 className="text-center text-5xl sm:text-7xl md:text-8xl lg:text-[96px] font-normal text-white leading-[1.1] tracking-tight animate-fade-in-down">
            We build the base.
            <br />
            your business{' '}
            <em
              className="not-italic"
              style={{ fontFamily: "'Instrument Serif', serif", fontStyle: 'italic' }}
            >
              blooms
            </em>
          </h1>
          <p className="text-white/80 text-sm md:text-base font-medium max-w-[420px] text-center mt-6">
            BaseBloom builds cinematic websites for the trades — twenty-seven
            live demos of what your business could feel like online
          </p>
          <div className="bg-black/25 backdrop-blur-md rounded-xl flex items-center gap-4 pl-6 pr-1 py-1 mt-8">
            <span className="hidden sm:block text-white text-sm font-medium">
              No templates. No stock sites. Just your trade, built to move.
            </span>
            <span className="sm:hidden text-white text-sm font-medium">
              Your trade, built to move.
            </span>
            <a
              href="mailto:hello@basebloom.studio?subject=Free%20demo"
              className="bg-white text-black text-sm font-medium px-5 py-2.5 rounded-xl hover:bg-white/90 transition-colors whitespace-nowrap"
            >
              Get a free demo
            </a>
          </div>
        </div>
      </section>
      <AboutSection />
      <FeaturesSection />
      <ConceptsSection />
    </>
  );
}
