import { Card, CardContent } from "./ui/card";
import { Clock, AlertTriangle, FileQuestion, TrendingDown } from "lucide-react";

export const Problem = () => {
  return (
    <section id="problem" className="container py-24 sm:py-32">
      <h2 className="text-3xl md:text-4xl font-bold text-center">
        The{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          $200K leak{" "}
        </span>
        in your practice
      </h2>

      <p className="md:w-3/4 mx-auto mt-4 mb-12 text-xl text-muted-foreground text-center">
        A qualified prospect submits an inquiry at 2pm on Tuesday. Your team
        sees it Wednesday morning. They call back Thursday. The prospect already
        signed with the firm that answered in 10 minutes.
      </p>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-destructive/20 bg-destructive/5">
          <CardContent className="pt-6 text-center">
            <Clock className="w-10 h-10 text-destructive mx-auto mb-3" />
            <h3 className="text-2xl font-bold">27 hrs</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Average firm response time to a web inquiry
            </p>
          </CardContent>
        </Card>

        <Card className="border-destructive/20 bg-destructive/5">
          <CardContent className="pt-6 text-center">
            <TrendingDown className="w-10 h-10 text-destructive mx-auto mb-3" />
            <h3 className="text-2xl font-bold">60%</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Qualified leads lost to slow follow-up
            </p>
          </CardContent>
        </Card>

        <Card className="border-destructive/20 bg-destructive/5">
          <CardContent className="pt-6 text-center">
            <FileQuestion className="w-10 h-10 text-destructive mx-auto mb-3" />
            <h3 className="text-2xl font-bold">0 prep</h3>
            <p className="text-sm text-muted-foreground mt-1">
              RCICs walk into consultations blind
            </p>
          </CardContent>
        </Card>

        <Card className="border-destructive/20 bg-destructive/5">
          <CardContent className="pt-6 text-center">
            <AlertTriangle className="w-10 h-10 text-destructive mx-auto mb-3" />
            <h3 className="text-2xl font-bold">$0</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Pipeline visibility — pure guesswork
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Before vs After timeline */}
      <div className="mt-16 max-w-4xl mx-auto space-y-6">
        <div className="p-6 rounded-xl border border-destructive/20 bg-destructive/5">
          <p className="text-sm font-semibold text-destructive mb-3">Without NeuronX</p>
          <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
            <span className="font-medium text-foreground">Inquiry</span>
            <span className="text-destructive font-mono">→ 27 hrs →</span>
            <span className="font-medium text-foreground">First callback</span>
            <span className="text-destructive font-mono">→ 3 days →</span>
            <span className="font-medium text-foreground">Booked</span>
            <span className="text-destructive font-mono">→ no prep →</span>
            <span className="font-medium text-foreground">Consultation</span>
            <span className="text-destructive font-mono">→ 2 days →</span>
            <span className="font-medium text-foreground">Retainer sent</span>
          </div>
        </div>

        <div className="p-6 rounded-xl border border-primary/30 bg-primary/5">
          <p className="text-sm font-semibold text-primary mb-3">With NeuronX</p>
          <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
            <span className="font-medium text-foreground">Inquiry</span>
            <span className="text-primary font-mono">→ 5 min →</span>
            <span className="font-medium text-foreground">AI call + scored</span>
            <span className="text-primary font-mono">→ instant →</span>
            <span className="font-medium text-foreground">Booked + briefed</span>
            <span className="text-primary font-mono">→ same day →</span>
            <span className="font-medium text-foreground">Consultation</span>
            <span className="text-primary font-mono">→ same day →</span>
            <span className="font-medium text-foreground">Retainer signed</span>
          </div>
        </div>
      </div>
    </section>
  );
};
