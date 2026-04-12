import { Button } from "./ui/button";
import { ScrollReveal } from "./ui/scroll-reveal";
import confetti from "canvas-confetti";

const fireConfetti = () => {
  confetti({
    particleCount: 80,
    spread: 70,
    origin: { y: 0.6 },
    colors: ["#4F46E5", "#7C3AED", "#3B82F6", "#818CF8"],
    disableForReducedMotion: true,
  });
};

export const Cta = () => {
  return (
    <section id="cta" className="bg-muted/50 py-16 mt-8 mb-16">
      <div className="container lg:grid lg:grid-cols-2 place-items-center">
        <ScrollReveal className="lg:col-start-1">
          <h2 className="text-3xl md:text-4xl font-bold">
            Your competitors are still
            <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
              {" "}checking voicemail
            </span>
          </h2>
          <p className="text-muted-foreground text-xl mt-4 mb-8 lg:mb-0">
            Start your 14-day pilot. We'll set up your account, run a live
            test, and show you exactly how many consultations you're currently
            missing.
          </p>
        </ScrollReveal>

        <ScrollReveal delay={0.2} className="space-y-4 lg:col-start-2">
          <a
            href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
            target="_blank"
            rel="noreferrer noopener"
            onClick={fireConfetti}
          >
            <Button className="cta-gradient text-white border-0 w-full md:mr-4 md:w-auto">
              Start Your Pilot
            </Button>
          </a>
          <a
            href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
            target="_blank"
            rel="noreferrer noopener"
          >
            <Button variant="outline" className="w-full md:w-auto">
              Book a 15-Min Demo
            </Button>
          </a>
        </ScrollReveal>
      </div>
    </section>
  );
};
