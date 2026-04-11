import { Card, CardContent } from "./ui/card";
import { Clock, TrendingDown, FileQuestion, Eye } from "lucide-react";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ui/scroll-reveal";

const painPoints = [
  {
    icon: <Clock className="w-8 h-8" />,
    stat: "Delayed",
    label: "Follow-ups take hours or days, not minutes",
  },
  {
    icon: <TrendingDown className="w-8 h-8" />,
    stat: "Unclear",
    label: "Lead quality is unknown until the consultation starts",
  },
  {
    icon: <FileQuestion className="w-8 h-8" />,
    stat: "Unprepared",
    label: "Consultations begin without context or structure",
  },
  {
    icon: <Eye className="w-8 h-8" />,
    stat: "Inconsistent",
    label: "Case processing is manual, fragmented, and hard to track",
  },
];

export const Problem = () => {
  return (
    <section id="problem" className="py-16 sm:py-24">
      <div className="container">
        <ScrollReveal className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            Most immigration firms don't lose leads — they lose{" "}
            <span className="gradient-text">
              speed, structure, and preparation.
            </span>
          </h2>
          <p className="mt-6 text-lg text-muted-foreground leading-relaxed">
            You invest to generate inquiries, but follow-ups are delayed, lead
            quality is unclear, consultations start without context, and case
            processing becomes manual and inconsistent.
          </p>
        </ScrollReveal>

        <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {painPoints.map((point) => (
            <StaggerItem key={point.stat}><Card
              key={point.stat}
              className="border-border bg-card hover:border-[#4F46E5]/20 hover:shadow-lg hover:shadow-[#4F46E5]/5 transition-all duration-300 hover:-translate-y-1"
            >
              <CardContent className="pt-6 text-center space-y-3">
                <div className="text-[#4F46E5] mx-auto">{point.icon}</div>
                <h3 className="text-lg font-bold text-foreground">
                  {point.stat}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {point.label}
                </p>
              </CardContent>
            </Card></StaggerItem>
          ))}
        </StaggerContainer>
      </div>
    </section>
  );
};
