import ScrollHero from './components/ScrollHero';
import FeaturesSection from './components/FeaturesSection';
import SpecsSection from './components/SpecsSection';
import ClosingCTA from './components/ClosingCTA';

export default function Home() {
  return (
    <main>
      <ScrollHero />
      <FeaturesSection />
      <SpecsSection />
      <ClosingCTA />
    </main>
  );
}
