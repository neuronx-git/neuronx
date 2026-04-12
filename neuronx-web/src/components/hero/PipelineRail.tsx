import { motion } from "framer-motion";
import { useState, useEffect } from "react";

const ease = [0.22, 1, 0.36, 1] as const;

const stages = [
  { label: "Inquiry", detail: "Form capture" },
  { label: "Scored", detail: "0-100 rating" },
  { label: "Booked", detail: "Auto booking" },
  { label: "Briefed", detail: "Prep docs" },
  { label: "Case", detail: "Doc collection" },
  { label: "Decision", detail: "Outcome" },
];

export const PipelineRail = () => {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev >= stages.length - 1 ? 0 : prev + 1));
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-3">
      <div className="text-[10px] font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400">
        Live Pipeline
      </div>
      <div className="flex items-center gap-1">
        {stages.map((stage, i) => (
          <div key={stage.label} className="flex items-center">
            {/* Node */}
            <motion.div
              className="relative flex flex-col items-center"
              initial={false}
            >
              <motion.div
                className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold border-2 transition-colors duration-300"
                animate={{
                  backgroundColor: i <= activeIndex ? "rgba(79,70,229,1)" : "rgba(79,70,229,0.1)",
                  borderColor: i <= activeIndex ? "rgba(79,70,229,1)" : "rgba(79,70,229,0.2)",
                  color: i <= activeIndex ? "#fff" : "rgba(79,70,229,0.4)",
                  boxShadow: i === activeIndex ? "0 0 16px rgba(79,70,229,0.5)" : "0 0 0 rgba(79,70,229,0)",
                }}
                transition={{ duration: 0.4, ease }}
              >
                {i + 1}
              </motion.div>
              <span className={`text-[9px] mt-1 font-medium whitespace-nowrap transition-colors duration-300 ${
                i <= activeIndex ? "text-foreground" : "text-muted-foreground/50"
              }`}>
                {stage.label}
              </span>
            </motion.div>

            {/* Connector */}
            {i < stages.length - 1 && (
              <div className="w-4 h-[2px] mx-0.5 mt-[-12px] bg-border dark:bg-white/10 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-[#4F46E5] rounded-full"
                  initial={{ width: "0%" }}
                  animate={{ width: i < activeIndex ? "100%" : "0%" }}
                  transition={{ duration: 0.5, ease }}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
