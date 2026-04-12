import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { ArrowRight, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";
import { HeroBackground, HeroBackgroundLight } from "./hero/HeroBackground";
import { PipelineRail } from "./hero/PipelineRail";
import { ScoreCard } from "./hero/ScoreCard";
import { BriefingCard } from "./hero/BriefingCard";
import { useTheme } from "./theme-provider";

const ease = [0.22, 1, 0.36, 1] as const;

const proofChips = [
  "0-100 Readiness Scoring",
  "Auto-Generated Briefings",
  "10-Stage Case Pipeline",
  "Built for RCIC Firms",
];

export const Hero = () => {
  const { theme } = useTheme();
  const isDark = theme === "dark" || (theme === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches);

  return (
    <section className={`relative pt-24 pb-16 md:pt-28 md:pb-20 overflow-hidden ${
      isDark ? "bg-[#0F172A] text-white" : "bg-[#F8FAFC]"
    }`}>
      {/* Background layers */}
      {isDark ? <HeroBackground /> : <HeroBackgroundLight />}

      <div className="container relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">

          {/* LEFT — Text block */}
          <div className="space-y-5 text-center lg:text-left">
            {/* Proof chips */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, ease }}
              className="flex flex-wrap justify-center lg:justify-start gap-2"
            >
              {proofChips.map((chip, i) => (
                <motion.div
                  key={chip}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.05 + i * 0.06, ease }}
                >
                  <Badge
                    variant="outline"
                    className={`px-3 py-1 text-[11px] font-medium backdrop-blur-sm transition-all duration-200 hover:-translate-y-0.5 ${
                      isDark
                        ? "border-white/15 text-white/70 bg-white/5"
                        : "border-border text-muted-foreground bg-white/80"
                    }`}
                  >
                    <CheckCircle className="w-3 h-3 mr-1.5 text-[#4F46E5]" />
                    {chip}
                  </Badge>
                </motion.div>
              ))}
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.15, ease }}
              className={`text-3xl md:text-4xl lg:text-5xl font-bold leading-[1.12] tracking-tight ${
                isDark ? "text-white" : "text-foreground"
              }`}
            >
              Convert immigration inquiries into retained clients{" "}
              <span className="gradient-text">
                — and manage every case with structure.
              </span>
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3, ease }}
              className={`text-base md:text-lg leading-relaxed max-w-xl mx-auto lg:mx-0 ${
                isDark ? "text-slate-300" : "text-muted-foreground"
              }`}
            >
              NeuronX captures, scores, and prepares every inquiry — then helps
              your team manage the entire lifecycle with immigration-specific
              workflows.
            </motion.p>

            {/* CTAs */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4, ease }}
              className="flex flex-col sm:flex-row gap-3 justify-center lg:justify-start pt-1"
            >
              <a
                href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
                target="_blank"
                rel="noreferrer noopener"
              >
                <Button
                  size="lg"
                  className="cta-gradient text-white px-7 py-5 text-sm font-semibold rounded-xl border-0 hover:scale-[1.02] transition-transform"
                >
                  Book a Demo
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </a>
              <a href="#howItWorks">
                <Button
                  size="lg"
                  variant="outline"
                  className={`px-7 py-5 text-sm rounded-xl transition-all duration-300 ${
                    isDark
                      ? "border-white/20 text-white bg-white/5 hover:bg-white/10"
                      : "border-border text-foreground hover:bg-muted"
                  }`}
                >
                  See How It Works
                </Button>
              </a>
            </motion.div>
          </div>

          {/* RIGHT — Visual system */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3, ease }}
            className="hidden lg:flex flex-col gap-4"
          >
            {/* Pipeline Rail */}
            <div className={`rounded-xl p-4 ${
              isDark ? "bg-white/[0.04] border border-white/[0.08]" : "bg-white border border-border shadow-sm"
            }`}>
              <PipelineRail />
            </div>

            {/* Score + Briefing side by side */}
            <div className="grid grid-cols-2 gap-4">
              <ScoreCard />
              <BriefingCard />
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};
