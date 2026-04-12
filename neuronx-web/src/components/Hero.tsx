import { useEffect, useRef } from "react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { ArrowRight, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";
import gsap from "gsap";

const ease = [0.22, 1, 0.36, 1] as const;

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
  const pipelineRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!pipelineRef.current) return;

    const nodes = pipelineRef.current.querySelectorAll(".p-node");
    const connectors = pipelineRef.current.querySelectorAll(".p-connector");
    const labels = pipelineRef.current.querySelectorAll(".p-label");
    const details = pipelineRef.current.querySelectorAll(".p-detail");

    const tl = gsap.timeline({ repeat: -1, repeatDelay: 2, delay: 1.2 });

    // Reset
    tl.set(nodes, { scale: 0.7, opacity: 0.2, boxShadow: "0 0 0 0 rgba(79,70,229,0)" });
    tl.set(connectors, { scaleX: 0, transformOrigin: "left center" });
    tl.set(labels, { opacity: 0.3 });
    tl.set(details, { opacity: 0 });

    // Sequential activation
    nodes.forEach((node, i) => {
      const t = i * 0.6;
      tl.to(node, {
        scale: 1.2, opacity: 1,
        boxShadow: "0 0 24px 8px rgba(79,70,229,0.5)",
        duration: 0.35, ease: "power2.out",
      }, t);
      tl.to(node, {
        scale: 1, boxShadow: "0 0 10px 3px rgba(79,70,229,0.25)",
        duration: 0.25, ease: "power2.inOut",
      }, t + 0.35);
      if (labels[i]) tl.to(labels[i], { opacity: 1, duration: 0.3 }, t + 0.1);
      if (details[i]) tl.to(details[i], { opacity: 1, duration: 0.3 }, t + 0.2);
      if (i < connectors.length) {
        tl.to(connectors[i], { scaleX: 1, duration: 0.35, ease: "power2.inOut" }, t + 0.25);
      }
    });

    // Hold
    tl.to({}, { duration: 3 });

    // Fade out
    tl.to(nodes, { scale: 0.7, opacity: 0.2, boxShadow: "0 0 0 0 rgba(79,70,229,0)", duration: 0.4, stagger: 0.03 });
    tl.to(connectors, { scaleX: 0, duration: 0.25, stagger: 0.03 }, "<");
    tl.to(labels, { opacity: 0.3, duration: 0.3 }, "<");
    tl.to(details, { opacity: 0, duration: 0.3 }, "<");

    return () => { tl.kill(); };
  }, []);

  return (
    <section className="hero-gradient noise-overlay relative pt-24 pb-16 md:pt-28 md:pb-24 overflow-hidden">
      <div className="container relative">
        <div className="max-w-4xl mx-auto text-center space-y-5">
          {/* Proof chips */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease }}
            className="flex flex-wrap justify-center gap-2"
          >
            {proofChips.map((chip, i) => (
              <motion.div
                key={chip}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 + i * 0.08, ease }}
              >
                <Badge
                  variant="outline"
                  className="border-white/15 text-white/70 bg-white/5 px-3 py-1 text-xs font-medium backdrop-blur-sm transition-all duration-200 hover:-translate-y-0.5"
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
            transition={{ duration: 0.7, delay: 0.2, ease }}
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
            transition={{ duration: 0.6, delay: 0.35, ease }}
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
            transition={{ duration: 0.6, delay: 0.45, ease }}
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

        {/* Pipeline Rail — GSAP-powered sequential animation */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease }}
          className="mt-12 max-w-6xl mx-auto"
        >
          <div ref={pipelineRef} className="bg-white/[0.04] backdrop-blur-md rounded-2xl border border-white/[0.08] p-5 md:p-6">
            <div className="flex items-start justify-between">
              {pipelineStages.map((stage, i) => (
                <div key={stage.label} className="flex items-start flex-1">
                  <div className="flex flex-col items-center gap-1.5 flex-shrink-0">
                    <div
                      className={`p-node w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold opacity-20 ${
                        stage.phase === 1
                          ? "bg-[#7C3AED] text-white"
                          : "bg-[#4F46E5] text-white"
                      }`}
                    >
                      {i + 1}
                    </div>
                    <span className="p-label text-xs font-semibold text-white whitespace-nowrap opacity-30">
                      {stage.label}
                    </span>
                    <span className="p-detail text-[10px] text-slate-400 text-center leading-tight opacity-0 max-w-[90px]">
                      {stage.detail}
                    </span>
                  </div>
                  {i < pipelineStages.length - 1 && (
                    <div className="flex-1 h-[2px] mt-[18px] mx-1 bg-white/10 rounded-full overflow-hidden min-w-[12px]">
                      <div className="p-connector h-full bg-gradient-to-r from-[#7C3AED] to-[#4F46E5] rounded-full origin-left scale-x-0" />
                    </div>
                  )}
                </div>
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
