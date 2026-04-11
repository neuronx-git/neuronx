import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { ArrowRight, CheckCircle } from "lucide-react";

const proofChips = [
  "0-100 Readiness Scoring",
  "Auto-Generated Briefings",
  "10-Stage Case Pipeline",
  "Built for RCIC Firms",
];

const pipelineStages = [
  { label: "Inquiry", detail: "Form capture + webhook", active: true },
  { label: "Scored", detail: "R1-R5 readiness (0-100)", active: true },
  { label: "Booked", detail: "Auto booking + reminders", active: true },
  { label: "Briefed", detail: "Consultation prep delivered", active: true },
  { label: "Case Started", detail: "10-stage pipeline begins", active: true, phase2: true },
  { label: "Submitted", detail: "IRCC forms + tracking", active: true, phase2: true },
  { label: "Decision", detail: "Outcome + next steps", active: true, phase2: true },
];

export const Hero = () => {
  return (
    <section className="dark-section pt-24 pb-16 md:pt-28 md:pb-24 relative overflow-hidden">
      {/* Subtle gradient orb */}
      <div className="absolute top-20 right-0 w-[500px] h-[500px] bg-[#4F46E5]/8 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-[#7C3AED]/6 rounded-full blur-[100px]" />

      <div className="container relative">
        <div className="max-w-4xl mx-auto text-center space-y-5">
          {/* Proof chips */}
          <div className="flex flex-wrap justify-center gap-2">
            {proofChips.map((chip) => (
              <Badge
                key={chip}
                variant="outline"
                className="border-white/20 text-white/70 bg-white/5 px-3 py-1 text-xs font-medium"
              >
                <CheckCircle className="w-3 h-3 mr-1.5 text-[#818CF8]" />
                {chip}
              </Badge>
            ))}
          </div>

          {/* Headline */}
          <h1 className="text-4xl md:text-5xl lg:text-[3.5rem] font-bold text-white leading-[1.1] tracking-tight">
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
            >
              <Button
                size="lg"
                variant="outline"
                className="border-white/30 text-white bg-white/5 hover:bg-white/10 px-8 py-6 text-base rounded-xl"
              >
                See How It Works
              </Button>
            </a>
          </div>
        </div>

        {/* Pipeline Animation Rail */}
        <div className="mt-12 max-w-5xl mx-auto">
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-5">
            <div className="flex items-start justify-between overflow-x-auto gap-1">
              {pipelineStages.map((stage, i) => (
                <div key={stage.label} className="flex items-center flex-shrink-0">
                  <div className="flex flex-col items-center gap-1.5 min-w-[80px]">
                    <div
                      className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                        stage.phase2
                          ? "bg-[#7C3AED] text-white shadow-lg shadow-[#7C3AED]/30"
                          : "bg-[#4F46E5] text-white shadow-lg shadow-[#4F46E5]/30"
                      }`}
                    >
                      {i + 1}
                    </div>
                    <span className="text-xs font-semibold text-white whitespace-nowrap">
                      {stage.label}
                    </span>
                    <span className="text-[10px] text-slate-400 whitespace-nowrap text-center leading-tight max-w-[90px]">
                      {stage.detail}
                    </span>
                  </div>
                  {i < pipelineStages.length - 1 && (
                    <div
                      className={`w-6 md:w-10 h-px mx-1 mt-[-20px] ${
                        stage.phase2 || pipelineStages[i + 1]?.phase2
                          ? "bg-[#7C3AED]/50"
                          : "bg-[#4F46E5]/50"
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
            <div className="flex justify-center gap-6 mt-4 pt-3 border-t border-white/5">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#4F46E5]" />
                <span className="text-xs text-slate-400">Phase 1: Conversion</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#7C3AED]" />
                <span className="text-xs text-slate-400">Phase 2: Case Ops</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
