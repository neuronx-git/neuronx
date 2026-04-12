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
  "8-Stage Case Pipeline",
  "Built for RCIC Firms",
];

const pipelineStages = [
  { label: "Inquiry", detail: "Captured instantly, zero manual entry", phase: 1 },
  { label: "Scored", detail: "AI rates readiness 0-100 in seconds", phase: 1 },
  { label: "Booked", detail: "Auto-scheduled, no back-and-forth", phase: 1 },
  { label: "Retained", detail: "Retainer signed, fully prepared", phase: 1 },
  { label: "Onboarded", detail: "Docs auto-collected, nothing missed", phase: 2 },
  { label: "Forms Ready", detail: "IRCC forms pre-filled automatically", phase: 2 },
  { label: "Submitted", detail: "Filed + tracked, no manual follow-up", phase: 2 },
  { label: "Decision", detail: "Outcome delivered, next steps queued", phase: 2 },
];

/* ─── Animated Background Blobs (Stripe-like) ─── */
const HeroBlobs = () => (
  <>
    <motion.div
      className="absolute inset-0 pointer-events-none"
      animate={{
        background: [
          "radial-gradient(ellipse 80% 60% at 20% 30%, rgba(79,70,229,0.3) 0%, transparent 70%)",
          "radial-gradient(ellipse 60% 80% at 50% 60%, rgba(79,70,229,0.25) 0%, transparent 70%)",
          "radial-gradient(ellipse 70% 50% at 30% 40%, rgba(79,70,229,0.3) 0%, transparent 70%)",
        ],
      }}
      transition={{ duration: 18, ease: "linear", repeat: Infinity }}
    />
    <motion.div
      className="absolute inset-0 pointer-events-none"
      animate={{
        background: [
          "radial-gradient(ellipse 50% 50% at 75% 25%, rgba(124,58,237,0.22) 0%, transparent 60%)",
          "radial-gradient(ellipse 60% 40% at 55% 55%, rgba(124,58,237,0.18) 0%, transparent 60%)",
          "radial-gradient(ellipse 45% 55% at 70% 35%, rgba(124,58,237,0.22) 0%, transparent 60%)",
        ],
      }}
      transition={{ duration: 14, ease: "linear", repeat: Infinity }}
    />
    <motion.div
      className="absolute inset-0 pointer-events-none"
      animate={{
        background: [
          "radial-gradient(ellipse 40% 40% at 60% 80%, rgba(59,130,246,0.15) 0%, transparent 50%)",
          "radial-gradient(ellipse 50% 30% at 30% 70%, rgba(59,130,246,0.12) 0%, transparent 50%)",
          "radial-gradient(ellipse 35% 45% at 55% 75%, rgba(59,130,246,0.15) 0%, transparent 50%)",
        ],
      }}
      transition={{ duration: 10, ease: "linear", repeat: Infinity }}
    />
  </>
);

/* ─── SVG Wave Transition ─── */
const HeroWave = () => (
  <motion.svg
    viewBox="0 0 1440 80"
    className="absolute bottom-0 left-0 w-full h-[40px] md:h-[60px]"
    preserveAspectRatio="none"
  >
    <motion.path
      fill="hsl(210, 40%, 98%)"
      className="dark:fill-[hsl(222,47%,8%)]"
      animate={{
        d: [
          "M0,40 C240,70 480,10 720,40 C960,70 1200,10 1440,40 L1440,80 L0,80 Z",
          "M0,50 C240,20 480,60 720,30 C960,10 1200,60 1440,45 L1440,80 L0,80 Z",
          "M0,40 C240,70 480,10 720,40 C960,70 1200,10 1440,40 L1440,80 L0,80 Z",
        ],
      }}
      transition={{ duration: 8, ease: "easeInOut", repeat: Infinity }}
    />
  </motion.svg>
);

