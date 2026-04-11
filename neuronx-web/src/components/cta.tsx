import { Button } from "./ui/button";

export const Cta = () => {
  return (
    <section id="cta" className="bg-muted/50 py-16 mt-8 mb-16">
      <div className="container lg:grid lg:grid-cols-2 place-items-center">
        <div className="lg:col-start-1">
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
        </div>

        <div className="space-y-4 lg:col-start-2">
          <a
            href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
            target="_blank"
            rel="noreferrer noopener"
          >
            <Button className="w-full md:mr-4 md:w-auto">
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
        </div>
      </div>
    </section>
  );
};
