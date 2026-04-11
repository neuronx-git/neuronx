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
  { label: "Inquiry", detail: "Form capture + webhook", phase: 1 },
  { label: "Scored", detail: "R1-R5 readiness (0-100)", phase: 1 },
  { label: "Booked", detail: "Auto booking + reminders", phase: 1 },
  { label: "Briefed", detail: "Consultation prep delivered", phase: 1 },
  { label: "Case Started", detail: "Onboarding + doc collection", phase: 2 },
  { label: "Form Prep", detail: "Smart intake + IRCC forms", phase: 2 },
  { label: "Submitted", detail: "IRCC submission + tracking", phase: 2 },
  { label: "Decision", detail: "Outcome + next steps", phase: 2 },
];

export const Hero = () => {
  return (
    <section className="dark-section pt-24 pb-16 md:pt-28 md:pb-24 relative overflow-hidden">
      <div className="absolute top-20 right-0 w-[500px] h-[500px] bg-[#7C3AED]/8 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-[#4F46E5]/6 rounded-full blur-[100px]" />

      <div className="container relative">
        <div className="max-w-4xl mx-auto text-center space-y-5">
          <div className="flex flex-wrap justify-center gap-2">
            {proofChips.map((chip) => (
              <Badge
                key={chip}
                variant="outline"
                className="border-white/20 text-white/70 bg-white/5 px-3 py-1 text-xs font-medium"
              >
                <CheckCircle className="w-3 h-3 mr-1.5 text-[#A78BFA]" />
                {chip}
              </Badge>
            ))}
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-[3.5rem] font-bold text-white leading-[1.1] tracking-tight">
            Convert immigration inquiries into retained clients{" "}
            <span className="gradient-text">
              — and manage every case with structured workflows.
            </span>
          </h1>

          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
            NeuronX captures, scores, and prepares every inquiry — then helps
            your team manage the entire case lifecycle with immigration-specific
            workflows.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-2">
            <a
              href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
              target="_blank"
              rel="noreferrer noopener"
            >
              <Button
                size="lg"
                className="bg-[#7C3AED] hover:bg-[#6D28D9] text-white px-8 py-6 text-base font-semibold rounded-xl shadow-lg shadow-[#7C3AED]/20 hover:shadow-xl hover:shadow-[#7C3AED]/30 transition-all hover:-translate-y-0.5"
              >
                Book a Demo
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </a>
            <a href="#howItWorks">
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

        {/* Pipeline Rail — no scrollbar, full width */}
        <div className="mt-12 max-w-6xl mx-auto">
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-5 md:p-6">
            <div className="grid grid-cols-4 md:grid-cols-8 gap-y-6 gap-x-2">
              {pipelineStages.map((stage, i) => (
                <div key={stage.label} className="flex flex-col items-center gap-1.5 relative">
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold ${
                      stage.phase === 1
                        ? "bg-[#7C3AED] text-white shadow-lg shadow-[#7C3AED]/30"
                        : "bg-[#4F46E5] text-white shadow-lg shadow-[#4F46E5]/30"
                    }`}
                  >
                    {i + 1}
                  </div>
                  <span className="text-xs font-semibold text-white whitespace-nowrap">
                    {stage.label}
                  </span>
                  <span className="text-[10px] text-slate-400 text-center leading-tight">
                    {stage.detail}
                  </span>
                </div>
              ))}
            </div>
            <div className="flex justify-center gap-6 mt-4 pt-3 border-t border-white/5">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#7C3AED]" />
                <span className="text-xs text-slate-400">Phase 1: Conversion</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#4F46E5]" />
                <span className="text-xs text-slate-400">Phase 2: Case Ops</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