export const Hero = () => {
  const pipelineRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!pipelineRef.current) return;

    const nodes = pipelineRef.current.querySelectorAll(".p-node");
    const connectors = pipelineRef.current.querySelectorAll(".p-connector-track");
    const particles = pipelineRef.current.querySelectorAll(".p-particle");
    const rings = pipelineRef.current.querySelectorAll(".p-ring");
    const labels = pipelineRef.current.querySelectorAll(".p-label");
    const details = pipelineRef.current.querySelectorAll(".p-detail");

    const tl = gsap.timeline({ repeat: -1, repeatDelay: 2, delay: 1.2 });

    // Reset all
    tl.set(nodes, { scale: 0.7, opacity: 0.2, boxShadow: "0 0 0 0 rgba(79,70,229,0)" });
    tl.set(connectors, { scaleX: 0, transformOrigin: "left center" });
    tl.set(particles, { opacity: 0, scale: 0 });
    tl.set(rings, { scale: 0.8, opacity: 0 });
    tl.set(labels, { opacity: 0.3 });
    tl.set(details, { opacity: 0 });

    // Sequential activation with electrifying effect
    nodes.forEach((node, i) => {
      const t = i * 0.65;

      // Node zap — scale up big, then settle
      tl.to(node, {
        scale: 1.3, opacity: 1,
        boxShadow: "0 0 28px 10px rgba(79,70,229,0.6)",
        duration: 0.25, ease: "power3.out",
      }, t);
      tl.to(node, {
        scale: 1, boxShadow: "0 0 12px 4px rgba(79,70,229,0.25)",
        duration: 0.3, ease: "power2.inOut",
      }, t + 0.25);

      // Ring pulse
      if (rings[i]) {
        tl.to(rings[i], {
          scale: 2.5, opacity: 0.6, duration: 0.3, ease: "power2.out",
        }, t);
        tl.to(rings[i], {
          scale: 3.5, opacity: 0, duration: 0.4, ease: "power2.in",
        }, t + 0.3);
      }

      // Labels
      if (labels[i]) tl.to(labels[i], { opacity: 1, duration: 0.3 }, t + 0.1);
      if (details[i]) tl.to(details[i], { opacity: 1, duration: 0.3 }, t + 0.2);

      // Connector electricity + particles
      if (i < connectors.length) {
        tl.to(connectors[i], { scaleX: 1, duration: 0.35, ease: "power2.inOut" }, t + 0.2);
        // Particle burst along connector
        const particleGroup = pipelineRef.current!.querySelectorAll(`.p-particles-${i} .p-particle`);
        if (particleGroup.length) {
          tl.to(particleGroup, {
            opacity: 1, scale: 1, x: "100%",
            duration: 0.4, stagger: 0.06, ease: "power2.out",
          }, t + 0.2);
          tl.to(particleGroup, {
            opacity: 0, duration: 0.2,
          }, t + 0.55);
        }
      }
    });

    // Hold at full illumination
    tl.to({}, { duration: 3 });

    // Fade out
    tl.to(nodes, { scale: 0.7, opacity: 0.2, boxShadow: "0 0 0 0 rgba(79,70,229,0)", duration: 0.5, stagger: 0.03 });
    tl.to(connectors, { scaleX: 0, duration: 0.3, stagger: 0.03 }, "<");
    tl.to(labels, { opacity: 0.3, duration: 0.3 }, "<");
    tl.to(details, { opacity: 0, duration: 0.3 }, "<");
    tl.to(rings, { scale: 0.8, opacity: 0, duration: 0.2 }, "<");

    return () => { tl.kill(); };
  }, []);

  return (
    <section className="hero-gradient noise-overlay relative pt-24 pb-20 md:pt-28 md:pb-28 overflow-hidden">
      {/* Animated gradient blobs */}
      <HeroBlobs />

      <div className="container relative z-10">
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

        {/* ═══ Pipeline Rail — Electrifying GSAP Animation ═══ */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease }}
          className="mt-12 max-w-6xl mx-auto"
        >
          {/* SVG glow filter */}
          <svg width="0" height="0" className="absolute">
            <defs>
              <filter id="electric-glow">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>
          </svg>

          <div ref={pipelineRef} className="bg-white/[0.04] backdrop-blur-md rounded-2xl border border-white/[0.08] p-4 md:p-6">
            {/* Desktop: horizontal */}
            <div className="hidden md:flex items-start justify-between">
              {pipelineStages.map((stage, i) => (
                <div key={stage.label} className="flex items-start flex-1">
                  <div className="flex flex-col items-center gap-1.5 flex-shrink-0 relative">
                    {/* Ring pulse element */}
                    <div className={`p-ring absolute w-9 h-9 rounded-full border-2 opacity-0 ${
                      stage.phase === 1 ? "border-[#7C3AED]" : "border-[#4F46E5]"
                    }`} style={{ top: 0 }} />
                    {/* Node */}
                    <div
                      className={`p-node w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold opacity-20 relative z-10 ${
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
                    <span className="p-detail text-[10px] text-slate-400 text-center leading-tight opacity-0 max-w-[100px]">
                      {stage.detail}
                    </span>
                  </div>
                  {i < pipelineStages.length - 1 && (
                    <div className="flex-1 h-[3px] mt-[18px] mx-1 bg-white/10 rounded-full overflow-hidden min-w-[8px] relative">
                      <div className="p-connector-track h-full bg-gradient-to-r from-[#7C3AED] to-[#4F46E5] rounded-full origin-left scale-x-0" />
                      {/* Particle dots */}
                      <div className={`p-particles-${i} absolute inset-0 flex items-center`}>
                        <div className="p-particle absolute w-1.5 h-1.5 rounded-full bg-white opacity-0" style={{ filter: "url(#electric-glow)", left: 0 }} />
                        <div className="p-particle absolute w-1 h-1 rounded-full bg-[#A78BFA] opacity-0" style={{ filter: "url(#electric-glow)", left: 0 }} />
                        <div className="p-particle absolute w-1.5 h-1.5 rounded-full bg-white opacity-0" style={{ filter: "url(#electric-glow)", left: 0 }} />
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Mobile: 2×4 grid */}
            <div className="grid grid-cols-4 gap-y-5 gap-x-3 md:hidden">
              {pipelineStages.map((stage, i) => (
                <div key={stage.label} className="flex flex-col items-center gap-1 relative">
                  <div className={`p-ring absolute w-8 h-8 rounded-full border-2 opacity-0 ${
                    stage.phase === 1 ? "border-[#7C3AED]" : "border-[#4F46E5]"
                  }`} style={{ top: 0 }} />
                  <div
                    className={`p-node w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold opacity-20 relative z-10 ${
                      stage.phase === 1
                        ? "bg-[#7C3AED] text-white"
                        : "bg-[#4F46E5] text-white"
                    }`}
                  >
                    {i + 1}
                  </div>
                  <span className="p-label text-[10px] font-semibold text-white whitespace-nowrap opacity-30">
                    {stage.label}
                  </span>
                </div>
              ))}
            </div>

            {/* Phase legend */}
            <div className="flex justify-center gap-4 md:gap-6 mt-4 pt-3 border-t border-white/5">
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 md:w-2.5 md:h-2.5 rounded-full bg-[#7C3AED]" />
                <span className="text-[10px] md:text-xs text-slate-500">Phase 1: Inquiry to Retainer</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 md:w-2.5 md:h-2.5 rounded-full bg-[#4F46E5]" />
                <span className="text-[10px] md:text-xs text-slate-500">Phase 2: Case Processing</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* SVG wave transition to next section */}
      <HeroWave />
    </section>
  );
};
