import { Statistics } from "./Statistics";

export const About = () => {
  return (
    <section id="about" className="container py-24 sm:py-32">
      <div className="bg-muted/50 border rounded-lg py-12">
        <div className="px-6 flex flex-col-reverse md:flex-row gap-8 md:gap-12">
          <div className="w-[300px] flex-shrink-0 bg-gradient-to-br from-[#0F172A] to-[#1E293B] rounded-lg flex items-center justify-center p-8">
            <div className="text-center">
              <div className="text-5xl font-extrabold text-[#E8380D] mb-2">NX</div>
              <div className="text-white text-sm font-medium">AI Sales OS</div>
              <div className="text-slate-400 text-xs mt-1">for Immigration</div>
            </div>
          </div>
          <div className="flex flex-col justify-between">
            <div className="pb-6">
              <h2 className="text-3xl md:text-4xl font-bold">
                <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
                  Why{" "}
                </span>
                NeuronX Exists
              </h2>
              <p className="text-xl text-muted-foreground mt-4">
                Immigration consulting is a high-ticket, trust-dependent business
                where firms spend thousands on lead generation — then lose prospects
                to slow follow-up, inconsistent assessments, and unprepared
                consultations. NeuronX fixes the entire pre-retention funnel with AI.
                From the moment a prospect inquires to the moment they sign a
                retainer, every step is automated, measured, and optimized.
              </p>
            </div>

            <Statistics />
          </div>
        </div>
      </div>
    </section>
  );
};
