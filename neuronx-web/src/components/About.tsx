import { ScrollReveal } from "./ui/scroll-reveal";
import { Statistics } from "./Statistics";

export const About = () => {
  return (
    <section id="about" className="container py-12 sm:py-16">
      <div className="bg-muted/50 border rounded-lg py-12">
        <div className="px-6 flex flex-col-reverse md:flex-row gap-8 md:gap-12">
          <div className="flex flex-col md:flex-row gap-6 flex-shrink-0">
            <img
              src="/team/sanjay.jpg"
              alt="Sanjay Singh Kumar, RCIC"
              className="w-32 h-32 rounded-xl object-cover object-top"
            />
            <div className="space-y-2">
              <div className="text-sm font-mono text-primary">R705959</div>
              <div className="text-lg font-bold">Sanjay Singh Kumar</div>
              <div className="text-sm text-muted-foreground">Licensed RCIC</div>
              <div className="text-sm text-muted-foreground">5,000+ cases processed</div>
              <div className="text-sm text-muted-foreground">5.0 Google Rating</div>
            </div>
          </div>
          <div className="flex flex-col justify-between">
            <ScrollReveal className="pb-6">
              <h2 className="text-3xl md:text-4xl font-bold">
                <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
                  Built by an RCIC{" "}
                </span>
                who processed 5,000+ cases
              </h2>
              <p className="text-xl text-muted-foreground mt-4">
                Most software companies build immigration tools by reading IRCC
                documentation. We built NeuronX from inside a firm that has filed
                5,000+ applications, maintained a 5.0 Google rating, and knows
                exactly where the process breaks — because we lived it. Paired
                with Big Five consulting expertise in product and sales operations
                to build the platform that should have existed a decade ago.
              </p>
            </ScrollReveal>

            <Statistics />
          </div>
        </div>
      </div>
    </section>
  );
};
