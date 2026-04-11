import { Button } from "./ui/button";
import { buttonVariants } from "./ui/button";
import { HeroCards } from "./HeroCards";

export const Hero = () => {
  return (
    <section className="container grid lg:grid-cols-2 place-items-center py-20 md:py-32 gap-10">
      <div className="text-center lg:text-start space-y-6">
        <main className="text-5xl md:text-6xl font-bold">
          <h1 className="inline">
            Your next client just called.{" "}
            <span className="inline bg-gradient-to-r from-[#E8380D] to-[#F59E0B] text-transparent bg-clip-text">
              You missed it.
            </span>
          </h1>
        </main>

        <p className="text-xl text-muted-foreground md:w-10/12 mx-auto lg:mx-0">
          Immigration firms lose 60% of qualified leads to slow follow-up.
          NeuronX calls every inquiry within 5 minutes, scores their readiness,
          and books consultations automatically — so your RCICs walk in prepared,
          not guessing.
        </p>

        <div className="space-y-4 md:space-y-0 md:space-x-4">
          <a
            href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
            target="_blank"
            rel="noreferrer noopener"
          >
            <Button className="w-full md:w-1/3">Book a Free Demo</Button>
          </a>

          <a
            href="#howItWorks"
            className={`w-full md:w-1/3 ${buttonVariants({
              variant: "outline",
            })}`}
          >
            See How It Works
          </a>
        </div>
      </div>

      <div className="z-10">
        <HeroCards />
      </div>

      <div className="shadow"></div>
    </section>
  );
};
