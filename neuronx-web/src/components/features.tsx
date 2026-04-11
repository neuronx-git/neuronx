import { Badge } from "./ui/badge";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface FeatureProps {
  title: string;
  description: string;
}

const features: FeatureProps[] = [
  {
    title: "AI Voice Intake",
    description:
      "Every inquiry gets an AI follow-up call within 5 minutes. Structured R1-R5 readiness assessment with compliance guardrails. The AI never assesses eligibility — it collects, scores, and routes.",
  },
  {
    title: "Pre-Consultation Briefings",
    description:
      "AI-assembled prep documents delivered to your RCIC before every meeting. Full prospect context, immigration history, program interest, urgency, and recommended talking points.",
  },
  {
    title: "Pipeline Intelligence",
    description:
      "Real-time funnel analytics, stuck-lead detection, and conversion metrics that GHL alone cannot provide. Know exactly where your pipeline leaks and fix it before revenue is lost.",
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
    <section id="features" className="container py-24 sm:py-32 space-y-8">
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

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map(({ title, description }: FeatureProps) => (
          <Card key={title}>
            <CardHeader>
              <CardTitle>{title}</CardTitle>
            </CardHeader>

            <CardContent>{description}</CardContent>

            <CardFooter>
              <div className="w-full h-32 bg-gradient-to-br from-primary/10 to-primary/5 rounded-lg flex items-center justify-center">
                <span className="text-4xl font-bold text-primary/30">NX</span>
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>
    </section>
  );
};
