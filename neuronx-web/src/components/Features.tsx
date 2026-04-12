import { Badge } from "./ui/badge";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ui/scroll-reveal";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Phone, FileText, BarChart3 } from "lucide-react";

interface FeatureProps {
  title: string;
  description: string;
  icon: JSX.Element;
}

const features: FeatureProps[] = [
  {
    title: "AI Voice Intake",
    description:
      "Every inquiry gets an AI follow-up call within 5 minutes. Structured R1-R5 readiness assessment with compliance guardrails. The AI never assesses eligibility — it collects, scores, and routes.",
    icon: <Phone className="w-10 h-10 text-primary" />,
  },
  {
    title: "Pre-Consultation Briefings",
    description:
      "Auto-generated prep documents delivered to your RCIC before every meeting. Full prospect context, program interest, urgency, and recommended talking points.",
    icon: <FileText className="w-10 h-10 text-primary" />,
  },
  {
    title: "Pipeline Intelligence",
    description:
      "Pipeline visibility, stuck-lead detection, and conversion tracking purpose-built for immigration firms. Know where your pipeline leaks and fix it before revenue is lost.",
    icon: <BarChart3 className="w-10 h-10 text-primary" />,
  },
];

const featureList: string[] = [
  "AI Voice Calling",
  "Lead Scoring (0-100)",
  "Smart Booking",
  "No-Show Recovery",
  "Nurture Sequences",
  "IRCC Data Sheets",
  "Trust Compliance",
  "Case Processing",
  "Chrome Extension",
];

export const Features = () => {
  return (
    <section id="features" className="container py-14 sm:py-16 space-y-8">
      <ScrollReveal>
      <h2 className="text-3xl lg:text-4xl font-bold md:text-center">
        Everything Your Firm Needs to{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          Convert More Clients
        </span>
      </h2>

      <div className="flex flex-wrap md:justify-center gap-4">
        {featureList.map((feature: string) => (
          <div key={feature}>
            <Badge variant="secondary" className="text-sm">
              {feature}
            </Badge>
          </div>
        ))}
      </div>
      </ScrollReveal>

      <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map(({ title, description, icon }: FeatureProps) => (
          <StaggerItem key={title}>
            <Card className="card-premium h-full hover:-translate-y-2 hover:scale-[1.02] transition-all duration-300">
              <CardHeader>
                <div className="mb-2">{icon}</div>
                <CardTitle>{title}</CardTitle>
              </CardHeader>
              <CardContent>{description}</CardContent>
            </Card>
          </StaggerItem>
        ))}
      </StaggerContainer>
    </section>
  );
};
