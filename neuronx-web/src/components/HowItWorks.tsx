import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { MedalIcon, MapIcon, PlaneIcon, GiftIcon } from "../components/Icons";

interface FeatureProps {
  icon: JSX.Element;
  title: string;
  description: string;
}

const features: FeatureProps[] = [
  {
    icon: <MedalIcon />,
    title: "1. Prospect Inquires",
    description:
      "A potential client fills out your branded intake form — from your website, an ad, or a referral. Their information flows into your CRM pipeline instantly.",
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
      "Before every consultation, your RCIC receives an AI-prepared briefing: prospect profile, immigration goals, key questions, and recommended talking points. Walk in prepared.",
  },
];

export const HowItWorks = () => {
  return (
    <section id="howItWorks" className="container text-center py-24 sm:py-32">
      <h2 className="text-3xl md:text-4xl font-bold">
        From Inquiry to{" "}
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          Retainer{" "}
        </span>
        in 4 Steps
      </h2>
      <p className="md:w-3/4 mx-auto mt-4 mb-8 text-xl text-muted-foreground">
        NeuronX manages the complete pre-retention lifecycle. Your team focuses
        on delivering great consultations — the system handles everything else.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map(({ icon, title, description }: FeatureProps) => (
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
