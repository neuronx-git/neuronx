import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ui/scroll-reveal";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Check, ArrowRight } from "lucide-react";

enum PopularPlanType {
  NO = 0,
  YES = 1,
}

interface PricingProps {
  title: string;
  popular: PopularPlanType;
  price: number;
  description: string;
  buttonText: string;
  benefitList: string[];
}

const pricingList: PricingProps[] = [
  {
    title: "Starter",
    popular: 0,
    price: 299,
    description: "For solo RCICs ready to stop missing leads.",
    buttonText: "Start 14-Day Pilot",
    benefitList: [
      "AI intake calls (100/month)",
      "Readiness scoring (R1-R5)",
      "Automated consultation booking",
      "Pre-consultation briefings",
      "Pipeline dashboard",
      "Email + chat support",
    ],
  },
  {
    title: "Professional",
    popular: 1,
    price: 599,
    description: "For growing firms that want full-funnel automation.",
    buttonText: "Start 14-Day Pilot",
    benefitList: [
      "Everything in Starter",
      "Unlimited AI calls",
      "9-branch program nurture",
      "IRCC form data sheets",
      "Case processing pipeline",
      "Chrome extension (auto-fill)",
      "Advanced analytics",
      "Priority support",
    ],
  },
  {
    title: "Scale",
    popular: 0,
    price: 1199,
    description: "For multi-RCIC firms running at full capacity.",
    buttonText: "Talk to Founders",
    benefitList: [
      "Everything in Professional",
      "Multi-RCIC calendar routing",
      "E-signatures (Planned)",
      "Client portal (Planned)",
      "Dedicated success manager",
      "Monthly performance review",
    ],
  },
];

export const Pricing = () => {
  return (
    <section id="pricing" className="container py-16 sm:py-20">
      <ScrollReveal>
      <h2 className="text-3xl md:text-4xl font-bold text-center">
        Pricing that pays for itself
        <span className="bg-gradient-to-b from-primary/60 to-primary text-transparent bg-clip-text">
          {" "}in your first week
        </span>
      </h2>
      <h3 className="text-xl text-center text-muted-foreground pt-4 pb-4">
        No per-seat charges. No feature gating. Every plan includes the full
        AI sales engine. Pick the one that matches your practice size.
      </h3>

      {/* ROI Anchor */}
      <div className="text-center mb-12 p-4 rounded-xl bg-primary/5 border border-primary/20 max-w-2xl mx-auto">
        <p className="text-sm font-medium">
          <span className="text-primary font-bold">Quick math:</span>{" "}
          2 extra clients/month × $3,000 average retainer = $6,000 in new revenue.
          That's a{" "}
          <span className="text-primary font-bold">20x return</span>{" "}
          on your Starter plan.
        </p>
      </div>
      </ScrollReveal>

      <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {pricingList.map((pricing: PricingProps) => (
          <StaggerItem key={pricing.title}>
          <Card
            className={
              pricing.popular === PopularPlanType.YES
                ? "drop-shadow-xl shadow-black/10 dark:shadow-white/10 border-primary/50"
                : ""
            }
          >
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                {pricing.title}
                {pricing.popular === PopularPlanType.YES ? (
                  <Badge variant="secondary" className="text-sm text-primary">
                    Most firms choose this
                  </Badge>
                ) : null}
              </CardTitle>
              <div>
                <span className="text-3xl font-bold">${pricing.price}</span>
                <span className="text-muted-foreground"> /month CAD</span>
              </div>
              <CardDescription>{pricing.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <a
                href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
                target="_blank"
                rel="noreferrer noopener"
              >
                <Button
                  variant={pricing.popular === PopularPlanType.YES ? "default" : "outline"}
                  className="w-full"
                >
                  {pricing.buttonText}
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </a>
            </CardContent>
            <hr className="w-4/5 m-auto mb-4" />
            <CardFooter className="flex">
              <div className="space-y-4">
                {pricing.benefitList.map((benefit: string) => (
                  <span key={benefit} className="flex">
                    <Check className="text-primary flex-shrink-0" />
                    <h3 className="ml-2">{benefit}</h3>
                  </span>
                ))}
              </div>
            </CardFooter>
          </Card>
          </StaggerItem>
        ))}
      </StaggerContainer>

      {/* Trust strip below pricing */}
      <div className="mt-12 text-center space-y-2">
        <p className="text-sm text-muted-foreground">
          14-day pilot included. Full setup. Real results. Cancel anytime.
        </p>
        <p className="text-xs text-muted-foreground">
          No contracts. No setup fees. Your data is always yours.
        </p>
      </div>
    </section>
  );
};
