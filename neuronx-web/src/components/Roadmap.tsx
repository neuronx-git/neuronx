import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Monitor, PenTool, BarChart3, FileCheck } from "lucide-react";

const roadmapItems = [
  {
    icon: <Monitor className="w-6 h-6" />,
    title: "Client Portal",
    description: "Self-serve case status, document upload, and appointment booking for your clients.",
    status: "Planned",
  },
  {
    icon: <PenTool className="w-6 h-6" />,
    title: "E-Signatures",
    description: "Send and track retainer agreements with integrated digital signatures.",
    status: "Planned",
  },
  {
    icon: <BarChart3 className="w-6 h-6" />,
    title: "Advanced Analytics",
    description: "Conversion funnels, RCIC performance, lead source ROI, and case pipeline metrics.",
    status: "Planned",
  },
  {
    icon: <FileCheck className="w-6 h-6" />,
    title: "Full IRCC Auto-Fill",
    description: "Complete auto-fill for all major IRCC forms across all immigration programs.",
    status: "Coming Soon",
  },
];

export const Roadmap = () => {
  return (
    <section id="roadmap" className="bg-muted/30 py-16 sm:py-20">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            What's next
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            NeuronX is actively expanding. These modules are in development and
            will be available to all plans.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {roadmapItems.map((item) => (
            <Card
              key={item.title}
              className="bg-white dark:bg-slate-800 border-border hover:border-[#7C3AED]/30 hover:shadow-lg transition-all duration-300"
            >
              <CardContent className="pt-6 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="text-muted-foreground">{item.icon}</div>
                  <Badge
                    variant="outline"
                    className="text-xs border-[#7C3AED]/30 text-[#7C3AED] bg-[#7C3AED]/5"
                  >
                    {item.status}
                  </Badge>
                </div>
                <h3 className="text-foreground font-semibold">{item.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {item.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};
