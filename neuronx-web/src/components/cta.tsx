import { Button } from "./ui/button";

export const Cta = () => {
  return (
    <section id="cta" className="bg-muted/50 py-16 my-24 sm:my-32">
      <div className="container lg:grid lg:grid-cols-2 place-items-center">
        <div className="lg:col-start-1">
          <h2 className="text-3xl md:text-4xl font-bold">
            Stop Losing Clients to
            <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
              {" "}Slow Follow-Up{" "}
            </span>
          </h2>
          <p className="text-muted-foreground text-xl mt-4 mb-8 lg:mb-0">
            Every hour you wait to respond, your competitor gets closer. NeuronX
            ensures every inquiry gets a professional AI response in under 5
            minutes — 24/7, even on weekends and holidays.
          </p>
        </div>

        <div className="space-y-4 lg:col-start-2">
          <a href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW" target="_blank" rel="noreferrer noopener">
            <Button className="w-full md:mr-4 md:w-auto">Book a Free Demo</Button>
          </a>
          <a href="#features">
            <Button variant="outline" className="w-full md:w-auto">Explore Features</Button>
          </a>
        </div>
      </div>
    </section>
  );
};
