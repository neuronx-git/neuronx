import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { ArrowRight, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";

const premiumEase = [0.22, 1, 0.36, 1] as const;

const proofChips = [
  "0-100 Readiness Scoring",
  "Auto-Generated Briefings",
  "10-Stage Case Pipeline",
  "Built for RCIC Firms",
];

const pipelineStages = [
  { label: "Inquiry", detail: "Automated form capture", phase: 1 },
  { label: "Scored", detail: "0-100 readiness scoring", phase: 1 },
  { label: "Booked", detail: "Auto booking + reminders", phase: 1 },
  { label: "Briefed", detail: "Auto-generated prep docs", phase: 1 },
  { label: "Case Started", detail: "Onboarding + doc collection", phase: 2 },
  { label: "Form Prep", detail: "Automated IRCC form filling", phase: 2 },
  { label: "Submitted", detail: "Submission + tracking", phase: 2 },
  { label: "Decision", detail: "Outcome + next steps", phase: 2 },
];

export const Hero = () => {
  return (
    <section className="hero-gradient noise-overlay relative pt-24 pb-16 md:pt-28 md:pb-24 overflow-hidden">
      <div className="container relative">
        <div className="max-w-4xl mx-auto text-center space-y-5">
          {/* Proof chips */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: premiumEase }}
            className="flex flex-wrap justify-center gap-2"
          >
            {proofChips.map((chip, i) => (
              <motion.div
                key={chip}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 + i * 0.08, ease: premiumEase }}
              >
                <Badge
                  variant="outline"
                  className="border-white/15 text-white/70 bg-white/5 px-3 py-1 text-xs font-medium backdrop-blur-sm"
                >
                  <CheckCircle className="w-3 h-3 mr-1.5 text-[#A78BFA]" />
                  {chip}
                </Badge>
              </motion.div>
            ))}
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2, ease: premiumEase }}
            className="text-4xl md:text-5xl lg:text-[3.5rem] font-bold text-white leading-[1.1] tracking-tight"
          >
            Convert immigration inquiries into retained clients{" "}
            <span className="gradient-text">
              — and manage every case with structured workflows.
            </span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.35, ease: premiumEase }}
            className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed"
          >
            NeuronX captures, scores, and prepares every inquiry — then helps
            your team manage the entire case lifecycle with immigration-specific
            workflows.
          </motion.p>

          {/* CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.45, ease: premiumEase }}
            className="flex flex-col sm:flex-row gap-4 justify-center pt-2"
          >
            <a
              href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
              target="_blank"
              rel="noreferrer noopener"
            >
              <Button
                size="lg"
                className="cta-gradient text-white px-8 py-6 text-base font-semibold rounded-xl border-0"
              >
                Book a Demo
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </a>
            <a href="#howItWorks">
              <Button
                size="lg"
                variant="outline"
                className="border-white/20 text-white bg-white/5 hover:bg-white/10 px-8 py-6 text-base rounded-xl backdrop-blur-sm transition-all duration-300"
              >
                See How It Works
              </Button>
            </a>
          </motion.div>
        </div>

        {/* Pipeline Rail — animated */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease: premiumEase }}
          className="mt-12 max-w-6xl mx-auto"
        >
          <div className="bg-white/[0.04] backdrop-blur-md rounded-2xl border border-white/[0.08] p-5 md:p-6">
            <div className="grid grid-cols-4 md:grid-cols-8 gap-y-6 gap-x-2">
              {pipelineStages.map((stage, i) => (
                <motion.div
                  key={stage.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: 0.8 + i * 0.1, ease: premiumEase }}
                  className="flex flex-col items-center gap-1.5 relative"
                >
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold animate-glow ${
                      stage.phase === 1
                        ? "bg-[#7C3AED] text-white"
                        : "bg-[#4F46E5] text-white"
                    }`}
                    style={{ animationDelay: `${i * 0.4}s` }}
                  >
                    {i + 1}
                  </div>
                  <span className="text-xs font-semibold text-white whitespace-nowrap">
                    {stage.label}
                  </span>
                  <span className="text-[10px] text-slate-400 text-center leading-tight">
                    {stage.detail}
                  </span>
                </motion.div>
              ))}
            </div>
            <div className="flex justify-center gap-6 mt-4 pt-3 border-t border-white/5">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-[#7C3AED]" />
                <span className="text-xs text-slate-500">Phase 1: Conversion</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-[#4F46E5]" />
                <span className="text-xs text-slate-500">Phase 2: Case Ops</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
