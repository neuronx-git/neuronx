import { useEffect, useRef } from "react";
import gsap from "gsap";

/**
 * PipelineRail — GSAP-powered sequential animation
 * Each node activates in sequence with glow + connector fill
 */

const stages = [
  { label: "Inquiry", detail: "Form capture" },
  { label: "Scored", detail: "0-100 rating" },
  { label: "Booked", detail: "Auto booking" },
  { label: "Briefed", detail: "Prep docs" },
  { label: "Case", detail: "Doc collection" },
  { label: "Decision", detail: "Outcome" },
];

export const PipelineRail = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const nodes = containerRef.current.querySelectorAll(".p-node");
    const connectors = containerRef.current.querySelectorAll(".p-connector");

    // Build GSAP timeline
    const tl = gsap.timeline({ repeat: -1, repeatDelay: 1.5 });

    // Reset all
    tl.set(nodes, { scale: 0.8, opacity: 0.3, boxShadow: "0 0 0 0 rgba(79,70,229,0)" });
    tl.set(connectors, { scaleX: 0, transformOrigin: "left center" });

    // Animate each node + connector sequentially
    nodes.forEach((node, i) => {
      tl.to(node, {
        scale: 1.15,
        opacity: 1,
        boxShadow: "0 0 20px 6px rgba(79,70,229,0.4)",
        duration: 0.4,
        ease: "power2.out",
      }, i * 0.8);

      tl.to(node, {
        scale: 1,
        boxShadow: "0 0 8px 2px rgba(79,70,229,0.2)",
        duration: 0.3,
        ease: "power2.inOut",
      }, i * 0.8 + 0.4);

      if (i < connectors.length) {
        tl.to(connectors[i], {
          scaleX: 1,
          duration: 0.4,
          ease: "power2.inOut",
        }, i * 0.8 + 0.3);
      }
    });

    // Hold at the end
    tl.to({}, { duration: 2 });

    // Fade everything out before restart
    tl.to(nodes, { scale: 0.8, opacity: 0.3, boxShadow: "0 0 0 0 rgba(79,70,229,0)", duration: 0.5, stagger: 0.05 });
    tl.to(connectors, { scaleX: 0, duration: 0.3, stagger: 0.05 }, "<");

    return () => { tl.kill(); };
  }, []);

  return (
    <div ref={containerRef} className="space-y-3">
      <div className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
        Live Pipeline
      </div>
      <div className="flex items-center justify-between">
        {stages.map((stage, i) => (
          <div key={stage.label} className="flex items-center">
            <div className="flex flex-col items-center">
              <div className="p-node w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold bg-[#4F46E5] text-white opacity-30">
                {i + 1}
              </div>
              <span className="text-[9px] mt-1 font-medium text-foreground whitespace-nowrap">
                {stage.label}
              </span>
              <span className="text-[8px] text-muted-foreground whitespace-nowrap">
                {stage.detail}
              </span>
            </div>
            {i < stages.length - 1 && (
              <div className="w-3 md:w-5 h-[2px] mx-0.5 mt-[-16px] bg-border dark:bg-white/10 rounded-full overflow-hidden">
                <div className="p-connector h-full bg-[#4F46E5] rounded-full origin-left scale-x-0" />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
