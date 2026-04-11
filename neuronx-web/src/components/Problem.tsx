import { Card, CardContent } from "./ui/card";
import { Clock, TrendingDown, FileQuestion, Eye } from "lucide-react";

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
    <section id="problem" className="py-24 sm:py-32">
      <div className="container">
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0F172A] tracking-tight">
            Most immigration firms don't lose leads — they lose{" "}
            <span className="gradient-text">
              speed, structure, and preparation.
            </span>
          </h2>
          <p className="mt-6 text-lg text-[#475569] leading-relaxed">
            You invest to generate inquiries, but follow-ups are delayed, lead
            quality is unclear, consultations start without context, and case
            processing becomes manual and inconsistent.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {painPoints.map((point) => (
            <Card
              key={point.stat}
              className="border-[#E2E8F0] bg-white hover:border-[#4F46E5]/20 hover:shadow-lg hover:shadow-[#4F46E5]/5 transition-all duration-300 hover:-translate-y-1"
            >
              <CardContent className="pt-6 text-center space-y-3">
                <div className="text-[#4F46E5] mx-auto">{point.icon}</div>
                <h3 className="text-lg font-bold text-[#0F172A]">
                  {point.stat}
                </h3>
                <p className="text-sm text-[#475569] leading-relaxed">
                  {point.label}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};
