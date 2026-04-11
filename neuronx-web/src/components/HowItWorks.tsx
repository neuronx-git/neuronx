import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { MedalIcon, MapIcon, PlaneIcon, GiftIcon } from "../components/Icons";
import { FileCheck, FileSpreadsheet, Send, CheckCircle } from "lucide-react";
import { Badge } from "./ui/badge";

interface StepProps {
  icon: JSX.Element;
  title: string;
  description: string;
}

const phase1Steps: StepProps[] = [
  {
    icon: <MedalIcon />,
    title: "1. Prospect Inquires",
    description:
      "A potential client fills out your branded intake form — from your website, an ad, or a referral. Their information flows into your pipeline instantly.",
  },
  {
    icon: <MapIcon />,
    title: "2. AI Calls in 5 Minutes",
    description:
      "NeuronX's AI calls the prospect, asks structured readiness questions (program, urgency, location, budget), and scores them 0-100. Fully compliant — no eligibility advice.",
  },
  {
    icon: <PlaneIcon />,
    title: "3. Qualified Leads Book",
    description:
      "High-scoring leads receive a booking link automatically. Low-scoring leads enter a smart nurture sequence with program-specific content. No lead falls through.",
  },
  {
    icon: <GiftIcon />,
    title: "4. RCIC Gets a Briefing",
    description:
      "Before every consultation, your RCIC receives an AI-prepared briefing: prospect profile, immigration goals, key questions, and recommended talking points.",
  },
];

const phase2Steps: StepProps[] = [
  {
    icon: <FileCheck className="w-12 h-12 text-primary" />,
    title: "5. Document Collection",
    description:
      "Automated checklists sent to your client based on their program. Track what's received, what's missing, and send reminders — no manual follow-up.",
  },
  {
    icon: <FileSpreadsheet className="w-12 h-12 text-primary" />,
    title: "6. IRCC Form Preparation",
    description:
      "Structured data sheets organized by IRCC form sections. Your team reviews and finalizes — reducing form prep effort significantly.",
  },
  {
    icon: <Send className="w-12 h-12 text-primary" />,
    title: "7. Submission & Tracking",
    description:
      "Track every application from submission through biometrics and medical exams. Stage-based status updates for your team with workflow-driven notifications.",
  },
  {
    icon: <CheckCircle className="w-12 h-12 text-primary" />,
    title: "8. Decision & Next Steps",
    description:
      "When a decision arrives, NeuronX updates the case, notifies the team, and triggers next-step workflows — approval, additional documents, or appeal preparation.",
  },
];

export const HowItWorks = () => {
  return (
    <section id="howItWorks" className="container text-center py-16 sm:py-20">
      <h2 className="text-3xl md:text-4xl font-bold">
        How{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          NeuronX{" "}
        </span>
        Works
      </h2>
      <p className="md:w-3/4 mx-auto mt-4 mb-12 text-xl text-muted-foreground">
        Two phases. Eight steps. One platform that manages everything from the
        first inquiry to the final immigration decision.
      </p>

      {/* Phase 1 */}
      <Badge className="mb-6 text-sm px-4 py-1">Phase 1: Inquiry to Retainer</Badge>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        {phase1Steps.map(({ icon, title, description }: StepProps) => (
          <Card key={title} className="bg-muted/50">
            <CardHeader>
              <CardTitle className="grid gap-4 place-items-center">
                {icon}
                {title}
              </CardTitle>
            </CardHeader>
            <CardContent>{description}</CardContent>
          </Card>
        ))}
      </div>

      {/* Phase 2 */}
      <Badge variant="outline" className="mb-6 text-sm px-4 py-1">Phase 2: Retainer to Decision</Badge>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {phase2Steps.map(({ icon, title, description }: StepProps) => (
          <Card key={title} className="bg-muted/50">
            <CardHeader>
              <CardTitle className="grid gap-4 place-items-center">
                {icon}
                {title}
              </CardTitle>
            </CardHeader>
            <CardContent>{description}</CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
};
