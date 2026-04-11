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
    <section className="bg-muted/50 py-24 sm:py-32">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            The transformation
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
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
                  <span className="text-muted-foreground text-sm">{item}</span>
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
                  <span className="text-muted-foreground text-sm">{item}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Briefing Preview */}
        <div className="mt-16 max-w-lg mx-auto">
          <Card className="bg-card border-border p-6">
            <div className="text-xs text-muted-foreground mb-3 font-mono">AUTO-GENERATED BRIEFING</div>
            <div className="space-y-3 text-sm text-muted-foreground">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Contact</span>
                <span className="text-foreground font-medium">Priya Sharma</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Program</span>
                <span className="text-foreground font-medium">Express Entry</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Score</span>
                <span className="text-[#4F46E5] font-bold">87/100 — Ready</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Timeline</span>
                <span className="text-foreground">Near-term (1-3 months)</span>
              </div>
              <hr className="border-border" />
              <div>
                <span className="text-muted-foreground text-xs">TALKING POINTS</span>
                <ul className="mt-1 text-xs text-muted-foreground space-y-1">
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
