import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import {
  Phone,
  BarChart3,
  FileText,
  Shield,
  Calendar,
  FolderOpen,
  GitBranch,
  ClipboardCheck,
} from "lucide-react";

const modules = [
  {
    icon: <Phone className="w-6 h-6" />,
    title: "Inquiry Capture",
    description: "Forms, webhooks, and intake channels feed every inquiry into a structured pipeline automatically.",
    status: "live",
  },
  {
    icon: <BarChart3 className="w-6 h-6" />,
    title: "Readiness Scoring",
    description: "Score every lead 0-100 across 5 structured dimensions: program, location, urgency, history, budget.",
    status: "live",
  },
  {
    icon: <Calendar className="w-6 h-6" />,
    title: "Consultation Booking",
    description: "Qualified leads routed to booking automatically. Reminders, confirmations, and no-show recovery built in.",
    status: "live",
  },
  {
    icon: <FileText className="w-6 h-6" />,
    title: "Auto-Generated Briefings",
    description: "Structured consultation prep documents assembled from scoring data and delivered before every meeting.",
    status: "live",
  },
  {
    icon: <Shield className="w-6 h-6" />,
    title: "Trust Boundary Enforcement",
    description: "Every AI interaction scanned for compliance. Automatic escalation on prohibited topics. RCIC-reviewed.",
    status: "live",
  },
  {
    icon: <FolderOpen className="w-6 h-6" />,
    title: "Case Pipeline",
    description: "10-stage case processing from onboarding through IRCC decision. Program-specific document checklists.",
    status: "live",
  },
  {
    icon: <GitBranch className="w-6 h-6" />,
    title: "Immigration Workflows",
    description: "13 published workflows covering intake, scoring, booking, follow-up, nurture, and case transitions.",
    status: "live",
  },
  {
    icon: <ClipboardCheck className="w-6 h-6" />,
    title: "IRCC Form Preparation",
    description: "Program-specific data sheets for IRCC forms. Field mappings for 8 Canadian immigration programs.",
    status: "live",
  },
];

export const ProductModules = () => {
  return (
    <section id="features" className="py-24 sm:py-32">
      <div className="container">
        <div className="text-center mb-16 max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground tracking-tight">
            Built for immigration.{" "}
            <span className="gradient-text">Every module.</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Purpose-built modules for the immigration consulting lifecycle —
            not generic CRM features with immigration labels.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {modules.map((mod) => (
            <Card
              key={mod.title}
              className="border-border bg-card hover:border-[#4F46E5]/20 hover:shadow-lg hover:shadow-[#4F46E5]/5 transition-all duration-300 hover:-translate-y-1 group"
            >
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-[#4F46E5] group-hover:scale-110 transition-transform">
                    {mod.icon}
                  </div>
                  {mod.status === "live" && (
                    <Badge variant="outline" className="text-xs text-emerald-600 border-emerald-200 bg-emerald-50">
                      Live
                    </Badge>
                  )}
                </div>
                <CardTitle className="text-base text-foreground">
                  {mod.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {mod.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};
