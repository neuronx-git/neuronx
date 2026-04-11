import { Button } from "./ui/button";
import { buttonVariants } from "./ui/button";
import { Badge } from "./ui/badge";
import { ArrowRight, CheckCircle } from "lucide-react";

const proofChips = [
  "0-100 Readiness Scoring",
  "Auto-Generated Briefings",
  "10-Stage Case Pipeline",
  "Built for RCIC Firms",
];

const pipelineStages = [
  { label: "Inquiry", active: true },
  { label: "Scored", active: true },
  { label: "Booked", active: true },
  { label: "Briefed", active: true },
  { label: "Case Started", active: false },
  { label: "Submitted", active: false },
  { label: "Decision", active: false },
];

export const Hero = () => {
  return (
    <section className="dark-section pt-28 pb-20 md:pt-36 md:pb-28 relative overflow-hidden">
      {/* Subtle gradient orb */}
      <div className="absolute top-20 right-0 w-[500px] h-[500px] bg-[#4F46E5]/8 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-[#7C3AED]/6 rounded-full blur-[100px]" />

      <div className="container relative">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Proof chips */}
          <div className="flex flex-wrap justify-center gap-3">
            {proofChips.map((chip) => (
              <Badge
                key={chip}
                variant="outline"
                className="border-white/20 text-white/70 bg-white/5 px-3 py-1 text-xs font-medium"
              >
                <CheckCircle className="w-3 h-3 mr-1.5 text-[#4F46E5]" />
                {chip}
              </Badge>
            ))}
          </div>

          {/* Headline */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white leading-[1.1] tracking-tight">
            Convert immigration inquiries into retained clients{" "}
            <span className="gradient-text">
              — and manage every case with structured workflows.
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
            NeuronX captures, scores, and prepares every inquiry — then helps
            your team manage the entire case lifecycle with immigration-specific
            workflows.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-2">
            <a
              href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
              target="_blank"
              rel="noreferrer noopener"
            >
              <Button
                size="lg"
                className="bg-[#4F46E5] hover:bg-[#4338CA] text-white px-8 py-6 text-base font-semibold rounded-xl shadow-lg shadow-[#4F46E5]/20 hover:shadow-xl hover:shadow-[#4F46E5]/30 transition-all hover:-translate-y-0.5"
              >
                Book a Demo
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </a>
            <a
              href="#howItWorks"
              className={`${buttonVariants({ variant: "outline", size: "lg" })} border-white/20 text-white hover:bg-white/10 px-8 py-6 text-base rounded-xl`}
            >
              See How It Works
            </a>
          </div>
        </div>

        {/* Pipeline Animation Rail */}
        <div className="mt-16 max-w-4xl mx-auto">
          <div className="flex items-center justify-between bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6 overflow-x-auto">
            {pipelineStages.map((stage, i) => (
              <div key={stage.label} className="flex items-center flex-shrink-0">
                <div className="flex flex-col items-center gap-2">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                      stage.active
                        ? "bg-[#4F46E5] text-white shadow-lg shadow-[#4F46E5]/30"
                        : "bg-white/10 text-white/40"
                    }`}
                    style={{ animationDelay: `${i * 0.3}s` }}
                  >
                    {i + 1}
                  </div>
                  <span
                    className={`text-xs font-medium whitespace-nowrap ${
                      stage.active ? "text-white" : "text-white/40"
                    }`}
                  >
                    {stage.label}
                  </span>
                </div>
                {i < pipelineStages.length - 1 && (
                  <div
                    className={`w-8 md:w-16 h-px mx-2 ${
                      stage.active && pipelineStages[i + 1]?.active
                        ? "bg-[#4F46E5]"
                        : "bg-white/10"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
