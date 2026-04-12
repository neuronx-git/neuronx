import { motion, useInView } from "framer-motion";
import { useRef, useState, useEffect } from "react";

const ease = [0.22, 1, 0.36, 1] as const;

const dimensions = [
  { label: "Program Interest", value: 95 },
  { label: "Location", value: 90 },
  { label: "Urgency", value: 80 },
  { label: "Prior Apps", value: 85 },
  { label: "Budget", value: 88 },
];

export const ScoreCard = () => {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true });
  const [score, setScore] = useState(0);

  useEffect(() => {
    if (!isInView) return;
    let current = 0;
    const interval = setInterval(() => {
      current += 2;
      if (current >= 87) {
        setScore(87);
        clearInterval(interval);
      } else {
        setScore(current);
      }
    }, 25);
    return () => clearInterval(interval);
  }, [isInView]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 15 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: 0.3, ease }}
      className="bg-white dark:bg-slate-800/80 rounded-xl border border-border dark:border-white/10 p-4 shadow-lg shadow-black/5 dark:shadow-black/20"
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
          Readiness Score
        </span>
        <span className="text-2xl font-bold text-[#4F46E5]">
          {score}
          <span className="text-sm text-muted-foreground font-normal">/100</span>
        </span>
      </div>

      <div className="space-y-2">
        {dimensions.map((dim, i) => (
          <div key={dim.label} className="space-y-0.5">
            <div className="flex justify-between text-[10px]">
              <span className="text-muted-foreground">{dim.label}</span>
              <span className="text-foreground font-medium">{dim.value}%</span>
            </div>
            <div className="h-1 bg-border dark:bg-white/10 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-[#4F46E5] to-[#7C3AED] rounded-full"
                initial={{ width: "0%" }}
                animate={isInView ? { width: `${dim.value}%` } : {}}
                transition={{ duration: 1, delay: 0.5 + i * 0.12, ease }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-3 flex items-center gap-2">
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-medium">
          Ready — Standard
        </span>
        <span className="text-[10px] text-muted-foreground">Express Entry</span>
      </div>
    </motion.div>
  );
};
