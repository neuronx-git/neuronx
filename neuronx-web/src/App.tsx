import { About } from "./components/About";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { Credibility } from "./components/Credibility";
import { Problem } from "./components/Problem";
import { TwoPhase } from "./components/TwoPhase";
import { HowItWorks } from "./components/HowItWorks";
import { Differentiation } from "./components/Differentiation";
import { BeforeAfter } from "./components/BeforeAfter";
import { ProductModules } from "./components/ProductModules";
import { Pricing } from "./components/Pricing";
import { Team } from "./components/Team";
import { FAQ } from "./components/FAQ";
import { Cta } from "./components/Cta";
import { Footer } from "./components/Footer";
import { ScrollToTop } from "./components/ScrollToTop";
import "./App.css";

function App() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Credibility />
        <Problem />
        <TwoPhase />
        <HowItWorks />
        <Differentiation />
        <BeforeAfter />
        <ProductModules />
        <Pricing />
        <About />
        <Team />
        <FAQ />
        <Cta />
      </main>
      <Footer />
      <ScrollToTop />
    </>
  );
}

export default App;
