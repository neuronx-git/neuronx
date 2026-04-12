import { motion, useInView } from "framer-motion";
import { useRef } from "react";

const ease = [0.22, 1, 0.36, 1] as const;

const lines = [
  { label: "Contact", value: "Priya Sharma" },
  { label: "Program", value: "Express Entry" },
  { label: "Score", value: "87/100 — Ready", highlight: true },
  { label: "Timeline", value: "Near-term" },
];

const talkingPoints = [
  "Discuss CRS score estimate",
  "Review ECA status",
  "Confirm language scores",
];

export const BriefingCard = () => {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, x: 20 }}
      animate={isInView ? { opacity: 1, x: 0 } : {}}
      transition={{ duration: 0.6, delay: 0.6, ease }}
      className="bg-white dark:bg-slate-800/80 rounded-xl border border-border dark:border-white/10 p-4 shadow-lg shadow-black/5 dark:shadow-black/20"
    >
      <div className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground mb-3">
        Auto-Generated Briefing
      </div>

      <div className="space-y-2">
        {lines.map((line, i) => (
          <motion.div
            key={line.label}
            initial={{ opacity: 0, y: 6 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.4, delay: 0.8 + i * 0.1, ease }}
            className="flex justify-between text-[11px]"
          >
            <span className="text-muted-foreground">{line.label}</span>
            <span className={line.highlight ? "text-[#4F46E5] font-bold" : "text-foreground font-medium"}>
              {line.value}
            </span>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={isInView ? { opacity: 1 } : {}}
        transition={{ duration: 0.4, delay: 1.3, ease }}
        className="mt-3 pt-3 border-t border-border dark:border-white/10"
      >
        <div className="text-[9px] font-mono uppercase tracking-wider text-muted-foreground mb-1.5">
          Talking Points
        </div>
        {talkingPoints.map((point, i) => (
          <motion.div
            key={point}
            initial={{ opacity: 0, x: 8 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.3, delay: 1.4 + i * 0.08, ease }}
            className="text-[10px] text-muted-foreground flex items-start gap-1.5 mb-1"
          >
            <span className="text-[#4F46E5] mt-px">—</span>
            {point}
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
};
