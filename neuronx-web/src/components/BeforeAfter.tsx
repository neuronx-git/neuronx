import { ScrollReveal, SlideIn } from "./ui/scroll-reveal";
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
    <section className="bg-muted/50 py-16 sm:py-20">
      <div className="container">
        <ScrollReveal className="text-center mb-10">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            The transformation
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            What changes when your firm runs on structured workflows instead of
            manual processes.
          </p>
        </ScrollReveal>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <SlideIn direction="left">
            <Card className="bg-red-500/5 border-red-500/20 h-full hover:-translate-y-2 hover:scale-[1.02] transition-all duration-300">
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
          </SlideIn>

          <SlideIn direction="right">
            <Card className="bg-[#4F46E5]/5 border-[#4F46E5]/20 h-full hover:-translate-y-2 hover:scale-[1.02] transition-all duration-300">
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
          </SlideIn>
        </div>

        {/* Briefing Preview */}
        <ScrollReveal delay={0.3} className="mt-8 max-w-4xl mx-auto">
          <Card className="bg-card border-border p-6 md:p-8 hover:-translate-y-1 transition-all duration-300">
            <div className="text-xs text-muted-foreground mb-4 font-mono tracking-wider">AUTO-GENERATED CONSULTATION BRIEFING</div>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3 text-sm">
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
              </div>
              <div className="border-t md:border-t-0 md:border-l border-border pt-4 md:pt-0 md:pl-6">
                <span className="text-muted-foreground text-xs font-mono tracking-wider">TALKING POINTS</span>
                <ul className="mt-2 text-sm text-muted-foreground space-y-2">
                  <li className="flex items-start gap-2"><span className="text-[#4F46E5]">-</span> Discuss CRS score calculation and estimated points</li>
                  <li className="flex items-start gap-2"><span className="text-[#4F46E5]">-</span> Review education credential assessment status</li>
                  <li className="flex items-start gap-2"><span className="text-[#4F46E5]">-</span> Confirm language test scores (IELTS/CELPIP)</li>
                  <li className="flex items-start gap-2"><span className="text-[#4F46E5]">-</span> Discuss settlement funds requirements</li>
                </ul>
              </div>
            </div>
          </Card>
        </ScrollReveal>
      </div>
    </section>
  );
};
