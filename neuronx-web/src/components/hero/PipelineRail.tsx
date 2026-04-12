/**
 * PipelineRail — CSS-driven animation (no React state re-renders)
 * Each node activates in sequence using animation-delay
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
  return (
    <div className="space-y-3">
      <div className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
        Live Pipeline
      </div>
      <div className="flex items-center justify-between">
        {stages.map((stage, i) => (
          <div key={stage.label} className="flex items-center">
            <div className="flex flex-col items-center">
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold bg-[#4F46E5] text-white pipeline-node"
                style={{
                  animationDelay: `${i * 1.2}s`,
                }}
              >
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
                <div
                  className="h-full bg-[#4F46E5] rounded-full pipeline-connector"
                  style={{ animationDelay: `${i * 1.2 + 0.6}s` }}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
