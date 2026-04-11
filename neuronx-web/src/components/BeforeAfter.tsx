import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

const beforeItems = [
  "Inquiries sit in inboxes for hours",
  "Lead quality unknown until consultation",
  "Consultations start with 'So, what brings you in?'",
  "Case stages tracked in spreadsheets",
  "Follow-ups depend on memory",
  "No visibility into pipeline health",
];

const afterItems = [
  "Every inquiry scored within minutes",
  "Lead readiness quantified on 5 dimensions",
  "RCIC walks in with a structured briefing",
  "10-stage pipeline with automated routing",
  "Workflow-driven follow-up at every stage",
  "Structured pipeline visibility",
];

export const BeforeAfter = () => {
  return (
    <section className="dark-section py-24 sm:py-32">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
            The transformation
          </h2>
          <p className="mt-4 text-lg text-slate-400">
            What changes when your firm runs on structured workflows instead of
            manual processes.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <Card className="bg-red-500/5 border-red-500/20">
            <CardHeader>
              <CardTitle className="text-red-400 text-lg">Before NeuronX</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {beforeItems.map((item) => (
                <div key={item} className="flex items-start gap-3">
                  <span className="text-red-400 mt-0.5">-</span>
                  <span className="text-slate-300 text-sm">{item}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="bg-[#4F46E5]/5 border-[#4F46E5]/20">
            <CardHeader>
              <CardTitle className="text-[#818CF8] text-lg">After NeuronX</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {afterItems.map((item) => (
                <div key={item} className="flex items-start gap-3">
                  <span className="text-[#4F46E5] mt-0.5">+</span>
                  <span className="text-slate-300 text-sm">{item}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Briefing Preview */}
        <div className="mt-16 max-w-lg mx-auto">
          <Card className="bg-white/5 border-white/10 p-6">
            <div className="text-xs text-slate-500 mb-3 font-mono">AUTO-GENERATED BRIEFING</div>
            <div className="space-y-3 text-sm text-slate-300">
              <div className="flex justify-between">
                <span className="text-slate-400">Contact</span>
                <span className="text-white font-medium">Priya Sharma</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Program</span>
                <span className="text-white font-medium">Express Entry</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Score</span>
                <span className="text-[#4F46E5] font-bold">87/100 — Ready</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Timeline</span>
                <span className="text-white">Near-term (1-3 months)</span>
              </div>
              <hr className="border-white/10" />
              <div>
                <span className="text-slate-400 text-xs">TALKING POINTS</span>
                <ul className="mt-1 text-xs text-slate-300 space-y-1">
                  <li>- Discuss CRS score calculation</li>
                  <li>- Review education credential assessment</li>
                  <li>- Confirm language test scores</li>
                </ul>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};
